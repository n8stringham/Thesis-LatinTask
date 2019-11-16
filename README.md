# Thesis-LatinTask

Work for this project began in the Fall of 2019 and is expected to continue into the Spring of 2020.

This is the repo for a NLP project undertaken to fulfill the senior thesis requirement of my undergraduate degree in Mathematics at Pomona College. The main goal of this project is to create word vectors from a Latin corpus that capture semantic meaning. That is, I hope to create a vectorspace in which the words representations that lie closest to each other have similar meanings. To create word vectors I primarily use the word2vec method introduced by Mikolov et al., though some extensions may also be employed. 

While much research regarding the creation of accurate word embeddings focuses on the English language, in this project I investigate the creation of word vectors for Latin. To this end I decided to construct my own data set from a collection of historical Latin documents written around the 4th century CE obtained from Project Gutenberg (Though the corpus has not been completely finalized). 

To account for the fundamental linguistic differences between Latin and English (and especially Latin's morphological richness) we employ lemmatization and other normalization techniques that reduce the total number of verb forms in our data. The majority of this preprocessing is handled using the Classical Language Toolkit (CLTK) library in Python. Like Mikolov et. al., we evaluate the accuracy of our vectors by testing them on a custom set of analogies. Our analogy set combines some of the same relationships tested by Mikolov's team with relationships that are more specific to the Latin Language and the context of our training corpus. Implementation of word2vec and analogy testing is carried out using the Gensim library in Python.

