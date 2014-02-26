#!/usr/bin/python
import dictionary
import codecs
import sys
import re
import copy
import string
from Datum import Datum
from Sentence import Sentence
from HolbrookCorpus import HolbrookCorpus
from StupidBackoffLanguageModel import StupidBackoffLanguageModel
import sys, os
import subprocess
import en


chinDict = dictionary.getdictionary()

replaceDictionary = {'、':',', '：':':', '；':';', '，':',', '％':'%', '。':'.', '？':'?'}

engCorpus = HolbrookCorpus('holbrook-tagged-train.dat')
engModel = StupidBackoffLanguageModel(engCorpus)

def replaceChinesePunctuation(sentence):
  for key in replaceDictionary:
    sentence = sentence.replace(key, replaceDictionary[key])
  return sentence

def fixPunctuationSpacing(sentence):
  for val in replaceDictionary.values():
    sentence = sentence.replace(' '+val, val)
  return sentence

def runCommandLineCommand(command):
  # arr = command.split(' ')
  # proc = subprocess.Popen([arr[0], command.replace(arr[0],'')], stdout=subprocess.PIPE, shell=False)
  return subprocess.check_output(command, shell=True)
  # (out, err) = proc.communicate()
  # return out

def addEndingPeriod(sentence):
  noEndingPunct = True
  for val in replaceDictionary.values():
    if sentence[-1] == val:
      noEndingPunct = False
      break
  if noEndingPunct:
    sentence.append('.')
  return sentence

def fixQuotes(sentence):
  sentence = sentence.replace('‘ ', "'")
  sentence = sentence.replace('“ ', '"')
  sentence = sentence.replace(' ’', "'")
  sentence = sentence.replace(' ”', '"')
  sentence = sentence.replace('‘', "'")
  sentence = sentence.replace('“', '"')
  return sentence

def fixDates(sentence):
  dateFormat = re.compile(r'.{,3}?(\d{2,4})年.{,3}(\d+)月.+?(\d+?)日')
  matches = re.findall(dateFormat,sentence)
  for m in matches:
    if m:
      newDate = m[1]+'/'+m[2]+'/'+m[0]
      sentencefix = dateFormat.sub(newDate,sentence)
      return sentencefix

  return sentence

def fixNumbers(sentence):
  sentencefix = sentence
  yiThousandFormat = re.compile(r'(\d*)亿 ?(\d*)万')
  matches = re.findall(yiThousandFormat,sentence)
  if matches:
    sentencefix = yiThousandFormat.sub(lambda x: str(int(x.group(1)+'00000000')+int(x.group(2)+'0000')),sentence)

  tenThousandFormat = re.compile(r'(\d*)万')
  matches = re.findall(tenThousandFormat,sentencefix)
  if matches:
    sentencefix = tenThousandFormat.sub(lambda x: x.group(1)+'0000',sentencefix)
    return sentencefix

  return sentence

partOfSpeechMapper = dictionary.getPartOfSpeechMapper()
def getChinesePOS(chineseSentence):
  pos = runCommandLineCommand('python posTagger.py "' + chineseSentence + '"')
  # print(pos)
  # print(str(pos, encoding='UTF-8'))
  # pos = os.system('python posTagger.py "' + chineseSentence + '"')

  # print(len(pos.split()), len(chineseSentence.split()))
  actualPOS = list()
  for p in pos.split():
    p = str(p, encoding='utf-8')
    if p not in partOfSpeechMapper:
      # print (p)
      actualPOS.append(p)
    else:
      actualPOS.append(partOfSpeechMapper[p])
  return actualPOS


def translateSentence(chineseSentence):
  # First, replace all punctuation in the original sentence with valid punctuation
  chineseSentence = replaceChinesePunctuation(chineseSentence)

  # Determine POS tags, split chinese sentence
  chinesePOS = getChinesePOS(chineseSentence)
  chineseSentence = chineseSentence.split()
  usePOS = len(chinesePOS) == len(chineseSentence)

  # Construct possible translations, add to list of sentences
  possibleSentences = []
  for index, word in enumerate(chineseSentence):
    # Get possible variations (list of strings)
    variations = getPossibleVariations(word, index, usePOS, chinesePOS)

    # Append variations to each element in possible sentences
    nextSentences = []
    if len(possibleSentences) == 0:
      for variation in variations:
        sentence = []
        sentence.append(variation)
        nextSentences.append(sentence)
    else:
      # Sentence should be a list of strings
      for sentence in possibleSentences:
        for variation in variations:
          # Append variation to individual sentence
          sentence.append(variation)
          nextSentences.append(sentence)

    # Update possibleSentences
    possibleSentences = nextSentences

  # Perform post operations on each sentence
  for i in range(len(possibleSentences)):
    possibleSentences[i] = addEndingPeriod(possibleSentences[i])
    possibleSentences[i][0] = possibleSentences[i][0].capitalize()
    possibleSentences[i] =  (' ').join(possibleSentences[i])
    possibleSentences[i] = fixQuotes(possibleSentences[i])
    possibleSentences[i] = fixPunctuationSpacing(possibleSentences[i])
    possibleSentences[i] = fixDates(possibleSentences[i])
    possibleSentences[i] = fixNumbers(possibleSentences[i])

  print(len(possibleSentences))
  result = chooseMostLikelySentence(possibleSentences)
  return result

def getPossibleVariations(word, index, usePOS, chinesePOS):
  variations = []

  if word in chinDict:
    if usePOS:
      chinPOS = chinesePOS[index]
      # print(chinPOS, word,end='')
      # print()
      for engWord in chinDict[word]:
        if engWord.pos == chinPOS:
          print('appending', engWord.word)
          variations.append(engWord.word)

    if len(variations) == 0:
      # fallback to the most frequent translation
      variations.append(chinDict[word][0].word)
  else:
    variations.append(word)

  return variations

# Uses the English language model (Stupid Backoff Bigram Model)
# to choose a most "likely" sentence among several alternatives.
# The input param "sentences" is a list of strings
def chooseMostLikelySentence(sentences):
  maxLogProbScore = float('-inf')
  result = ""

  # "sentence" is a string (assume delimited by spaces)
  for sentence in sentences:
    cleanSentence = removePunctuation(sentence)
    logProbScore = engModel.score(cleanSentence.split())
    if logProbScore > maxLogProbScore:
      maxLogProbScore = logProbScore
      result = sentence

  # Return the most likely sentence
  return result

def removePunctuation(inputString):
  result = inputString
  for c in string.punctuation:
    result = result.replace(c, "")

  return result


if __name__ == "__main__":
  i = 0
  corpus = 'corpus_dev_segmented.txt'
  if len(sys.argv) > 1 and sys.argv[1] == '-t': corpus = 'corpus_test_segmented.txt'
  for line in codecs.open(corpus, encoding='utf-8').readlines():
    i += 1
    print(str(i) + '.', translateSentence(line))
    # translateSentence(line)
    # break
