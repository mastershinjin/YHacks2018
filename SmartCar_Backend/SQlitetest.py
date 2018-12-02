import sqlite3


conn = sqlite3.connect("users.db")
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS accessUser(firstName TEXT, lastName TEXT, facebookID TEXT, smartcarToken TEXT, expDate REAL)')


def data_entry(firstname, lastname, userId, accesstoken, expdate):
    with conn:
        c.execute("INSERT INTO accessUser VALUES(:firstName, :lastName, :facebookID, :smartcarToken, :expDate)", {'firstName': firstname, 'lastName': lastname, 'facebookID': userId, 'smartcarToken': accesstoken, 'expDate': expdate})
        conn.commit()

create_table()
data_entry(firstname, lastname, userId, accesstoken, expdate)

c.close()
conn.close()




