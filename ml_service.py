import os.path as path

import pandas as pd

from flask import Flask
from flask import jsonify
from flask import request

from sklearn.svm import LinearSVR

app = Flask(__name__)
classifier = None
trained_columns = None

#Adjust for dummy columns used in training set
def preparePredictInput(df):
	missingLabels = list(set(trained_columns) - set(df.columns.values) - set(['score']))
	for label in missingLabels:
		if(label[8:] == df.iloc[:1]['species'][0]): df[label] = 1
		else: df[label] = 0
	df.drop(columns=['species'], axis=1, inplace=True)
	return df

#Extract json data from http request
def data_extraction():
	learn_data = request.get_json()
	req_frame = pd.DataFrame(learn_data, index=[0])
	return req_frame

#Load pre-existing data
def get_existing():
	existing_frame = pd.DataFrame()
	if path.isfile('learner.csv'):
		existing_frame = pd.read_csv('learner.csv')
	return existing_frame

#index route
@app.route("/")
def startup():
    return '<h1>This is an ml_service for amphilabs<h1>'

#learn route to store new examples
@app.route("/learn", methods=['POST'])
def learn():
	existing_frame = get_existing()
	req_frame = data_extraction()
	if existing_frame.empty==False:
		req_frame = pd.concat([existing_frame,req_frame])
		req_frame.drop_duplicates()
	req_frame.to_csv('learner.csv', index=False)
	return 'ok'

#train route to run classifier training
@app.route("/train", methods=['POST'])
def train():
	existing_frame = get_existing()
	if existing_frame.empty==False:
		existing_frame = pd.get_dummies(existing_frame, columns=['species']).head()
		global trained_columns, classifier
		trained_columns = existing_frame.columns.values
		existing_frame.to_csv('check.csv')
		classifier = LinearSVR().fit(existing_frame.loc[:,existing_frame.columns != 'score'],existing_frame[['score']])
		return 'ok'
	else : return "Error: No training data available!"

#Route to retian predictions
@app.route("/predict", methods=['POST'])
def predict():
	if classifier != None :
		predict_frame = data_extraction()
		predict_frame = preparePredictInput(predict_frame)
		predict_frame.to_csv('Check2.csv')
		prediction = classifier.predict(predict_frame)
		return str(prediction)
	return 'Please Train Classifier'

if __name__ == "__main__":
	app.run(use_reloader=True)
