#!/usr/bin/env python
import sqlite3, json

DB_PATH = '../db/'
DB_NAME = 'sample.db'

db = sqlite3.connect(DB_PATH + DB_NAME)

#def JSONifyCursor(cursor):

def fetchAll(location, event, fromEpoch, toEpoch):
    queryString = 'SELECT timestamp, event, angry, disgust, fear, happy, sad, surprise, neutral FROM stuffToPlot WHERE '#?<timestamp '
    params = []

    if location is not None:
        queryString += " AND location=? "
        params += [location]

    if event is not None:
        queryString += " event=? "
        params += [event]

    if location is not None:
        queryString += " AND ?>timestamp "
        params += [toEpoch]

    cursor = db.cursor()
    cursor.execute(queryString, params)
    r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    return r


if __name__ == "__main__":
    json_output = json.dumps(fetchAll(None,'Jurassic Park',None,None))
    print(json_output)

#def create_table():
#    c.execute("CREATE TABLE IF NOT EXISTS stuffToPlot(timestamp TEXT, event TEXT, location TEXT, angry  REAL, disgust  REAL, fear  REAL, happy  REAL, sad  REAL, surprise  REAL, neutral  REAL)")
