#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 07:17:58 2021

@author: katebelisle
"""
from __future__ import unicode_literals, print_function
from spacy.lang.en import English # updated


import urllib.request

import spacy

"""
BILUO SCHEME
B – Token is the beginning of a multi-token entity.
I – Token is inside a multi-token entity.
L – Token is the last token of a multi-token entity.
U – Token is a single-token unit entity.
O – Toke is outside an entity.

IOB SCHEME
I – Token is inside an entity.
O – Token is outside an entity.
B – Token is the beginning of an entity.

TOKENIZE
"""
#nlp=spacy.load('en_core_web_sm')

# Getting the pipeline component
#ner=nlp.get_pipe("ner")

URI="http://www.gencourt.state.nh.us/rsa/html/III/31/31-mrg.htm"
fp = urllib.request.urlopen(URI)
mybytes = fp.read()

mystr = mybytes.decode("utf8")
fp.close()



nlp = English()
nlp.add_pipe('sentencizer') # updated
doc = nlp(mystr)
#sentences = [sent.string.strip() for sent in doc.sents]
sentences = [sent for sent in doc.sents]
