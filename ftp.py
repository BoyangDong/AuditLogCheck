import pysftp as sftp
import paramiko 
import os
import time
import zipfile
from time import gmtime, strftime

#Another pair of credentials 
#password = "Wonderwall$AtlantisSlumberAdvisory"
#username = "BUDO_ATTLAN"
password = 'q&4r)1bx*Y'
username = 'BudoAudit'

now = time.time() #current time in milliseconds
current_date = strftime("%m-%d-%Y", gmtime())


def check_logs(path_to_folder, server_name, topdown=False):
	"""This function walks through the files under server log folder
	check sequentially, remove the empty logs while retain the recent 5-day ones 
	and zip them together into a folder, then invoke the upload ftp funtion
	"""
	print "checking logs..."
	zipped_folder_name = ''.join(['_'.join([server_name, current_date]), '.zip'])
	myZipFile = zipfile.ZipFile(zipped_folder_name, "w")
	counter = 0
	for r, d, f in os.walk(path_to_folder):
		for all_files in f:
			full_path = os.path.join(r, all_files)
			date_file = os.path.getmtime(full_path)
			if all_files.endswith(".log") or all_files.endswith(".txt"):
				# Check the recent five days, starting from Sunday 8pm to Friday 8pm 
				if now - date_file <= 7200: # 7200 for a cheap test, change back to 43200 for weekly-check					
					if os.path.getsize(full_path) == long(0):
						counter = counter + 1
						os.remove(full_path)
						print "%s is  empty and removed.." % all_files
					else:
						#Zip the non-empty files and uploaded under FTP 
						myZipFile.write(full_path, ''.join(["\\", all_files]), zipfile.ZIP_DEFLATED)						
	print "# of empty log files within 5 days: %s" % counter 
	upload_files(zipped_folder_name)


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


def get_file_creation_time(file_path):
	#This function is currently unused, it provides a formatted time stamp format given a absolute path of the file
    t = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S") # strftime can disregard the millisecond
	

if __name__ == "__main__":
	#main function for module test 
	check_logs("Z:\\\\Program Files\\Actant\\Log", "BUDO-TEST-1")
	#10.64.0.5