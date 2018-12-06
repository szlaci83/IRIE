#!/usr/bin/env python
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

PORT = 4444
HOST = '0.0.0.0'
JSON_ERROR = {"error": "Bad request", "code": "400", "message": "Field missing, or bad format!"}

DB_PATH = 'db/'
DB_NAME = 'IRIE.db'
TABLE_NAME = 'event'

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
        db = sqlite3.connect(DB_PATH + DB_NAME)
        queryString = 'SELECT rowid, name, address FROM location WHERE id = ?'
        cursor = db.cursor()
        cursor.execute(queryString, [int(id)])
        r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        return addHeaders(r, 200)

    if request.method == 'DELETE':
        db = sqlite3.connect(DB_PATH + DB_NAME)
        queryString = 'DELETE FROM location WHERE id = ?'
        cursor = db.cursor()
        cursor.execute(queryString, [int(id)])
        db.commit()
        return addHeaders(True, 200)

# return a list of locations, or create a new one
@app.route("/location", methods=['POST', 'GET'])
def locationFetchAll():
    if request.method == 'GET':
        queryString = '''SELECT rowid, name, address FROM location'''
        db = sqlite3.connect(DB_PATH + DB_NAME)
        cursor = db.cursor()
        cursor.execute(queryString)
        return [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]

    if request.method == 'POST':

        if not validateJSON(request, ['name', 'address']):
            return addHeaders(JSON_ERROR, 400)

        # create the table if not exists
        db = sqlite3.connect(DB_PATH + DB_NAME)
        cursor = db.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS location (id INTEGER PRIMARY KEY, name TEXT, address TEXT)''')

        queryString = 'INSERT INTO location (name, address) VALUES(?,?)'
        cursor = db.cursor()
        cursor.execute(queryString, [request.json['name'], request.json['address']])
        db.commit()
        return addHeaders(True, 200)

# return or delete an event by ID
@app.route("/event/<event_id>", methods=['GET', 'DELETE'])
def event(event_id):
    if request.method == 'GET':
        db = sqlite3.connect(DB_PATH + DB_NAME)
        queryString = 'SELECT rowid, name, info, URL FROM event WHERE id = ?'
        cursor = db.cursor()
        cursor.execute(queryString, [int(event_id)])
        r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        return addHeaders(r, 200)

    if request.method == 'DELETE':
        db = sqlite3.connect(DB_PATH + DB_NAME)
        queryString = '''DELETE FROM event WHERE id = ?'''
        cursor = db.cursor()
        cursor.execute(queryString, [int(id)])
        db.commit()
        return addHeaders(True, 200)

# return list of events, or create one
@app.route("/event", methods=['GET', 'POST'])
def eventFetchAll():
    if request.method == 'GET':
        db = sqlite3.connect(DB_PATH + DB_NAME)
        queryString = '''SELECT rowid, name, info, URL FROM event'''
        cursor = db.cursor()
        cursor.execute(queryString)
        r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        return addHeaders(r, 200)

    if request.method == 'POST':

        if not validateJSON(request,['name', 'info', 'URL']):
            return addHeaders(JSON_ERROR, 400)
        # create the table if not exists
        db = sqlite3.connect(DB_PATH + DB_NAME)
        cursor = db.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS event (id INTEGER PRIMARY KEY, name TEXT, info TEXT, URL TEXT)''')
        db.commit()

        queryString = 'INSERT INTO ' + TABLE_NAME + '(name, info, URL) VALUES(?,?,?)'
        cursor = db.cursor()
        cursor.execute(queryString, [request.json['name'], request.json['info'], request.json['URL']])
        db.commit()

        return addHeaders(True, 200)

# create emotion and return emotion for a given event and location, event for a given time range
@app.route("/emotion", methods=['GET', 'POST'])
def emotion():
    if request.method == 'GET':
        fromDate = request.args.get('from')
        toDate = request.args.get('to')
        location = request.args.get('location')
        event = request.args.get('event')

        queryString = 'SELECT timestamp, location, event, angry, disgust, fear, happy, sad, surprise, neutral FROM emotion WHERE 1'
        params = []

        if event is not None:
            queryString += " AND event=?"
            params += [event]

        if location is not None:
            queryString += " AND location=?"
            params += [location]

        db = sqlite3.connect(DB_PATH + DB_NAME)
        cursor = db.cursor()
        cursor.execute(queryString, params)
        r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]


        response =[]
        if fromDate is None:
            fromDate = 0
        if toDate is None:
            toDate = 100000000000000000000

        for record in r:
            try:
                if (int(toDate) > int(record['timestamp']) > int(fromDate)):
                    response.append(record)
            except(TypeError, ValueError):
                pass

        return addHeaders(response, 200)

    if request.method == 'POST':
        fields = ['timestamp', 'location', 'event', 'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        if not validateJSON(request, fields):
            return addHeaders(JSON_ERROR, 400)

        JSON = request.json
        #create if not exists
        queryString = 'CREATE TABLE IF NOT EXISTS emotion (timestamp TEXT, location TEXT, event TEXT, angry TEXT, disgust TEXT, fear TEXT, happy TEXT, sad TEXT, surprise TEXT, neutral TEXT);'
        db = sqlite3.connect(DB_PATH + DB_NAME)
        cursor = db.cursor()
        cursor.execute(queryString)

        params = [JSON['timestamp'],JSON['location'], JSON['event'],JSON['angry'],JSON['disgust'],JSON['fear'],
                JSON['happy'], JSON['sad'], JSON['surprise'], JSON['neutral']]
        queryString = 'INSERT INTO ' + TABLE_NAME + '(timestamp, location, event, angry, disgust, fear, happy, sad, surprise, neutral) VALUES(?,?,?,?,?,?,?,?,?,?)'
        cursor = db.cursor()
        cursor.execute(queryString, params)
        db.commit()
        return addHeaders(JSON, 200)

# gets aggregated emotion data for a given event
@app.route("/emotion/aggregated", methods=['GET'])
def aggregated_emotion():
    event = request.args.get('event')

    if event is None:
        return addHeaders('error": "Bad request", "code": "400", "message": "Event missing from request parameter!', 400)

    countQuery = '''SELECT COUNT(*) FROM emotion WHERE event=?;'''
    db = sqlite3.connect(DB_PATH + DB_NAME)

    cursor = db.cursor()
    cursor.execute(countQuery, [event])
    total = cursor.fetchone()[0]

    queryString = 'SELECT SUM(angry) as angry, SUM(disgust) as disgust, SUM(fear) as fear, SUM(happy) as happy, SUM(sad) as sad, SUM(surprise) as surprise, SUM(neutral)  as neutral FROM emotion WHERE event=?'
    db = sqlite3.connect(DB_PATH + DB_NAME)

    cursor = db.cursor()
    cursor.execute(queryString, [event])
    r = [dict((cursor.description[i][0], value / total) for i, value in enumerate(row)) for row in cursor.fetchall()]
    return addHeaders(r[0], 200)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)