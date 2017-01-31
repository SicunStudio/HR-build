#!/usr/bin/python3
# -*- coding: utf-8 -*-

'   self-made utils for operating .xlsx files based on openpyxl (*nix only) ---- by smdsbz   '

from openpyxl import Workbook, load_workbook
from datetime import datetime
#import os, shutil


######## utils ########

def _read_test():
	''' return table header line '''
	wb = load_workbook('./score-sheets/template.xlsx')
	data = wb.get_sheet_by_name(wb.get_sheet_names()[0])
	return tuple([ content.value for content in data['A2':'M2'][0] ])

def _move_cursor(data, name='something you have to mess up with'):
	'''
	  return the index asked
	  IF no match THEN yield index-number for the next empty row
	'''
	nameCells = data['A'][2:] # 1: test-use; running: 2
	names = tuple(filter(lambda s: s and s.strip(), [ content.value for content in nameCells ]))  # thx 2 MichealLiao
	#print(names)
	if name in names:
		return names.index(name) + 3 # 2: test-use
	else:
		return len(names) + 3

def newFile(title="测试测试", depart="其他", *, date=str(datetime.now())):
	filename = './score-sheets/' + title + ' - ' + date + '.xlsx'
	wb = load_workbook('./score-sheets/template.xlsx')
	ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
	ws.title = title
	ws['B1'], ws['F1'], ws['J1'] = title, depart, date
	wb.save(filename)

def write(src, data):
	wb = load_workbook(src)
	ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
	cur = str(_move_cursor(ws, data[0]))
	dst = ws['A'+cur:'K'+cur][0]
	# here goes the ugly lines again....
	organized = {0:data[0], 1:data[1], 2:data[2], 3:data[3], 4:data[4], 5:data[5], 6:data[6], 7:data[7], 8:data[8], 9:data[9], 10:data[10]}
	for k, v in organized.items():
		dst[k].value = v
	wb.save(src)

def read(src):
	wb = load_workbook(src)
	ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
	end = _move_cursor(ws)
	if end == 3:
		return []
	rtr = []
	for each in range(3, end):
		cur = str(each)
		tmp = [ws['A'+cur].value, ws['B'+cur].value, ws['C'+cur].value, ws['D'+cur].value, ws['E'+cur].value, ws['F'+cur].value, ws['G'+cur].value, ws['H'+cur].value, ws['I'+cur].value, ws['J'+cur].value, ws['K'+cur].value]
		rtr.append(tmp)
	return rtr

######## test-use ########

if __name__ == '__main__':
	# expecting result in console ==> "姓名\项目"
	print(_read_test())
	# expecting result in console ==> 2
	print("姓名\项目 is at", _move_cursor(name="姓名\\项目"))
	# expecting result in console ==> 3
	print("if no match:", _move_cursor())
