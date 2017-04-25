import MySQLdb
import csv 
from server import server


def get_server_objs(spreadsheet):
	with open (spreadsheet, "r") as f:
		next(f) #skip the header
		reader = csv.reader(f)
		server_id = 0
		for row in reader:
			if len(row[1]) == 0 or not row[2]: # or row[7] == 'Shut': #skip the server that is shut/empty line/log path is N/A, the shut servers are also recorded 
		 		continue
		 	else:
		 		server_id += 1
		 		update_list(row[0], str(row[1]), row[2], row[3], row[4], row[5], str(row[6]), row[7], row[8])
		 		    # Server Name, IP,     Trader, Software,OS,    S/N,DC,Notes,Path 
		print "There are " + str(server_id) + " servers now."

def update_list(server_name, ip_address, trader, software, os, SorN, DC, Notes, path):
	db = MySQLdb.connect(host="localhost",
	                     user="bdong",     
	                     passwd="bdong",  
	                     db="log_report")
	cur = db.cursor()
	try:
		cur.execute("""INSERT INTO server_list VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",[server_name, ip_address, trader, software, os, SorN, DC, Notes, path])
		db.commit()
	except Exception, e:
		db.rollback()
		print str(e)
	finally:
		if db:
			db.close()

def main():
	get_server_objs("Budo_Server_Spreadsheet.csv")

if __name__ == '__main__':
	main()