#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 04:56:06 2021

@author: katebelisle
"""

from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import collections 
from xml.etree import ElementTree as ET
from hypertext import *
from lxml.html import builder as E
from lxml.html import fromstring, tostring
import networkx as nx
import spacy
from spacy.matcher import Matcher
#%%
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab, validate=True)

RSA_DIR="/Users/katebelisle/Documents/nhrsa/"
NRSA_DIR="/Users/katebelisle/Documents/nhrsa_linked/"

pattern = [{"ORTH": "RSA"}, {}]
matcher.add("rsa", [pattern])
meta=["titlename","chapter","sectiontitle","sourcenote","codesect"]
#RSA_REG=re.compile("RSA\s\d{1,3}-?[A-Z]?")
# Then lookahead :
#%%
rsahtml=os.listdir(RSA_DIR)
#%%
rsahtml=[r for r in rsahtml if not (r.startswith("mrg"))]
rsahtml=[r for r in rsahtml if not (r.startswith("toc"))]
rsahtml=[r for r in rsahtml if r.endswith(".htm")]


#rsahtml<-rsahtml[!(rsahtml %like% "NHTOC")]
#%%
nh={} #collections.defaultdict(list)
g=[] #nx.DiGraph()
# 
#%%
for h in rsahtml:
#%%
    with open(RSA_DIR+h) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
#%%
    basename, extension = os.path.splitext(h)
    chparts=basename.split('-')
    chapter="-".join(chparts[:-1])
    if (not (chapter in nh.keys())):
        nh[chapter]={} #collections.OrderedDict()
    section=chparts[-1]
#%%
    sec=collections.OrderedDict()
#    metatags = sech.find_all('meta')
#    for tag in metatags:
#        if tag not in meta:
#            print (tag)
    sec["titlename"]=soup.body.h1.contents
    chapterful=soup.find_all('h2')
    ctitle=chapterful[0].contents
    sec["chapter"]=ctitle[0]
    sec["chaptername"]=ctitle[2]
    if(len(chapterful)>1):  
        sec["subdivision"]=chapterful[1].contents
    else:   
        sec["subdivision"]=""
    sec["section"]=soup.body.h3.contents[0].split(" ")[1]
    sec["sectiontitle"]=soup.find("meta",{"name":"sectiontitle"})["content"]
    sec["codesect"]=str(soup.body.codesect.contents[0])
    sec["sourcenote"]=soup.body.sourcenote
    doc=nlp(sec["codesect"])
    # for tag in meta:
    #     sec[tag] = sech.find("meta",  {"name":tag})["content"]
#%%#
    rsas=[r.text[4:] for r in matcher(doc,as_spans=True) ]

    #    riter=RSA_REG.match(sec["codesect"])  
    if rsas is None:
        sec["num"]=0
    else:
        sec["refs"]=rsas #riter.groups()
        sec["refpos"]=rsas #riter.span()
        sec["num"]=len(sec["refpos"])
        for r in rsas:
 #           g.add_edge(sec["section"],r
         ch=r.split(":")[0]
         if (not (ch==chapter)):
             g=g+[(sec["section"],r)]
    nh[chapter][section]=sec
#%%        
    
    
#%%