# **Don't talk🤐, Emoji it.**


By Vince Pan

-----------------



# Table of Contents📝

[1. Background](#motivation)<br> 
[2. Data](#DATA)<br> 
>   [2.1. Source](#DATA)<br>
>   [2.2. EDA](#EDA)<br>
    
[3. EDA](#EDA)

[4. Model](#model)

[5. APP](#app)

[6. Summary](#sm)

[7. Appendix](#Appendix)

-----------------------
# Background
<a id="motivation"> </a>

## Movitation

> Originating on Japanese mobile phones in 1997, emoji became increasingly popular worldwide in the 2010s after being added to several mobile operating systems.

In 2020-01-29, the most recent version Emoji 13.0 was released with 117 new emojis which sum up to 3,304 emojis in total.

Although 3,000 doesn't seem like a big number, emojis have rich meanings and easily understood by people from different background. For instance, here is a example of behavior guideline under COVID-19.

👑🦠            (Coronavirus)

* 🚫🤦          (Don't touch your face)
* 🚫🤧🤲        (Don't sneeze into hands)
* ✅🤧💪        (Do sneeze into your elbow)
* 🧼🖐⏲        (Wash your hands regularly)
* 🚇😷🛒        (Wearing a mask in public)

Above emoji sentenses are easy to read and understood by people with different culture background. However, it is not easy to come up the correct emojis you can use to express yourself concisely.

## Goal

Our objective is to provide a solution to translate sentences from English to Emojis.

## Project Setup

The idea underneathe is we can let machine learn from how people use emoji on internet and compare with how they use English words. If they use a specific emoji and a certain word in the same situation, we believe they are substitable.

We are going to use an two-layer Nereul Network called **Word2Vec** and build two models based on CBOW and Skip-gram. After that, we tuned the models by comparing our predicting result with a ground truth dataset from web-scraping and ensemble them together to achieve the final model.

The model will be applied on an AWS EC2 instance in the form of a Web App done with Dash. The app also collects user feedback into SQL database which able us to adjust the model regularly.

<img workflow>

----------------

# DATA

## Source

### Twitter Data

There are various internet platforms like Facebook, Twitter, Instagram, where people heavily using emojis to make friend, chitchat and express their feelings. Here we utilized a **Twitter** dataset collected millions of tweets that contain at least one emoji.

* Original Site: Twitter
* Feature: Only text content

Sample Tweet

> That’s awesome! Plus you’re a Meredith Angel!!😇🤗😉

> Happy Birthday 🎊❤️

**Data Source** See [Appendix - Data Source](#DataSource)

### Ground Truth

The usage of a Ground Truth in building a translator is to benchmark how well you predict which also develops the metrics accuracy for comparing models.

Our Ground Truth data was webscraping from various emoji set which has their own emoji meanings.

For example, ☁️ in Emojipedia.com

has 3 meanings

> Cloud, Cloudy, Overcast

We webstraped the meanings for all emojis and set it as our Ground Truth data(Sometimes Grouth Truth Knowledge). We say the prediction is correct if the translate "cloud" to ☁️. The accuracy metric we use later is design as how many percentage of words in the ground Truth data was predicted correctly.


**Ground Truth** See [Appendix - Data Source](#DataSource)


## EDA<a id="EDA"> </a>

Let's take a quick look at the data.

* Size: 18,866,900 records
* 11.1 words per tweet
* 3.8 emoji per tweet*
* 2,890 Unique Emojis

Note:multiple Emoji connected with each other without space treated as one word

| Word_1 | Word_2 ... Word_(n-1) | Word_n |
|:------:|:-------------------:|:------:|
|   9%   |         31%         |   59%  |

Most emojis come in the last word of a tweet.

<img>

😂 is not only the most frequent emoji but also has a higher frequency than any English words including "the".
Fun fact: Oxford Dictionaries named 😂 as 2015 Word of the Year.


# Model<a id="model"> </a>

The technique we use in this model is called **Word2Vec** which is a two-layer Nereul Network. In simple, it vectorizes word(corpus) into numerical vectors by exploring the relationship between a target word and the neighborhood words(window). After that, we can find out the most similar emoji and English word.

> Word2vec is a group of related models that are used to produce word embeddings. These models are shallow, two-layer neural networks that are trained to reconstruct linguistic contexts of words. Word2vec takes as its input a large corpus of text and produces a vector space, typically of several hundred dimensions, with each unique word in the corpus being assigned a corresponding vector in the space. Word vectors are positioned in the vector space such that words that share common contexts in the corpus are located close to one another in the space. -Wikipedia

The word2vec model was developed by Google and easy to run in various language environment. However, it is not a straight foward work to finish well. 


## Tuning<a id="model"> </a>

In python, `work2vec` was built in the Gensim package. Here is part of the tunning history of our model in small sample.

<tunning history>
    
We can see there is % improvement from the first model to the latest tuned. More sensitive than other NLP models, text processing step in word2vec contributed a high portion in the improvement.

## Ensemble<a id="model"> </a>

We can see above models tuning history, the CBOW and Skip-gram are two algorithm we can adopt in the model which have similar scores. The different between them are CBOW is using neiborhood to predict target work while skip-gram on the opposite.


<img CBOW and Skip-gram >

The difference between them makes them tends to predict common words(CBOW) and rare words(Skip-gram) which can be seen if we weighted our accuracy by word frequency. There is a famous quoto in Chinese.

> Only kids make choice. Adults get both.

Ensembling could help us on that. The idea of ensemble models is we can merge two bad model into a faily good model. The way we ensemble these two model by a threshold determine which word should be frequent and rare.

<ensemble plot>

The final Model recorded 62% accuracy in predicting the Ground Truth, improved 55% compared to baseline(7%).

# Go Live<a id="model"> </a>

----------------

# Summary<a id="sm"> </a>

----------------

## Takeaway

### From data

* Not limited to the original meaning, people use Emoji creatively, for instance, the emoji 🍆 is often used in flirting. 
Tuning in the text processing steps is as crucial as tuning model hyperparameter in this NLP analysis.
The ensemble method is a solution to make bad predictors into a better one when advanced methods are not applicable. (RNN text generator requires TB level memory since we had 3000 more characters which usually 26+10)


### Technically:

* b

### Projects:

* c


# Appendix
<a id="Appendix"> </a>

**Data Source**
<a id="DataSource"> </a>
- **EmojifyData-EN: English tweets, with emojis**

    source: https://www.kaggle.com/rexhaif/emojifydata-en Collected by Daniil Larionov

