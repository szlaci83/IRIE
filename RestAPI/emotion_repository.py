#!/usr/bin/env python
import sqlite3, json

DB_PATH = '../db/'
DB_NAME = 'IRIE.db'
TABLE_NAME = 'emotion'

db = sqlite3.connect(DB_PATH + DB_NAME)

def drop():
    cursor = db.cursor()
    cursor.execute('''DROP TABLE ''' + TABLE_NAME)
    db.commit()
    return True

def createTable():
    queryString = 'CREATE TABLE IF NOT EXISTS ' + TABLE_NAME +' (timestamp TEXT, location TEXT, event TEXT, angry TEXT, disgust TEXT, fear TEXT, happy TEXT, sad TEXT, surprise TEXT, neutral TEXT);'
    cursor = db.cursor()
    cursor.execute(queryString)
    db.commit()

def save(timestamp, location, event, angry, disgust, fear, happy, sad, surprise, neutral):
    params = [timestamp, location, event, angry, disgust, fear, happy, sad, surprise, neutral]
    queryString = 'INSERT INTO ' + TABLE_NAME +'(timestamp, location, event, angry, disgust, fear, happy, sad, surprise, neutral) VALUES(?,?,?,?,?,?,?,?,?,?)'
    cursor = db.cursor()
    cursor.execute(queryString, params)
    db.commit()

def getByFilter(location, event, fromEpoch, toEpoch):
    queryString = 'SELECT timestamp, location, event, angry, disgust, fear, happy, sad, surprise, neutral FROM ' + TABLE_NAME +' WHERE 1'
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

def getAggregated(event):
    countQuery = 'SELECT COUNT(*) FROM ' + TABLE_NAME + " WHERE event=?;"
    cursor = db.cursor()
    cursor.execute(countQuery, [event])
    total = cursor.fetchone()[0]

    queryString = 'SELECT SUM(angry) as angry, SUM(disgust) as disgust, SUM(fear) as fear, SUM(happy) as happy, SUM(sad) as sad, SUM(surprise) as surprise, SUM(neutral)  as neutral FROM ' + TABLE_NAME + ' WHERE event=?'
    cursor = db.cursor()
    cursor.execute(queryString, [event])
    r = [dict((cursor.description[i][0], value/ total) for i, value in enumerate(row)) for row in cursor.fetchall()]
    return  r[0]

if __name__ == "__main__":

    #drop()
    #createTable()
    #save("TEST1","TEST1","TEST1",12,13,11,11,11, 11,11)
    print(getAggregated("TEST"))
    #json_output = json.dumps(getByFilter(None,'TEST',None,None))
    #print(json_output)


