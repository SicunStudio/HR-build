#!/usr/bin/python3
# -*- coding: utf-8 -*-

'   self-made utils for operating .xlsx files based on openpyxl ---- by smdsbz   '

from openpyxl import Workbook, load_workbook
from flask import flash
from datetime import datetime
import os, sqlite3

######## general config ########

FOLDER = os.path.join(os.curdir, 'score-sheets')  # xlsx location
INVENTORY = os.path.join(FOLDER, 'inventory.db')
DATABASE = os.path.join(os.curdir, 'data.db')  # db loaction
# that is to say: main.py, xlsxSwissKnife.py and data.da must be under the same dir

######## utils ########

def _read_test():
	''' return table header line '''
	wb = load_workbook(os.path.join(FOLDER, 'template.xlsx'))
	data = wb.get_sheet_by_name(wb.get_sheet_names()[0])
	return tuple([ content.value for content in data['A2':'M2'][0] ])

def _move_cursor(ws, name='something you have to mess up with'):
	'''
	return the index asked
	IF no match THEN return index-number of the adjacent empty row
	'''
	nameCells = ws['A'][2:] # 1: test-use; running: 2
	names = tuple(filter(lambda s: s and s.strip(), [ content.value for content in nameCells ]))  # thx 2 MichealLiao
	if name in names:
		return names.index(name) + 3 # 2: test-use
	else:
		return len(names) + 3

def newFile(title="测试测试", depart="其它", *, date=str(datetime.now())):
	'''
	  derive a new .xlsx from ./score-sheets/template.xlsx
	  (openpyxl Compatibility: always use MS Excel to generate the template.xlsx)
	'''
	filename = title + '.xlsx'
	dst = os.path.join(FOLDER, filename)
	if filename in os.listdir(FOLDER):
		flash("该表格已经存在！", category='error')
		return 0
	try:
		wb = load_workbook(os.path.join(FOLDER, 'template.xlsx'))
	except IOError:
		flash("表格模板损坏！<br>请联系管理员！", category='error')
		return 0
	else:
		with sqlite3.connect(INVENTORY) as database:
			try:
				cursor = database.execute("insert into score values ('%s', '%s', '%s')" % (title, date, depart))
			except sqlite3.IntegrityError:
				flash("该表格名称已被占用！", category='error')
				return 0
			else:
				database.commit()
		ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
		# fill header
		ws.title = title
		ws['B1'].value, ws['F1'].value, ws['J1'].value = title, depart, date
		# import names
		with sqlite3.connect(DATABASE) as database:
			cursor = database.execute("select name from test where depart = '%s'" % depart)
			names = cursor.fetchall()
			print('hi?')
		for i in range(len(names)):
			ws['A'+str(i+3)].value = names[i][0]
		wb.save(dst)
		# register at inventory.db
		flash("成功创建表格！<br><sup>请一次性填写完表格！</sup>", category='success')
		return 1

def write(filname, data_in):
	''' write/update one persona at a time '''
	dst = os.path.join(FOLDER, filename)
	try:
		wb = load_workbook(dst)
	except IOError:
		flash("写入表格错误！", category='error')
		return 0
	else:
		ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
		cur = str(_move_cursor(ws, data_in[0]))
		for i, o in zip(ws['B'+cur:'K'+cur][0], data_in[1:]):
			o.value = i
		wb.save(dst)
		return 1

def read(filename):
	'''
	  returns a dict of * in the file
	    format:
	    {'name':{'B':1, 'C': 2, ..., 'K':10}, 'next person':{...}, ...}
	'''
	# TODO: 同名问题
	dst = os.path.join(FOLDER, filename)
	try:
		wb = load_workbook(dst)
	except IOError:
		print('IOError during read({})'.format(dst))
		flash("表格读取错误！", category='error')
		return []
	else:
		print('load successully!')
		ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
		end = _move_cursor(ws)
		everyone = dict()
		for row in tuple(map(str, range(3, end))):  # get ('3', '4', '5', ..., '{end-1}')
			someone = dict()  # single person container
			for col in 'BCDEFGHIJK':
				someone[col] = ws[col+row].value
			everyone[ws['A'+row].value] = someone  # join the party
		return everyone
