#!/usr/bin/python
# -*- coding: utf-8 -*-

import dictionary
import codecs


dictionary = dictionary.getdictionary()

def translateSentence(sentence):
  ret = ''
  for char in sentence:
    char = char.encode('utf-8')
    if char in dictionary:
      ret += dictionary[char][0].word
      ret += ' '
    else:
      ret += char
  return ret


# print dictionary['从'][0].word

for line in codecs.open('corpus_dev.txt', encoding='utf-8').readlines():
  # line = line.encode('utf-8')
  print translateSentence(line)
