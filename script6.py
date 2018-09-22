import requests
from bs4 import BeautifulSoup
import sys
import MySQLdb
import urllib2
import re
import json
import time

DB_IP = "23.229.183.228"
DB_PORT = 3306
DB_NAME = "instacandanga"
DB_USER = "administrador"
DB_PASSWORD = "BtCFfa~G5n=9"

def update_pct(w_str):
    w_str = str(w_str)
    sys.stdout.write("\b" * len(w_str))
    sys.stdout.write(" " * len(w_str))
    sys.stdout.write("\b" * len(w_str))
    sys.stdout.write(w_str)
    sys.stdout.flush()

with open('sitios.1.json', 'r') as f:
    distros_dict = json.load(f)
print "==============================================================="
print "Leyendo Json..."

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
print "==============================================================="
print "iniciando analisis de la URL:"
for distro in distros_dict:
    now2 = time.time()
    print distro['url']
    pagina = distro['url']
    peticion = urllib2.Request(pagina)  
    html = urllib2.urlopen(peticion).read()
    bhtml = BeautifulSoup(html, "html.parser")
    print "==============================================================="
    print "Obteniendo enlances de las categorias de los productos..."
    list_categorias = bhtml.find_all(distro['esquema']['listaCategorias']['bloque']['elemento'],\
    {distro['esquema']['listaCategorias']['bloque']['atributo']:distro['esquema']['listaCategorias']['bloque']['valor'] })
    numero = 0
    numero1 = 0
    print "==============================================================="
    print "Obteniendo productos..."
    #print list_categorias
    for lista in list_categorias:
        categorias = lista.find_all(distro['esquema']['listaCategorias']['secciones']['elemento'])
        for categoria in categorias:
            numero = numero + 1
            # update_pct("Leyendo Categorias {n}".format(n=str(numero)))
            link = categoria.find(distro['esquema']['listaCategorias']['enlaces']['elemento'],\
            {distro['esquema']['listaCategorias']['enlaces']['atributo']:distro['esquema']['listaCategorias']['enlaces']['valor']})
            enlaces =  link.get(distro['esquema']['listaCategorias']['enlaces']['link'])
            #print enlaces
            # print "==============================================================="
            # print enlaces
            # print "==============================================================="
            # print "Obteniendo lista de productos"
            pagina_interna = enlaces
            peticion_interna = urllib2.Request(pagina_interna)  
            html_interno = urllib2.urlopen(peticion_interna).read()
            bhtml_interno = BeautifulSoup(html_interno, "html.parser")
            list_product = bhtml_interno.find_all(distro['esquema']['listaProductos']['bloque']['elemento'],\
            {distro['esquema']['listaProductos']['bloque']['atributo']:distro['esquema']['listaProductos']['bloque']['valor'] })
            
            for lista in list_product:
                prod = lista.find_all(distro['esquema']['listaProductos']['secciones']['elemento'])
                for productos in prod:
                    numero1 = numero1 + 1
                    # update_pct("Leyendo productos {n}".format(n=str(numero1)))
                    link_interno = productos.find(distro['esquema']['listaProductos']['enlaces']['elemento'],\
                    {distro['esquema']['listaProductos']['enlaces']['atributo']:distro['esquema']['listaProductos']['enlaces']['valor']})
                    pagina_producto =  link_interno.get(distro['esquema']['listaProductos']['enlaces']['link'])
                    #obteniendo detalles del producto.
                    peticion_detalle = urllib2.Request(pagina_producto)  
                    html_detalle = urllib2.urlopen(peticion_detalle).read()
                    bhtml_detalle = BeautifulSoup(html_detalle, "html.parser")
                    detail_product = bhtml_detalle.find('div', {'id': 'center_column'})

                    cabecera = detail_product.find('div',{'class':'product-title'})
                    titulo = detail_product.select('div.product-title h1')
                    marca = detail_product.select('img.imglog')
                    # referencia = cabecera.find('p',{'id':'product_reference'})
                    codigo = detail_product.select('p#product_reference span.editable')
                    # condicion = cabecera.select('p',{'id':'product_condition'})
                    cond = detail_product.select('p#product_condition span.editable')
                    #descripcion
                    # descripcion_corta = detail_product.find('div',{'id':'short_description_block'})
                    descripcion_short = detail_product.select('div#short_description_block span')
                    #cantidad
                    disponibilidad = detail_product.select('span#quantityAvailable')
                    #precio
                    precio = detail_product.select('span#our_price_display')
                    # precio_old = detail_product.find('span',{'id':'old_price_display'})
                    precio_old_span = detail_product.select('span#old_price_display span.price')
                    precio_descuento = detail_product.select('span#reduction_amount_display')
                    #categogiras
                    list_categorias = detail_product.select('ul.iqitproducttags li a')
                    if list_categorias:
                        li_categorias = list_categorias

                    #imagenes
                    list_images = detail_product.select('ul#thumbs_list_frame li a')
                    if list_images:
                        images = list_images
                    
                    #impresion
                    titulo_camp = ""
                    if titulo:
                        # print 'Titulo: ' + titulo.text
                        titulo_camp = titulo[0].text
                        print titulo_camp
                    marca_camp = ""
                    if marca:
                        # print '---- Marca: ' + marca.get('alt')
                        marca_camp = marca[0].get('alt')
                        print marca_camp
                    codigo_camp = ""
                    if codigo:
                        # print '---- Codigo: ' + codigo.text
                        codigo_camp = codigo[0].text
                        print codigo_camp
                    cond_camp =""
                    if cond:
                        # print '---- Condicion: ' + cond.text
                        cond_camp = cond[0].text
                        print cond_camp
                    descripcion_short_camp = ""
                    if descripcion_short:
                        # print '---- Descripcion Corta: ' + descripcion_short.text
                        descripcion_short_camp = descripcion_short[0].text
                        print descripcion_short_camp
                    disponibilidad_camp =""
                    if disponibilidad:
                        # print '---- Disponibilidad: ' + disponibilidad.text
                        disponibilidad_camp = disponibilidad[0].text
                        print disponibilidad_camp
                    precio_camp = ""
                    if precio:
                        # print '---- Precio: ' + precio.text
                        precio_camp = precio[0].text
                        print precio_camp
                    precio_old_span_camp = ""
                    if precio_old_span:
                        # print '---- Precio Viejo: ' + precio_old_span.text
                        precio_old_span_camp = precio_old_span[0].text
                        print precio_old_span_camp
                    precio_descuento_camp = ""
                    if precio_descuento:
                        # print '---- Precio Descuento: ' + precio_descuento.text
                        precio_descuento_camp = precio_descuento[0].text
                        print precio_descuento_camp
                    categorias_camp = "";
                    if li_categorias:
                        # print '---- Categorias:'
                        for lis in li_categorias: 
                            if lis:
                                cat = lis.text
                                if cat:
                                    # print '---- ----' + cat.text
                                    categorias_camp = categorias_camp + cat + ', '
                        print categorias_camp
                    imagenes_camp = "";
                    if images:
                        ni = 0
                        # print '---- Categorias:'
                        for img in images: 
                            ni = ni + 1
                            if img:
                                i = img.get('href')
                                if i:
                                    # print '---- ----' + i.get('href')
                                    # archivoDescargar = i.get('href')
                                    # archivoGuardar = codigo_camp + "_"+  str(ni) +".jpg"
                                    # now = time.time()
                                    # descarga = urllib2.urlopen(archivoDescargar)
                                    # ficheroGuardar=file(archivoGuardar,"w")
                                    # ficheroGuardar.write(descarga.read())
                                    # ficheroGuardar.close()
                                    # elapsed = time.time() - now
                                    # print "Descargado el archivo: %s en %0.3fs" % (archivoDescargar,elapsed)
                                    imagenes_camp = imagenes_camp + i + ', '
                        print imagenes_camp
                    
                    #sql = "INSERT INTO `gs_productos` (`id`, `url`, `titulo`, `marca`, `codigo`, `condicion`, `descripcion`, `disponibilidad`, `precio`, `precio_viejo`, `descuento`, `categorias`, `imagenes`) \
        #VALUES (NULL, '"+ pagina_producto +"', '"+ titulo_camp +"', '"+ marca_camp +"', '"+ codigo_camp +"', '"+ cond_camp +"', '"+ descripcion_short_camp +"', '"+ disponibilidad_camp +"', '"+ precio_camp +"', '"+ precio_old_span_camp +"', '"+ precio_descuento_camp +"', '"+ categorias_camp +"', '"+ imagenes_camp +"');"
                    # print sql
                    # try:
                    #     db_connection = MySQLdb.connect(DB_IP, DB_USER, DB_PASSWORD, DB_NAME)
                    #     cursor = db_connection.cursor()
                    #     conectado = True
                    # except MySQLdb.Error as mysql_error:
                    #     print "Error connecting to database: %s" % (str(mysql_error))
                    
                    # try:
                    #     cursor.execute(sql)
                    #     print '[*] >> insert'
                    # except (MySQLdb.Error, MySQLdb.Warning) as e:
                    #     print '[*] >> not insert'
                    # cursor.close()
                    # db_connection.close()
                    # print pagina_producto  
    elapsed2 = time.time() - now2
    print "==============================================================="
    print "Numero de Categorias: " + str(numero)
    print "Numero de Productos: " + str(numero1) 
    print "tiempo de consulta: " + str(elapsed2)

