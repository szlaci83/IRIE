#!/usr/bin/env python
from flask import Flask, jsonify, request, Response, make_response, current_app
from flask_cors import CORS
import emotion_repository as repo

app = Flask(__name__)
CORS(app)

# return/add/delete location
@app.route("/location/<location_id>", methods=['GET', 'POST', 'DELETE'])
def location(location_id):
    if request.method == 'GET':
        return 0
    if request.method == 'POST':
        return 0
    if request.method == 'DELETE':
        return 0

# return/add/delete  event for a given event
@app.route("/event/<event_id>", methods=['GET', 'POST', 'DELETE'])
def event(event_id):
    if request.method == 'GET':
        return 0
    if request.method == 'POST':
        return 0
    if request.method == 'DELETE':
        return 0

# return emotion for a given event and location
@app.route("/", methods=['POST'])
def saveEmotion():
    fields = ['timestamp', 'event', 'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

    for field in fields:
        if not request.json or not field in request.json:
            response = jsonify({"error": "Bad request", "code": "400", "message": "Field missing, or bad format!"}), 400
            make_response(response)
            return response

    JSON = request.json
    repo.create(JSON['timestamp'], JSON['event'],JSON['angry'],JSON['disgust'],JSON['fear'],
                JSON['happy'], JSON['sad'], JSON['surprise'], JSON['neutral'])

    response = jsonify(JSON), 200
    response = make_response(response)
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['content-type'] = "application/json"
    return response


# return emotion for a given event and location
@app.route("/emotion", methods=['GET'])
def getEmotionForEventAndLocation():

    fromDate = request.args.get('from')
    toDate = request.args.get('to')
    location = request.args.get('location')
    event = request.args.get('event')

    responseJSON = repo.fetchAll(location, event, fromDate, toDate)

    response = jsonify(responseJSON), 200
    response = make_response(response)
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['content-type'] = "application/json"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4444)