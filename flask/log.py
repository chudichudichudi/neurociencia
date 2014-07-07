from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView

import json

app = Flask(__name__, static_url_path='')
app.config.from_object('config')
db = SQLAlchemy(app)

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column('id', db.Integer, primary_key=True)
    sujeto = db.Column(db.String(60))
    log = db.Column(db.String)

    def __init__(self, sujeto, log):
        self.sujeto = sujeto
        self.log = log



admin = Admin(app)
admin.add_view(ModelView(Log, db.session))

@app.route('/')
def show_all():
    return ""
    
@app.route('/createlog', methods = ['POST'])
def create_log():
    if not request.json or not 'sujeto' in request.json or not 'log' in request.json:
        return "request.json"
    log = Log(request.json['sujeto'], json.dumps(request.json['log']))
    db.session.add(log)
    db.session.commit()
    return "ok", 201

if __name__ == '__main__':
    app.run()