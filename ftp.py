import MySQLdb
import pysftp as sftp
import paramiko 
import os
import time
import datetime 
import zipfile
import csv 

from time import gmtime, strftime
from os.path import isfile, join 
from server import server 
from VictoryUtil import MountDrive 

#Another pair of credentials 
#password = "Wonderwall$AtlantisSlumberAdvisory"
#username = "BUDO_ATTLAN"
password = 'q&4r)1bx*Y'
username = 'BudoAudit'

now = time.time() #current time in milliseconds
current_date = strftime("%m-%d-%Y", gmtime())

servers = []
server_id = 0


#def check_logs(path_to_folder, server_name, topdown=False):
def check_logs(obj, topdown=False):
	"""Mount the drive first and it walks through the files under server log folder
	check sequentially, remove the empty logs while retain the recent 5-day ones 
	and zip them together into a folder, then invoke the upload ftp funtion
	"""
	# Mount the drive out 
	newdrive = MountDrive("\\\\"+obj.ip+"\\C$", 'vadmin12', '131wang', 'victory')
	# Create the zipped folder 
	zipped_folder_name = ''.join(['_'.join([obj.server_name, current_date]), '.zip'])
	myZipFile = zipfile.ZipFile(zipped_folder_name, "w")
	# Construct the absolute log path based on the spreadsheet info  
	s = obj.log_path 
	toks = s.split("\\")
	path_to_logs = "Z:"
	for i in range(len(toks)-1):
		path_to_logs = path_to_logs + "\\\\"+toks[i+1]

	print path_to_logs
	# Walk through the log files 
	print "checking logs..."
	m = 0 # counter for empty log files 
	n = 0 # counter for non-empty log files 
	for r, d, f in os.walk(path_to_logs):
		for log in f:
			full_path = os.path.join(r, log)
			date_file = os.path.getmtime(full_path)
			if log.endswith(".log") or log.endswith(".txt"):
				# Check the recent five days, starting from Sunday 8pm to Friday 8pm 
				if now - date_file <= 14400: # !!!!14400 for a cheap test for 48 hours, change back to 43200 for weekly-check					
					n = n + 1
					if os.path.getsize(full_path) == long(0):
						m = m + 1
						#os.remove(full_path)   #!!!!!! remove the "remove" function just for now 
						record_in_db(obj, log, full_path)
						print "%s is  empty and removed.." % log
					else:
						#Zip the non-empty files and uploaded under FTP 
						#myZipFile.write(full_path, ''.join(["\\", log]), zipfile.ZIP_DEFLATED)
						myZipFile.write('E:\\Repos\\Project_1\\test_logs\\ActantRmt_20170428.log', ''.join(["\\", log]), zipfile.ZIP_DEFLATED)
												
	print "Empty Logs: %s" % m 
	print "Total Logs: %s" % n
	myZipFile.close()
	upload_files(zipped_folder_name)
	newdrive.unmount() 


def upload_files(zipped_folder):
	'''Upload the zipped log files through sftp to edfman
	'''
	current_dir = os.path.dirname(os.path.realpath(__file__))
	path_to_zipped_folder = ''.join([current_dir, '\\', zipped_folder])
	path_out = ''.join(['\\weekly_test\\', zipped_folder])
	try:
		print "connection establishing..."
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		trans = paramiko.Transport(("ftpc.edfmancapital.com", 2222))
		trans.connect(username = username, password = password)
		sftp = paramiko.SFTPClient.from_transport(trans)
		print "connected!"
		#sftp.put(path_to_file, outgoing_path)
		sftp.put(path_to_zipped_folder, path_out)
		print "Folder hase been uploaded!"
	except Exception, e:
		print str(e)
	finally: 
		trans.close() 
		os.remove(zipped_folder)
		

def record_in_db(obj, log_name, file_path):
	db = MySQLdb.connect(host="localhost", user="bdong", passwd="bdong", db="log_report")
	cur = db.cursor()
	try:
		cur.execute("""INSERT INTO error_log_info VALUES (%s,%s,%s,%s,%s)""",(obj.server_name, obj.ip, log_name, get_file_creation_time(file_path),"EMPTY FILE")) #time stamp format: '2017-04-21 13:59:45'
												 			                 #server,          ip,     file_name,time_stamp,                       error_type
		print get_file_creation_time(file_path)
		db.commit()
	except Exception, e:
		db.rollback()
		print str(e)
	finally: 
		if db: db.close()


def get_file_creation_time(file_path):
	#This function is currently unused, it provides a formatted time stamp format given a absolute path of the file
    t = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S") # strftime can disregard the millisecond


def get_server_objects(spreadsheet):
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

'''
if __name__ == "__main__":
	#main function for module test 
	check_logs("Z:\\\\Program Files\\Actant\\Log", "BUDO-TEST-1")
	#10.64.0.5
'''
if __name__ == "__main__":
	spreadsheet = "Budo_Server_Spreadsheet.csv"
	get_server_objects(spreadsheet)
	for server in servers: check_logs(server)
	#check_logs(servers[0])
	#print servers[2].ip