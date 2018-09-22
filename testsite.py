from sitemap import *
import MySQLdb

DB_IP = "23.229.183.228"
DB_PORT = 3306
DB_NAME = "instacandanga"
DB_USER = "administrador"
DB_PASSWORD = "BtCFfa~G5n=9"

try:
    db_connection = MySQLdb.connect(DB_IP, DB_USER, DB_PASSWORD, DB_NAME)
    cursor = db_connection.cursor()
    conectado = True
    query = "SELECT gs_sitios.id, gs_sitios.url, COUNT(*) as numero FROM `gs_sitios` WHERE  gs_sitios.id=33";
    cursor.execute(query)
    result = cursor.fetchall()
except MySQLdb.Error as mysql_error:
    print "Error connecting to database: %s" % (str(mysql_error))

if len(result) > 0:
    for record in result:
        url = record[1]
        print url
        oformat = 'txt'
        id = str(record[0])
        print id
        crawl = Crawler(url=url, id=id, oformat=oformat)
        crawl.crawl()
else:
    print result

