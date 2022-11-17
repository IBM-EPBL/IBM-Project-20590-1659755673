import numpy as np
from flask import Flask, render_template, request, redirect, jsonify
import joblib
import inputScript
import pickle
import regex
import sys
import logging

app = Flask(__name__)
model = pickle.load(open(r'C:\SavedModel\Phishing_Website.pkl', 'rb'))


@app.route('/')   #decorator
def phishing_detection():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    url = request.form['url']
    checkprediction = inputScript.main(url)
    prediction = model.predict(checkprediction)
    print(prediction)
    output=prediction[0]
    if(output==-1):
        pred = "You are safe!! This is a Legitimate Website."
    else:
        pred = "You are on the wrong site. Be cautious!"
    return render_template('y_predict.html',prediction_text='{}'.format(pred),url=url)
        
@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    prediction = model.y_predict([np.array(list(data.values()))])
    output = prediction[0]
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)