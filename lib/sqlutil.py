"""
    SQLITE DATABASE UTILITIES
    ~~~~~~~~~~~~~~

    Database manager module for AUHR-HUST. This is the core of the whole project.
"""
#################  IMPORTS  #################
import sqlite3, os, re
from operator import itemgetter
from functools import wraps
from flask import flash, redirect, url_for
from lib.debug_utils import *
from globalvar import *
try:
    from pymysql.err import *
except:
    pass



######################### BASIC FUNCTIONS #########################

def getAll():
    """
    Query all PERSONAL data from database.
    :return: Personal data assembly.
    """
    with sqlite3.connect(DATABASE) as database:
        cursor = database.execute('select * from test')
        data = cursor.fetchall()
        return data


def getConditonal(column, conditon, require):
    # TODO: Must figure out what this function do.
    """
    Query a person with given conditions.

    :param column:
    :param conditon:
    :param require:
    :return: Personal data.
    """
    with sqlite3.connect(DATABASE) as database:
        cursor = database.execute("select %s from test where %s = '%s'" % (column, conditon, require))
        data = cursor.fetchall()
        return data


def check_person_info(person_modifier):
    """
    Check input of new person info, to avoid illegal inputs.
    :param person_modifier:
    :return:
    """
    @wraps(person_modifier)
    def prerequisite_person(d, *args, **kwargs):
        if ' ' in d.get('name', ''):
            flash("名字中不能包含空格！", 'warning')
            return redirect(url_for('personal'))
        #elif not re.match(r'^AU\d{9}', d.get('id', '')):
        elif not re.match(r'^AU\d{9}', kwargs['id']):
            flash("社联编号格式不正确！", 'warning')
            flash("格式要求：AUxxxxxxxxx，其中X为数字！")
            return redirect(url_for('personal'))
        else:
            return person_modifier(d, *args, **kwargs)
    return prerequisite_person




#########################  PERSONAL DATA MANAGE  #########################

@check_person_info
def addPerson(d):
    """
    Add a new personal data entry.
    :param d: A dict from Flask request object. Data of the form in webpage.
    :return: Return 1 if succeed, otherwise return 0.
    """

    with sqlite3.connect(DATABASE) as database:
        data = dict(
            id=d.get('id', ''), name=d.get('name', ''), gender=d.get('gender', ''),
            qq=d.get('qq', ''), tel=d.get('tel', ''), wchat=d.get('wchat', ''), emg=d.get('emg', ''),
            school=d.get('school', ''), clas=d.get('class', ''), apart=d.get('apart', ''),
            depart=d.get('depart', ''), group=d.get('group', ''), occup=d.get('occup', ''),
            dateofjoin=d.get('dateofjoin', '')
        )
        SQL = "insert into test (id,name,gender,qq,tel,wchat,emg,school,class,apart,depart,grp,occup,dateofjoin) values ('{id}','{name}','{gender}','{qq}','{tel}','{wchat}','{emg}','{school}','{clas}','{apart}','{depart}','{group}','{occup}','{dateofjoin}')".format_map(data)
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
            flash("成功录入人员：{}，<br>编号 {}".format(data['name'], data['id']), category="success")
            return 1


@check_person_info
def updatePerson(d, id):
    """
    Update an modified personal data entry into database.
    :param d: A dict from Flask request object. Data of the form in webpage.
    :param id: Current person's ID.
    :return: Return 1 if succeed, otherwise return 0.
    """
    with sqlite3.connect(DATABASE) as database:
        data = dict(
            name=d.get('name', ''), gender=d.get('gender', ''),
            qq=d.get('qq', ''), tel=d.get('tel', ''), wchat=d.get('wchat', ''), emg=d.get('emg', ''),
            school=d.get('school', ''), clas=d.get('class', ''), apart=d.get('apart', ''),
            depart=d.get('depart', ''), group=d.get('group', ''), occup=d.get('occup', ''),
            dateofjoin=d.get('dateofjoin', ''), id=id
        )

        printLog("[updatePerson]  User is submitting this modified personal data:")
        printLog(data)

        SQL = "update test set name = '{name}', gender = '{gender}', qq = '{qq}', tel = '{tel}', wchat = '{wchat}', emg = '{emg}', school = '{school}', class = '{clas}', apart = '{apart}', depart = '{depart}', grp = '{group}', occup = '{occup}', dateofjoin = '{dateofjoin}' where id = '{id}'".format_map(data)
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
            flash("成功修改 {}（{}） 的资料".format(data['name'], data['id']), category="success")
            return 1


def grepPerson(column, require):
    """
    Query a personal data entry with given requirements.
    :param column:
    :param require:
    :return: Queried entry.
    """
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




#########################  ISSUE MANAGE  #########################
# TODO: The following function used to have a bug...
def addIssue(data):
    """
    Add a new issue.
    :param data: A dict from Flask request object. Data of the form in webpage.
    :return: Error level.
    """
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
    """
    Update a modified existing issue.
    :param idx:
    :param data:
    :return: Error level.
    """
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
    """
    Query issues with given requirements.
    :param column:
    :param require:
    :return:
    """
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




#########################  SCORE MANAGE  #########################

def grepScore(direction, content):
    """
    Query an existing score table with given direction.
    :param direction:
    :param content:
    :return:
    """
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




