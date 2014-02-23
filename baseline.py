#!/usr/bin/python
# -*- coding: utf-8 -*-

import dictionary
import codecs
import os
import urllib


chinDict = dictionary.getdictionary()

def translateSentence(sentence):
  ret = ''
  for char in sentence:
    char = char.encode('utf-8')
    if char in chinDict:
      ret += chinDict[char][0].word #use the most frequent translation
      ret += ' '
    else:
      ret += char
      # if not dictionary.only_roman_chars(char):
        # print 'hi'
        # url = urllib.quote('http://translate.google.com/#auto/en/'+char)
        # print url
        # print 'open "http://translate.google.com/#auto/en/'+char +'"'
  return ret


# print chinDict['从'][0].word

i = 0
for line in codecs.open('corpus_dev.txt', encoding='utf-8').readlines():
  # line = line.encode('utf-8')
  i += 1
  print str(i) + '.', translateSentence(line)
