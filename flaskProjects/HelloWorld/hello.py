#!/usr/bin/python

from flask import Flask
from flask import render_template
from datetime import datetime
from flask import request


app = Flask(__name__)

@app.route('/')
@app.route('/test')
def hello_world():
   now =  datetime.now()
   rule = request.url_rule
   return render_template('hello.html', name=now ,path=str (rule) 
)
   
