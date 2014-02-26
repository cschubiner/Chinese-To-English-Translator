#!/usr/bin/python
import dictionary
import codecs
import sys
import re
import copy

chinDict = dictionary.getdictionary()

replaceDictionary = {'、':',', '：':':', '；':';', '，':',', '％':'%', '。':'.', '？':'?'}
def replaceChinesePunctuation(sentence):
  for key in replaceDictionary:
    sentence = sentence.replace(key, replaceDictionary[key])
  return sentence

def fixPunctuationSpacing(sentence):
  for val in replaceDictionary.values():
    sentence = sentence.replace(' '+val, val)
  return sentence

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

def translateSentence(chineseSentence):
  chineseSentence = replaceChinesePunctuation(chineseSentence)
  chineseSentence = chineseSentence.split()
  newSentence = list()
  for word in chineseSentence:
    if word in chinDict:
      newSentence.append(chinDict[word][0].word) #use the most frequent translation
    else:
      newSentence.append(word)

  newSentence = addEndingPeriod(newSentence)
  newSentence[0] = newSentence[0].capitalize()
  newSentence =  (' ').join(newSentence)
  newSentence = fixQuotes(newSentence)
  newSentence = fixPunctuationSpacing(newSentence)
  newSentence = fixDates(newSentence)
  return newSentence

if __name__ == "__main__":
  i = 0
  corpus = 'corpus_dev_segmented.txt'
  if len(sys.argv) > 1 and sys.argv[1] == '-t': corpus = 'corpus_test_segmented.txt'
  for line in codecs.open(corpus, encoding='utf-8').readlines():
    i += 1
    print(str(i) + '.', translateSentence(line))
    # translateSentence(line)
    # break
