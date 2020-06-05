import pickle
import sys
from src.helper import *
from nltk.corpus import stopwords

input = sys.argv[1]
# input = "Type in the box."

# imports modules

with open('emoji_order_by_freq.pkl', 'rb') as f:
    emoji_rank = pickle.load(f)

with open('cbow.pkl', 'rb') as f:
    model1 = pickle.load(f)

with open('sg.pkl', 'rb') as f:
    model2 = pickle.load(f)

with open('gt.pickle', 'rb') as f:
    gt = pickle.load(f)

stop_words = set(stopwords.words('english')) 
stop_words.add("really")

# ensemble model determine by threshold
def ensemble_emoji_prodictor(word, model1, model2, thres):
    if word in gt:
        return gt[word]
    elif word in stop_words:
        return word
    else:
        p1 = emoji_prodictor(word, model1)
        p2 = emoji_prodictor(word, model2)
        t = int(thres * non_zero_count)
        l1 = emoji_rank[:t]
        l2 = emoji_rank[t:]
        if p2 in l2:
            return p2
        else:
            return p1

def predict_sentense(s):
    notes = [",", ".", "/'", "(" ,")",  '/"', ":", ";", "/", "(", ")", "“", "”", "-", "+", "#", "…", "!", "?"]
    for note in notes:
        s = s.replace(note, "")
    out = ""
    for c in s.lower().split(" "):
        out += " "
        out += ensemble_emoji_prodictor(c, model1, model2, thres)
    return out

def predict_para(p):
    sl = p.split("\n")
    out = ""
    for s in sl:
        out += predict_sentense(s)
        out += "\n"
    return out

print(predict_para(input))
