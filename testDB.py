__author__ = 'wei'
import MySQLdb as sql
import MySQLdb.cursors
db = sql.connect(host='cloud.comtnuycjpkv.us-west-2.rds.amazonaws.com', user='weixc1234', passwd='wxc16888', db='innodb', cursorclass=MySQLdb.cursors.DictCursor)
cursor = db.cursor()

