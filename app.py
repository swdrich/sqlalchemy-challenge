### Import dependencies ###
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#############################

#############################
### Set up database ###
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
##############################

##############################
### Create an app, being sure to pass __name__ ###
app = Flask(__name__)
##############################

##############################
### Flask routes ###

# Define what to do when a user hits the index route
@app.route("/")
def index():
    return (f"Welcome to the 'Index' page!<br/>"
            f"Available routes:<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/start-date/end-date</br>"
            f"&nbsp&nbsp&nbsp&nbsp When entering start and end dates for variable API, please use 'YYYY-mm-dd' format.")


# Define what to do when a user hits the /stations route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
            
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)
   
            
# Define what to do when a user hits the /tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    #Work out dates
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    session.close
    recent_date = recent_date[0]
    print(recent_date)

    recent_date = dt.datetime.strptime(recent_date, '%Y-%m-%d')
    last_year = recent_date.date() - dt.timedelta(days=365)
    print(last_year)

    # Work out station counts
    max_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    session.close
    max_station = max_station[0][0]
    print(max_station)

    #Query temperature observations
    results = session.query(Measurement.tobs).filter(Measurement.date >= last_year).filter(Measurement.station == max_station).all()

    temp_obs = list(np.ravel(results))
    
    return jsonify(temp_obs)
    
   
# Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Work out dates
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_date = recent_date[0]
    print(recent_date)

    recent_date = dt.datetime.strptime(recent_date, '%Y-%m-%d')
    last_year = recent_date.date() - dt.timedelta(days=365)
    print(last_year)

    # Perform query
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()
    session.close()

    all_precip = []
    for date, prcp in results:
        precip_dict = {}   
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)    
    
    return jsonify(all_precip) 


# Define what to do when a user hits the /start/end route
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def variable_date(start=None, end='2017-08-23'):
    session = Session(engine)
    sel = [func.min(Measurement.tobs),
           func.max(Measurement.tobs),
           func.avg(Measurement.tobs)]
    results = session.query(*sel).filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    session.close()
    
    temp_dict = {"Min Temp": results[0][0],
                 "Max Temp": results[0][1],
                 "Avg Temp": results[0][2]}

    print(start, end)
    return jsonify(temp_dict)
    
##############################

if __name__ == "__main__":
    app.run(debug=True)