import requests
from bs4 import BeautifulSoup
import sys


def update_pct(w_str):
    w_str = str(w_str)
    sys.stdout.write("\b" * len(w_str))
    sys.stdout.write(" " * len(w_str))
    sys.stdout.write("\b" * len(w_str))
    sys.stdout.write(w_str)
    sys.stdout.flush()
    
class Sitios:
    pass

req = requests.get('https://guiadegrows.cl/')
html = BeautifulSoup(req.text, "html.parser")
entradas = html.find_all('div', {'class': 'content-global footer'})

pct = 0
for en in entradas:
    pct = pct + 1
    update_pct("Leyendo paginas {n}".format(n=str(pct)))
    lis = en.find_all('a')
sits = [[]]
pct = 0

print '\n'
for li in lis:
    url = 'https://guiadegrows.cl'+li.get('href')
    req_temporal = requests.get(url)
    html_temporal = BeautifulSoup(req_temporal.text, "html.parser")
    sitios = html_temporal.find_all('div', {'class': 'grow-item'})
    for sit in sitios:
        update_pct("Leyendo contenidos {n}".format(n=str(pct)))
        cabecera = sit.find_all('a')
        detalle = sit.find_all('div', {'class': 'detalles-grows'})
        pct = pct + 1
        sits.append([])
        for hiper in cabecera:
            if hiper.text =="":
                vacio = ""
            else:
                sits[pct].append(hiper.text.replace('\n', ''))
        #    print hiper.text
        for deta in detalle:
            deta1 = deta.find_all('div', {'class': 'dron-grow'})
            deta2 = deta.find_all('div', {'class': 'telefono-grow'})
            deta3 = deta.find_all('div', {'class': 'site-grow'})
            for detal in deta1:
                if detal.text == "":
                    vacio = ""
                else:
                    sits[pct].append(detal.text.replace('            ', ''))
            for detal in deta2:
                if detal.text == "":
                    vacio = ""
                else:
                    sits[pct].append(detal.text.replace('\n', ''))
            for detal in deta3:
                if detal.text == "":
                    vacio = ""
                else:
                    sits[pct].append(detal.text.replace('\n', ''))

print '\n'
print '=========== imprimiento resultados ================'            

#print sits

for sitios1 in sits:
    #print '\n'
    #print sitios1
    print '-------------------------------------------------------'
    for ist in sitios1:
        print ist
    print '\n'