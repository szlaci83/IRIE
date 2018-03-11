import sqlite3

DB_PATH = '../db/'
DB_NAME = 'sample.db'

db = sqlite3.connect(DB_PATH + DB_NAME)

def create():
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS event(id INTEGER PRIMARY KEY, name TEXT)''')
    db.commit()
    return True

def drop():
    cursor = db.cursor()
    cursor.execute('''DROP TABLE event''')
    db.commit()
    return True

def getById(id):
    queryString = 'SELECT rowid, name FROM event WHERE id = ?'
    cursor = db.cursor()
    cursor.execute(queryString, [int(id)])
    return cursor.fetchone()

def save(name):
    queryString = 'INSERT INTO event(name) VALUES(?)'
    cursor = db.cursor()
    cursor.execute(queryString, [name])
    db.commit()
    return True


def delete(id):
    queryString = 'DELETE FROM event WHERE id = ?'
    cursor = db.cursor()
    cursor.execute(queryString, [int(id)])
    db.commit()
    return True

if __name__ == "__main__":
    #drop()
    #create()
    #save('VUE')
    #save('GALAXY')
    print(getById(1))
    print(getById(2))
    #print ('After deleting id = 1:')
    #delete(1)
    #print(getById(1))
    #print(getById(2))