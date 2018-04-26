#!/usr/bin/env python
import sqlite3

DB_PATH = 'db/'
DB_NAME = 'IRIE.db'
TABLE_NAME = 'event'

#pic_url = http://laszlo-codes.com/KIOSK/img/spiderman.jpg
#batman.jpg  little-mermaid.jpg  spiderman.jpg  sw.jpg  tom-and-jerry.png  winnie-the-pooh.jpg

db = sqlite3.connect(DB_PATH + DB_NAME)

def create():
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ''' + TABLE_NAME +'''(id INTEGER PRIMARY KEY, name TEXT, info TEXT, URL TEXT)''')
    db.commit()
    return True

def drop():
    cursor = db.cursor()
    cursor.execute('''DROP TABLE '''+ TABLE_NAME)
    db.commit()
    return True

def getById(id):
    queryString = 'SELECT rowid, name, info, URL FROM '+ TABLE_NAME +' WHERE id = ?'
    cursor = db.cursor()
    cursor.execute(queryString, [int(id)])
    r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    return r

def fetchAll():
    queryString = 'SELECT rowid, name, info, URL FROM '+ TABLE_NAME
    cursor = db.cursor()
    cursor.execute(queryString)
    r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    return r

def save(name, info, URL):
    queryString = 'INSERT INTO '+ TABLE_NAME +'(name, info, URL) VALUES(?,?,?)'
    cursor = db.cursor()
    cursor.execute(queryString, [name, info, URL])
    db.commit()
    return True


def delete(id):
    queryString = 'DELETE FROM '+ TABLE_NAME +' WHERE id = ?'
    cursor = db.cursor()
    cursor.execute(queryString, [int(id)])
    db.commit()
    return True

def init():
    drop()
    create()
    save('Spiderman', 'Spider-Man is a fictional superhero appearing in American comic books published by Marvel Comics.'
                      ' The character was created by writer-editor Stan Lee and writer-artist Steve Ditko, and first'
                      ' appeared in the anthology comic book Amazing Fantasy #15 (August 1962) in the'
                      ' Silver Age of Comic Books.', 'http://laszlo-codes.com/KIOSK/img/spiderman.jpg')
    save('Tom and Jerry', 'Tom and Jerry is an American animated series of short films created in 1940 by William Hanna'
                          ' and Joseph Barbera. It centers on a rivalry between its two title characters, Tom, a cat, '
                          'and Jerry, a mouse, and many recurring characters,'
                          ' based around slapstick comedy.', 'http://laszlo-codes.com/KIOSK/img/tom-and-jerry.png')
    save('Winnie the Pooh', 'Winnie-the-Pooh, also called Pooh Bear, is a fictional anthropomorphic teddy bear created'
                            ' by English author A. A. Milne. The first collection of stories about the character was '
                            'the book Winnie-the-Pooh (1926), and this was followed by '
                            'The House at Pooh Corner (1928).', 'http://laszlo-codes.com/KIOSK/img/winnie-the-pooh.jpg')
    save('Star Wars', "Luke Skywalker's peaceful and solitary existence gets upended when he encounters Rey,"
                      " a young woman who shows strong signs of the Force. Her desire to learn the ways of "
                      "the Jedi forces Luke to make a decision "
                      "that changes their lives forever.", 'http://laszlo-codes.com/KIOSK/img/sw.jpg')
    save('The little mermaid', 'The Little Mermaid is a 1989 American animated musical fantasy film produced by'
                               ' Walt Disney Feature Animation and released by Walt Disney Pictures.'
                               ' Based on the Danish fairy tale of the same name by Hans Christian Andersen, '
                               'The Little Mermaid tells the story of a mermaid princess who dreams of'
                               ' becoming human.', 'http://laszlo-codes.com/KIOSK/img/little-mermaid.jpg')
    save('Batman', 'Batman is a fictional superhero appearing in American comic books published by DC Comics. '
                   'The character was created by artist Bob Kane and writer Bill Finger, '
                   'and first appeared in Detective Comics #27 (1939). ', 'http://laszlo-codes.com/KIOSK/img/batman.jpg')

if __name__ == "__main__":
    #drop()
    #create()
    #init()

    print(getById(1))
    #print(getById(2))
    #print ('After deleting id = 1:')
    #delete(1)
    #print(getById(1))
    #print(getById(2))