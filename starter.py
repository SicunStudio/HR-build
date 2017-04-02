#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''   HR System build   '''

from flask import Flask, request, session, render_template, url_for, redirect
from flask import make_response, flash, jsonify, send_from_directory

from functools import wraps
import sqlite3, os, re, hashlib

from lib.sqlutil import *
from lib import xlsxSwissKnife

from globalvar import *

from lib.debug_utils import *
try:
    from pymysql.err import *
except:
    pass




######## global configuration ########

# see globalvar.py


######## initializaton ########

app = Flask(__name__)
app.secret_key = 'DogLeeNation(2B||!2B)-->|'


######## user utils ########

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
            treated = hashlib.sha256((passwd+SALT+id).encode('utf-8'))
            if treated.hexdigest()==correct[0]:
                return 1
            else:  # wrong passwd
                flash("用户名或密码错误！", category="error")
                return 0


def adminRegist(id, passwd):
    if id == '':
        flash("用户名不能为空！", category='error')
        return 0
    elif passwd == '':
        flash("密码不能为空！", category='error')
        return 0
    with sqlite3.connect(DATABASE) as database:
        cur = database.execute("select passwd from admin where id = '%s'" % id)
        empty = cur.fetchone()
        if empty != None:
            flash("用户名已经存在!", category='warning')
            return 0
        else:  # id is new
            treated = hashlib.sha256((passwd+SALT+id).encode('utf-8'))
            sql_sentence = "insert into admin (id, passwd) values ('%s', '%s')" % (id, treated.hexdigest())
            cur = database.execute(sql_sentence)
            database.commit()
            flash("注册成功！<br>请登录！", category='success')
            return 1


def login_verify(to_be_decorated):
    '''  check-in decorator  '''
    @wraps(to_be_decorated)
    def decorated(*args, **kwargs):
        if 'id' not in session:
            flash("请登录！", category="error")
            return redirect(url_for('login'))
        return to_be_decorated(*args, **kwargs)
    return decorated




######## views ########

''' user page '''

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html');
    elif request.method == 'POST':
        session['id'] = request.form['id']
        session['passwd'] = request.form['passwd']
        if verify(session['id'], session['passwd']):
            try:
                # don't carry your passwd with you
                assert session.pop('passwd', None) != None
            except:
                pass
            return redirect(url_for('personal'))
        else:
            session.pop('id', None)
            session.pop('passwd', None)
            #session.pop('filename', None)
            return redirect(url_for('login'))


@app.route('/registering/', methods=['POST'])
def register():
    id = request.form.get('id', '')
    passwd = request.form.get('passwd_first', '')
    if passwd != request.form.get('passwd_second', ''):
        # TODO: if using 'warning', will toast an empty warning and then the info-toast containning the message
        flash("两次密码不相同！<br>换个好记一点的吧？", category='warning')
        return redirect(url_for('login'))
    elif len(passwd) < 8:
        flash("密码太短了！", category='warning')
        return redirect(url_for('login'))
    elif request.form.get('invitation', '') != INVITATION:
        flash("邀请码错误！", category='warning')
        return redirect(url_for('login'))
    else:
        if adminRegist(id, passwd):
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    if 'id' in session:
        # clear session
        session.pop('id', None)
        print(session.pop('passwd', None))  # should get `None`
        session.pop('filename', None)
        flash("已登出", category='message')
        return redirect(url_for('index'))


@app.route('/personal/', methods=['GET', 'POST'])
@login_verify
def personal():
    if request.method == 'GET':
        database = getAdmin('id','id',session['id'])
        return render_template('personal_base.html', database = database)
    elif request.method == 'POST':
        filename = request.form['title'] + '.xlsx'
        session['filename'] = filename
        if xlsxSwissKnife.newFile(request.form['title'], request.form['depart'], date=request.form['date']):
            return redirect(url_for('score', title=request.form['title']))
        else:
            # flash msg added in xlsxSwissKnife
            return redirect(url_for('personal'))




''' add to server '''

@app.route('/entry_person/', methods=['GET', 'POST'])
@login_verify
def entryPerson():
    if request.method == 'POST':
        addPerson(request.form)
        printLog("addPerson() called")
        return redirect(url_for('personal'))
    elif request.method == 'GET':
        return render_template('info_entry.html')


