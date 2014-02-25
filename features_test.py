#!/usr/bin/env python
# -*- coding: utf-8 -*

import numpy
import nltk
from nltk.tag.stanford import POSTagger

## Configure this to be your Java directory
# nltk.internals.config_java(u"C:/Program Files/Java/jre7/bin/java.exe")

chunk = u"古往今来 ， 有 多少 的 成功者 被 人们 赞赏"
#chunk = u"妈我"
#tagger = POSTagger()
#token_tags = tagger.tag(chunk)

#for token,tag in token_tags:
#   print token,tag

text = nltk.word_tokenize(chunk.encode('utf-8'))
st = POSTagger('chinese-distsim.tagger', 'stanford-postagger-3.1.4.jar')

# print (text)
poop = st.tag(text)
# print (poop)
for w in poop:
  # print type(w[1]), type(w[1].decode('utf-8'))
  print w[1].decode('utf-8'),
#tagger = pickle.load(open('sinica_treebank_brill_aubt.pickle'))
#poop = tagger.tag(text)
#print poop

#poop2 = nltk.pos_tag(text)
#print poop2
