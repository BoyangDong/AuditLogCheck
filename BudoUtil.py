import MySQLdb
import smtplib

from server import server 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class send_email:
	def __init__(self, content, sender='test.budo@gmail.com', pw='test.budo1234'):
		self.sender = sender
		self.pw = pw
		self.content = content
		print "Setting up email server..."
		mail = smtplib.SMTP('smtp.gmail.com', 587)
		mail.ehlo()
		mail.starttls()
		mail.login(sender, pw)
		mail.sendmail(sender, 'boyang.dong@budoholdings.com', content)
		#mail.sendmail(sender, 'becky.ali@budoholdings.com', content)
		#mail.sendmail('test.budo@gmail.com', 'mark.cukier@budoholdings.com', content)
		print "Email Sent!"
		mail.close()

class record_in_db:
	def __init__(self, server_name, server_ip, log_name, time_stamp, error_type="EMPTY_FILE", host="localhost", user="bdong", passwd="bdong", db="log_report"):
		self.server_name = server_name
		self.server_ip = server_ip
		self.log_name = log_name

		db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
		cur = db.cursor()
		try:
			cur.execute("""INSERT INTO error_log_info VALUES (%s,%s,%s,%s,%s)""",(server_name, server_ip, log_name, time_stamp,"EMPTY FILE")) #time stamp format: '2017-04-21 13:59:45'
													 			                 #server,          ip,     file_name,time_stamp,                       error_type
			db.commit()
		except Exception, e:
			db.rollback()
			print str(e)
		finally: 
			if db: 
				db.close()
