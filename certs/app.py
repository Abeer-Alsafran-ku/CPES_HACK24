#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Peter Simeth's basic flask pretty youtube downloader (v1.3)
https://github.com/petersimeth/basic-flask-template
© MIT licensed, 2018-2023
"""

from flask import Flask, render_template
import requests
from flask import request, jsonify
DEVELOPMENT_ENV = True

app = Flask(__name__)

app_data = {
    "name": "Peter's Starter Template for a Flask Web App",
    "description": "A basic Flask app using bootstrap for layout",
    "author": "Peter Simeth",
    "html_title": "Peter's Starter Template for a Flask Web App",
    "project_name": "Starter Template",
    "keywords": "flask, webapp, template, basic",
}


@app.route("/",methods = ['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html", app_data=app_data)
    if request.method == 'POST':
        file = request.form.get('file')
        print(file)


if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)