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
    def __init__(self,UserID, Value):
        self.Profile = UserID
        self.score = Value

@app.route('/')
def hello():
    print("Connected!")
    return render_template("login.html")

@app.route('/viewPostMatches' , methods=['POST'])
def viewPostMatches():
    print("Viewing Potential Matches")
    email = session['Email']
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.callproc('getSuccessfulMatches', (email,))
    Alluser = cursor.fetchall()
    AllUsers2 = []
    for k in range(len(Alluser)):
        print(Alluser[k])
        AllUsers2.append(Alluser[k])
    print(AllUsers2)
    return render_template("acceptedMatches.html",sessionOwner = email,
                                                acceptedMatches = AllUsers2)

@app.route('/viewPreMatches', methods=['POST'])
def viewPreMatches():
    print("Viewing Potential Matches")
    connection = mysql.connect()
    cursor = connection.cursor()
    email = session['Email']
    print(email)
    cursor.callproc('getTopMatches', (email,))
    Alluser = cursor.fetchall()
    AllUsers2 = []
    for k in range(len(Alluser)):
        print(Alluser[k])
        AllUsers2.append(Alluser[k])
    print(AllUsers2)
    return render_template('matches.html',sessionOwner = email, matches = AllUsers2)

@app.route('/Authenticate', methods=['POST'])
def authenticate():
    print('Authentication Starting')
    emailForm = str(request.form['Email']).strip()
    password = str(request.form['Password']).strip()
    if (len(emailForm)==0) or (len(password)==0):
        return render_template("FailedLogin.html", loginError="Missing Email/Password")

    splitEmail = emailForm.strip().split(' ')
    email = splitEmail[0]
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.callproc('Authenticate', (email,))
    dbPass = cursor.fetchone()
    hashedPass = (hashlib.sha1((password + email).encode('UTF-8'))).hexdigest()
    print(hashedPass)

    if dbPass is not None:
        if hashedPass == dbPass[0]:
            print("Authentication Sucessful")
            session['Email'] = emailForm
            # Alex do this VVVV
            cursor.callproc('getProfileInformation', (str(email),))
            records = cursor.fetchall()
            major_names = []
            for record in records:
                if record[16] != None:
                    major_names.append(record[16])
            major_names = ", ".join(major_names)
            return render_template('profile.html',
                                   Username=emailForm,
                                   email=email,
                                   academic_status=records[0][1],
                                   major=major_names,
                                   gpa=records[0][2],
                                   study_habit=records[0][3],
                                   alc_use=records[0][4],
                                   cig_use=records[0][5],
                                   vape_use=records[0][6],
                                   hair=records[0][7],
                                   ethnicity=records[0][8],
                                   sex=records[0][9],
                                   height=records[0][10],
                                   week_end_bed=str(records[0][11]),
                                   week_end_wake=str(records[0][12]),
                                   week_bed=str(records[0][13]),
                                   week_wake=str(records[0][14]))
    print("Authentication Failed...")
    return render_template("FailedLogin.html",loginError="invalid Email and Password")

@app.route('/profile2', methods=['GET'])
def viewMatchedProfiles():
    val = int(request.args.get('id'))
    connection = mysql.connect()
    cursor = connection.cursor()
    email = session['Email']
    cursor.callproc('getSuccessfulMatches', (email,))
    AllMatches = cursor.fetchall()
    otherEmail = ""
    for k in range(len(AllMatches)):
        cProfile = AllMatches[k]
        if (val == cProfile[0]):
            otherEmail = cProfile[2]
    cursor.callproc('getProfileInformation', (str(otherEmail),))
    records = cursor.fetchall()
    session['otherEmail'] = otherEmail
    major_names = []
    for record in records:
        if record[16] != None:
            major_names.append(record[16])
    major_names = ", ".join(major_names)
    return render_template('matchPostProfile.html',
                           email=otherEmail,
                           academic_status=records[0][1],
                           major=major_names,
                           gpa=records[0][2],
                           study_habit=records[0][3],
                           alc_use=records[0][4],
                           cig_use=records[0][5],
                           vape_use=records[0][6],
                           hair=records[0][7],
                           ethnicity=records[0][8],
                           sex=records[0][9],
                           height=records[0][10],
                           week_end_bed=str(records[0][11]),
                           week_end_wake=str(records[0][12]),
                           week_bed=str(records[0][13]),
                           week_wake=str(records[0][14]))

