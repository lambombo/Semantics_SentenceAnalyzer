import os

from flask import Flask, Blueprint, request, jsonify, make_response
from config import config
from nltk import ngrams
from string import punctuation

def get_ngrams(text):
    translation = str.maketrans("","", punctuation)
    data = {}
    data['rawSentence'] = text
    data['cleanSentence'] = text.translate(translation)
    data['parsedSentence'] = data['cleanSentence'].split()
    for i in range(3,len(data['parsedSentence'])+1):
        ngramStr = str(i) + 'gram'
        ngram = ngrams(data['parsedSentence'], i)
        data[ngramStr] = [i for i in ngram]
    return data

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize flask extensions

    # Register API routes
    @app.route('/', methods=['POST','GET'])
    def main():
        if request.method == 'GET':
            data = {"status":"ok"}
            return jsonify(data=data), 200
        if request.method == 'POST':
            try:
                json_data = request.get_json()
                text = json_data['body']
                data = get_ngrams(text)
                return make_response(jsonify(data = data), 200) 
            except Exception as e:
                data = dict(error = 'Unable to process request')
                return make_response(jsonify(data = data), 200)
        return jsonify(data = {"status":"ok"}), 200
        
    return app
