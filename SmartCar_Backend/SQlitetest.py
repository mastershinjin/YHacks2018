import sqlite3


conn = sqlite3.connect("users.db")
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS accessUser(firstName TEXT, lastName TEXT, facebookID TEXT, smartcarToken TEXT, expDate REAL)')


def check_new_user(id):
    c.execute("SELECT facebookID FROM accessUser")
    stringList=[]
    for elem in c.fetchall():
        stringList.append(elem[0])
    for elem in stringList:
        elem = elem.encode('utf-8')
    if id in stringList:
        return False
    else:
        return True


def data_entry(firstname, lastname, userId, accesstoken, expdate):
    if check_new_user(userId) == True:
        with conn:
            c.execute("INSERT INTO accessUser VALUES(:firstName, :lastName, :facebookID, :smartcarToken, :expDate)", {'firstName': firstname, 'lastName': lastname, 'facebookID': userId, 'smartcarToken': accesstoken, 'expDate': expdate})
            conn.commit()

c.close()
conn.close()





