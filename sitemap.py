# -*- coding: utf-8 -*-
import __future__
import sys
if sys.version_info.major == 2:
    import urlparse
else:
    from urllib import parse as urlparse
import requests
from lxml import html
import re
import MySQLdb
import time
try:
    import sys
    if 'threading' in sys.modules:
        del sys.modules['threading']
    from gevent import monkey, pool
    monkey.patch_all()
    gevent_installed = True
except:
    gevent_installed = False


class Crawler:
    def __init__(self, url, id, oformat='xml'):
        self.url = url
        self.id = id
        self.oformat = oformat
        # create lists for urls in queue and visited urls
        self.urls = set([url])
        self.visited = set([url])
        self.exts = ['html','htm', 'php']
        self.allowed_regex = '\.((?!htm)(?!php)\w+)$'
        self.errors = {'404': []}

    def set_exts(self, exts):
        self.exts = exts

    def allow_regex(self, regex=None):
        if regex is not None:
            self.allowed_regex = regex
        else:
            allowed_regex = ''
            for ext in self.exts:
                allowed_regex += '(!{})'.format(ext)
            self.allowed_regex = '\.({}\w+)$'.format(allowed_regex)

    def crawl(self, echo=False, pool_size=1):
        # sys.stdout.write('echo attribute deprecated and will be removed in future')
        self.echo = echo
        self.regex = re.compile(self.allowed_regex)

        print('Parsing pages')
        if gevent_installed and pool_size >= 1:
            self.pool = pool.Pool(pool_size)
            self.pool.spawn(self.parse_gevent)
            self.pool.join()
        else:
            self.pool = [None,] # fixing n_pool exception in self.parse with poolsize > 1 and gevent_installed == False
            while len(self.urls) > 0:
                self.parse()
        if self.oformat == 'txt':
            self.write_txt()
 

    def parse_gevent(self):
        self.parse()
        while len(self.urls) > 0 and not self.pool.full():
            self.pool.spawn(self.parse_gevent)

    def parse(self):
        if self.echo:
            n_visited, n_urls, n_pool = len(self.visited), len(self.urls), len(self.pool)
            status = (
                '{} pages parsed :: {} pages in the queue'.format(n_visited, n_urls),
                '{} pages parsed :: {} parsing processes  :: {} pages in the queue'.format(n_visited, n_pool, n_urls)
            )
            print(status[int(gevent_installed)])

        if not self.urls:
            return
        else:
            url = self.urls.pop()
            try:
                response = requests.get(url)
                # if status code is not 404, then add url in seld.errors dictionary
                if response.status_code != 200:
                    if self.errors.get(str(response.status_code), False):
                        self.errors[str(response.status_code)].extend([url])
                    else:
                        self.errors.update({str(response.status_code): [url]})
                    return

                try:
                    tree = html.fromstring(response.text)
                except ValueError as e:
                    tree = html.fromstring(response.content)
                for link_tag in tree.findall('.//a'):
                    link = link_tag.attrib.get('href', '')
                    newurl = urlparse.urljoin(self.url, link)
                    # print(newurl)
                    if self.is_valid(newurl):
                        self.visited.update([newurl])
                        self.urls.update([newurl])
            except Exception as e:
                print 'error'

    def is_valid(self, url):
        oldurl = url
        if '#' in url:
            url = url[:url.find('#')]
        if url in self.visited or oldurl in self.visited:
            return False
        if self.url not in url:
            return False
        if re.search(self.regex, url):
            return False
        return True


    def write_txt(self):
        DB_IP = "23.229.183.228"
        DB_PORT = 3306
        DB_NAME = "instacandanga"
        DB_USER = "administrador"
        DB_PASSWORD = "BtCFfa~G5n=9"
        try:
            db_connection = MySQLdb.connect(DB_IP, DB_USER, DB_PASSWORD, DB_NAME)
            cursor = db_connection.cursor()
            conectado = True
            url_str = u'{}\n'
            while self.visited:
                query = "INSERT INTO gs_sitios_mapas (id, name, sitios_id, url) VALUES (NULL, '', "+ self.id +", '" + url_str.format(self.visited.pop()) + "');"
                #print query
                try:
                    cursor.execute(query)
                    print '[*] >> insert'
                except (MySQLdb.Error, MySQLdb.Warning) as e:
                    print '[*] >> not insert'
        except MySQLdb.Error as mysql_error:
            print "Error connecting to database: %s" % (str(mysql_error))
        cursor.close()
        db_connection.close()