"""Doesn't Match Evaluation Script

This script allows the user to leverage gensim's doesn't_match function on a custom .txt file
of categories. This tool creates and evaluates all possible groups of 4 words from 
a user-specified .txt file where 3 words are selected from one category and one word from a different 
category. As such, it is assumed that each category in the file contains atleast 3 words.

The script expects the .txt file to follow the formatting conventions of gensim's 
evaluate_word_analogies function where each category has a heading line followed 
by a list of space separated words that belong to that category on the next line.

e.g.
:fruits
apple banana pear raspberry

It also provides a method which creates a file with LaTex code to visualize 
the cross-category accuracies as a table.

This script requires the following modules be installed within the Python
environment you are running this script in.
- gensim
- re
- itertools
"""


# access/load word2vec model
from gensim.models import Word2Vec

# handle regex
import re

# used to calculate nCr to create odd-one-out groups
from itertools import combinations

def evaluate_doesnt_match(cat_file, model, debug=False):
    """Performs the doesn't match task

    Parameters
    ----------
    cat_file : str
        Path to the .txt file of categories
    model : str
        Location of word2vec model to be loaded
    debug : bool, optional
        A flag used to print the comparisons to the console (default is
        False)

    Returns
    -------
    dictionary
        Returns a dictionary of cross-category scores where each key identifies the categories being compared
        and the value is the accuracy of the odd-one-out task for that pairing.

    """

    # read in test set file as dictionary where each category is a key
    # and the corresponding value is the list of words belonging to it.
    cats = {}
    with open(cat_file, 'r') as f:
        for line in f:
            if re.search('^:',line):
                key = line.rstrip()
            elif not len(line.strip()) == 0: 
                cats.update({key: line.split()}) 

    # load the word2vec model to be tested
    test_model = Word2Vec.load(model)

    # odd-one-out testing
    combos = {} # place to store all possible category combos
    one_out = []  # place to store the predicted odd-one-out
    labels = [] # place to store the actual odd-one-out

    cross_cat_acc = {}

    # find all 3-combos and 1-combos for each category and store in dictionary
    for key in cats:
        three_combos = list(combinations(cats[key],3))
        one_combos = list(combinations(cats[key],1))
        combos.update({str(key)+'3': [three_combos], str(key)+'1': one_combos})
    # pair each 3-combo with all possible other 1-combos 
    test_set = list(combinations(combos.keys(),2))
    if(debug):
        print(len(test_set))
    for pair in range(len(test_set)):
        # ignore comparisons between two groups of 3
        if(re.search('3$',test_set[pair][0]) and re.search('3$',test_set[pair][1])):
            pass
        # ignore comparisons between two groups of 1
        elif(re.search('1$',test_set[pair][0]) and re.search('1$',test_set[pair][1])):
            pass
        # ignore pairings with a 1-comb and 3-comb from the same category
        elif(test_set[pair][0][0:-1] == test_set[pair][1][0:-1]):
            pass
        # store the value from each pair for accessibility
        else:
            if(debug):
                print('test pair =', test_set[pair][0][0:-1], test_set[pair][1][0:-1])
            ls1 = combos[test_set[pair][0]] # access values from combo dict for 1st key in pair
            ls2 = combos[test_set[pair][1]] # access values from combo dict for 2nd key in pair
            # create key for categories being compared
            cross_cat_acc.update({test_set[pair][0]+'-'+test_set[pair][1]: 0})
            # zero out score for this comparison pair
            score = 0
            count = 0
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
                            if(debug):
                                print(pair,i,j,k,l,'this is the comparison=',result)
                            # predict odd-one-out using gensims doesnt_match function
                            pred = test_model.wv.doesnt_match(result)
                            if(debug):
                                print('predicted doesnt match=',pred)
                            # append predicted and actual to master lists
                            one_out.append(pred)
                            labels.append(actual)
                            # score
                            score += int(pred == actual)
                            count += 1
                            # update accuracy dict
                            cross_cat_acc.update({test_set[pair][0]+'-'+test_set[pair][1]: score/count})


    # compare the prediction list with the labels list to calculate total accuracy
    correct = 0.0
    total = len(one_out)
    for prediction in range(total):
        correct += int(one_out[prediction] == labels[prediction])
        accuracy = correct/total
    if debug:
        print('total accuracy =',accuracy)
        print('number of comparisons =',total)
        print('score =',cross_cat_acc)
    return cross_cat_acc



# visualize the cross category accuracies as a table in latex
import pandas as pd

def make_table(results, cat_file, debug=False):
    """Creates a LaTex file with code to produce a cross-category
    comparison table.

    Parameters
    ----------
    results : dictionary
        dictionary of results returned from the evaluate_doesnt_match() function
    cat_file : str
        Path to the .txt file of categories
    debug : bool, optional
        A flag used to print the latex code to the console (default is
        False)

    Returns
    -------
    None
        LaTex file 'comparison_table.tex' created in pwd

    """
    pd.options.display.max_columns = None
    # create df with rows and columns indexed by all categories
    rows = []
    cols = []
    with open(cat_file, 'r') as f:
        for line in f:
            # identify the categ
            if re.search('^:',line):
                rows.append(line.rstrip())
                cols.append(line.rstrip())
            elif not len(line.strip()) == 0: 
                pass
            table = pd.DataFrame(index=rows, columns=cols)

    # loop through the dictionary of scores
    for key, value in results.items():
        names = key.split('-')
        # convention will be to put groups of 3 as rows and 1 as columns
        if(re.search('3$', names[0] )):
            table.loc[names[0][:-1], names[1][:-1]] = value
        elif(re.search('1$', names[0])):
            table.loc[names[1][:-1], names[0][:-1]] = value
    latex = table.to_latex(na_rep='NA', bold_rows=True, col_space=.5, 
                           float_format="{:0.2f}".format, 
                           caption="Cross Category Results of the odd-one-out task", 
                           label='label')
    # Write LaTex code to a file
    with open('comparison_table.tex', 'w') as f:
        f.write(latex)
    # Print out the code that was written
    if debug:
        print(latex)
    

# My tests of the functions
#evaluate_doesnt_match('odd-one-out.txt','../full.model', debug=True)
#make_table(evaluate_doesnt_match('odd-one-out.txt','../full.model'), 'odd-one-out.txt', debug=True)



