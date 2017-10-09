import MySQLdb
import smtplib
import paramiko

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
	def __init__(self, server_name, server_ip, log_name, time_stamp, error_type="EMPTY_FILE", host="172.30.80.25", user="root", passwd="Password1", db="budo_firm"):
		self.server_name = server_name
		self.server_ip = server_ip
		self.log_name = log_name

		db = MySQLdb.connect(host=host, port=3306, user=user, passwd=passwd, db=db)
		cur = db.cursor()
		try:
			cur.execute("""INSERT INTO empty_log_info VALUES (%s,%s,%s,%s,%s)""",(server_name, server_ip, log_name, time_stamp,"EMPTY FILE")) #time stamp format: '2017-04-21 13:59:45'
			db.commit()
		except Exception, e:
			db.rollback()
			print str(e)
		finally: 
			if db: 
				db.close()


class upload_to_EDFMan:
	def __init__(self, folder_uploaded, path_out, username='BudoAudit', password='q&4r)1bx*Y'):
		'''Upload the zipped log files through sftp to edfman
		'''
		#path_out = ''.join(['\\weekly_test\\', current_date, '\\', zipped_folder])
		try:
			print "connection establishing..."
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			trans = paramiko.Transport(("ftpc.edfmancapital.com", 2222))
			trans.connect(username = username, password = password)
			sftp = paramiko.SFTPClient.from_transport(trans)
			print "connected!"
			#sftp.put(path_to_file, outgoing_path)
			sftp.put(folder_uploaded, path_out)
			print "Folder hase been uploaded!"
		except Exception, e:
			print str(e)
		finally: 
			trans.close() 
			