@app.route('/profile', methods=['GET'])
def ViewOtherProfile():
    val = int(request.args.get('id'))
    connection = mysql.connect()
    cursor = connection.cursor()
    email = session['Email']
    cursor.callproc('getTopMatches', (email,))
    AllMatches = cursor.fetchall()
    otherEmail = ""
    for k in range(len(AllMatches)):
        cProfile = AllMatches[k]
        if(val == cProfile[0]):
            otherEmail = cProfile[2]
    cursor.callproc('getProfileInformation', (str(otherEmail),))
    records = cursor.fetchall()
    session['otherEmail'] = otherEmail
    major_names = []
    for record in records:
        if record[16] != None:
            major_names.append(record[16])
    major_names = ", ".join(major_names)
    return render_template('matchPreProfile.html',
                           email=otherEmail,
                           academic_status=records[0][1],
                           major=major_names,
                           gpa=records[0][2],
                           study_habit=records[0][3],
                           alc_use=records[0][4],
                           cig_use=records[0][5],
                           vape_use=records[0][6],
                           hair=records[0][7],
                           ethnicity=records[0][8],
                           sex=records[0][9],
                           height=records[0][10],
                           week_end_bed=str(records[0][11]),
                           week_end_wake=str(records[0][12]),
                           week_bed=str(records[0][13]),
                           week_wake=str(records[0][14]))

@app.route('/accept', methods=['POST'])
def accept():
    connection = mysql.connect()
    cursor = connection.cursor()
    email = session['Email']
    otherEmail = session['otherEmail']
    string = 'approve'
    cursor.callproc('updateMatchStatus',(email,otherEmail,string,))
    connection.commit()
    session.pop('otherEmail')
    cursor.callproc('getTopMatches', (email,))
    Alluser = cursor.fetchall()
    print(Alluser)
    AllUsers2 = []
    for k in range(len(Alluser)):
        print(Alluser[k])
        AllUsers2.append(Alluser[k])
    print(AllUsers2)
    return render_template('matches.html', sessionOwner=email, matches=AllUsers2)

@app.route('/reject', methods=['POST'])
def reject():
    connection = mysql.connect()
    cursor = connection.cursor()
    email = session['Email']
    otherEmail = session['otherEmail']
    string = 'reject'
    cursor.callproc('updateMatchStatus', (email, otherEmail, string,))
    connection.commit()
    session.pop('otherEmail',None)
    cursor.callproc('getTopMatches', (email,))
    Alluser = cursor.fetchall()
    print(Alluser)
    AllUsers2 = []
    for k in range(len(Alluser)):
        print(Alluser[k])
        AllUsers2.append(Alluser[k])
    print(AllUsers2)
    return render_template('matches.html', sessionOwner=email, matches=AllUsers2)

@app.route('/home', methods=['POST'])
def Home():
    email = session['Email']
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.callproc('getProfileInformation', (str(email),))
    records = cursor.fetchall()
    major_names = []
    for record in records:
        if record[16] != None:
            major_names.append(record[16])
    major_names = ", ".join(major_names)
    session.pop('otherEmail', None)
    return render_template('profile.html',
                           Username=email,
                           email=email,
                           academic_status=records[0][1],
                           major=major_names,
                           gpa=records[0][2],
                           study_habit=records[0][3],
                           alc_use=records[0][4],
                           cig_use=records[0][5],
                           vape_use=records[0][6],
                           hair=records[0][7],
                           ethnicity=records[0][8],
                           sex=records[0][9],
                           height=records[0][10],
                           week_end_bed=str(records[0][11]),
                           week_end_wake=str(records[0][12]),
                           week_bed=str(records[0][13]),
                           week_wake=str(records[0][14]))

