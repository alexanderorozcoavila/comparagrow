import requests
from bs4 import BeautifulSoup
import sys
import MySQLdb
import urllib2
import re
import json

with open('sitios.json', 'r') as f:
    distros_dict = json.load(f)


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
for distro in distros_dict:
    pagina = distro['url']
    peticion = urllib2.Request(pagina)  
    html = urllib2.urlopen(peticion).read()
    bhtml = BeautifulSoup(html, "html.parser")
    list_product = bhtml.find_all(distro['esquema']['listaProductos']['bloque']['elemento'],\
    {distro['esquema']['listaProductos']['bloque']['atributo']:distro['esquema']['listaProductos']['bloque']['valor'] })
    numero = 0
    for lista in list_product:
        prod = lista.find_all(distro['esquema']['listaProductos']['secciones']['elemento'])
        for productos in prod:
            numero = numero + 1
            link = productos.find(distro['esquema']['listaProductos']['enlaces']['elemento'],\
            {distro['esquema']['listaProductos']['enlaces']['atributo']:distro['esquema']['listaProductos']['enlaces']['valor']})
            pagina =  link.get(distro['esquema']['listaProductos']['enlaces']['link'])
            print pagina
    print distro['url']
    print numero

    # print(distro['id'])
    # print(distro['esquema']['listaProductos']['bloque']['elemento'])