#import paramiko
import os, sys, traceback, string, time, fnmatch
from datetime import date, timedelta
import win32api
import zipfile



'''
Version 2016.08.31
Contact Eric Wang for any question
at (312)451-7994
or eric.wang@victorynetworks.com



example:
##################################MountDrive########################################
from VictoryUtil import MountDrive
import time
drive = MountDrive('\\\\10.10.18.4\\shr', 'username', 'password', 'domain[optional]')
time.sleep(5)
drive.unmount()

###################################SFTPClient########################################
from VictoryUtil import SFTPClient
ftp = SFTPClient('10.60.3.186', 'eric', 'Eric1987', 22)
ftp.setDestinationPath('CME')
ftp.addFile('D:\\tools\\','README.md')
ftp.start()
ftp.close()


####################################################################################
from VictoryUtil import MountDrive, Archive
#from archive import Archive

drive = MountDrive("\\\\10.60.3.186\\share1", 'eric', 'Eric1987')
arc = Archive(dest = drive.path, name ="test")
arc.addFolder("D:\\Program Files\\Actant\\Data")
arc.write()
drive.unmount()
####################################################################################
Note: linux file seperator is a back slash, and windows file
	  seperator is a forward slash, but in Python, a forward slash needs
	  to be escaped so one single forward slash needs two, like \\ 
	  
	  
	  
'''

class SFTPClient:
	def __init__(self, host, username, password, port=22):
		try:
			transport = paramiko.Transport((host, port))
			transport.connect(username=username, password=password)
			self.sftp = paramiko.SFTPClient.from_transport(transport)
			self.files = []
			self.dest = None
			self.stat = None
		except Exception as e:
			print('*** Caught exception: %s: %s' %(e.__class__, e))
			traceback.print_exc()
			try:
				self.sftp.close()
			except:
				pass
				sys.exit(1)
				
	def addFile(self, path, file):
		if file:
			for f in os.listdir(path):
				if file == f:
					test = os.path.join(path, f)
					print test
					self.files.append(test)
					break
		else:
			print "*** file does not exist <<<"
	
	def setDestinationPath(self, path):
		if path:
			self.dest = path
			self.sftp.chdir(path)
		else:
			print "*** invalid path <<<"
			
	def start(self):
		try:
			for file in self.files:
				f = file.split('\\')[-1]
				print '*** ', file
				self.sftp.put(file,f)
		except Exception as e:
			print('*** Caught exception: %s: %s' %(e.__class__, e))
			traceback.print_exc()
			try:
				self.sftp.close()
			except:
				pass
				sys.exit(1)		
	def close(self):
		self.sftp.close()
				


class MountDrive:
	def __init__(self, path, user=None, pw=None, domain=None):
		self.drive = self.__getDriveLetter__()
		if domain:
			user = domain + "\\" + user
		self.path = self.__mount__(path, user, pw, self.drive)
		
	
	def __getDriveLetter__(self):
		drives = win32api.GetLogicalDriveStrings()
		drives = [drive[0] for drive in drives.split('\000')[:-1]]
		drives = [drive for drive in string.ascii_uppercase if drive not in drives]
		if len(drives) < 1:
			"no available drive letter"
		return drives[-1]+':'
		
	def __mount__(self, path, user, pw, drive):
		'''This method requires unmount in the end'''
		print "***************************************************************"
		print "running:"
		cmd = r"NET USE %s %s %s /USER:%s" %(drive, path, pw, user)		
		print cmd
		print " "
		os.system(cmd)
		#print d

		print ""
		print ""
		return drive +"\\"
	
	def unmount(self):
		if self.drive:
			cmd = r"NET USE %s /DELETE /YES" %(self.drive)
			print "***************************************************************"
			print "running:"
			print cmd
			os.system(cmd)
		print ""
		print ""
		
		
	

class Archive:
	def __init__(self, dest = None, name = None):
		if dest and os.path.exists(dest):
			self.dest = dest
		else:
			self.dest = os.curdir
		print "*** Backup Location: %s" %(os.path.realpath(self.dest))
		
		if name:
			self.arc_name = name + time.strftime("_%Y-%m-%d.zip")
		else:
			self.arc_name = time.strftime("%Y-%m-%d.zip")
			
		self.files = []
		self.exFiles = []
		
	def exclude(self, suff):
		self.exFiles.append(suff)
		
	def addFile(self,file):
		if os.path.isfile(file):
			self.files.append(file)
			print "\n %s added" %(file)
		else:
			print "\n*** file does not exist ***"
			print file
			print ""
		
	def addFolder(self, folder):
		if os.path.exists(folder):
			for root, dirs, files in os.walk(folder):
				print "*** %s ***" %(root)
				for file in files:
					full_name = os.path.join(root, file)
					print file
					self.files.append(full_name)
					
		else:
			print "*** Invalid Path ***"


	def addFilesByDate(self, dir, date = time.strftime("%Y%m%d")):
		print "*** %s ***" %(dir)
		for file in os.listdir(dir):
			if date in file:
				print "%s added" %(file)
				self.files.append(os.path.join(dir,file))
		
	

	def __removeFiles__(self):
		#remove excluded files from writing queue
		print "*** Removing Excluded Files ***"
		
		def remove(suff):
			temp = []
			print " >>> removing: " + suff
			for file in self.files:
				if  fnmatch.fnmatch(file, suff):
					#self.files.remove(file)
					print file
				else:
					temp.append(file)
			return temp

		for suff in self.exFiles:
			self.files = remove(suff)
		print ""	
					
					
	def write(self):
		if self.exFiles:
			self.__removeFiles__()
			
		if self.files:
			zipf = zipfile.ZipFile(os.path.join(self.dest,self.arc_name), 'w', zipfile.ZIP_DEFLATED)
			print "***\nwriting ***"
			for file in self.files:
				zipf.write(file)
			print "    complete"
	
def removeOldFiles(path, dateDelta = None):
	if dateDelta is not None:
		print "*** %s ***" %(path)
		date_to_remove = date.today() - timedelta(days = dateDelta)
		date_to_remove = date_to_remove.strftime("%Y%m%d")
		for file in os.listdir(path):
			if date_to_remove in file:
				print "    removing: %s" %(file)
				os.remove(os.path.join(path,file))













		
if __name__ == "__main__":
    print "\n>>>Testint Imports<<<\n"
		
