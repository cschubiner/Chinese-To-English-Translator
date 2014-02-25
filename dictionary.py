#!/usr/bin/python
# -*- coding: utf-8 -*-
romanCharSet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
def only_roman_chars(s):
    try:
      return len(s) > 1 or s in romanCharSet
        # s.encode("iso-8859-1")
        # for c in s:
        #   if ord(c) >= 0x4e00:
        #     return True
        # return False
    except UnicodeDecodeError:
        return False

dictionary = dict()
def getdictionary():
  return dictionary

class EnglishWord:
  def __init__(self, word, pos):
    self.word = word
    self.pos = pos
  def addTarget(self, swissprot_id, swissprot_name):
    self.proteinSet.add((swissprot_id, swissprot_name))

char = ''
pos = ''
partsOfSpeech = set(['verb', 'auxiliary verb', 'pronoun', 'noun', 'adverb', 'preposition', 'adjective', 'conjunction', 'article', 'abbreviation', 'number', 'phrase'])
for line in open('raw_dictionary.txt', 'r').readlines():
  line = line.strip()
  if '-' in line and line.split('-')[1].strip() in partsOfSpeech:
    pos = line.split('-')[1].strip()
    char = line.split('-')[0].strip()
    if char not in dictionary:
      dictionary[char] = list()
  elif len(line) >= 1 and only_roman_chars(line):
    dictionary[char].append(EnglishWord(line, pos))

# print (dictionary['我'])
