#!/usr/bin/env python
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import emotion_repository as emo_repo
import location_repository as loc_repo
import event_repository as event_repo

app = Flask(__name__)
CORS(app)

PORT = '4444'
HOST = '0.0.0.0'
JSON_ERROR = {"error": "Bad request", "code": "400", "message": "Field missing, or bad format!"}

def addHeaders(response, HTTP_code):
    response = jsonify(response), HTTP_code
    response = make_response(response)
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['content-type'] = "application/json"
    return response

def validateJSON(req, fields):
    for field in fields:
        if not req.json or not field in req.json:
            return False
    return True

# return or delete a location by ID
@app.route("/location/<location_id>", methods=['GET', 'DELETE'])
def location(location_id):
    if request.method == 'GET':
        return addHeaders(loc_repo.getById(location_id), 200)

    if request.method == 'DELETE':
        return addHeaders(loc_repo.delete(location_id), 200)

# return a list of locations, or create a new one
@app.route("/location", methods=['POST', 'GET'])
def locationFetchAll():
    if request.method == 'GET':
        return addHeaders(loc_repo.fetchAll(), 200)

    if request.method == 'POST':
        if not validateJSON(request,['name', 'address']):
            return addHeaders(JSON_ERROR, 400)

        # create the table if not exists
        loc_repo.create()
        return addHeaders(loc_repo.save(request.json['name'], request.json['address']), 200)

# return or delete an event by ID
@app.route("/event/<event_id>", methods=['GET', 'DELETE'])
def event(event_id):
    if request.method == 'GET':
        return addHeaders(event_repo.getById(event_id), 200)

    if request.method == 'DELETE':
        return addHeaders(event_repo.delete(event_id), 200)

# return list of events, or create one
@app.route("/event", methods=['GET', 'POST'])
def eventFetchAll():
    if request.method == 'GET':
        return addHeaders(event_repo.fetchAll(), 200)

    if request.method == 'POST':
        if not validateJSON(request,['name', 'info', 'URL']):
            return addHeaders(JSON_ERROR, 400)
        # create the table if not exists
        event_repo.create()
        return addHeaders(event_repo.save(request.json['name'], request.json['info'], request.json['URL']), 200)

# create emotion and return emotion for a given event and location, event for a given time range
@app.route("/emotion", methods=['GET', 'POST'])
def emotion():
    if request.method == 'GET':
        fromDate = request.args.get('from')
        toDate = request.args.get('to')
        location = request.args.get('location')
        event = request.args.get('event')

        responseJSON = emo_repo.getByFilter(location, event, fromDate, toDate)
        return addHeaders(responseJSON, 200)

    if request.method == 'POST':
        fields = ['timestamp', 'location', 'event', 'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        if not validateJSON(request, fields):
            return addHeaders(JSON_ERROR, 400)

        JSON = request.json
        #create if not exists
        emo_repo.createTable()
        emo_repo.save(JSON['timestamp'],JSON['location'], JSON['event'],JSON['angry'],JSON['disgust'],JSON['fear'],
                JSON['happy'], JSON['sad'], JSON['surprise'], JSON['neutral'])
        return addHeaders(JSON, 200)

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)