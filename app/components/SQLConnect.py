import MySQLdb

#######################
### CONFIG SETTINGS ###
#######################

host = 'localhost'
password = '6928542m'
user = 'root'
db = 'MEMBERS_CLUB'

def runSQLQuery(_sql, code):
    con = MySQLdb.connect(host, user, password, db)
    cursor = con.cursor()

    if code == 0: # All select queries here
        cursor.execute(_sql)
        data = cursor.fetchall()
        return data
    elif code == 1: #All insert queries here
        try:
            cursor.execute(_sql)
            con.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    cursor.close()
    con.close()
