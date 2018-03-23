#!/usr/bin/env python
import sqlite3, json

DB_PATH = '../db/'
DB_NAME = 'sample.db'

db = sqlite3.connect(DB_PATH + DB_NAME)

#TODO: add create table if not exist

def create(timestamp, event, angry, disgust, fear, happy, sad, surprise, neutral):
    params = [timestamp, event, angry, disgust, fear, happy, sad, surprise, neutral]
    queryString = 'INSERT INTO stuffToPlot(timestamp, event, angry, disgust, fear, happy, sad, surprise, neutral) VALUES(?,?,?,?,?,?,?,?,?)'
    cursor = db.cursor()
    cursor.execute(queryString, params)
    db.commit()


#def JSONifyCursor(cursor):

def fetchAll(location, event, fromEpoch, toEpoch):
    queryString = 'SELECT timestamp, event, angry, disgust, fear, happy, sad, surprise, neutral FROM stuffToPlot WHERE 1'
    params = []

    if event is not None:
        queryString += " AND event=?"
        params += [event]

    if location is not None:
        queryString += " AND location=?"
        params += [location]

    if fromEpoch is not None:
        queryString += " AND ?<timestamp"
        params += [toEpoch]

    if toEpoch is not None:
        queryString += " AND ?>timestamp"
        params += [toEpoch]

    cursor = db.cursor()
    cursor.execute(queryString, params)
    r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    return r


if __name__ == "__main__":
    json_output = json.dumps(fetchAll(None,'Jurassic Park',None,None))
    print(json_output)