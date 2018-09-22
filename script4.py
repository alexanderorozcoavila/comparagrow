import requests
from bs4 import BeautifulSoup
import sys
import MySQLdb
import urllib2
import re

DB_IP = "23.229.183.228"
DB_PORT = 3306
DB_NAME = "instacandanga"
DB_USER = "administrador"
DB_PASSWORD = "BtCFfa~G5n=9"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
pagina = "https://www.lajuana.cl/promociones-en-la-juana-growshop?n=159"
peticion = urllib2.Request(pagina)  
html = urllib2.urlopen(peticion).read()
bhtml = BeautifulSoup(html, "html.parser")
list_product = bhtml.find_all('ul', {'class': 'product_list grid row'})
numero = 0
for lista in list_product:
    prod = lista.find_all('li')
    for productos in prod:
        numero = numero + 1
        link = productos.find('a',{'class':'product_img_link'})
        pagina =  link.get('href')
        peticion = urllib2.Request(pagina)  
        html = urllib2.urlopen(peticion).read()
        bhtml = BeautifulSoup(html, "html.parser")
        detail_product = bhtml.find('div', {'id': 'center_column'})
        #Cabecera
        cabecera = detail_product.find('div',{'class':'product-title'})
        titulo = cabecera.find('h1')
        
        marca = cabecera.find('img',{'class':'imglog'})
        referencia = cabecera.find('p',{'id':'product_reference'})
        codigo = referencia.find('span',{'class':'editable'})
        condicion = cabecera.find('p',{'id':'product_condition'})
        cond = condicion.find('span',{'class':'editable'})
        #descripcion
        descripcion_corta = detail_product.find('div',{'id':'short_description_block'})
        descripcion_short = descripcion_corta.find('span')
        #cantidad
        disponibilidad = detail_product.find('span',{'id':'quantityAvailable'})
        #precio
        precio = detail_product.find('span',{'id':'our_price_display','class':'price'})
        precio_old = detail_product.find('span',{'id':'old_price_display'})
        precio_old_span = precio_old.find('span',{'class':'price'})
        precio_descuento = detail_product.find('span',{'id':'reduction_amount_display'})
        #categogiras
        list_categorias = detail_product.find('ul',{'class':'iqitproducttags'})
        if list_categorias:
            li_categorias = list_categorias.find_all('li')

        #imagenes
        list_images = detail_product.find('ul',{'id':'thumbs_list_frame'})
        if list_images:
            images = list_images.find_all('li')
        
        #impresion
        titulo_camp = ""
        if titulo:
            print 'Titulo: ' + titulo.text
            titulo_camp = titulo.text
        marca_camp = ""
        if marca:
            print '---- Marca: ' + marca.get('alt')
            marca_camp = marca.get('alt')
        codigo_camp = ""
        if codigo:
            print '---- Codigo: ' + codigo.text
            codigo_camp = codigo.text
        cond_camp =""
        if cond:
            print '---- Condicion: ' + cond.text
            cond_camp = ""
        descripcion_short_camp = ""
        if descripcion_short:
            print '---- Descripcion Corta: ' + descripcion_short.text
            descripcion_short_camp = descripcion_short.text
        disponibilidad_camp =""
        if disponibilidad:
            print '---- Disponibilidad: ' + disponibilidad.text
            disponibilidad_camp = disponibilidad.text
        precio_camp = ""
        if precio:
            print '---- Precio: ' + precio.text
            precio_camp = precio.text
        precio_old_span_camp = ""
        if precio_old_span:
            print '---- Precio Viejo: ' + precio_old_span.text
            precio_old_span_camp = precio_old_span.text
        precio_descuento_camp = ""
        if precio_descuento:
            print '---- Precio Descuento: ' + precio_descuento.text
            precio_descuento_camp = precio_descuento.text
        categorias_camp = "";
        if li_categorias:
            print '---- Categorias:'
            for lis in li_categorias: 
                if lis:
                    cat = lis.find('a')
                    if cat:
                        print '---- ----' + cat.text
                        categorias_camp = categorias_camp + cat.text + ', '
        imagenes_camp = "";
        if images:
            print '---- Categorias:'
            for img in images: 
                if img:
                    i = img.find('a')
                    if i:
                        print '---- ----' + i.get('href')
                        imagenes_camp = imagenes_camp + i.get('href') + ', '
        
        sql = "INSERT INTO `gs_productos` (`id`, `url`, `titulo`, `marca`, `codigo`, `condicion`, `descripcion`, `disponibilidad`, `precio`, `precio_viejo`, `descuento`, `categorias`, `imagenes`) \
        VALUES (NULL, '"+ pagina +"', '"+ titulo_camp +"', '"+ marca_camp +"', '"+ codigo_camp +"', '"+ cond_camp +"', '"+ descripcion_short_camp +"', '"+ disponibilidad_camp +"', '"+ precio_camp +"', '"+ precio_old_span_camp +"', '"+ precio_descuento_camp +"', '"+ categorias_camp +"', '"+ imagenes_camp +"');"
        print sql
        try:
            db_connection = MySQLdb.connect(DB_IP, DB_USER, DB_PASSWORD, DB_NAME)
            cursor = db_connection.cursor()
            conectado = True
        except MySQLdb.Error as mysql_error:
            print "Error connecting to database: %s" % (str(mysql_error))
        
        try:
            cursor.execute(sql)
            print '[*] >> insert'
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print '[*] >> not insert'
        cursor.close()
        db_connection.close()
        print "\n"

print numero