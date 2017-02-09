#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''   HR System build   '''

from flask import Flask, request, session, render_template, url_for, redirect
from flask import make_response, flash, jsonify, send_from_directory
from functools import wraps
import sqlite3, os, re, xlsxSwissKnife
from debug_utils import *

######## initializaton ########

app = Flask(__name__)
app.secret_key = 'DogLeeNation(2B||!2B)-->|'

######## global configuration ########

FOLDER = os.path.join(os.curdir, 'score-sheets')  # xlsx location
INVENTORY = os.path.join(FOLDER, 'inventory.db')
DATABASE = os.path.join(app.root_path, 'data.db')  # db loaction

######## functions ########

def getAll():
	with sqlite3.connect(DATABASE) as database:
		cursor = database.execute('select * from test')
		data = cursor.fetchall()
		return data

def getConditonal(column, conditon, require):
	with sqlite3.connect(DATABASE) as database:
		cursor = database.execute("select %s from test where %s = '%s'" % (column, conditon, require))
		data = cursor.fetchall()
		return data

def getAdmin(column, conditon, require):
	with sqlite3.connect(DATABASE) as database:
		cursor = database.execute("select %s from admin where %s = '%s'" % (column, conditon, require))
		data = cursor.fetchall()
		return data

def verify(id, passwd):
	with sqlite3.connect(DATABASE) as database:
		cursor = database.execute("select passwd from admin where id = '%s'" % id)
		correct = cursor.fetchone()
		if correct==None:  # wrong id
			flash("用户名或密码错误！", category="error")
			return 0
		else:  # correct
			if passwd==correct[0]:
				return 1
			else:  # wrong passwd
				flash("用户名或密码错误！", category="error")
				return 0

def login_verify(to_be_decorated):
	'''  check-in decorator  '''
	@wraps(to_be_decorated)
	def decorated(*args, **kwargs):
		if 'id' not in session:
			flash("请登录！", category="error")
			return redirect(url_for('login'))
		return to_be_decorated(*args, **kwargs)
	return decorated

def updatePerson(id):
	with sqlite3.connect(DATABASE) as database:
		SQL = "update test set name = '%s', gender = '%s', qq = '%s', tel = '%s', wchat = '%s', emg = '%s', school = '%s', class = '%s', apart = '%s', depart = '%s', grp = '%s', occup = '%s', dateofjoin = '%s' where id = '%s'" % (request.form['name'], request.form['gender'], request.form['qq'], request.form['tel'], request.form['wchat'], request.form['emg'], request.form['school'], request.form['class'], request.form['apart'], request.form['depart'], request.form['group'], request.form['occup'], request.form['dateofjoin'], id)
		printLog("============== UPDATE PERSON ==============")
		printLog(SQL)
		printLog("===========================================")

		try:
			database.execute(SQL)
			database.commit()
		except Exception as e:
			flash("(⊙﹏⊙)b 修改资料时出错了：%s <br>请狠狠地戳开发人员~~~" % e.args(0), category="error")
			return
		else:
			flash("成功修改 %s 的资料" % id, category="success")
			return


def updateIssue(idx):
	with sqlite3.connect(DATABASE) as database:
		SQL = "update issue set title = '%s', body = '%s' where idx = '%s'" % (request.form['title'], request.form['body'], idx)
		printLog("============== UPDATE ISSUE ==============")
		printLog(SQL)
		printLog("===========================================")

		try:
			database.execute(SQL)
			database.commit()
		except Exception as e:
			flash("(⊙﹏⊙)b 修改资料时出错了：%s 请狠狠地戳开发人员~~~" % e.args(0), category="error")
			return
		else:
			flash("成功修改事务", category="success")
			return

def grepPerson(column, require):
	with sqlite3.connect(DATABASE) as database:
		cursor = database.execute("select * from test where %s GLOB '*%s*'" % (column, require))
		data = cursor.fetchall()
		result = dict()
		for each in data:
			result[each[0]] = each[1:]
		return result

def grepIssue(column, require):
	with sqlite3.connect(DATABASE) as database:
		raw_data = []
		if column == 'idx':
			cursor = database.execute("select * from issue where idx = %s" % require)
			raw_data = cursor.fetchall()
		else:
			if column == 'name':
				cursor = database.execute("select id from test where name = '%s'" % require)
				id = cursor.fetchone()
			elif column == 'id':
				id = require
			cursor = database.execute("select * from issue where id = '%s'" % id)
			data = cursor.fetchall()
			raw_data = data
		return raw_data[0]

def addPerson():
	with sqlite3.connect(DATABASE) as database:
		SQL = "insert into test (id,name,gender,qq,tel,wchat,emg,school,class,apart,depart,grp,occup,dateofjoin) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (request.form['id'], request.form['name'], request.form['gender'], request.form['qq'], request.form['tel'], request.form['wchat'], request.form['emg'], request.form['school'], request.form['class'], request.form['apart'], request.form['depart'], request.form['group'], request.form['occup'], request.form['dateofjoin'])
		printLog("============== ADD PERSON ==============")
		printLog(SQL)
		printLog("===========================================")

		try:
			database.execute(SQL)
			database.commit()
		except Exception as e:
			flash("(⊙﹏⊙)b 修改资料时出错了：%s <br>请狠狠地戳开发人员~~~" % e.args(0), category="error")
			return
		else:
			flash("成功录入人员：%s，<br>编号 %s" % (request.form['name'], request.form['id']), category="success")
			return

