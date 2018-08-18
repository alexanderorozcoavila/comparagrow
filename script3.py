from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time
from datetime import datetime
import urllib2
import requests
# import psycopg2
import json
import sys
import MySQLdb

#from dicttoxml import dicttoxml
import xml.etree.ElementTree as ET
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException

url = "https://guiaweed.com/mapa"
DB_IP = "23.229.183.228"
DB_PORT = 3306
DB_NAME = "instacandanga"
DB_USER = "administrador"
DB_PASSWORD = "BtCFfa~G5n=9"


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

driver = webdriver.PhantomJS()
driver.implicitly_wait(30)
try:
    driver.get(url)
except (NoSuchElementException, ElementNotVisibleException):
    driver.close()
    sys.exit()

paginas = 1
recorrido = True

while recorrido:  
    print 'GrowShopId: '+ str(paginas)
    scr = driver.execute_script("getContent('lugar',"+ str(paginas) +");")
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pagina = soup.find_all('div', {'class': 'btn-group btn-group-justified'})
    # cabecera = soup.find_all('div', {'class': 'btn-group btn-group-justified'})
    for en in pagina:
        if en:
            a = en.find_all('a')
            for a_tmp in a:
                url = a_tmp['href'].encode('utf-8')
                if url <> 'javascript:void(0)':
                    # activo = descargar(url)
                    print url
                    activo = 0
                    query = "INSERT INTO gs_sitios (id, name, description, address, url, activo) VALUES (NULL, '', '', '', '"+ url +"'," + str(activo) +");"
                    # print query
                    try:
                        cursor.execute(query)
                        print '[*] >> insert'
                    except (MySQLdb.Error, MySQLdb.Warning) as e:
                        print '[*] >> not insert'

                    
        else:
            print "error"
    paginas = paginas + 1
    if paginas == 1600:
        recorrido = False

driver.close()
cursor.close()
db_connection.close()
