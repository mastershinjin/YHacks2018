import sqlite3
import json

#facebookid to json

conn = sqlite3.connect("users.db")
c = conn.cursor()

def create_table_user_info():
    c.execute('CREATE TABLE IF NOT EXISTS accessUser(firstName TEXT, lastName TEXT, facebookID TEXT, smartcarToken TEXT, expDate TEXT)')

def check_new_user(FBid):
    c.execute("SELECT facebookID FROM accessUser")
    stringList=[]
    for elem in c.fetchall():
        stringList.append(elem[0])
    for elem in stringList:
        elem = elem.encode('utf-8')
    if FBid in stringList:
        return False
    else:
        return True

def data_entry_user_info(firstname, lastname, facebookid, accesstoken, expdate):
    if check_new_user(facebookid) == True:
        with conn:
            c.execute("INSERT INTO accessUser VALUES(:firstName, :lastName, :facebookID, :smartcarToken, :expDate)", {'firstName': firstname, 'lastName': lastname, 'facebookID': facebookid, 'smartcarToken': accesstoken, 'expDate': expdate})
            conn.commit()

def user_info(FBid):
    c.execute("SELECT * FROM accessUser")
    all_users_list = []
    for lists in c.fetchall():
        stringList=[]
        lists = list(lists)
        for elem in lists:
            stringList.append(elem.encode('utf-8'))
        all_users_list.append(stringList)
    for elem in all_users_list:
        if elem[2] == FBid:
            userDict = {
                'firstname': elem[0],
                'lastname': elem[1],
                'facebookID': elem[2],
                'accessToken': elem[3],
                'expDate': elem[4]
            }
            print(userDict)
            returnJSON=json.dumps(userDict)
            return returnJSON

def create_table_car():
    c.execute('CREATE TABLE IF NOT EXISTS userCarInfo(facebookID TEXT,jsonObject JSON)')

def car_data_entry(facebookid, jsonObject):
    with conn:
        c.execute("INSERT INTO userCarInfo VALUES(:facebookID, :jsonobject)", {'facebookID': facebookid, 'jsonobject': jsonObject})
        conn.commit()

def get_user_car_info(FBid):
    c.execute("SELECT * FROM accessUser")
    for row in c.fetchall():
       if 'facebookid' == FBid:
           return row[1]

c.close()
conn.close()
