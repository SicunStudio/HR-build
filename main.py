#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''   HR System build   '''

from flask import Flask, request, session, render_template, url_for, redirect
from flask import make_response, flash, jsonify, send_from_directory
from functools import wraps
from operator import itemgetter
import sqlite3, os, re, xlsxSwissKnife
from pymysql.err import *


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
            flash("(⊙﹏⊙)b 修改资料时出错了：%s <br>请狠狠地戳开发人员~~~" % e.args[0], category="error")
            printLog("[updatePerson Error] %s" % e.args[0])
            printErrTraceback(title="updatePerson", exception=e)
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
            flash("(⊙﹏⊙)b 修改资料时出错了：%s 请狠狠地戳开发人员~~~" % e.args[0], category="error")
            printLog("[updateIssue Error] %s" % e.args[0])
            printErrTraceback(title="updateIssue", exception=e)
            return
        else:
            flash("成功修改事务", category="success")
            return

def grepPerson(column, require):
    try:
        with sqlite3.connect(DATABASE) as database:
            cursor = database.execute("select * from test where %s GLOB '*%s*'" % (column, require))
            data = cursor.fetchall()
            result = dict()
            for each in data:
                result[each[0]] = each[1:]
            return result
    except Exception as e:
        flash("(⊙﹏⊙)b 查询资料时出错了：%s 请狠狠地戳开发人员~~~" % e.args[0], category="error")
        printLog("[grepPerson Error] %s" % e.args[0])
        printErrTraceback(title="grepPerson", exception=e)
        return


def grepIssue(column, require):
    try:
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
            # print(raw_data)
            return raw_data
    except Exception as e:
        flash("(⊙﹏⊙)b 查询资料时出错了：%s 请狠狠地戳开发人员~~~" % e.args[0], category="error")
        printLog("[grepIssue Error] %s" % e.args[0])
        printErrTraceback(title="grepIssue", exception=e)
        return


# TODO: not safe ---- use parameters next time
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
            flash("(⊙﹏⊙)b 修改资料时出错了：%s <br>请狠狠地戳开发人员~~~" % e.args[0], category="error")
            printLog("[addPerson Error] %s" % e.args[0])
            printErrTraceback(title="addPerson", exception=e)
            return
        else:
            flash("成功录入人员：%s，<br>编号 %s" % (request.form['name'], request.form['id']), category="success")
            return


# TODO: not safe ---- use parameters next time
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
            flash("(⊙﹏⊙)b 录入资料时出错了：%s <br>请狠狠地戳开发人员~~~" % e.args[0], category="error")
            printLog("[addIssue Error] %s" % e.args[0])
            printErrTraceback(title="addIssue", exception=e)
            return
        else:
            flash("成功录入事务：%s" % request.form['title'], category="success")
            return


def grepScore(direction, content):
    '''
      format:
      [{'title': 'title_0', 'date': '1 January, 1970', 'depart': '部门', 'id': 1}, ...]
    '''
    result = []
    ls = []
    try:
        with sqlite3.connect(INVENTORY) as database:
            if direction=='title':
                cur = database.execute("select * from score where title = '%s'" % content)
                ls = cur.fetchall()
            elif direction=='date':
                cur = database.execute("select * from score where date glob '%s'" % content)
                ls = cur.fetchall()
            elif direction=='depart':
                cur = database.execute("select * from score where depart = '%s'" % content)
                ls = cur.fetchall()
        # re-formatting
        for each in ls:
            result.append({'title':each[0], 'date':each[1], 'depart':each[2], 'id': each[3]})
        result_ordered_by_date = sorted(result, key=itemgetter('id'))  # i.e. sorted in time of creation
        return result_ordered_by_date
    except Exception as e:
        flash("(⊙﹏⊙)b 查询资料时出错了：%s <br> 请狠狠地戳开发人员~~~" % e.args[0], category="error")
        printLog("[grepScore Error] %s" % e.args[0])
        printErrTraceback(title="grepScore",exception=e)




######## route ########

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
        return redirect(url_for('logout'))


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


@app.route('/score_page/<title>')
@login_verify
def score(title):
    if 'filename' not in session:
        return redirect(url_for('personal'))
    else:
        data = xlsxSwissKnife.read(session['filename'])
        printLog(data)
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
        updatePerson(id)
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
        updateIssue(idx)
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
    print(data['dim-self'])
    for each in data:
        print(each, data[each])
    xlsxSwissKnife.write(session['filename'], data)
    return jsonify(result=data)



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
def searching_score():
    direction = request.args.get('d', 'date')
    content = request.args.get('c', '*')
    return jsonify(result=grepScore(direction, content))




######## run ########

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
