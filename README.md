# **Don't talk🤐, Emoji it.**


By Vince Pan

-----------------



# Table of Contents📝

[1. ⁉️Motivation](#motivation)<br> 
[2. Data](#DATA)<br> 
>   [2.1. A](#DATA)<br>
>   [2.2. B](#Dataacquisition)<br>
    
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


## EDA

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

33

Model building:
Processed text into a two-layer Nereul Network called Word2Vec
Tuned model hyperparameters in a small sample
Tuned model with text processing techniques in a small sample
Built 2 Word2Vec algorithms.  CBOW and skip-gram have different advantages in predicting common or rare words.                                           
Ensembled two algorithms with a threshold to determine which word is frequent.
The final Model recorded 62% accuracy in predicting the Ground Truth, improved 55% compared to baseline(7%).
Web APP:
Built a real-time translation Web App with Dash
Published on an AWS EC2 instance
Collecting user feedback into SQL database which able us to adjust the model regularly

## Data acquisition
<a id="Dataacquisition"> </a>


### Pipeline



------------------------

# EDA<a id="EDA"> </a>

-------------------
## EDA on Case Data<a id="case"> </a>

----------------

----------------

# Model<a id="model"> </a>



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

