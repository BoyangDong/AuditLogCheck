# -*- coding: utf-8 -*-  

import os
import datetime as dt

folders = []

rival_servers = {
	"BUDO-DC3-RIVAL-1"	: ['10.133.64.71',	'Rod Valeroso'],
	"BUDO-DC3-DC3-2"	: ['10.133.64.72',	'Duncan Robinson']
	#"Budo-350-DEV-1"	: ['10.62.0.9',		'Ted Hilk']
}

x = os.listdir('\\\\172.30.80.25\\Upload\\Rival\\')

current_day = dt.datetime.now() 

folders.append("%s_rival" % current_day.strftime('%Y%m%d'))

for i in xrange(1,5):
	yesterday = current_day - dt.timedelta(days=1)
	date = yesterday.strftime('%Y%m%d')
	rival_folder_name = "%s_rival" % date
	folders.append(rival_folder_name)
	current_day = yesterday


print folders