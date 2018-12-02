import sqlite3
import datetime as dt
import smartcar

conn = sqlite3.connect("users.db")
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS accessUser(firstName TEXT, lastName TEXT, facebookID TEXT, smartcarToken TEXT, expDate REAL)')

#Useless get expiration date function:
# def get_expiration_date():
#     currentDateTemp = str(dt.datetime.now())
#     currentDateList = currentDateTemp[:10].split('-')
#     for elem in currentDateList:
#         elem = int(elem)
#     months_31 = [1,3,5,7,8,10,12]
#     months_30 = [4,6,9,11]
#     daysCount = 0
#     while dayCount < 58:
#         if currentDateList[1] in months_31: #If there's 31 days in the month
#             while currentDateList[2] <= 31 and daysCount < 58:
#                 currentDateList[2] += 1
#                 if currentDateList[2] == 31 #Moves to next month
#                     if currentDateList[1] < 12
#                         currentDateList[1] += 1
#                         currentDateList[2] = 0
#                     else: #Moves to next year
#                         currentDateList[0] += 1
#                         currentDaysList[1] = 1
#                         currentDaysList[2] = 1
#                 daysCount += 1
#             currentDaysList[1] = str ##

def data_entry(firstname, lastname, userId, accesstoken, expdate):
    with conn:
        firstname = #get first name here (str)
        lastname = #get last name here (str)
        userId = #get facebook user id here (str)
        accesstoken = #get refresh token here (str)
        expdate = #get exp date here (str/int??/float??)
        c.execute("INSERT INTO accessUser VALUES(:firstName, :lastName, :facebookID, :smartcarToken, :expDate)", {'firstName': firstname, 'lastName': lastname, 'facebookID': userId, 'smartcarToken': accesstoken, 'expDate': expdate})
        conn.commit()
        c.close()
        #conn.close()

# create_table()
# data_entry()




