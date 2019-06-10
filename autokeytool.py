#!/usr/bin/python
#-*-coding UTF-8 -*-
import os
import sys
import xlrd
import string
from datetime import date,datetime

file = "key.xls"
keyfile = "key.ini"
autokeyfile = "autokeyfile.sh"
cmdlist = []

def read_excel():

	#open excel
	readfile = xlrd.open_workbook(filename=file)

	#get excel index
	sheet1 = readfile.sheet_by_index(0)

	#get index size
	count = sheet1.nrows
	#print count

	#get excel index value
	i = 1;
	while i < count:
		rows = sheet1.row_values(i)
		cmd="\trepeatkey \""+str(rows[0])+"\" \""+str(rows[1])+"\" \""+str(rows[2])+"\"\n"
		cmdlist.append(cmd)
		i=i+1

def createautotestkey():
	lines = []
	dontwrite=0
	tarstring="autotestkey()"
	source_file=open(keyfile,"r")
	for line in source_file:
		if dontwrite == 1 and "}" in line:
		 	dontwrite = 0
		 	continue
		if dontwrite == 1:
			continue
		lines.append(line)
		if tarstring in line:
			lines.append("{\n")
			for cmd in cmdlist:
				lines.append(cmd)
			lines.append("}\n")
			dontwrite=1
	source_file.close()

	target_file=open(autokeyfile,"w")
	for x in lines:
		target_file.write(x)
	target_file.close()

if __name__ == '__main__':
	print "auto create autokeyfile.sh"
	read_excel()
	createautotestkey()
	print "sucess!!!"
