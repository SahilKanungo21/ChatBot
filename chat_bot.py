import random
import json
import pickle

import nltk
import numpy as np

from nltk.stem import WordNetLemmatizer

from keras.models import load_model

from flask import Flask, jsonify

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

model = load_model('chatbot.model.h5')

app = Flask(__name__)


def clean_up_sentence(sentence):
    sentence_tokenize = nltk.word_tokenize(sentence)
    sentence_tokenize = [lemmatizer.lemmatize(word) for word in sentence_tokenize]
    return sentence_tokenize


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for token_words in sentence_words:
        for pos, word in enumerate(words):
            if word == token_words:
                bag[pos] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESOLD = 0.25
    result = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESOLD]

    result.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in result:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})

    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


def MessageFromModel(user_message):
    ints = predict_class(user_message)
    bot_message = get_response(ints, intents)
    return bot_message


@app.route('/BotMessage/<string:userMessage>', methods=['GET'])
def GetBotMessageFromModel(userMessage: str):
    result = {'botMessage': MessageFromModel(userMessage)}
    return jsonify(result)


if __name__ == '__main__':
    app.run()
