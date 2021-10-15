import mysql.connector as mariadb

class MyDB(object):

    def __init__(self):
        self._db_connection = mariadb.connect(host='192.168.1.20', port=3307 ,user='application', password='8*vcjn.nwACH+m6f', database='dataset')
        self._db_cur = self._db_connection.cursor()

    def query(self, query):
        return self._db_cur.execute(query)

    def fetchone(self):
    	return self._db_cur.fetchone()

    def fetchall(self):
    	return self._db_cur.fetchall()

    def __del__(self):
        self._db_connection.commit()
        self._db_connection.close()



if __name__ == '__main__':
	tt = MyDB()
	tt.query('SELECT count(name) from PICTURE ;')
	print( tt.fetchone() )

