import sqlite3


conn = sqlite3.connect("users.db")
c = conn.cursor()

def create_table_car():
    c.execute('CREATE TABLE IF NOT EXISTS userCarInfo(facebookID TEXT,jsonObject JSON)')

def car_data_entry(facebookid, jsonObject):
    with conn:
        c.execute("INSERT INTO userCarInfo VALUES(facebook id, jsonobject)")
        conn.commit()

def get_user_car_info(FBid):
    c.execute("SELECT * FROM accessUser")
    for row in c.fetchall():
       if

