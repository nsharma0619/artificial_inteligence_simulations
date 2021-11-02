import json
import os
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tensorflow as tf
import tflearn
import random
import json
import pickle

def bag_of_words(s, words, stemmer):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w==se:
                bag[i] = 1
    return np.array(bag)


def chatbot(query, username):
    inp = query
    stemmer = LancasterStemmer()
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(path, 'static/chatbot/models', f'{username}')
    with open(os.path.join(path, 'data.pickle'), "rb") as f:
        data, words, labels, training, output = pickle.load(f)
    tf.compat.v1.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)
    model.load(os.path.join(path, 'model.tflearn'))
    results = model.predict([bag_of_words(inp, words, stemmer)])[0]
    results_index = np.argmax(results)
    tag = labels[results_index]
    
    if results[results_index]>0.8:
        for tg in data["intents"]:
            if tg['tag']==tag:
                responses = tg["responses"]
        return random.choice(responses)
    return "I didn't get that, try again."

def train_chatbot(username):
    path = os.path.abspath(os.path.dirname(__file__))
    path1 = os.path.join(path, 'static/chatbot/intents/personal_intents', f'{username}_personal_intent.json')
    path2 = os.path.join(path, 'static/chatbot/intents/general_intents/general_intents.json')
    stemmer = LancasterStemmer()
    with open(path1) as file:
        data1 = json.load(file)
    with open(path2) as file:
        data2 = json.load(file)
    data = {'intents':data1['intents']+data2['intents']}
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data['intents']:
        for pattern in intent['patterns']:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent['tag'])
        
        if intent['tag'] not in labels:
            labels.append(intent['tag'])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    path3 = os.path.join(os.path.join(path, 'static/chatbot/models', username))

    try:
        os.mkdir(path3)
    except OSError as error: 
        pass
    with open(os.path.join(path3, "data.pickle"), "wb") as f:
        pickle.dump((data, words, labels, training, output), f)

    tf.compat.v1.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save(os.path.join(os.path.join(path, 'static/chatbot/models', username, "model.tflearn")))
    return True

def make_intents(data, username):
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(path, 'static/chatbot/intents/personal_intents', f'{username}_personal_intent.json')
    intents = {"intents": [
        {"tag": "name",
         "patterns": ["what is your name", "what should I call you", "whats your name?", "who are you?", "What could I call you?", "What do your friends call you?", "Tell me your name?"],
         "responses": [f"You can call me {data.get('name')}.", f"I'm {data.get('name')}!", f"Myself {data.get('name')}."],
         "context_set": ""
        },
        {"tag": "email",
         "patterns": ["what is your email?", "how can i contact you?", "what is your contact number?"],
         "responses": [f'Our email id is {data.get("email")}.'],
         "context_set": ""
        },
        {"tag": "about",
         "patterns": ["Tell me about yourself.", "what do you do?", "how can you help me?"],
         "responses": [data.get("about")],
         "context_set": ""
        },
        {"tag": "service_areas",
         "patterns": ["where are you serving?", "where are you operational?"],
         "responses": [f'we are operational in {data.get("service_areas")}'],
         "context_set": ""
        }
    ]
    }
    with open(path, "w") as outfile:
        json.dump(intents, outfile)


if __name__ == "__main__":
    make_intents("name", "email", "about", "service_areas", "abd")