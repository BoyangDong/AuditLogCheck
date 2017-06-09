# -*- coding: utf-8 -*-  
import paramiko
import time 
import os 
import zipfile
from time import gmtime, strftime 
from ftp import upload_files

now = time.time() #current time in milliseconds
current_date = strftime('%Y%m%d', gmtime())



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

file_path = ''.join([file_path_root, 'Budo-JerryAttlan_AuditTrail_20170523.zip'])
local_path = ''.join([local_path_root, 'Budo-JerryAttlan_AuditTrail_20170523.zip'])

counter = 0
#Iterate zip folders sequencially 
# Create the zipped folder 
zipped_folder_name = ''.join(['_'.join(["SERVER_TBD", current_date]), '.zip']) 
myZipFile = zipfile.ZipFile(zipped_folder_name, "w")

'''
folders = sftp.listdir(file_path_root)
for i in range(len(folders)):
	print sftp.listdir(file_path_root)[i] #Budo-JerryAttlan_AuditTrail_20170523.zip
	counter = counter + 1
'''
'''Unzip to local dir 
sftp.get(file_path, local_path)
zip_ref = zipfile.ZipFile(local_path, 'r')
zip_ref.extractall(local_path_root)
zip_ref.close()
'''
for r, d, f in os.walk(local_path_root):
	for log in f:
		full_path = os.path.join(r, log)
		date_file = os.path.getmtime(full_path)
		if log.endswith(".log") or log.endswith(".txt"): 
			if now - date_file <= 86400:
				if os.path.getsize(full_path) == long(0):
					counter = counter + 1
					print counter
					# record this empty log files into db
				else:
					#zip and upload to edfman  
					file_name = full_path.split('/')[-1] #file name that shows up in the zipped folder is from the last token of full path 
					myZipFile.write(full_path, file_name, zipfile.ZIP_DEFLATED)
					#with open(r'%s' %'e:/Repos/Project_1/') as f:
					upload_files(zipped_folder_name)
					# zip folders need to be remoted.. 
					#os.remove(zipped_folder_name)


# Close
#zip_ref.close()
sftp.close()
transport.close()

# Reference Page 
# https://stackoverflow.com/questions/3635131/paramikos-sshclient-with-sftp
