import sqlite3


conn = sqlite3.connect('Kaffee.db')

conn.execute('''CREATE TABLE IF NOT EXISTS Kaffeeliste 
         (ID INTEGER PRIMARY KEY,
         HASH           TEXT,
         NAME           TEXT,
         COFFEES        INT NOT NULL,
         PAID           INT);''')


conn.commit()
conn.close()