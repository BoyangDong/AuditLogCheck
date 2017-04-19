
class server:

	def __init__(self, server_name, ip, trader, software, os, uid, hasVisited, log_path):
		self.server_name = server_name
		self.ip = ip
		self.trader = trader
		self.software = software
		self.os = os
		self.uid = uid #user defined id, starting from 1 to n
		self.hasVisited = False
		self.log_path = log_path 
		self.messages = {None: 'N/A', True: 'yes', False: 'no'}


	def print_all(self):
		print "Server Name: %s, ip: %s, checked? %s" % (self.server_name, self.ip, self.messages[self.hasVisited])		

	def __str__(self):
		self.print_all()

	
	def __repr__(self):
		self.print_all()

	def __lt__(self,other):
		pass
	
			