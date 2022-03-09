import pandas as pd
import sklearn_crfsuite
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer


'''def get_features(word):
    word=word.lower()
    try:
         vector=model1[word]
    except:
        # if the word is not in vocabulary,
        # returns zeros array
        vector=np.zeros(300,)

    return vector'''

from nltk import word_tokenize, pos_tag

def ner_extract(crf, sentence):
    tokens = word_tokenize(sentence)
    posttag = pos_tag(tokens)
    list_postag = [list(tuple) for tuple in posttag]
    features = [sent2features(list_postag)]
    labels = crf.predict(features)[0]


    result = []
    i= 0
    while i < len(labels):
        if labels[i][0] == 'I':
            result.append(tokens[i])
            i+=1
        elif labels[i][0] == 'O':
            i+=1
        elif labels[i][0] == 'B':
            word = tokens[i]
            j = i+1
            final_label = labels[i][2:]
            while j < len(labels) and (labels[j][0] != "B" and labels[j][2:] == final_label) :
                word+=" "+tokens[j]
                if (j < len(labels)):
                    j+=1
            result.append(word)
            i = j

    return ' '.join(result)

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
        'postag[:3]': postag[:3],
        #'postag[:4]': postag[:4],
        #'length': len(word),
    }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]


def train_crf():
    training_data = pd.read_json("../datasets/annotated_dataset.json")
    test_data = pd.read_json("../datasets/experttestdata.json")

    train_sents = training_data['SpanPosTag'].to_list()
    test_sents = test_data['SpanPosTag'].to_list()
    test_tokens = test_data['Tokens'].to_list()
    test_sentences = test_data['Sentences'].to_list()
    X_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]

    X_test = [sent2features(s) for s in test_sents]
    y_test = [sent2labels(s) for s in test_sents]

    # print(X_train)
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=150,
        all_possible_transitions=True
    )

    crf.fit(X_train, y_train)
    labels = list(crf.classes_)
    labels.remove('O')

    return crf
#dict_entities = dictionary_matching.build_dictionary()

#training crf for results
'''training_data = pd.read_json("../datasets/annotated_dataset.json")
test_data = pd.read_json("../datasets/experttestdata.json")

train_sents = training_data['SpanPosTag'].to_list()
test_sents = test_data['SpanPosTag'].to_list()
test_tokens = test_data['Tokens'].to_list()
test_sentences = test_data['Sentences'].to_list()
X_train = [sent2features(s) for s in train_sents]
y_train = [sent2labels(s) for s in train_sents]

X_test = [sent2features(s) for s in test_sents]
y_test = [sent2labels(s) for s in test_sents]

#print(X_train)
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=150,
    all_possible_transitions=True
)

crf.fit(X_train, y_train)
labels = list(crf.classes_)
labels.remove('O')

y_pred = crf.predict(X_test)'''


'''from seqeval.metrics import classification_report
from seqeval.scheme import IOB1
print(classification_report(y_test, y_pred,scheme = IOB1))'''





#test query
#input_text = input("Inserisci frase per la query \n")
'''sentence = input("Insert your query  \n")

print(ner_extract(sentence))
'''
