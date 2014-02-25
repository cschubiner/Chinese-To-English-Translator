#!/usr/bin/python
# -*- coding: utf-8 -*-

import dictionary
import codecs

chinDict = dictionary.getdictionary()

def translateSentence(sentence):
  ret = ''
  for word in sentence:
    if word in chinDict:
      ret += chinDict[word][0].word #use the most frequent translation
      ret += ' '
    else:
      ret += word
  return ret


i = 0
for line in codecs.open('corpus_dev_segmented.txt', encoding='utf-8').readlines():
  i += 1
  print(str(i) + '.', translateSentence(line.split()))
  # translateSentence(line)
  # break
