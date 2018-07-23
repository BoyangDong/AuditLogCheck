import os, string

'''
Usage 
mt = MountDrive(r'10.10.18.5\Customer-Archives', 'username', 'password', domain)
mt = MountDrive(r'\\10.10.18.5\Customer-Archives', 'jobrunner', '$#*****', 'sumocap')

mt.drive   =>   'Z:'

mt.unmount()

'''

class MountDrive:
	def __init__(self, path, user=None, pw=None, domain=None):
		self.drive = self.__getDriveLetter__()
		if domain:
			user = domain + "\\" + user
		self.path = self.__mount__(path, user, pw, self.drive)
		
	
	def __getDriveLetter__(self):
		drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
		drives = [drive + ':' for drive in string.ascii_uppercase if drive + ':' not in drives]
		if len(drives) < 1:
			"no available drive letter"
		return drives[-1]
		
	def __mount__(self, path, user, pw, drive):
		'''This method requires unmount in the end'''
		print("***************************************************************")
		print("running:")
		cmd = r"NET USE %s %s %s /USER:%s" %(drive, path, pw, user)		
		print(cmd)
		print(" ")
		os.system(cmd)
		#print d

		print("")
		print("")
		return drive +"\\"
	
	def unmount(self):
		if self.drive:
			cmd = r"NET USE %s /DELETE /YES" %(self.drive)
			print("***************************************************************")
			print("running:")
			print(cmd)
			os.system(cmd)
		print("")
		print("")