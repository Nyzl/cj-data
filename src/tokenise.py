import pandas as pd
import nltk, string
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

#def clean(frame): 
def tokenise(**kwargs):
    frame = kwargs.get('frame')
    col = kwargs.get('col_name')

    frame[col] = frame[col].apply(lambda x: x.lower())
    frame[col] = frame[col].apply(lambda x: x.translate(string.punctuation))
    frame[col] = frame[col].apply(lambda x: x.translate(string.digits))
    frame['tokens'] = frame[col].apply(nltk.word_tokenize)
    #frame['tokens'] = frame[col].apply(lambda x: x.split(" "))
    frame = frame.explode('tokens')

    stop = set(stopwords.words('english'))
    #stop.add('uk')
    frame = frame[~frame['tokens'].isin(stop)]

    lemma = WordNetLemmatizer()
    frame['tokens'] = frame['tokens'].apply(lambda x: lemma.lemmatize(x, pos="v"))
    

    return frame