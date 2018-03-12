#!/usr/bin/env python
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import emotion_repository as emo_repo
import location_repository as loc_repo
import event_repository as event_repo

app = Flask(__name__)
CORS(app)

def addHeader(response, HTTP_code):
    response = jsonify(response), HTTP_code
    response = make_response(response)
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['content-type'] = "application/json"
    return response

# return or delete a location by ID
@app.route("/location/<location_id>", methods=['GET', 'DELETE'])
def location(location_id):
    if request.method == 'GET':
        return addHeader(loc_repo.getById(location_id), 200)

    if request.method == 'DELETE':
        return addHeader(loc_repo.delete(location_id), 200)

# return a list of locations, or create a new one
@app.route("/location", methods=['POST', 'GET'])
def locationFetchAll():
    if request.method == 'GET':
        return addHeader(loc_repo.fetchAll(), 200)

    if request.method == 'POST':
        if not request.json or not 'name' in request.json:
            return addHeader({"error": "Bad request", "code": "400", "message": "Field missing, or bad format!"}, 400)

        # create the table if not exists
        loc_repo.create()
        return addHeader(loc_repo.save(request.json['name']), 200)

# return or delete an event by ID
@app.route("/event/<event_id>", methods=['GET', 'DELETE'])
def event(event_id):
    if request.method == 'GET':
        return addHeader(event_repo.getById(event_id), 200)

    if request.method == 'DELETE':
        return addHeader(event_repo.delete(event_id), 200)

# return list of events, or create one
@app.route("/event", methods=['GET', 'POST'])
def eventFetchAll():
    if request.method == 'GET':
        return addHeader(event_repo.fetchAll(), 200)

    if request.method == 'POST':
        if not request.json or not 'name' in request.json:
            return addHeader({"error": "Bad request", "code": "400", "message": "Field missing, or bad format!"}, 400)

        # create the table if not exists
        event_repo.create()
        return addHeader(event_repo.save(request.json['name']), 200)

# create emotion
@app.route("/", methods=['POST'])
def saveEmotion():
    fields = ['timestamp', 'event', 'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

    for field in fields:
        if not request.json or not field in request.json:
            return addHeader({"error": "Bad request", "code": "400", "message": "Field missing, or bad format!"}, 400)


    JSON = request.json
    emo_repo.create(JSON['timestamp'], JSON['event'],JSON['angry'],JSON['disgust'],JSON['fear'],
                JSON['happy'], JSON['sad'], JSON['surprise'], JSON['neutral'])

    return addHeader(JSON, 200)

# return emotion for a given event and location
@app.route("/emotion", methods=['GET'])
def getEmotionForEventAndLocation():

    fromDate = request.args.get('from')
    toDate = request.args.get('to')
    location = request.args.get('location')
    event = request.args.get('event')

    responseJSON = emo_repo.fetchAll(location, event, fromDate, toDate)

    return addHeader(responseJSON, 200)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4444)