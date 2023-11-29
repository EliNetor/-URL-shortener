import sqlite3 as sq
import random
import logging

logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)

def AddToDB(naamDB, link):
    con = sq.connect(naamDB)
    cur = con.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS URLS (FULLURL TEXT, SHORTURL TEXT)")
    con.commit()

    rand_link = ''
    while True:
        rand_link = GenRandLink()
        result = cur.execute('SELECT FULLURL FROM URLS WHERE SHORTURL = ?', (rand_link,)).fetchone()
        result = cur.execute('SELECT SHORTURL FROM URLS WHERE FULLURL = ?', (link,)).fetchone()
        if not result:
            break
    
    cur.execute("INSERT INTO URLS VALUES (?, ?)", (link, rand_link))
    logging.info(f"Url added: {link}, with short prefix: {rand_link}")
    con.commit()
    con.close()



def GenRandLink():
    r_url = ""
    for x in range(4):
        r_url += chr(random.randint(97,122))
    return r_url