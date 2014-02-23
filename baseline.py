#!/usr/bin/python
# -*- coding: utf-8 -*-

import dictionary
import codecs


dictionary = dictionary.getdictionary()

def translateSentence(sentence):
  for i in range(0, len(sentence) - 2):
    word = sentence[i:i+3]
    # print word
    if word in dictionary:
      print dictionary[word][0].word
    else:
      pass
      # print repr(word)
      # print word.encode('utf-8')


# print dictionary['从'][0].word

for line in codecs.open('corpus_dev.txt', encoding='utf-8').readlines():
  # print line.encode('utf-8')
  for char in line:
    print char.encode('utf-8')
  for char in repr(line).split('\\'):
    # print eval(repr(char))
    # print ('\\' + char).encode('utf-8')
    pass
  translateSentence(line)
  # print line
  # print line[:3]
  break
