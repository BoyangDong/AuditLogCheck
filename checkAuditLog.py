#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import csv 
import os
import os.path 
from os.path import isfile, join 
from server import server 
from VictoryUtil import MountDrive 

servers = []
server_id = 0
spreadsheet = "Budo_Server_Spreadsheet.csv"


def get_server_objs():
	with open (spreadsheet, "r") as f:
		next(f) #skip the header
		reader = csv.reader(f)
		for row in reader:
			if len(row[1]) == 0 or row[7] == 'Shut' or not row[8]: #skip the server that is shut/empty line/log path is N/A 
		 		continue
		 	else:
		 		global server_id
		 		server_id += 1
		 		s = server(row[0], row[1], row[2], row[3], row[4], server_id, False, row[8])
		 		servers.append(s)


def fetch_log(obj):
	newdrive = MountDrive("\\\\"+obj.ip+"\\C$", 'vadmin12', '131wang', 'victory')

	s = obj.log_path 
	toks = s.split("\\")
	dir = "Z:"
	for i in range(len(toks)-1):
		dir = dir + "\\\\"+toks[i+1]

	print "the audit logs path under mount drive is: ", dir
	# get the log names with the given path of mount drive 
	log_names = [f for f in os.listdir(dir) if isfile(join(dir, f))]
	print "there are %i log files under this dir", len(log_names)

	counter = 0
	for i in log_names:
		with open(dir + "\\" + i) as f:
			f.seek(0)
			first_char = f.read(1)
			if not first_char:
				print "Empty file is found..."
				write_log(obj, i)
			else:
				counter += 1

	newdrive.unmount() 


def write_log(obj, log_name):

	print "Writing into database..."
	db = MySQLdb.connect(host="localhost",
	                     user="bdong",     
	                     passwd="bdong",  
	                     db="log_report")

	cur = db.cursor()
	
	try:
		cur.execute("""INSERT INTO loginfo VALUES (%s,%s,%s,%s)""",(obj.server_name, obj.ip, log_name, "EMPTY FILE"))
		db.commit()

	except:
		db.rollback()

	db.close()
	print "Finish updating"...""


if __name__ == '__main__':

	get_server_objs()
	for i in range(len(servers)):
		print "--- Working on the Server: " + servers[i].server_name + "---"
		fetch_log(servers[i])