from flask import Flask, Response
from datetime import datetime
from flask import request, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Environment, select_autoescape
from datetime import datetime
from datetime import timedelta
from flask_http2_push import http2push

import pymssql

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="mssql+pymssql://LineDaq:Ll123456@10.49.0.9/kanban"
db = SQLAlchemy(app)

@app.route("/")

def hello():
    return "Hello Prettl"

@app.route("/time")
def utime():
    return "%s"% int(datetime.today().timestamp())

class CalculatedTurns(db.Model):

    __tablename__ = 'LDAQcalculatedTable'
    id = db.Column( 'id', db.Integer, primary_key=True )
    iP = db.Column('iP', db.String(50), nullable=False)
    line = db.Column('line', db.String(50), nullable=False)
    startTime = db.Column('startTime', db.String(11), nullable=False)
    stopTime = db.Column('stopTime', db.String(11), nullable=False)
    workIntervals = db.Column('workIntervals', db.String(11), nullable=False)
    turns = db.Column('turns', db.String(11), nullable=False)
    userAgent = db.Column('userAgent', db.String(200), nullable=False)
    descrption = db.Column('descrption', db.String(50), nullable=False)

class TimeTurns(db.Model):

    __tablename__ = 'LDAQrealTimeTable'
    id = db.Column( 'id', db.Integer, primary_key=True )
    ip = db.Column('ip', db.String(50), nullable=False)
    line = db.Column('line', db.String(50), nullable=False)
    eventTime = db.Column('eventTime', db.String(11), nullable=False)
    userAgent = db.Column('userAgent', db.String(200), nullable=False)
    event = db.Column('event', db.String(50), nullable=False)

@app.route("/timeCturns")

def select_info():

    db.session.add( CalculatedTurns( iP=request.headers['Host'],
                                     line=request.args['line'],
                                     startTime=request.args['starttime'],
                                     stopTime=request.args['stoptime'],
                                     workIntervals=request.args['workintervals'],
                                     turns=request.args['turns'],
                                     userAgent=request.headers['User-Agent'],
                                     descrption=request.args['descrption'] ) )
    db.session.commit()

    return "OK\n"

@app.route("/timeturns")

def select_info_time():

    db.session.add(TimeTurns(ip=request.headers['Host'],
                                line=request.args['line'],
                                eventTime=request.args['eventTime'],
                                userAgent=request.headers['User-Agent'],
                                event=request.args['event']))
    db.session.commit()

    return "OK\n"

@app.route("/report")
def report():

    timeturns = db.session.query(TimeTurns).order_by(TimeTurns.id.desc()).limit(100)

    return render_template('template.html', title='Peter', timeturns=timeturns, datetime=datetime, int=int, timedelta=timedelta(hours=2))

def dateClock():

    datetime.fromtimestamp()

@app.route("/test")
def test():
    timeturns = db.session.query( TimeTurns ).order_by( TimeTurns.id.desc() ).limit( 2 )
    timeturns2 = db.session.query( TimeTurns ).order_by( TimeTurns.id.desc() ).limit( 8 )
    roundStart = int( timeturns[1].eventTime )
    roundEnd = int( timeturns[0].eventTime )
    roundSpeed = roundEnd - roundStart

    return render_template('setInterval.html', speedRound=roundSpeed, timeturns=timeturns2, datetime=datetime, int=int, timedelta=timedelta(hours=2))

@app.route("/lastcw")
def lastcw():
    timeturns = db.session.query(TimeTurns).order_by(TimeTurns.id.desc()).limit(2)
    response = make_response()
    response.headers['Content-Type'] = 'application/json'

    import json
    obj = {"startTime": timeturns[1].eventTime,
           "startEvent": timeturns[1].event,
           "endTime": timeturns[0].eventTime,
           "endEvent": timeturns[0].event,
           }
    json = json.dumps(obj)
    response.set_data(json)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=61234)