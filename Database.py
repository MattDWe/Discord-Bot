import psycopg2
import sys
import logging
import time
import config

class Database:
    def __init__(self):
        logging.basicConfig(filename="logfile.text", level=logging.DEBUG)
        try:
            self.conn = psycopg2.connect(config.postgres_server)
            self.cur = self.conn.cursor()
        except:
            print("Unable to connect to database. Please make sure database is online. Error was logged.")
            logging.exception("Issue connecting to database " + time.asctime())
            sys.exit()
            
    def refreshList(self):
        self.cur.close()
        self.cur = self.conn.cursor()
        self.cur.execute("""SELECT urls FROM websites""")
        urls = self.cur.fetchall()
        return urls
    
    def addImage(self, url):
        self.cur.execute("""INSERT INTO websites(urls) VALUES(\'%s\');""" % (url))
        self.conn.commit()
        
    def deleteImage(self, index):
        urls = self.refreshList()
        url = urls[int(index) - 1][0]
        self.cur.execute("""DELETE FROM websites WHERE urls = \'%s\';""" % (url))
        self.conn.commit()
