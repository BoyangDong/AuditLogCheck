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

# Close
sftp.close()
transport.close()

# Reference Page 
# https://stackoverflow.com/questions/3635131/paramikos-sshclient-with-sftp