@app.route('/entry_issue/', methods=['GET', 'POST'])
@login_verify
def entryIssue():
    if request.method == 'POST':
        addIssue(request.form)
        printLog("addIssue() called")
        return redirect(url_for('personal'))
    elif request.method == 'GET':
        return render_template('issue_entry.html')


@app.route('/score_page/<title>')
@login_verify
def score(title):
    session['filename'] = title + '.xlsx'
    data = xlsxSwissKnife.read(session['filename'])
    printLog(data)
    for each in data:
        print(each, data[each])
    return render_template('score_entry.html', data=data)




''' commit updates to server '''

@app.route('/update/<id>', methods=['GET', 'POST'])
@login_verify
def update(id):
    '''  update for personale info  '''
    if request.method == 'GET':
        printLog(id)
        return render_template('info_update.html', database=getConditonal('*','id',id),id=id)
    elif request.method == 'POST':
        updatePerson(request.form, id)
        return redirect(url_for('personal'))


@app.route('/update_issue/<idx>', methods=['GET', 'POST'])
@login_verify
def alter(idx):
    ''' alter for issue '''
    if request.method == 'GET':
        printLog(id)
        print(grepIssue('idx', idx))
        return render_template('issue_update.html', database=grepIssue('idx', idx))
    elif request.method == 'POST':
        updateIssue(idx, request.form)
        return redirect(url_for('personal'))




''' search entries '''

@app.route('/search_person/')
@login_verify
def search_person():
    ''' search_person entry '''
    return render_template('search_person.html', result=grepPerson('id','苟'))

@app.route('/search_issue/')
@login_verify
def search_issue():
    return render_template('search_issue.html', result=grepIssue('id', '苟'))

@app.route('/search_score/')
@login_verify
def search_score():
    return render_template('score_download.html', collection=grepScore('date', '*'))


''' Free time entry/search '''
@app.route('/freetime_entry/')
@login_verify
def freetime_entry():
    return render_template('freetime_entry.html')


######## process ########

@app.route('/searching_person/', methods=['GET'])
@login_verify
def searching_person():
    ''' search_person process '''
    direction = request.args.get('d')
    content = request.args.get('c')
    return jsonify(result=grepPerson(direction, content))

@app.route('/searching_issue/', methods=['GET'])
@login_verify
def searching_issue():
    direction = request.args.get('d')
    content = request.args.get('c')
    return jsonify(result=grepIssue(direction, content))

@app.route('/scoring_page/', methods=['POST'])
@login_verify
def scoring():
    data = request.get_json()
    # for each in data:
    #     print(each, data[each])
    xlsxSwissKnife.write(session['filename'], data)
    # print('===========================')
    # for each in xlsxSwissKnife.getPerson(session['filename'], data['name']):
    #     print(each, data[each])
    return jsonify(result=xlsxSwissKnife.getPerson(
        session['filename'], data['name']))




@app.route('/downloading/<title>')
@login_verify
def downloading(title):
    return send_from_directory(FOLDER, title+'.xlsx', as_attachment=True)

@app.route('/deleting/<title>')
@login_verify
def deleting(title):
    xlsxSwissKnife.delFile(title+'.xlsx')
    return redirect(url_for('search_score'))

@app.route('/searching_score/', methods=['GET'])
@login_verify
def searching_score():
    direction = request.args.get('d', 'date')
    content = request.args.get('c', '*')
    return jsonify(result=grepScore(direction, content))


###### TODO: TEST AREA! ######
@app.route('/submit_freetime/', methods=('GET', 'POST'))
@login_verify
def submit_freetime():
    raw_data = request.form.get('result','')
    output=parse_result(raw_data=raw_data)

    return jsonify(backMessage={'message':output})


def parse_result(raw_data):
    result=[]
    weekdays_name = {
        'MON': '周一', 'TUE': '周二', 'WED': '周三', 'THU': '周四', 'FRI': '周五', 'SAT': '周六', 'SUN': '周日'
    }
    lesson_time = raw_data.split(',')
    for item in lesson_time:
        buff=item.split('-', 1)
        day=buff[0]
        time=buff[1]
        result.append("%s %s节" % (weekdays_name[day], time))

    return result


@app.route('/get_person_freetime/', methods=['GET'])
@login_verify
def get_person_freetime():
    depart = request.args.get('depart', '')
    direction = request.args.get('direction', '')
    content = request.args.get('content', '')
    # print(depart)
    return jsonify(result=getOnePerson(depart, direction, content))



######## run ########

if __name__ == '__main__':

    app.run(host="0.0.0.0", debug=True)
