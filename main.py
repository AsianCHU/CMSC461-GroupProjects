import sqlite3

db_name = ''
connection = sqlite3.connect(db_name)
cursor = connection.cursor()

def insertOffice(name, city, area):
    cursor.execute('INSERT INTO office (name, city, area) VALUES (?, ?, ?)', 
    (name, city, area))
    connection.commit

def getOffice():
    cursor.execute('SELECT * FROM office')

def deleteOffice(name):
    cursor.execute('DELETE FROM office WHERE name = ?', name)


#at end of program
connection.close()