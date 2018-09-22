# from sitemap import *
import requests
import sys
import MySQLdb
import urllib2
import re

# DB_IP = "localhost"
# DB_PORT = 3306
# DB_NAME = "gshop2"
# DB_USER = "root"
# DB_PASSWORD = "SergiO2018#"

DB_IP = "23.229.183.228"
DB_PORT = 3306
DB_NAME = "instacandanga"
DB_USER = "administrador"
DB_PASSWORD = "BtCFfa~G5n=9"

def descargar(pagina):
    try:
        peticion = urllib2.Request(pagina)  
        html = urllib2.urlopen(peticion).read()
        print("[*] Connect OK >>", pagina)
        return 1
    except:
        print('[!] Not Found >>',pagina)
        return 0

try:
    db_connection = MySQLdb.connect(DB_IP, DB_USER, DB_PASSWORD, DB_NAME)
    cursor = db_connection.cursor()
    conectado = True
    query = "SELECT * FROM `gs_sitios` WHERE `url` like '%.cl/' and social = 0 and activo = 0";
    cursor.execute(query)
    result = cursor.fetchall()
except MySQLdb.Error as mysql_error:
    print "Error connecting to database: %s" % (str(mysql_error))

existe = 0
noexiste = 0
if len(result) > 0:
    for record in result:
        print record[5] + '\n'
        if descargar(record[5]):
            existe = existe + 1
            query = "UPDATE gs_sitios SET activo = 1 WHERE id =" + str(record[0])
            try:
                cursor.execute(query)
                print '[*] >> Update \n'
            except (MySQLdb.Error, MySQLdb.Warning) as e:
                print '[*] >> not update \n'
        else:
            noexiste = noexiste + 1        
else:
    print result

