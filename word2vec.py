#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 11:31:17 2019

@author: Nate Stringham
"""

import gensim
from gensim import models

from gensim.summarization import textcleaner
from gensim.utils import simple_preprocess
from gensim.models import Word2Vec

import re

 
filename = 'Augustine_Confesiones.txt'

#Read in Latin Document and eliminate some line breaks
with open(filename) as f_obj:
    contents = f_obj.read()
    cleaned_contents = re.sub(r'\n|\s+|\*', ' ', contents)

# Split the text file into a list of sentences. Then split each sentence into
# its words
sentences = textcleaner.split_sentences(cleaned_contents)
sentence_tokens = [simple_preprocess(sentence) for sentence in sentences]

# Train a Word2Vec model on the data
model = Word2Vec(sentence_tokens, size=100, window=10, min_count=10)
model.train(sentence_tokens, total_examples=1, epochs=1)

#Analyze similar words
model.wv.most_similar(positive="infantia")




    
