import hashlib
from flask import Flask, render_template, request, session
from flaskext.mysql import MySQL
import datetime
import time

app = Flask(__name__)
app.secret_key = 'any random string'
mysql = MySQL()

# MySQL configurations;
app.config['MYSQL_DATABASE_USER'] = 'guest'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'majormatch'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

class Node:
    def __init__(self, UserID, Value):
        self.Profile = UserID
        self.score = Value

def matching(DesiredAttributes, AllAttributes):
    List = []
    DesiredAcademicStatus = DesiredAttributes[1]
    DesiredGPA  = DesiredAttributes[2]
    DesiredSH = DesiredAttributes[3]
    DesiredAU = DesiredAttributes[4]
    DesiredCU = DesiredAttributes[5]
    DesiredVU = DesiredAttributes[6]
    DesiredHC = DesiredAttributes[7]
    DesiredEth = DesiredAttributes[8]
    DesiredGender = DesiredAttributes[9]
    DesiredHE = DesiredAttributes[10]
    DesiredWeekendSt = DesiredAttributes[11]
    DesiredWeekendE = DesiredAttributes[12]
    DesiredWeekSt = DesiredAttributes[13]
    DesiredWeekE = DesiredAttributes[14]
    DesiredMajorID = DesiredAttributes[15]
    DesiredMajorName = DesiredAttributes[16]


    for k in range(len(AllAttributes)):
        Attributes = AllAttributes[k]
        Score = 0
        OtherAcademicStatus = Attributes[1]
        OtherGPA = Attributes[2]
        OtherSH = Attributes[3]
        OtherAU = Attributes[4]
        OtherCU = Attributes[5]
        OtherVU = Attributes[6]
        OtherHC = Attributes[7]
        OtherEth = Attributes[8]
        OtherGender = Attributes[9]
        OtherHE = Attributes[10]
        OtherWeekendSt = Attributes[11]
        OtherWeekendE = Attributes[12]
        OtherWeekSt = Attributes[13]
        OtherWeekE = Attributes[14]
        OtherMajorID = Attributes[15]
        OtherMajorName = Attributes[16]
        #GPA
        if OtherGPA > DesiredGPA:
            Score+=2
        #StudyHabits
        if DesiredSH == OtherSH:
            Score += 1
        #Academic
        if DesiredAcademicStatus == OtherAcademicStatus:
            Score += 2
        #Alcohol
        if DesiredAU == OtherAU:
            Score += 1
        #Cigs
        if DesiredCU == OtherCU:
            Score += 1
        #Vape
        if DesiredVU == OtherVU:
            Score += 1
        #Hair Color
        if DesiredHC == OtherHC:
            Score += 1
        #Ethnicity
        if DesiredEth == OtherEth:
            Score += 1
        #Height
        if DesiredHE < OtherHE:
            Score += 1
        #Weekend Intersection
        if(OtherWeekendSt <= DesiredWeekendSt <= OtherWeekendE ) or (DesiredWeekendSt <= OtherWeekendSt <= DesiredWeekendE):
            Score+=4
        #WeekDay Intersection
        if (OtherWeekSt <= DesiredWeekSt <= OtherWeekE) or (DesiredWeekSt <= OtherWeekSt <= DesiredWeekE):
            Score+=6
        if DesiredGender == OtherGender:
            Score += 2
        if DesiredAcademicStatus == OtherAcademicStatus:
            Score += 2
        newNode = Node(Attributes[0], Score)
        print(str(newNode.Profile)+" "+str(newNode.score))
        List.append(newNode)
    return List

def RegistrationMatching(email):
    connection = mysql.connect()
    cursor = connection.cursor()
    currentEmail = email
    print(currentEmail)
    cursor.callproc('getDesiredProfile', (currentEmail,))
    currentProfile = cursor.fetchall()
    print(currentProfile)
    if(len(currentProfile)!= 0):
        cursor.callproc('getOtherProfiles', (str(currentEmail),))
        otherProfiles = cursor.fetchall()

        tupleProfileList = matching(currentProfile[0], otherProfiles)

        for k in range(len(tupleProfileList)):
            cursor.callproc('addMatch', (tupleProfileList[k].Profile, tupleProfileList[k].score, currentProfile[0][0],))

        connection.commit()
    print("Done")
    return 0

def matchbatch():
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.callproc('deleteOldMatches',)
    connection.commit()
    #print('HERE')
    cursor.execute("SELECT email from People")
    AllEmails= cursor.fetchall()
    #print(AllEmails)
    for j in range(len(AllEmails)):
        #print (j)
        currentEmail = AllEmails[j][0]
        #print(currentEmail)
        cursor.callproc('getDesiredProfile', (currentEmail,))
        currentProfile = cursor.fetchall()
        #print(currentProfile)
        if(len(currentProfile)!= 0):
            cursor.callproc('getOtherProfiles', (str(currentEmail),))
            otherProfiles = cursor.fetchall()

            tupleProfileList = matching(currentProfile[0], otherProfiles)

            for k in range(len(tupleProfileList)):
                cursor.callproc('addMatch', (tupleProfileList[k].Profile, tupleProfileList[k].score,
                                             currentProfile[0][0],))

            connection.commit()
    print("Done")
    return 0


if __name__ == '__main__':
    matchbatch()
