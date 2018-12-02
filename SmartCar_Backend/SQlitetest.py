import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS accessUser(firstName TEXT, lastName TEXT, facebookID TEXT, smartcarToken TEXT, expDate TEXT)')

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
            return(elem)

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

def data_entry(firstname, lastname, facebookid, accesstoken, expdate):
    if check_new_user(facebookid) == True:
        with conn:
            c.execute("INSERT INTO accessUser VALUES(:firstName, :lastName, :facebookID, :smartcarToken, :expDate)", {'firstName': firstname, 'lastName': lastname, 'facebookID': facebookid, 'smartcarToken': accesstoken, 'expDate': expdate})
            conn.commit()

c.close()
conn.close()





