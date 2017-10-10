# -*- coding: utf-8 -*-  

import os
import datetime as dt
import zipfile 


folders = []

current_day = dt.datetime.now() 

date = current_day.strftime('%Y%m%d')

source_dir = '\\\\172.30.80.25\\Upload\\Rival'
local_path_root = r'%s' % 'e:/Repos/Project_1/test_logs/Rival/'
edfman_path_dir = r'%s' % (''.join(['/weekly_test/', date, '_', 'rival', '/'])) #add postfix _rival to differentiate log from TT servers  
zipped_folder_name = ''.join([date, '_', 'rival', '.zip'])

print edfman_path_dir

rival_servers = {
	"BUDO-DC3-RIVAL-1"	: ['10.133.64.71',	'Rod Valeroso'],
	"BUDO-DC3-DC3-2"	: ['10.133.64.72',	'Duncan Robinson']
	#"Budo-350-DEV-1"	: ['10.62.0.9',		'Ted Hilk']
}

myZipFile = zipfile.ZipFile(zipped_folder_name, mode='w', allowZip64=True) # Allow to zip a folder which size is greater than 4gb 

folders.append("%s\\%s_rival" % (source_dir, date)) 

'''Trggered on 9pm Saturday weekly, it will grab the logs from last 7 days'''
for i in xrange(1,7):
	yesterday = current_day - dt.timedelta(days=1)
	date = yesterday.strftime('%Y%m%d')
	rival_folder_name = "%s\\%s_rival" % (source_dir, date) #construct the full dir w/ postfix  
	folders.append(rival_folder_name)
	current_day = yesterday


for j in range(len(folders)): # hit files sequentially 
	for r, d, f in os.walk(folders[j]):
		print folders[j]
		for log in f: 
			full_log_path = folders[j] + '\\' + log
			print full_log_path
			if os.path.getsize(full_log_path) is not 0:
				print "%s is not empty " % log 
				myZipFile.write(full_log_path, log, zipfile.ZIP_DEFLATED)

myZipFile.close()