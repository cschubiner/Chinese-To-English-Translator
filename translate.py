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

## PARAMETERS ##
FLAG_FIX_DATES = True
FLAG_FIX_NUMBERS = True
FLAG_SWITCH_TENSE = True
FLAG_FIX_YI = True
FLAG_USE_LANGUAGE_MODEL = True
FLAG_USE_POS_TAGGING = True
FLAG_REMOVE_FILLER_WORDS = True
FLAG_MODIFY_POSSESSIVES = True
FLAG_REMOVE_ADJACENT_DUPLICATES = True

# Chinese dictionary
chinDict = dictionary.getdictionary()

# Chinese punctuation replacement dictionary
replaceDictionary = {'、':',', '：':':', '；':';', '，':',', '％':'%', '。':'.', '？':'?'}

# Chinese POS mapper
partOfSpeechMapper = dictionary.getPartOfSpeechMapper()

# Language model + corpus
engCorpus = HolbrookCorpus('holbrook-tagged-train.dat')
engModel = StupidBackoffLanguageModel(engCorpus)

# Enum class to track Chinese tense
def enum(**enums):
  return type('Enum', (), enums)
Tense = enum(Past=1, Present=2, Future=3)

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

def runCommandLineCommand2(command):
  # arr = command.split(' ')
  # proc = subprocess.Popen([arr[0], command.replace(arr[0],'')], stdout=subprocess.PIPE, shell=False)
  commandLine = str(subprocess.check_output(command, shell=True))
  return commandLine[2:-3]


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
  if not FLAG_FIX_DATES:
    return sentence

  dateFormat = re.compile(r'.{,3}?(\d{2,4})年.{,3}(\d+)月.+?(\d+?)日')
  matches = re.findall(dateFormat,sentence)
  for m in matches:
    if m:
      newDate = m[1]+'/'+m[2]+'/'+m[0]
      sentencefix = dateFormat.sub(newDate,sentence)
      return sentencefix

  return sentence

def fixNumbers(sentence):
  if not FLAG_FIX_NUMBERS:
    return sentence

  sentencefix = sentence
  yiThousandFormat = re.compile(r'(\d*)亿 ?(\d*)万')
  matches = re.findall(yiThousandFormat,sentence)
  if matches:
    sentencefix = yiThousandFormat.sub(lambda x: str(runCommandLineCommand2('python number-convert.py ' +str(int(x.group(1)+'00000000')+int(x.group(2)+'0000')))),sentence)

  tenThousandFormat = re.compile(r'(\d*)万')
  matches = re.findall(tenThousandFormat,sentencefix)
  if matches:
    sentencefix = tenThousandFormat.sub(lambda x: str(runCommandLineCommand2('python number-convert.py ' + str(x.group(1)+'0000'))),sentencefix)
    return sentencefix

  return sentence

def modifyyi(chineseSentence):
  if not FLAG_FIX_YI:
    return chineseSentence

  regex = re.compile(r'一 .')
  newChineseSentence = regex.sub('一', chineseSentence)
  return newChineseSentence

# Currently, this function estimates a single tense for an entire Chinese sentence
# Obviously, this doesn't cover all cases especially for heterogeneous cases:
# "In the past I used to sing, but now I play basketball instead."
def getChineseTense(chineseSentence):
  # If sentence contains any of past tense words, mark as past tense
  pastTenseWords = [u"了", u"昨天", u"前"]
  for pastTenseWord in pastTenseWords:
    if pastTenseWord in chineseSentence:
      return Tense.Past

  # If sentence contains a verb before "过", mark as past tense
  guo4 = u"过"
  if guo4 in chineseSentence:
    # Verify that word before guo4 is a verb
    chineseTokens = chineseSentence.split()
    guo4Idx = -1
    prevWordIdx = -1

    # Determine index of guo4 / word before
    for index, token in enumerate(chineseTokens):
      if guo4 in token:
        guo4Idx = index

        # If another word group is before guo4 in the token, this
        # must be the index we want to tag
        if token[0] != guo4:
          prevWordIdx = guo4Idx

    if prevWordIdx < 0:
      prevWordIdx = guo4Idx - 1

    # Determine word before index only if found
    if prevWordIdx >= 0:
      prevWord = chineseTokens[prevWordIdx]
      prevPos = getChinesePOS(prevWord)
      prevPos = prevPos[0][0]
      if prevPos in partOfSpeechMapper and partOfSpeechMapper[prevPos] == 'verb':
        return Tense.Past

  # If sentence contains any of future tense words, mark as past tense
  futureTenseWords = [u"未来", u"将来", u"后天", u"明天"]
  for futureTenseWord in futureTenseWords:
    if futureTenseWord in chineseSentence:
      return Tense.Future

  # Return present tense if no other tenses were identified
  return Tense.Present

def vowelMod(sentence):
  if not FLAG_MODIFY_POSSESSIVES:
    return sentence

  regex = re.compile(r' a \'?[aeiou]')
  lookfora = re.compile(r' a ')
  matches = re.findall(regex,sentence)
  #print(matches)
  if matches:
    newSentence = lookfora.sub(" an ", sentence)
    return newSentence

  regex = re.compile(r'A \'?[aeiou]')
  lookfora = re.compile(r'A ')
  matches = re.findall(regex,sentence)
  #print(matches)
  if matches:
    newSentence = lookfora.sub("An ", sentence)
    return newSentence

  return sentence

