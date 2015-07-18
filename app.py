import os
from flask import Flask, render_template, request, redirect, url_for, session
from google import search

import bechdel_test as bechdel

app = Flask(__name__)

app.config["DEBUG"] = True # delete this line before deploying!

def bechdel_test(movie):
    for url in search("%s screenplay pdf" % movie, stop=5):
        if url.endswith('.pdf'):
            pdf = bechdel.convert_pdf(url, 'screenplay.pdf')
            list = bechdel.find_names(pdf)
            return bechdel.bechdel_test(list)
    print "didn't find screenplay"
    return -1

@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/', methods=['POST'])
def homepage_post():
    movie = request.form['movie']
    bechdel_result = bechdel_test(movie)
    session['movie'] = movie
    session['bechdel_result'] = bechdel_result
    return redirect(url_for('result'))

@app.route('/result')
def result():
    bechdel_result = session['bechdel_result']
    print "bechdel_result: %d" % bechdel_result
    movie = session['movie']
    print movie
    return render_template("result.html", result=bechdel_result, movie=movie)

@app.route('/what-the-hechdel')
def about_bechdel():
    return render_template("what-the-hechdel.html")

@app.route('/about')
def about_us():
    return render_template("about.html")

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run(host="0.0.0.0")




