#!/usr/bin/env python
# -*- coding: utf-8 -*

import numpy
import nltk
from nltk.tag.stanford import POSTagger

## Configure this to be your Java directory
# nltk.internals.config_java(u"C:/Program Files/Java/jre7/bin/java.exe")

chunk = u"妈妈 带 我 去 公园 散步"
#chunk = u"妈我"
#tagger = POSTagger()
#token_tags = tagger.tag(chunk)

#for token,tag in token_tags:
#   print token,tag

text = nltk.word_tokenize(chunk.encode('utf-8'))
st = POSTagger('chinese-distsim.tagger', 'stanford-postagger-3.1.4.jar')

print (text)
poop = st.tag(text)
print (poop)
#tagger = pickle.load(open('sinica_treebank_brill_aubt.pickle'))
#poop = tagger.tag(text)
#print poop

#poop2 = nltk.pos_tag(text)
#print poop2
