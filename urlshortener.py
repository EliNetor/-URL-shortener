import functions as f
from flask import Flask, request, redirect, render_template
import classes

app = Flask(__name__)

my_url = classes.url()

@app.route('/', methods=['GET', 'POST'])
def home():
    global my_url
    if request.method == 'POST':
        my_url.link = request.form["URL"]
    return render_template('home.html', mijn_link = str(my_url.link))

