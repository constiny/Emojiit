from nltk.tokenize import sent_tokenize, word_tokenize 
import pandas as pd
import numpy as np
import pickle

# move to helper
# load emoji list
val_df = pd.read_csv("data/emoji_val.2csv",index_col=0)
emoji_list = val_df["emoji"].values.tolist()

non_zero_count = 1436
thres = 0.44

def data_input_preprocess(filename):
    # read
    sample = open(filename, "r") 
    s = sample.read() 

    # Replaces escape character with space 
    f = s.replace("\n", " ") 
    # replace all punc
    notes = [",", ".", "/'", "(" ,")", "'", '/"', ":", ";", "/", "(", ")", "“", "”", "-", "+", "#", "…", "!"]
    for note in notes:
        f = f.replace(note, "")
    for emoji in emoji_list:
        f = f.replace(emoji, emoji+" ")
    return f

def data_tokenize(f):
    data = [] 
    # iterate through each sentence in the file 
    for i in sent_tokenize(f): 
        temp = [] 

        # tokenize the sentence into words 
        for j in word_tokenize(i): 
            temp.append(j.lower()) 

        data.append(temp)
    return data
        
# move to helper
def emoji_prodictor(word, model):
    if word in model.wv:
        sim = model.most_similar(word,topn=75)
        for i in sim:
            if i[0] in emoji_list:
                return i[0]

    return word

# ensemble model determine by threshold
def ensemble_emoji_prodictor(word, model1, model2, thres):
    p1 = emoji_prodictor(word, model1)
    p2 = emoji_prodictor(word, model2)
    t = int(thres*non_zero_count)
    l1 = list(sort_freq.keys())[:t]
    l2 = list(sort_freq.keys())[t:]
    if p2 in l2:
        return p2
    else:
        return p1
        
########### Scoring ############
    
# load the ground-truth
with open('val_dict2.pickle', 'rb') as handle:
    val_dict = pickle.load(handle)
  
# define score function 
def word2vec_score(val_dict, model):
    total_words = 0
    total_predicts = 0
    correct = 0
    words = []
    word_vectors = model.wv
    for word in val_dict:
#         print(word)
        if word:
            w = word.lower()
            words.append(w)
            if w in word_vectors:
                total_words += 1
                if emoji_prodictor(w, model) in val_dict[word]:
                    correct += 1
                    total_predicts += 1
                elif emoji_prodictor(w, model) in emoji_list:
                    total_predicts += 1
    return correct/total_words, correct/total_predicts, words
            
def word2vec_weighted_score(val_dict, model,emoji_frequency):
    total_words = 0
    total_weighted = 0
    correct_weighted = 0
#     words = []
    word_vectors = model.wv
    for word in val_dict:
        if word:
            w = word.lower()
#             words.append(w)
            if w in word_vectors:
                total_words += 1
                prediction = emoji_prodictor(w, model)
                if prediction in val_dict[word]:
                    correct_weighted += emoji_frequency[prediction]
                    total_weighted += emoji_frequency[prediction]
                elif prediction in emoji_list:
                    total_weighted += emoji_frequency[prediction]
    return correct_weighted/total_weighted
    
# new predictor with higher requirement to predict
def emoji_prodictor_restricted(word, model, thres_n_word=75, thres_corr=0):
    sim = model.most_similar(word,topn=thres_n_word)
    for i in sim:
        if i[0] in emoji_list and i[1] >= thres_corr:
            return i[0]
    return word


def word2vec_score_emsemble(val_dict,model1, model2, thres):
    total_words = 0
    total_predicts = 0
    correct = 0
    words = []
    word_vectors = model1.wv
    for word in val_dict:
#         print(word)
        if word:
            w = word.lower()
            words.append(w)
            if w in word_vectors:
                total_words += 1
                pred = ensemble_emoji_prodictor(w, model1, model2, thres)
                if pred in val_dict[word]:
                    correct += 1
                    total_predicts += 1
                elif pred in emoji_list:
                    total_predicts += 1
    return correct/total_words, correct/total_predicts, words
            

    
    
########## Abondon #############
# move to helper (abandon)
def word_pipeline(sentense):
    out = [word for word in sentense.lower().split(" ") if word not in stop]
    out = [snowball.stem(word) for word in out]
    return out
    
# define score function with stemmer and trim stop words
def word2vec_score_stemmer(val_dict, model):
    total_words = 0
    total_predicts = 0
    correct = 0
    words = []
    word_vectors = model.wv
    for word in val_dict:
#         print(word)
        if word_pipeline(word):
            w = word_pipeline(word)[0]
            words.append(w)
            if w in word_vectors:
                total_words += 1
                if emoji_prodictor(w, model) in val_dict[word]:
                    correct += 1
                    total_predicts += 1
                elif emoji_prodictor(w, model) in emoji_set:
                    total_predicts += 1
    return correct/total_words, correct/total_predicts, words
