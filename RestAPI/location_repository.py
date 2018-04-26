#!/usr/bin/env python
import sqlite3

DB_PATH = 'db/'
DB_NAME = 'IRIE.db'
TABLE_NAME = 'location'

db = sqlite3.connect(DB_PATH + DB_NAME)

def create():
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ''' + TABLE_NAME +'''(id INTEGER PRIMARY KEY, name TEXT, address TEXT)''')
    db.commit()
    return True

def drop():
    cursor = db.cursor()
    cursor.execute('''DROP TABLE ''' + TABLE_NAME)
    db.commit()
    return True

def getById(id):
    queryString = 'SELECT rowid, name, address FROM ' + TABLE_NAME +' WHERE id = ?'
    cursor = db.cursor()
    cursor.execute(queryString, [int(id)])
    r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    return r

def fetchAll():
    queryString = 'SELECT rowid, name, address FROM ' + TABLE_NAME
    cursor = db.cursor()
    cursor.execute(queryString)
    r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    return r

def save(name, address):
    queryString = 'INSERT INTO ' + TABLE_NAME +'(name, address) VALUES(?,?)'
    cursor = db.cursor()
    cursor.execute(queryString, [name, address])
    db.commit()
    return True


def delete(id):
    queryString = 'DELETE FROM ' + TABLE_NAME +' WHERE id = ?'
    cursor = db.cursor()
    cursor.execute(queryString, [int(id)])
    db.commit()
    return True

if __name__ == "__main__":
   # drop()
    create()
   # save('VUE6', 'TEST')
   # save('GALAXY6', 'TEST')
    #print(getById(1))
   # print(getById(2))
   # print ('After deleting id = 1:')
   # delete(1)
   # print(getById(1))
   # print(getById(2))
