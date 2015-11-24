
# Out sourced connection object control

import MySQLdb

class MySQLdbConnection(object):
	def __init__(self):
		return MySQLdb.connect('kmjb.mysql.pythonanywhere-services.com', "kmjb", "passworditcarlow", 'kmjb$MEMBERS_CLUB')