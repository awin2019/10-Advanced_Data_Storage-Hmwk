import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

session = Session(engine)

#############################################

@app.route('/')
def home():
    return(
    f"Available routes below:<br/>"
    f"<br/>"
    f"/api/v1.0/precipitation<start>/<end><br/>"
    f"Dates and temperature observations over range of dates<br/>"
    f"Date range must be entered to end of URL as /YYYY-MM-DD/YYYY-MM-DD beginning with the start date<br/>"
    f"<br/>"
    f"/api/v1.0/stations<br/>"
    f"List of stations<br/>"
    f"<br/>"
    f"/api/v1.0/tobs/<start>/<end><br/>"
    f"Temprature observations over range of dates<br/>"
    f"Date range must be entered to end of URL as /YYYY-MM-DD/YYYY-MM-DD beginning with the start date<br/>"
    f"<br/>"
    f"/api/v1.0/<start><br/>"
    f"Minimum temperature, average temperature, and max temperature for a given date<br/>"
    f"Date must be entered to end of URL as /YYYY-MM-DD<br/>"
    f"<br/>"
    f"/api/v1.0/<start>/<end><br/>"
    f"Minimum temperature, average temperature, and max temperature for a given date range<br/>"
    f"Date range must be entered to end of URL as /YYYY-MM-DD/YYYY-MM-DD beginning with the start date<br/>"
    )

@app.route("/api/v1.0/precipitation/<start>/<end>")
def pcrp(start, end):
  prcp_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

  return jsonify(prcp_query)


@app.route("/api/v1.0/stations")
def stations():

  stations_query = session.query(Station.station, Station.name).all()

  station_list=[]
  for sublist in stations_query:
    for item in sublist:
      station_list.append(item)

  return jsonify(station_list)

@app.route("/api/v1.0/tobs/<start>/<end>")
def tobs(start, end):
  tobs_query = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()

  return jsonify(tobs_query)

@app.route("/api/v1.0/<start>")
def start_date(start):

  temp_query = session.query(func.min(Measurement.tobs),\
    func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    
  return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def range_dates(start, end):

  temp_query = session.query(func.min(Measurement.tobs),\
    func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    
  return jsonify(temp_data)

if __name__ == '__main__':
    app.run(debug=True)