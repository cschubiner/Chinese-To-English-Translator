#!/usr/bin/env python
# -*- coding: utf-8 -*

import numpy
import nltk
from nltk.tag.stanford import POSTagger
from Datum import Datum
from Sentence import Sentence
from HolbrookCorpus import HolbrookCorpus
from StupidBackoffLanguageModel import StupidBackoffLanguageModel

### Test Bigram Backoff Language model
eng_corpus = HolbrookCorpus('holbrook-tagged-train.dat')
eng_model = StupidBackoffLanguageModel(eng_corpus)

sentence = 'what do you want to eat for dinner'
print ("Score for sentence \"" + sentence + "\": " + str(eng_model.score(sentence.split())))

sentence = 'what do you want to eat for dinner'
print ("Score for sentence \"" + sentence + "\": " + str(eng_model.score(sentence.split())))


### Test POS
## Configure this to be your Java directory
# nltk.internals.config_java(u"C:/Program Files/Java/jre7/bin/java.exe")

# chunk = u"古往今来 ， 有 多少 的 成功者 被 人们 赞赏"

# text = nltk.word_tokenize(chunk.encode('utf-8'))
#st = POSTagger('chinese-distsim.tagger', 'stanford-postagger-3.1.4.jar')

#poop = st.tag(text)
#for w in poop:
#  print w[1].decode('utf-8'),
