#!/usr/bin/python
#-*-coding UTF-8 -*-
import os
import sys
import xlrd
import platform
from datetime import date,datetime
import argparse
import warnings

file = "key.xls"
keyfile = "mode.key"
sys = platform.system()
autosyskeyfile="autokeyfile"+sys+".sh"
autokeyfile = "autokeyfile.sh"
cmdlist = []
keymapdict = dict()

def read_excel(sheetkeymap):

	#open excel
	readfile = xlrd.open_workbook(filename=file)

	#check sheet count
	sheetcount=len(readfile.sheets())
	#print ("sheet count "+str(sheetcount))
	if sheetkeymap >= sheetcount:
		warnings.warn("map sheet index big than sheet number error!!!")
		exit(0)
	#get excel key map index
	sheetmap = readfile.sheet_by_index(sheetkeymap)
	#get key map count
	keymapscout = sheetmap.nrows 
	imap = 1
	#counstruct keymap
	while imap < keymapscout:
		maprows = sheetmap.row_values(imap)
		keymapdict[str(maprows[0])]=str(maprows[1])
		imap=imap+1

	#get excel index
	sheet1 = readfile.sheet_by_index(0)

	#get index size
	count = sheet1.nrows
	#print count

	#get excel index value
	i = 1
	while i < count:
		rows = sheet1.row_values(i)
		#cmd="\trepeatkey \""+str(rows[0])+"\" \""+str(rows[1])+"\" \""+str(rows[2])+"\"\n"
		if str(rows[0]) in keymapdict:
			cmd="\trepeatkey \""+str(rows[0])+"\" \""+str(rows[1])+"\" \""+str(rows[2])+"\" \""+keymapdict.get(str(rows[0]))+"\"\n"
			cmdlist.append(cmd)
		else:
			warnings.warn (str(rows[0])+" can not map keycode!!!!!!!!!!,may don't you want or need add scan key code in key.xmls sheet"+str(sheetkeymap+1))
		i=i+1


def readPaserLogfile(filename):
	#open the log file
	path=os.getcwd()
	#print("patch : "+path)
	cmd=""
	pre_event_sec=0
	pre_event_usec=0
	pre_code=0
	event_sec=0
	event_usec=0
	code=0
	#paser log file
	with open(path+"/"+filename,"r") as logfile:
		while True:
			line = logfile.readline();
			if not line:
				#print("parser log file end")
				break
			elif 'MANGODANRecordKeyEvent' in line:
			    list=line.split(',')
			    #print(list)
			    for index ,val in enumerate(list):
			    	if index == 1: #code=value
			    		pre_code=code
			    		code=val.split('=')[-1]
			    		#print("code: %s"%code)
			    	elif index == 2: #event_sec=value
			    		pre_event_sec=event_sec
			    		event_sec=long(val.split('=')[-1])
			    		#print("event_sec:%s"%event_sec)
			    	elif index == 3: #event_usec=value
			    		pre_event_usec=event_usec
			    		event_usec=long(val.split('=')[-1])
			    		#print("event_usec:%s"%event_usec)
			    	elif index == 0:
			    		#print("=============================")
			    		if pre_code != 0:
			    			now=event_sec*1000*1000+event_usec
			    			before=pre_event_sec*1000*1000+pre_event_usec
			    			diff=(now-before)/1000
			    			cmd="\trepeatkey \""+"CODE"+"\" \""+"1"+"\" \""+str(diff/100)+"\" \""+str(pre_code)+"\"\n"
			    			#print("cmd: %s"%cmd)
			    			cmdlist.append(cmd)
			else:
				pass
		if cmd != "":
			now=event_sec*1000*1000+event_usec
			before=pre_event_sec*1000*1000+pre_event_usec
			diff=(now-before)/1000
			cmd="\trepeatkey \""+"CODE"+"\" \""+"1"+"\" \""+str(diff/100)+"\" \""+str(pre_code)+"\"\n"
			#print("cmd: %s"%cmd)
			cmdlist.append(cmd)
			#add last keyevent
			cmd="\trepeatkey \""+"CODE"+"\" \""+"1"+"\" \""+"0"+"\" \""+str(code)+"\"\n"
			#print("cmd: %s"%cmd)
			cmdlist.append(cmd)
		logfile.close()

#create auto test key file 		
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

	target_file=open(autosyskeyfile,"w")
	for x in lines:
		target_file.write(x)
	target_file.close()

def dos2unix(file,dirfile,toformat='dos2unix'):
	if not os.path.isfile(file):
		print("ERROR!!!, file not")
		return
	if toformat == 'unix2dos':
		line_sep = '\r\n'
	else:
		line_sep = '\n'

	with open(file, 'r') as fd:
		tempfile = open(toformat+file, 'w+b')
		for line in fd:
			line = line.replace('\r','')
			line = line.replace('\n','')
			tempfile.write(line+line_sep)
		tempfile.close()
		os.rename(toformat+file, dirfile)
	print("dos2unix sucess!!!")
	os.remove(autosyskeyfile)

if __name__ == '__main__':
	if os.path.isfile(autokeyfile):
		os.remove(autokeyfile)
	parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
	parser.add_argument("--type", type=str,default="key.xls",help="default import key.xls, type : import keyvent from log file name",dest="typefilename")
	parser.add_argument("--sheet",type=int,default=2,help="keymapsheet index number",dest="sheet")
	args = parser.parse_args()
	filetype = args.typefilename

	if filetype == file:
		print("import key event form key.xls")
		#parse xml sheet 
		keymapsheet = args.sheet - 1
		if keymapsheet < 1:
			warnings.warn("key map sheet need big than 1 error!!!")
			exit(0)
		read_excel(keymapsheet)
	else:
		print("import key event from log file :"+filetype)
		readPaserLogfile(filetype)
	
	createautotestkey()
	if len(cmdlist) == 0:
		warnings.warn("invalue sh, keymap can't map any scankeycode!!!!")
		print("fail !!!")
		exit(0)
	if sys == "Windows":
		print ("os is windows will dos2unix!!!")
		dos2unix(autosyskeyfile,autokeyfile)
	elif sys == "Linux":
		os.rename(autosyskeyfile,autokeyfile)
	else:
		pass
	print ("sucess!!!")