@app.route('/sendMessage', methods=['POST'])
def sendingMessage():
    email = session['Email']
    otherEmail = session['otherEmail']
    connection = mysql.connect()
    cursor = connection.cursor()
    _message = request.form['messageToSend']
    print(otherEmail)
    ts = datetime.datetime.fromtimestamp(timestamp=time.time()).strftime('%Y-%m-%d %H:%M:%S')
    cursor.callproc('createMessage', (str(email),str(otherEmail),_message,str(ts),))
    connection.commit()
    cursor.callproc('getMessages', (email, otherEmail,))
    val = cursor.fetchall()
    return render_template('conversation.html',
                           sessionOwner=email,
                           otherUser=otherEmail,
                           messages=val
                           )

@app.route('/message', methods=['POST'])
def MessageBox():
    email = session['Email']
    otherEmail = session['otherEmail']
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.callproc('getMessages', (email, otherEmail,))
    val = cursor.fetchall()
    return render_template('conversation.html',
                           sessionOwner=email,
                           otherUser=otherEmail,
                           messages=val
                           )

@app.route('/refreshMessages', methods = ['POST'])
def refreshMessage():
    email = session['Email']
    otherEmail = session['otherEmail']
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.callproc('getMessages',(email,otherEmail,))
    val = cursor.fetchall()
    return render_template('conversation.html',
                           sessionOwner=email,
                           otherUser=otherEmail,
                           messages = val
                           )

@app.route('/returnConversation', methods=['POST'])
def returnToConversation():
    email = session['Email']
    otherEmail = session['otherEmail']
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.callproc('getProfileInformation', (str(otherEmail),))
    records = cursor.fetchall()
    major_names = []
    for record in records:
        if record[16] != None:
            major_names.append(record[16])
    major_names = ", ".join(major_names)
    return render_template('matchPostProfile.html',
                           email=otherEmail,
                           academic_status=records[0][1],
                           major=major_names,
                           gpa=records[0][2],
                           study_habit=records[0][3],
                           alc_use=records[0][4],
                           cig_use=records[0][5],
                           vape_use=records[0][6],
                           hair=records[0][7],
                           ethnicity=records[0][8],
                           sex=records[0][9],
                           height=records[0][10],
                           week_end_bed=str(records[0][11]),
                           week_end_wake=str(records[0][12]),
                           week_bed=str(records[0][13]),
                           week_wake=str(records[0][14]))

@app.route('/meetup', methods=['POST'])
def meet():
    email = session['Email']
    print('In MeetUp')
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.callproc('getMeetUps', (str(email),))
    val = cursor.fetchall()
    return render_template('meetup2.html',
                           sessionOwner = email,
                           meetUp = val
                           )

@app.route('/suggestMeet', methods=['POST'])
def suggestMeetUp():
    email = session['Email']
    otherEmail = session['otherEmail']
    connection = mysql.connect()
    cursor = connection.cursor()
    _location = request.form['locationInput']
    _time = request.form['timeInput']
    cursor.callproc('setUpMeetUp', (_location,_time,email,otherEmail))
    connection.commit()

@app.route('/refreshMeet', methods=['POST'])
def refreshMeetUp():
    email = session['Email']
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.callproc('getMeetUps', (str(email),))
    val = cursor.fetchall()
    return render_template('meetup2.html',
                           sessionOwner=email,
                           meetUp=val
                           )

