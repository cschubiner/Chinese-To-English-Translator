#!/usr/bin/python
# -*- coding: utf-8 -*-
romanCharSet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
def only_roman_chars(s):
    try:
      for c in s:
        if ord(c) >= 0x4e00 and ord(c) <= 0x9fff:
        # if c not in romanCharSet:
          return False
      return True
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


partOfSpeechMapper = {'AD' : 'phrase', 'CC' : 'conjunction', 'CD' : 'phrase', 'CS' : 'phrase', 'DEC' : 'preposition', 'DEG' : 'possessive particle', 'IN' : 'preposition', 'JJ' : 'adjective', 'JJR' : 'adjective', 'JJS' : 'adjective', 'LS' : 'punctuation', 'LB' : 'passive switch', 'NN' : 'noun', 'NNS' : 'noun', 'NNP' : 'noun', 'NNPS' : 'noun', 'PRP' : 'pronoun', 'PRP$' :' pronoun', 'RB' : 'adverb', 'RBR' : 'adverb', 'RBS' : 'adverb', 'TO' : 'preposition', 'VA' : 'adverb', 'VE' : 'verb', 'VB' : 'verb', 'VV' : 'verb', 'VBD' : 'verb', 'VBG' : 'verb', 'VBN' : 'verb', 'VBP' : 'verb', 'VBZ' : 'verb', 'WP' : 'pronoun', 'WP$' :' ­pronoun', 'WRB' : '­adverb', 'ETC' : 'etc', 'NR' : 'noun', 'PN' : 'pronoun', 'NT' : 'noun', 'M' : 'noun', 'LC' : 'preposition', 'DEV' : 'filler', 'P': 'verb'}

def getPartOfSpeechMapper():
  return partOfSpeechMapper

class EnglishWord:
  def __init__(self, word, pos):
    self.word = word
    self.pos = pos

char = ''
pos = ''
partsOfSpeech = set(['verb', 'auxiliary verb', 'pronoun', 'noun', 'adverb', 'preposition', 'adjective', 'conjunction', 'article', 'abbreviation', 'number', 'phrase', 'passive switch', 'filler', 'possessive particle'])
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
