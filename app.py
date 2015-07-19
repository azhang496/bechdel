import os
from flask import Flask, render_template, request, redirect, url_for, session
from google import search

import bechdel_test as bechdel

app = Flask(__name__)

app.config["DEBUG"] = True # delete this line before deploying!

def bechdel_test(movie):
    for url in search("%s screenplay pdf" % movie, stop=5):
        if url.endswith('.pdf'):
            try:
                pdf = bechdel.convert_pdf(url, 'screenplay.pdf')
            except Exception as e:
                return [-1, None]
            list = bechdel.find_names(pdf)
            result = bechdel.bechdel_test(list)
            if result == 0:
                return [result, bechdel.global_dialog(list)]
            else:
                print "failed, None"
                return [result, None]
    print "didn't find screenplay"
    return [-1, None]

@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/', methods=['POST'])
def homepage_post():
    movie = request.form['movie']
    bechdel_result = bechdel_test(movie)
    session['movie'] = movie
    session['pass_test'] = bechdel_result[0]
    session['lines'] = bechdel_result[1]
    return redirect(url_for('result'))

@app.route('/result')
def result():
    movie = session['movie']
    pass_test = session['pass_test']
    lines = session['lines']
    return render_template("result.html", result=pass_test, movie=movie, lines=lines)

@app.route('/what-the-hechdel')
def about_bechdel():
    return render_template("what-the-hechdel.html")

@app.route('/about')
def about_us():
    return render_template("about.html")

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run(host="0.0.0.0")