def getChinesePOS(chineseSentence):
  pos = runCommandLineCommand('python posTagger.py "' + chineseSentence + '"')
  # pos = os.system('python posTagger.py "' + chineseSentence + '"')

  actualPOS = list()
  for p in pos.split():
    p = str(p, encoding='utf-8')
    if p not in partOfSpeechMapper:
      actualPOS.append((p, p))
    else:
      actualPOS.append((p, partOfSpeechMapper[p]))
  return actualPOS

# Changes the tense of an English word (only applicable if verb)
def changeEnglishTense(word, pos, tense):
  # Return the word itself if the part of speech is not a verb
  if pos != 'verb' or not FLAG_SWITCH_TENSE:
    return word

  # Change word based on the tense
  return str(runCommandLineCommand2('python tense.py "' + word + '" ' + str(tense)))

# Removes any adjacent 2-in-a-row duplicates of a given sentence
def removeDuplicates(sentence):
  if not FLAG_REMOVE_ADJACENT_DUPLICATES:
    return sentence

  # Tokenize and compare adjacent tokens
  tokens = sentence.split()
  prevToken = ""

  resultTokens = []
  for currToken in tokens:
    # Compare tokens with punctuation removed
    if removePunctuation(prevToken) == removePunctuation(currToken):
      # Remove previous token iff it doesn't have punctuation
      if prevToken == removePunctuation(prevToken):
        resultTokens.pop()
        resultTokens.append(currToken)
        prevToken = currToken
      elif currToken != removePunctuation(currToken):
        # Add current token as duplicate iff it has punctuation
        resultTokens.append(currToken)
        prevToken = currToken
    else:
      resultTokens.append(currToken)
      prevToken = currToken

  return (' ').join(resultTokens)



def translateSentence(chineseSentence):
  # First, replace all punctuation in the original sentence with valid punctuation
  chineseSentence = replaceChinesePunctuation(chineseSentence)
  chineseSentence = modifyyi(chineseSentence)

  # Determine POS tags, split chinese sentence
  chinesePOS = getChinesePOS(chineseSentence)
  chineseTense = getChineseTense(chineseSentence)
  chineseSentence = chineseSentence.split()
  usePOS = len(chinesePOS) == len(chineseSentence) and FLAG_USE_POS_TAGGING

  # Construct possible translations, add to list of sentences
  possibleSentences = []
  for index, word in enumerate(chineseSentence):
    # Get possible variations (list of strings)
    variations = getPossibleVariations(word, index, usePOS, chinesePOS, chineseTense)

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
          newSentence = copy.deepcopy(sentence)
          newSentence.append(variation)
          nextSentences.append(newSentence)

    # Update possibleSentences
    possibleSentences = nextSentences

  # Perform post operations on each sentence
  for i in range(len(possibleSentences)):
    possibleSentences[i] = addEndingPeriod(possibleSentences[i])
    possibleSentences[i][0] = possibleSentences[i][0].capitalize()
    possibleSentences[i] =  (' ').join(possibleSentences[i])
    possibleSentences[i] = possibleSentences[i].replace('  ', ' ')
    possibleSentences[i] = fixQuotes(possibleSentences[i])
    possibleSentences[i] = fixPunctuationSpacing(possibleSentences[i])
    possibleSentences[i] = fixDates(possibleSentences[i])
    possibleSentences[i] = fixNumbers(possibleSentences[i])
    possibleSentences[i] = vowelMod(possibleSentences[i])

  # Utilize the language model to choose the most likely sentence
  result = chooseMostLikelySentence(possibleSentences)

  # Remove all final duplicates
  result = removeDuplicates(result)
  return result

fillerPOSSet = set(['DEG', 'LB', 'DEV'])
def getPossibleVariations(word, index, usePOS, chinesePOS, chineseTense):
  variations = []
  if usePOS:
    chinPOS = chinesePOS[index]
    # print(chinPOS, word,end='')
    # print()
    if chinPOS[0] in fillerPOSSet and FLAG_REMOVE_FILLER_WORDS:
      # print('Removing part of speech:', chinPOS)
      return ['']


  if word in chinDict:
    if usePOS:
      chinPOS = chinesePOS[index]

      for engWord in chinDict[word]:
        if engWord.pos == chinPOS[1]:
          translation = changeEnglishTense(engWord.word, chinPOS[1], chineseTense)
          #translation = engWord.word
          variations.append(translation)

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
  if not FLAG_USE_LANGUAGE_MODEL:
    return sentences[0] if len(sentences) > 0 else ""

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
  outputFilename = 'output/translations_dev.txt'
  corpus = 'corpus_dev_segmented.txt'
  if len(sys.argv) > 1 and sys.argv[1] == '-t': corpus = 'corpus_test_segmented.txt'; outputFilename = 'output/translations_test.txt'
  outputFile = open(outputFilename, 'w')

  i = 0
  for line in codecs.open(corpus, encoding='utf-8').readlines():
    i += 1
    print(line.strip(),)
    out = str(i) + '. ' + translateSentence(line)
    print(out + '\n')
    outputFile.write(out + '\n')
    # translateSentence(line)
    # break
outputFile.close()