def addIssue():
	with sqlite3.connect(DATABASE) as database:
		SQL = "insert into issue (id,title,body) values ('%s','%s','%s')" % (request.form['id'],request.form['title'],request.form['body'])
		printLog("============== ADD ISSUE ==============")
		printLog(SQL)
		printLog("===========================================")

		try:
			database.execute(SQL)
			database.commit()
		except Exception as e:
			flash("(⊙﹏⊙)b 录入资料时出错了：%s <br>请狠狠地戳开发人员~~~" % e.args(0), category="error")
			return
		else:
			flash("成功录入事务：%s" % request.form['title'], category="success")
			return

def grepScore(*, title=None, date=None, depart=None):
	result = dict()
	if not (title or date or depart):
		return result
	with sqlite3.connect(INVENTORY) as database:
		if title:
			cur = database.execute("select * from score where title glob '%s'" % title)
			ls = cur.fetchall()
		elif date:
			cur = database.execute("select * from score where date glob '%s'" % date)
			ls = cur.fetchall()
		elif depart:
			cur = database.execute("select * from score where depart glob '%s'" % depart)
			ls = cur.fetchall()
		for each in ls:
			result[each[0]] = each[1:]
		return result

######## route ########

@app.route('/')
def index():
	# a useless port
	return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html');
	elif request.method == 'POST':
		session['id'] = request.form['id']
		session['passwd'] = request.form['passwd']
		if verify(session['id'], session['passwd']):
			return redirect(url_for('personal'))
		return redirect(url_for('logout'))

@app.route('/personal/', methods=['GET', 'POST'])
@login_verify
def personal():
	if request.method == 'GET':
		database = getAdmin('id','id',session['id'])
		return render_template('personal_base.html', database = database)
	elif request.method == 'POST':
		filename = request.form['title'] + ' - ' + request.form['date'] + '.xlsx'
		session['filename'] = filename
		if xlsxSwissKnife.newFile(request.form['title'], request.form['depart'], date=request.form['date']):
			return redirect(url_for('score'))
		else:
			flash("创建表格失败！", category="error")
			return redirect(url_for('personal'))

@app.route('/logout/')
def logout():
	if 'id' in session:
		session.pop('id', None)
		# the following lines are weird
		session.pop('passwd', None)
		session.pop('filename', None)
		# Give out a flash toast
		# flash("已登出", category='message')
	return redirect(url_for('index'))

@app.route('/update/<id>', methods=['GET', 'POST'])
@login_verify
def update(id):
	'''  update for personale info  '''
	if request.method == 'GET':
		printLog(id)
		return render_template('info_update.html', database=getConditonal('*','id',id),id=id)
	elif request.method == 'POST':
		updatePerson(id)
		return redirect(url_for('personal'))

@app.route('/search_person/')
@login_verify
def search_person():
	''' search_person entry '''
	return render_template('search_person.html', result=grepPerson('id','苟'))

@app.route('/searching_person/', methods=['GET'])
@login_verify
def searching_person():
	''' search_person process '''
	direction = request.args.get('d')
	content = request.args.get('c')
	return jsonify(result=grepPerson(direction, content))

@app.route('/entry_person/', methods=['GET', 'POST'])
@login_verify
def entryPerson():
	if request.method == 'POST':
		addPerson()
		printLog("addPerson() called")
		return redirect(url_for('personal'))
	elif request.method == 'GET':
		return render_template('info_entry.html')

@app.route('/entry_issue/', methods=['GET', 'POST'])
@login_verify
def entryIssue():
	if request.method == 'POST':
		addIssue()
		printLog("addIssue() called")
		return redirect(url_for('personal'))
	elif request.method == 'GET':
		return render_template('issue_entry.html')

@app.route('/search_issue/')
@login_verify
def search_issue():
	return render_template('search_issue.html', result=grepIssue('id', '苟'))

@app.route('/searching_issue/', methods=['GET'])
@login_verify
def searching_issue():
	direction = request.args.get('d')
	content = request.args.get('c')
	return jsonify(result=grepIssue(direction, content))

@app.route('/update_issue/<idx>', methods=['GET', 'POST'])
@login_verify
def alter(idx):
	''' alter for issue '''
	if request.method == 'GET':
		printLog(id)
		print(grepIssue('idx', idx))
		return render_template('issue_update.html', database=grepIssue('idx', idx))
	elif request.method == 'POST':
		updateIssue(idx)
		return redirect(url_for('personal'))

# openpyxl issue solved
# just don't know when I could get the new release
@app.route('/score_page/')
@login_verify
def score():
	if 'filename' not in session:
		return redirect(url_for('personal'))
	else:
		data = xlsxSwissKnife.read(session['filename'])
		printLog(data)
		return render_template('score_entry.html', data=data)

@app.route('/score_dl/')
@login_verify
def score_download():
	#collection = os.listdir(FOLDER)
	collection = grepScore(title='*')
	print(collection)
	return render_template('score_download.html', collection=collection)

@app.route('/download/<filename>')
@login_verify
def download(filename):
	return send_from_directory(FOLDER, filename+'.xlsx', as_attachment=True)

######## run ########

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)
