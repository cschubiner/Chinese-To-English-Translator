#!/usr/bin/env python
# -*- coding: utf-8 -*

import numpy
import nltk
from nltk.tag.stanford import POSTagger
import sys

if len(sys.argv) != 2:
  print 'must have one argument'
  sys.exit()

chunk = sys.argv[1].decode('utf-8')
#chunk = u"妈我"

text = nltk.word_tokenize(chunk.encode('utf-8'))
st = POSTagger('chinese-distsim.tagger', 'stanford-postagger-3.1.4.jar')

tsentence = st.tag(text)
for w in tsentence:
  # print w[1].decode('utf-8'),
  print w[1].split('#')[1],