@app.route('/postReg', methods=['POST'])
def postRegister():
    _ac = request.form['acs']
    _major = request.form['major']
    _ah = request.form['ah']
    _ch = request.form['ch']
    _vh = request.form['vh']
    _gpa = request.form['gpa']
    _hc = request.form['hc']
    _et = request.form['et']
    _sx = request.form['sx']
    _he = request.form['he']
    _yemail = request.form['yemail']
    _ypass = request.form['ypassword']
    _name = request.form['fname']
    _pacs = request.form['pacs']
    _pgpa = request.form['pgpa']
    _pm = request.form.getlist('pm')
    _psh = request.form['psh']
    _pWeekWake = request.form['pWeekWakeup']
    _pWeekBed = request.form['pWeekBedtime']
    _pWeekendWake = request.form['pWeekendWakeup']
    _pWeekendBed = request.form['pWeekendBedtime']
    _pah = request.form['pah']
    _pch = request.form['pch']
    _pvh = request.form['pvh']
    _pet = request.form['pet']
    _psx = request.form['psx']
    _phc = request.form['phc']
    _phe = request.form['phe']
    print(_ac)
    print(_major)
    print(_ah)
    print(_ch)
    print(_vh)
    print(_gpa)
    print(_vh)
    hashedPass = (hashlib.sha1((_ypass + _yemail).encode('UTF-8'))).hexdigest()
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.callproc('Registration',
                    (_pacs,
                     _pgpa,
                     _psh,
                     _pah,
                     _pch,
                     _pvh,
                     _phc,
                     _pet,
                     _psx,
                     _phe,
                     _pWeekendWake,
                     _pWeekendBed,
                     _pWeekWake,
                     _pWeekBed,
                     _pacs,
                     _gpa,
                     _psh,
                     _ah,
                     _ch,
                     _vh,
                     _hc,
                     _et,
                     _sx,
                     _he,
                     _pWeekendWake,
                     _pWeekendBed,
                     _pWeekWake,
                     _pWeekBed,
                     _yemail,
                     hashedPass,
                     _name,))
    print("Finished Query")
    tuples = cursor.fetchmany(2)
    print(str(tuples))
    profileID1 = tuples[0][0]
    profileID2 = tuples[1][0]

    print(profileID1)
    print(profileID2)
    if (len(_pm) != 0):
        if (int(_major) == 1):
            for k in range(len(_pm)):
                cursor.callproc('addMajor', (profileID1, _pm[k],))
                cursor.callproc('addMajor', (profileID2, _pm[k],))
        else:
            small = min(int(profileID1), int(profileID2))
            for k in range(len(_pm)):
                cursor.callproc('addMajor', (small, _pm[k],))

    connection.commit()
    RegistrationMatching(_yemail)

    return render_template('login.html')

@app.route('/Logout',methods = ['POST'])
def Logout():
    print("Logout")
    session.pop('Email',None)
    return render_template('login.html')

@app.route('/Registration', methods=['POST'])
def Registration():
    return render_template('newTempReg.html')

@app.route('/SetPref', methods=['POST'])
def SetPref():
    return render_template("preference.html")

@app.route('/SavePref', methods=['POST'])
def SavePref():
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.callproc('getProfileInformation', (str('Ldh@redred.com'),))
    records = cursor.fetchall()
    major_names = []
    _emailAtBeg = request.form['']
    _name = request.form['']
    _email = request.form['']
    _academic = request.form['']
    _major = request.form['']
    _gpa = request.form['']
    _studyHabits = request.form['']
    _alc = request.form['']
    _cig = request.form['']
    _vape = request.form['']
    _hair = request.form['']
    _end_bed = request.form['']
    _end_wake = request.form['']
    _week_bed = request.form['']
    _week_wake = request.form['']
    for record in records:
        if record[16] != None:
            major_names.append(record[16])
    major_names = ", ".join(major_names)
    return render_template('profile.html',
                           email='Ldh@redred.com',
                           academic_status=records[0][1],
                           major=major_names,
                           gpa=records[0][2],
                           study_habit=records[0][3],
                           alc_use=records[0][4],
                           cig_use=records[0][5],
                           vape_use=records[0][6],
                           hair=records[0][7],
                           ethnicity=records[0][8],
                           sex=records[0][9],
                           height=records[0][10],
                           week_end_bed=str(records[0][11]),
                           week_end_wake=str(records[0][12]),
                           week_bed=str(records[0][13]),
                           week_wake=str(records[0][14]))

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
    cursor.execute("SELECT email from People")
    AllEmails= cursor.fetchall()
    for j in range(len(AllEmails)):
        print (j)
        currentEmail = AllEmails[j][0]
        print(currentEmail)
        cursor.callproc('getDesiredProfile', (currentEmail,))
        currentProfile = cursor.fetchall()
        print(currentProfile)
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
