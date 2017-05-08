import hashlib
from flask import Flask, render_template, request, session
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key = 'any random string'
mysql = MySQL()

# MySQL configurations;
app.config['MYSQL_DATABASE_USER'] = 'guest'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'majormatch'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def hello():
    print("Connected!")
    return render_template("login.html")


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
    # print(_ac)
    # print(_major)
    # print(_ah)
    # print(_ch)
    # print(_vh)
    # print(_gpa)
    # print(_hc)
    # print(_et)
    # print(_sx)
    # print(_he)
    # # Profile -> P
    # print(_yemail)
    # print(_ypass)
    # print(_pacs)
    # print(_pgpa)
    # print(_pm)
    # print(_psh)
    # print(_pWeekWake)
    # print(_pWeekBed)
    # print(_pWeekendWake)
    # print(_pWeekendBed)
    # print(_pah)
    # print(_pch)
    # print(_pvh)
    # print(_pet)
    # print(_psx)
    # print(_phe)
    # print(_phc)
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
                     hashedPass,))
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
