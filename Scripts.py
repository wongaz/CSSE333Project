from flask import Flask, render_template, request, url_for,escape,request
from flaskext.mysql import MySQL
from random import randrange
import hashlib
app = Flask(__name__)
app.secret_key = 'any random string'
mysql = MySQL()

#MySQL configurations;
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
def Authenticate():
	print('Authentication Starting')
	emailForm = request.form['Email']
	password = request.form['Password']
	splitEmail = emailForm.strip().split(' ')
	email = splitEmail[0]
	connection = mysql.connect()
	cursor = connection.cursor()
	print(email)
	cursor.callproc('Authenticate',(email,))
	dbPass = cursor.fetchone()
	hashedPass = (hashlib.sha1((password+email).encode('UTF-8'))).hexdigest()
	if hashedPass == dbPass[0]:
		print("Authentication Sucessful")
		#Alex do this VVVV
		cursor.callproc('getProfileInformation',(str(email),))
		records = cursor.fetchall()
		major_names = []
		for record in records:
			if record[16] != None:
				major_names.append(record[16])

		major_names = ", ".join(major_names)
		return render_template('profile.html',
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
	else:
		print("Authentication Failed...")
		return render_template("FailedLogin.html")

@app.route('/postRegister',methods =['POST'])
def postRegister():
	print('***************************')	
	_ac = request.form['acs']
	_major = request.form['major']
	_ah=request.form['ah']
	_ch =request.form['ch']
	_vh = request.form['vh']
	_gpa = request.form['gpa']
	_hc = request.form['hc']
	_et = request.form['et']
	_sx = request.form['sx']
	_he = request.form['he']
	#Profile -> P
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
	_phe = request.form['phe']
	_phc = request.form['phc']
	hashedPass = (hashlib.sha1((yemail+ypass).encode('UTF-8'))).hexdigest()	
	connection = mysql.connect()
        cursor= connection.cursor()
	cursor.callproc('Registration',
					_pac,
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
					_pac
					_gpa,
					_psh,
					_ah,
					_ch,
					_vh,
					_hc,
					_et,
					_he,
					_pWeekendWake.
					_pWeekendBed,
					_pWeekWake,
					_pWeekBed,
					_yemail,
					_hashedPass,)
	tuples = cursor.fetchmany(2)
	profileID1 = tuples[0]
	profileID2 = tuples[1]
	if(major==1):
		for k in range(len(_pm)):
			cursor.callproc('AddMajor',profileID1, _pm[k],)
			cursor.callproc('AddMajor',profileID2, _pm[k],)
	else:
		small = min(profileID1, profileID2)
		for k in range(len(_pm)):
			cursor.callproc('AddMajor',small,_pm[k],)	
					
	return render_template('login.html')
@app.route('/Logout')
def Logout():
	return redirect(url('home'))

@app.route('/Registration',methods=['POST'])
def Registration():
	return render_template('Reg.html')

@app.route('/SetPref', methods = ['POST'])
def SetPref():
	return render_template("preference.html")

@app.route('/SavePref', methods = ['POST'])
def SavePref():
	connection = mysql.connect()
	cursor= connection.cursor()
	cursor.callproc('getProfileInformation',(str('Ldh@redred.com'),))
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
