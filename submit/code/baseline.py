#!/usr/bin/python
# -*- coding: utf-8 -*-

import dictionary
import codecs
import random

chinDict = dictionary.getdictionary()

def translateSentence(sentence):
  sentence = sentence.split()
  ret = ''
  for word in sentence:
    if word in chinDict:
      ret += chinDict[word][random.randint(0,len(chinDict[word])-1)].word #as our dictionary is unordered, we'll use a random translation
      ret += ' '
    else:
      ret += word
  return ret

def translateSentenceNoSegmentation(sentence):
  ret = ''
  for char in sentence:
    if char in chinDict:
      ret += chinDict[char][0].word #use the most frequent translation
      ret += ' '
    else:
      ret += char
  return ret


if __name__ == "__main__":
  i = 0
  for line in codecs.open('corpus_test_segmented.txt', encoding='utf-8').readlines():
    i += 1
    print(str(i) + '.', translateSentence(line))
    # translateSentence(line)
    # break
