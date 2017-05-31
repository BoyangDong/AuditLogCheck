import pysftp as sftp
import paramiko 
import os
import datetime 
import time

#Another pair of credentials 
#password = "Wonderwall$AtlantisSlumberAdvisory"
#username = "BUDO_ATTLAN"
password = 'q&4r)1bx*Y'
username = 'BudoAudit'

now = time.time()

#Two paths below are for local test 
path_to_file = 'E:\\Repos\\Project_1\\hello_world.txt'
outgoing_path = '\\test_weekly_audit_logs\\hello_world.txt'

def check_logs(path_to_folder, topdown=False):
	print "checking sequentially..."
	counter = 0
	for r, d, f in os.walk(path_to_folder):
		for all_files in f:
			full_path = os.path.join(r, all_files)
			date_file = os.path.getmtime(full_path)
			if all_files.endswith(".log") or all_files.endswith(".txt"):
				# Check the recent five days, starting from Sunday 8pm to Friday 8pm 
				if now - date_file <= 432000:					
					if os.path.getsize(full_path) == long(0):
						counter = counter + 1
						os.remove(full_path)
						print "%s is  empty and removed.." % all_files
					else:
						#Zip the non-empty files and uploaded under FTP 
						continue 
	print "# of empty log files within 5 days: %i" % counter 

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
	'''
	print get_file_creation_time(path_to_file)
	print os.stat(path_to_file).st_size
	print "---"
	print get_file_creation_time("Z:\\\\Program Files\\Actant\\Log\\ActantRmt_20170508.log")
	'''
	print "---"
	#upload_files()
	check_logs("Z:\\\\Program Files\\Actant\\Log")

	#10.64.0.5