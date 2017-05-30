import pysftp as sftp
import paramiko 
import os
import datetime 


#Another pair of credentials 
#password = "Wonderwall$AtlantisSlumberAdvisory"
#username = "BUDO_ATTLAN"
password = 'q&4r)1bx*Y'
username = 'BudoAudit'


#path_to_file = 'E:\\Repos\\Project_1\\README.md'
path_to_file = 'E:\\Repos\\Project_1\\hello_world.txt'
outgoing_path = '\\test_weekly_audit_logs\\hello_world.txt'


def upload_files():
	try:
		print "connection establishing..."
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		trans = paramiko.Transport(("ftpc.edfmancapital.com", 2222))
		trans.connect(username = username, password = password)
		sftp = paramiko.SFTPClient.from_transport(trans)
		print "connected!"
		sftp.put(path_to_file, outgoing_path)
		print "file has been uploaded..."
	except Exception, e:
		print str(e)


def get_file_creation_time(file_path):
    t = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S") # strftime can disregard the millisecond


if __name__ == "__main__":
	#send_email()
	#print get_file_creation_time(path_to_file)
	upload_files()