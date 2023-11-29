import functions as f
from flask import Flask, request, redirect, render_template, url_for
import classes
import sqlite3
from collections import OrderedDict
import logging

logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)

app = Flask(__name__)

my_url = classes.url()

#function that caches the last 500 urls that are looked up, oldest first newest get added at the end
def cache(og_func):

    urls = OrderedDict()

    def wrapper(url):
        if url not in urls:
            urls[url] = None
        else:
            urls.move_to_end(url, last=True)
        
        if len(urls) > 500:
            urls.popitem(last=False)
            
        return urls
    return wrapper

#Displays main page with an imput field to write a link in that should be shortened
@app.route('/', methods=['GET', 'POST'])
def home():
    global my_url
    if request.method == 'POST':
        my_url.link = request.form["URL"]
        f.AddToDB("URL_DATA",my_url.link)

    con = sqlite3.connect("URL_DATA") 
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS URLS (`FULLURL`, `SHORTURL`)")
    cur.execute("SELECT * FROM URLS")
    data = cur.fetchall()

    css_url = url_for('static', filename='style.css')

    return render_template('home.html', data=data, css_url=css_url)

#Check if the link has a match in the db and redirects to set link that coresponds with it
@app.route('/<short_url>')
def redirect_to_full_url(short_url):
    con = sqlite3.connect("URL_DATA") 
    cur = con.cursor()
    url = cur.execute("SELECT FULLURL FROM URLS WHERE SHORTURL = ?", (short_url,)).fetchone()
    con.close()

    if url:
        full_url = url[0]
        logging.info(f"Url redirected: {full_url}")
        add_to_cache(full_url)
        return redirect(full_url)
    else:
        return "Short URL not found", 404

@cache
def add_to_cache(url):
    pass