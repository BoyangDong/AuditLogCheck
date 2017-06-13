# -*- coding: utf-8 -*-  
import paramiko
import time 
import datetime
import os 
import zipfile
from time import gmtime, strftime 
from ftp import upload_files
from BudoUtil import send_email
from BudoUtil import record_in_db
from BudoUtil import upload_to_EDFMan 

now = time.time() #current time in milliseconds
date_today = strftime('%m-%d-%Y', gmtime())
current_date = strftime('%Y%m%d', gmtime())

empty_logs_counter = 0
email_toks = []
servers_with_empty_logs = {}
servers_info = {
	"BudoTrading"			: ['10.64.0.8'	, 'BUDO-DC3-OC-1', 'Todd Jones, Niel Hunt'	],
	"BudoTrading-Kiran"		: ['10.64.0.131', 'BUDO-DC3-OC-2', 'Kiran Khambhampati'		],
	"Budo-JerryAttlan"		: ['10.64.0.131', 'BUDO-DC3-OC-2', 'Jerry Attlan'			],
	"Budo-LennyZaban"		: ['10.64.0.139', 'BUDO-DC3-OC-4', 'Jeff**, Lenny, Erin'	],
	"Budo-LennyZabanQuoter"	: ['10.64.0.139', 'BUDO-DC3-OC-4', 'Jeff, Lenny(Quoter)'	],
	"Budo-MichaelHandwerker": ['10.64.0.2'	, 'BUDO-DC3-OC-5', 'Michael Handwerker'		]
}


# Open a transport
host = "ftp.optionscity.com" #64.74.102.118
port = 4242
transport = paramiko.Transport((host, port))

# Auth
password = "0duBptFsNow@!"
username = "sftpbudo"
pkey = r'%s' % 'C:/Users/boyang.dong/.ssh/sftpbudo-id_rsa'
key=paramiko.RSAKey.from_private_key_file(pkey,password=password)  

transport.connect(username=username, pkey=key)

# Go!
sftp = paramiko.SFTPClient.from_transport(transport)

file_path_root = r'%s' % 'instance1/audit_logs/'
local_path_root = r'%s' %'e:/Repos/Project_1/test_logs/OptionsCity/'

sftp.chdir(file_path_root)
print 'connected!'

folders = sftp.listdir('.')

for i in range(len(folders)): 
	folder_path = folders[i]  #folder_path = Budo-JerryAttlan_AuditTrail_20170523.zip
	folder_stat = sftp.stat(folder_path)
	folder_creation_time = folder_stat.st_mtime
	if now - folder_creation_time <= 86400: #!!!! cheap test for now, 24 hours 
		folder_ts = datetime.datetime.fromtimestamp(folder_creation_time).strftime('%Y-%m-%d %H:%M:%S')
		#print "File is found: %s" % folder_path	
		#print "File create on %s" % folder_ts
		#print "From stat    : %s" % folder_stat		
		folder_prefix = folder_path.split('_')[0] #prefix is used as key in servers_info dict initialized at the beginning of the script 
		server_ip, server_name = servers_info[folder_prefix][0], servers_info[folder_prefix][1]
		if 0 == folder_stat.st_size:
			record_in_db(server_name=server_name, server_ip=server_ip, log_name=folder_path.split('.')[0], time_stamp=folder_ts)  # get rid of extension name .zip, server name is actually the host name
			empty_logs_counter += 1
			if folder_path in servers_with_empty_logs:  #!!!! TODO: Use folder_path for now will SUBSTITUTE to SERVER NAME LATER!!!!
				servers_with_empty_logs[folder_path] += 1
			else:
				servers_with_empty_logs[folder_path] = 1
		else:
			path_out = ''.join(['\\weekly_test\\', current_date, '\\', folder_path])
			full_local_folder_path = ''.join([local_path_root, folder_path])
			sftp.get(folder_path, full_local_folder_path)
			#upload_to_EDFMan(path_in=full_local_folder_path, path_out=path_out, current_date=current_date, zipped_folder=folder_path) #!!!!! TODO!!!!
			#print "Folder has been uploaded!"
		#sftp.remove(folder_path) !!!! once the audit log zip folder has been checked, remove it
			
# Close
#zip_ref.close()
sftp.close()
transport.close()


# send email with report 
if 0 == len(servers_with_empty_logs):  
	send_email(content = ("No empty log files is found from OptionsCity servers on %s." % date_today))
else: 		
	email_toks.extend(["Audit Log Checker Report: ",date_today, "\n"])
	for k, v in servers_with_empty_logs.iteritems():    
		email_toks.extend(["Empty audit log exists: ", k, " \t" , '# OF EMPTY LOG FILES:', str(v),' \n']) 
	send_email(content = (''.join(email_toks)))