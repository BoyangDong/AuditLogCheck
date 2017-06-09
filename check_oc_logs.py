# -*- coding: utf-8 -*-  

import paramiko

pkey = 'C:\\Users\\boyang.dong\\.ssh\\sftpbudo-id_rsa'

# Open a transport
host = "ftp.optionscity.com" #64.74.102.118
port = 4242
transport = paramiko.Transport((host, port))

# Auth
password = "0duBptFsNow@!"
username = "sftpbudo"
key=paramiko.RSAKey.from_private_key_file(pkey,password=password)  

transport.connect(username=username, pkey=key)

# Go!
sftp = paramiko.SFTPClient.from_transport(transport)

file_path_root = 'instance1/audit_logs/'
local_path_root = 'e:/Repos/Project_1/test_logs/OptionsCity/'

file_path = ''.join([file_path_root, 'Budo-JerryAttlan_AuditTrail_20170529.zip'])#\\instance1\\audit_logs\\Budo-JerryAttlan_AuditTrail_20170529.zip'
local_path = ''.join([local_path_root, 'newzip.zip'])
#local_path = 'E:\\Repos\\Project_1\\test_logs\\OptionsCity\\Log1.zip'
sftp.get(r'%s' % file_path, r'%s' % local_path)

# Close
sftp.close()
transport.close()

# Reference Page 
# https://stackoverflow.com/questions/3635131/paramikos-sshclient-with-sftp

#sftp://sftpbudo@64.74.102.118:4242/instance1/audit_logs/Budo-JerryAttlan_AuditTrail_20170529.zip