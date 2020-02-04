# Implement word2vec
from gensim.models import Word2Vec

# process command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--type',choices=['latin-analogies.txt','odd-one-out.txt','similar.txt'],default='odd-one-out.txt')
args = parser.parse_args()

# handle regex
import re

# calculate nCr to create odd-one-out groups
from itertools import combinations

# read in test set file as dictionary
cats = {}
with open('odd-one-out.txt', 'r') as f:
    for line in f:
        if re.search('^:',line):
            key = line.rstrip()
        elif not len(line.strip()) == 0: 
            cats.update({key: line.split()}) 

# load the word2vec model to be tested
test_model = Word2Vec.load('../full.model')

# perform evaluation depending on type of test desired
# analogy testing
if(args.type == 'latin-analogies.txt'):
    analogy_score = test_model.wv.evaluate_word_analogies(args.type)
    print(analogy_score)
# odd-one-out testing
elif (args.type == 'odd-one-out.txt'):
    combos = {} # place to store all possible category combos
    one_out = []  # place to store the predicted odd-one-out
    labels = [] # place to store the actual odd-one-out

    # find all 3-combos and 1-combos for each category and store in dictionary
    for key in cats:
        three_combos = list(combinations(cats[key],3))
        one_combos = list(combinations(cats[key],1))
        combos.update({str(key)+'3': [three_combos], str(key)+'1': one_combos})
    # pair each 3-combo with all possible other 1-combos 
    test_set = list(combinations(combos.keys(),2))
    print(len(test_set))
    for pair in range(len(test_set)):
        # ignore comparisons between two groups of 3 and two groups of 1
        if(re.search('3$',test_set[pair][0]) and re.search('3$',test_set[pair][1])):
            pass
        elif(re.search('1$',test_set[pair][0]) and re.search('1$',test_set[pair][1])):
            pass
        # store the value from each pair for accessibility
        else:
            ls1 = combos[test_set[pair][0]] # access values from combo dict for 1st key in pair
            ls2 = combos[test_set[pair][1]] # access values from combo dict for 2nd key in pair
            # loop through all value comparisons for this pair
            for i in range(len(ls1)):
                for j in range(len(ls1[i])):
                    for k in range(len(ls2)):
                        for l in range(len(ls2[k])):
                            # find which of the value is a 1-comb and therefore the actual odd-one-out
                            if isinstance(ls1[i][j], tuple):
                                actual = ls2[k][l] 
                                result = list(ls1[i][j])
                                result.append(ls2[k][l])
                            else:
                                actual = ls1[i][j]
                                result = list(ls2[k][l])
                                result.append(ls1[i][j])
                            print(pair,i,j,k,l,'this is the comparison=',result)
                            answer = test_model.wv.doesnt_match(result)
                            print('predicted doesnt match=',answer)
                            one_out.append(answer)
                            labels.append(actual)
    # compare the prediction list with the labels list to calculate total accuracy
    correct = 0.0
    total = len(one_out)
    for prediction in range(total):
        correct += int(one_out[prediction] == labels[prediction])
        accuracy = correct/total
    print('total accuracy =',accuracy)
    print('number of comparisons =',total)

