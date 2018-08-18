import requests
from bs4 import BeautifulSoup
import sys
import MySQLdb
import urllib2
import re

recorrido = True
page = 1
linea = []
fila = [] * 2

DB_IP = "23.229.183.228"
DB_PORT = 3306
DB_NAME = "instacandanga"
DB_USER = "administrador"
DB_PASSWORD = "BtCFfa~G5n=9"

conectado = False

def descargar(pagina):
    try:
        peticion = urllib2.Request(pagina)  
        html = urllib2.urlopen(peticion).read()
        print("[*] Descarga OK >>", pagina)
        return 1
    except:
        print('[!] Error descargando',pagina)
        return 0

try:
    db_connection = MySQLdb.connect(DB_IP, DB_USER, DB_PASSWORD, DB_NAME)
    cursor = db_connection.cursor()
    conectado = True
except MySQLdb.Error as mysql_error:
    print "Error connecting to database: %s" % (str(mysql_error))

while recorrido:
    nombre = ""
    url = ""
    activo = False
    print 'GrowShopId: '+ str(page)
    req = requests.get('https://guiadegrows.cl/grows/search/online?page='+str(page))
    html = BeautifulSoup(req.text, "html.parser")
    error = html.find_all('div', {'class': 'alert alert-warning text-center'})
    if error:
        recorrido = False
    else:
        entradas = html.find_all('div', {'class': 'grow-item'})
        for en in entradas:
            cab = en.find_all('div', {'class': 'grows-normales'})
            if cab:
                for cabe in cab:
                    c = cabe.find_all('a')
                    for c_tmp in c:
                        nombre = c_tmp.text.encode('utf-8')
            else:
                cab2 = en.find_all('div', {'class': 'grows'})
                if cab:
                    for cabe in cab:
                        c = cabe.find_all('a')
                        for c_tmp in c:
                            nombre = c_tmp.text.encode('utf-8')
            lis = en.find_all('div', {'class': 'site-grow'})
            for link in lis:
                a = link.find_all('a',href=True)
                for a_tmp in a:
                    url = a_tmp['href'].encode('utf-8')
            # activo = descargar(url)
            activo = 0
            if conectado:
                query = "INSERT INTO gs_sitios (id,origen, name, description, address, url, social,activo) VALUES (NULL, 2,'"+ nombre +"', '', '', '"+ url +"',0," + str(activo) +");"
                print url
                try:
                    cursor.execute(query)
                    print '[*] >> insert'
                except (MySQLdb.Error, MySQLdb.Warning) as e:
                    print '[*] >> not insert'
            print '\n'
            #linea[page] = fila
        page = page + 1
        recorrido = True
cursor.close()
db_connection.close()
