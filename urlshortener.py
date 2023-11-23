import functions as f
from flask import Flask, request, redirect, render_template
import classes
import sqlite3

app = Flask(__name__)

my_url = classes.url()

#Displays main page with an imput field to write a link in that should be shortened
@app.route('/', methods=['GET', 'POST'])
def home():
    global my_url
    if request.method == 'POST':
        my_url.link = request.form["URL"]
        f.AddToDB("URL_DATA",my_url.link)
    return render_template('home.html', mijn_link = str(my_url.link))

#Check if the link has a match in the db and redirects to set link that coresponds with it
@app.route('/<short_url>')
def redirect_to_full_url(short_url):
    con = sqlite3.connect("URL_DATA") 
    cur = con.cursor()
    url = cur.execute("SELECT FULLURL FROM URLS WHERE SHORTURL = ?", (short_url,)).fetchone()
    con.close()

    if url:
        full_url = url[0]
        return redirect(full_url)
    else:
        return "Short URL not found", 404