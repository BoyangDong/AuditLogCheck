#!/usr/bin/python
# -*- coding: utf-8 -*-

#####################################################################################
# Audit Log Checker																	#
#																					#
# Discription: It checks the log files from servers listed on the csv file.			#
#              The error files will be recored and the users will be notified.		#
#																					#
# Created on 04/21/2017																#
# Version 1.0																		#
# boyang.dong@budoholdings.com														#
#####################################################################################

import MySQLdb
import csv 
import os
import os.path 
import smtplib
import datetime 
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
	directory = "Z:"
	for i in range(len(toks)-1):
		directory = directory + "\\\\"+toks[i+1]
	print "the audit logs path under mount drive is: ", directory
	# get the log names with the given path of mount drive 
	log_names = [f for f in os.listdir(directory) if isfile(join(directory, f))]
	print "FILE NUMBER: %s" % len(log_names)
	counter = 0
	print "CHECKING AUDIT LOGS..."
	for i in log_names:
		if os.stat(directory + "\\" + i).st_size == 0:
			record_in_db(obj, i, directory)
		else:
			continue
	newdrive.unmount() 


def record_in_db(obj, log_name, file_path):
	db = MySQLdb.connect(host="localhost",
	                     user="bdong",     
	                     passwd="bdong",  
	                     db="log_report")
	cur = db.cursor()
	try:
		cur.execute("""INSERT INTO error_log_info VALUES (%s,%s,%s,%s,%s)""",(obj.server_name, obj.ip, log_name, get_file_creation_time(file_path),"EMPTY FILE")) #time stamp format: '2017-04-21 13:59:45'
												 			                 #server,          ip,     file_name,time_stamp,                       error_type
		db.commit()
	except Exception, e:
		db.rollback()
		print str(e)
	db.close()


def get_file_creation_time(file_path):
    t = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S") # strftime can disregard the millisecond


def send_email():
	content = "testing email"
	print "Setting up email server..."
	mail = smtplib.SMTP('smtp.gmail.com', 587)
	mail.ehlo()
	mail.starttls()
	mail.login('test.budo@gmail.com', 'test.budo123')
	mail.sendmail('test.budo@gmail.com', 'boyang.dong@budoholdings.com', content)
	print "Email Sent!"
	mail.close()

if __name__ == '__main__':
	
	# fetch the list of servers 
	get_server_objs()
	# check the logs under each server 

	for i in range(len(servers)):
		print "--- Working on the Server: " + servers[i].server_name + "---"
		fetch_log(servers[i])

	
	#print get_file_creation_time("Z:\\Program Files\\Actant\\Log\\ActantRisk_20161118_1")
