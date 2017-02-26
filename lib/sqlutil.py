import sqlite3, os, re
from operator import itemgetter
from flask import flash
from debug_utils import *
from globalvar import *
try:
    from pymysql.err import *
except:
    pass

######## configuration ########

# DATABASE = os.path.join(app.root_path, 'data.db')  # db loaction



######## _basic_funcs ########

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




######## person ########

def addPerson(data):
    with sqlite3.connect(DATABASE) as database:
        SQL = "insert into test (id,name,gender,qq,tel,wchat,emg,school,class,apart,depart,grp,occup,dateofjoin) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (data['id'], data['name'], data['gender'], data['qq'], data['tel'], data['wchat'], data['emg'], data['school'], data['class'], data['apart'], data['depart'], data['group'], data['occup'], data['dateofjoin'])
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
            return 0
        else:
            flash("成功录入人员：%s，<br>编号 %s" % (data['name'], data['id']), category="success")
            return 1


def updatePerson(id, data):
    with sqlite3.connect(DATABASE) as database:
        SQL = "update test set name = '%s', gender = '%s', qq = '%s', tel = '%s', wchat = '%s', emg = '%s', school = '%s', class = '%s', apart = '%s', depart = '%s', grp = '%s', occup = '%s', dateofjoin = '%s' where id = '%s'" % (data['name'], data['gender'], data['qq'], data['tel'], data['wchat'], data['emg'], data['school'], data['class'], data['apart'], data['depart'], data['group'], data['occup'], data['dateofjoin'], id)
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
            return 0
        else:
            flash("成功修改 %s 的资料" % id, category="success")
            return 1


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
        return dict()




######## issue ########

def addIssue():
    with sqlite3.connect(DATABASE) as database:
        SQL = "insert into issue (id,title,body) values ('%s','%s','%s')" % (data['id'],data['title'],data['body'])
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
            return 0
        else:
            flash("成功录入事务：%s" % data['title'], category="success")
            return 1


def updateIssue(idx, data):
    with sqlite3.connect(DATABASE) as database:
        SQL = "update issue set title = '%s', body = '%s' where idx = '%s'" % (data['title'], data['body'], idx)
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
            return 0
        else:
            flash("成功修改事务", category="success")
            return 1


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
        return []




######## score ########

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
        return dict()
