# flask_sklearn_dumb
-Download all packages using npm
-Dependencies: 
-	Python 3.6.__
-	pandas 0.22.0
-	numpy 1.14.0
-	scipy 1.0.0
-	sklearn 0.19.1
-	flask 0.12.2
-Can use the versions.py to check if all dependencies are correct versions
-open command line and run : 
-$ python ml_service


Project
A python app ml_service that can be used use to train a model that predicts the variable
score based on the given variables age and species by sending JSON data to it over HTTP.

Example usage:
# start the server
$ ml_service &
# send a training examples to server
$ curl -H "Content-Type: application/json" -X POST -d '{"age": 1.1, "species": "cat", "score": 3.1}' http://localhost:5000/learn
ok
# send a few more examples
# train model
$ curl -X POST http://localhost:5000/train
ok
# ask server for a prediction
$ curl -H "Content-Type: application/json" -X POST -d '{"age": 4.5, "species": "dog"}' http://localhost:5000/predict
{"score": 5.245}

