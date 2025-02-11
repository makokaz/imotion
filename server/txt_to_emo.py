# Using the trained model for making predictions
# from server.image_captioning import image2caption
import pandas as pd
from nltk.corpus import stopwords
from textblob import Word
import pickle
from flask import Flask, request, render_template,jsonify
from flask_cors import CORS
import sys

# sys.path.append('../')
# import image_captioning

file = './server/text_to_emotion/count_vector.sav'
count_vect = pickle.load(open(file, 'rb'))

filename = './server/text_to_emotion/finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

tweets = pd.DataFrame(['She seems very happy in the picture, and you want to know\n what what is behind the smile.',
'This woman has really knotty hands which makes her look like she has arthritis.', 
'When looking at this woman, I am filled with curiosity about what \nshe is thinking about with her elbow on the table and a very emotionless face.', 
'A woman looking at ease, peaceful, and satisfied amongst her books makes me feel content.',
'She looks like a lady from that past that might have been a teacher (books).\nShe looks tired and I wondered how hard it must have been for them back then.',
'The bright colors make a very unique scene for the interesting shapes.',
'The way the image is presented, with large chunks of paint used to depict each of the subjects,\nmakes for a slight amount of confusion and an unsureness on the part of the viewer: what, exactly, was Kandinsky trying to depict during Autumn?'])
# print(tweets)

# Doing some preprocessing on the text
tweets[0] = tweets[0].str.replace('[^\w\s]',' ')
from nltk.corpus import stopwords
stop = stopwords.words('english')
tweets[0] = tweets[0].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
# from textblob import Word
tweets[0] = tweets[0].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
# Extracting Count Vectors feature from our tweets
tweet_count = count_vect.transform(tweets[0])

#Predicting the emotion of the tweet using our already trained linear SVM
tweet_pred = loaded_model.predict(tweet_count)
# print(tweet_pred)

def preprocess(txt):
    t = str(txt)
    tweets = pd.DataFrame([t], columns=['str'])
    # print(tweets)

    # Doing some preprocessing on these tweets as done before
    tweets['str'] = tweets['str'].str.replace('[^\w\s]',' ')

    stop = stopwords.words('english')
    tweets['str'] = tweets['str'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

    tweets['str'] = tweets['str'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
    # Extracting Count Vectors feature from our tweets
    tweet_count = count_vect.transform(tweets['str'])
    tweet_pred = loaded_model.predict(tweet_count)
    return tweet_pred

def generate_emo(txt):
    res = []
    for i in txt:
        if i==4:
            print('Happiness')
            res.append('hapiness')
        elif i==6:
            print('Sadness')
            res.append('sadness')
        elif i==8:
            print('Enthusiasm')
            res.append('surprise')
        elif i==5:
            print('Hate')
            res.append('anger')
        else: # default emotion
            print('Deafult emotion: Surprise')
            res.append('surprise')
    return res

# app = Flask(__name__)
# CORS(app, supports_credentials=True)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/res', methods=['GET'])
# def txt_to_emo():
#     text = image_captioning.image2caption('../img2.jpg')
#     print(text)
#     preds = preprocess(text)
#     response = generate_emo(preds)
#     return jsonify(result=response)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