#########################  FREE TIME MANAGE  #########################
# TODO: 1. Try to figure out valid introductions of the following functions.
# TODO: 2. Allow querying any person without specifying its department and requirement type.
# TODO: 3. If repeated infos are found, pop up a warning dialog for choosing a valid one.

def getOnePerson(depart, direction, content):
    """
    Query a person's free time.
    :param depart:
    :param direction:
    :param content:
    :return:
    """
    try:
        with sqlite3.connect(DATABASE) as db:
            raw = tuple()
            SQL = (
                "SELECT id, name FROM test "
                "WHERE {} = '{}' AND depart = '{}'".format(direction, content, depart)
            )
            # print(SQL)
            cur = db.execute(SQL)
            raw = cur.fetchall()

            # only one person should be passed to the front
            if len(raw) == 1:
                return raw[0]
            else:
                #flash("查询结果为空！", category="warning")
                return ("", "查询结果为空！")

    except Exception as e:
        flash("(⊙﹏⊙)b 查询资料时出错了：%s <br> 请狠狠地戳开发人员~~~" % e.args[0], category="error")
        printLog("[getOnePerson Error] %s" % e.args[0])
        printErrTraceback(title="getOnePerson",exception=e)
        return tuple()


def registerFreetime(data):
    """
    Add free time entry for a person.
    :param data: A formatted dict. Free time entry data
        parameter format:
        data = {
            'id': ...,
            'freetime': [ list of freetime in 'MON-1-2' ]
        }
    :return: True if succeed, and False if fail.
    """
    try:
        with sqlite3.connect(DATABASE) as db:
            SQL = "INSERT INTO freetime (id, "
            if len(data['freetime']) == 0:
                SQL = SQL[:-2] + ') VALUES ("{}")'.format(data['id'])
            else:
                for each in data['freetime']:
                    SQL += each.replace('-', '_') + ', '
                SQL = SQL[:-2] + ') values ("{}", '.format(data['id'])
                for each in data['freetime']:
                    SQL += '1, '    # 1 as the freetime flag
                SQL = SQL[:-2] + ')'
            # print(SQL)
            db.execute('''
                DELETE FROM freetime
                WHERE id = "{}"
            '''.format(data['id'])
            )
            db.execute(SQL)
            db.commit()
            return True

    except Exception as e:
        errmsg = "(⊙﹏⊙)b 录入空闲时间时出错了：%s <br> 请狠狠地戳开发人员~~~" % e.args[0]
        #flash("(⊙﹏⊙)b 录入空闲时间时出错了：%s <br> 请狠狠地戳开发人员~~~" % e.args[0], category="error")
        printLog("[getOnePerson Error] %s" % e.args[0])
        printErrTraceback(title="getOnePerson",exception=e)
        return errmsg



def getFreetime(depart, direction, content):
    """
    (??????) Query free time by department.
    :param depart:
    :param direction:
    :param content:
    :return: Queried result in the following format:
          :format:
            ("AU000000", 0, 0, 1, 0, ...) - in table head order
    """

    # TODO: stupid way of getting id
    id = getOnePerson(depart, direction, content)[0]
    try:
        with sqlite3.connect(DATABASE) as db:
            SQL = '''
                SELECT * FROM freetime
                WHERE id = "{}"
            '''.format(id)
            cur = db.execute(SQL)
            result = cur.fetchone() # id primary key - only one will be found
            # print(result)
            if result == None:
                result = []
            return result

    except Exception as e:
        flash("(⊙﹏⊙)b 查询某人的空闲时间时出错了：%s <br> 请狠狠地戳开发人员~~~" % e.args[0], category="error")
        printLog("[getFreetime Error] %s" % e.args[0])
        printErrTraceback(title="getFreetime",exception=e)



def searchFreetime(require):
    """
    Query free time by a given time array. Those who are free at given time will be picked out.
    :param require: A list of time array for querying person free at those time.
        :format
            require = ['MON-1-2', ...]
    :return:
    """

    require = require.split(',')
    # print(require)
    try:
        id_container = []
        person = []
        with sqlite3.connect(DATABASE) as db:
            SQL = "SELECT id FROM freetime WHERE "
            if require[0] == '':
                SQL = "SELECT id FROM freetime WHERE id = '苟'"
            else:
                for each in require:
                    tmp = each.split('-')
                    SQL += tmp[0] + '_' + tmp [1] + '_' + tmp[2] + " = 1 AND "
                SQL = SQL[:-4]
            print(SQL)
            cur = db.execute(SQL)
            id_container = cur.fetchall()
        with sqlite3.connect(DATABASE) as db:
            # print(id_container)
            SQL = "SELECT * FROM test WHERE id IN ("
            if len(id_container) == 0:
                SQL = "SELECT * FROM test WHERE id = '苟'"
            else:
                for each in id_container:
                    SQL += '"' + each[0] + '"' + ', '
                SQL = SQL[:-2] + ')'
            print(SQL)
            cur = db.execute(SQL)
            person = cur.fetchall()
        print(person)
        return person

    except Exception as e:
        flash("(⊙﹏⊙)b 查询空闲时间段时出错了：%s <br> 请狠狠地戳开发人员~~~" % e.args[0], category="error")
        printLog("[searchFreetime Error] %s" % e.args[0])
        printErrTraceback(title="searchFreetime",exception=e)
