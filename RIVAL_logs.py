# -*- coding: utf-8 -*-  

import os
import datetime as dt
import zipfile 
from BudoUtil import send_email
from BudoUtil import record_in_db
from BudoUtil import upload_to_EDFMan 

folders = []
num_empty_logs = 0

current_day = dt.datetime.now() 

date = current_day.strftime('%Y%m%d')

source_dir = '\\\\172.30.80.25\\Upload\\Rival'
edfman_path_dir = r'%s' % (''.join(['/weekly_test/', date, '_', 'RIVAL', '/'])) #add postfix _rival to differentiate log from TT servers  
zipped_folder_name = ''.join([date, '_', 'rival', '.zip'])

rival_servers = {
	"BUDO-DC3-RIVAL-1"	: ['10.133.64.71',	'Rod Valeroso'],
	"BUDO-DC3-RIVAL-2"	: ['10.133.64.72',	'Duncan Robinson']
	#"Budo-350-DEV-1"	: ['10.62.0.9',		'Ted Hilk']
}

myZipFile = zipfile.ZipFile(zipped_folder_name, mode='w', allowZip64=True) # Allow to zip a folder which size is greater than 4gb 

folders.append("%s\\%s_rival" % (source_dir, date)) 

'''Trggered on 9pm Saturday weekly, it will grab the logs from last 7 days'''
# Construct the 7 folders name
for i in xrange(1,7):
	yesterday = current_day - dt.timedelta(days=1)
	date = yesterday.strftime('%Y%m%d')
	rival_folder_name = "%s\\%s_rival" % (source_dir, date) #construct the full dir w/ postfix  
	folders.append(rival_folder_name)
	current_day = yesterday

# Traverse 7 folders, check and zip 
for j in range(len(folders)): # hit files sequentially 
	for r, d, f in os.walk(folders[j]):
		for log in f: 
			full_log_path = folders[j] + '\\' + log
			#print full_log_path # full log path is the full dir of the log file is 
			if os.path.getsize(full_log_path) != 0:
				#print "%s is not empty " % log # "log" is the file name 
				myZipFile.write(full_log_path, log, zipfile.ZIP_DEFLATED) 
			else: 
				toks = log.split('_') # log = "H4U.D6MLog20171008.LOG.csv_rvaleroso_20171008" 
				ts = os.path.getctime(full_log_path) 
				num_empty_logs = num_empty_logs+1
				if toks[1] is 'rvaleroso':					
					record_in_db(server_name="BUDO-DC3-RIVAL-1", server_ip='10.133.64.71', log_name=log, time_stamp=ts) 
				elif toks[1] is 'drobinson':
					record_in_db(server_name="BUDO-DC3-RIVAL-2", server_ip='10.133.64.72', log_name=log, time_stamp=ts) 
				else:
					record_in_db(server_name="SERVER_UNKNOWN", server_ip='ATTENTION_NEEDED', log_name=log, time_stamp=ts)
				print full_log_path 

myZipFile.close()

os.remove(zipped_folder_name)

# Upload to Clearing Firm
upload_to_EDFMan(folder_uploaded=zipped_folder_name, path_out=edfman_path_dir)

# Notify Users 
if 0 != num_empty_logs:
	send_email(content = ("empty log file is captured found from RivalSystems servers during the week of %s." % date))
else:
	send_email(content = ("No empty log file is found from RivalSystems servers during the week of %s." % date))