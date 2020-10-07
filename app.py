# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import joblib

app = Flask(__name__)

model = joblib.load("Students_Score_Predictor.pkl")

df = pd.DataFrame()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    global df
    
    input_features = [int(x) for x in request.form.values()]
    features_value = np.array(input_features)
    
    #validate input hours
    if input_features[0] <1 or input_features[0] >11:
        return render_template('index.html', prediction_text='Please enter valid hours greater than 0 to less than 12 as we also care for your health and proper sleep along with studies.')
        

    output = model.predict([features_value])[0][0].round(2)

    # input and predicted value store in df then save in csv file
    df= pd.concat([df,pd.DataFrame({'Study Hours':input_features,'Predicted Output':[output]})],ignore_index=True)
    print(df)   
    df.to_csv('smp_data_from_app.csv')

    return render_template('index.html', prediction_text='You will get [{}%] Score, when you do study [{}] hours per day. '.format(output, int(features_value[0])))


if __name__ == "__main__":
    app.run()
