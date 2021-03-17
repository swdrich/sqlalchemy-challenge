### Import dependencies ###
import numpy as np

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
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').\
            filter(Measurement.station == 'USC00519281').all()
    session.close()

    all_temps = []
    for date, tobs in results:
        temp_obs = {}   
        temp_obs["date"] = date
        temp_obs["tobs"] = tobs
        all_temps.append(temp_obs)    
    
    return jsonify(all_temps) 
            
            
# Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    session.close()

    all_precip = []
    for date, prcp in results:
        precip_dict = {}   
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)    
    
    return jsonify(all_precip) 


# Define what to do when a user hits the /start/end route
@app.route("/api/v1.0/<start>/<end>")
def variable_date(start, end):
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '%Y-%m-%d').\
        filter(Measurement.date <= '%Y-%m-%d').filter(Measurement.station == 'USC00519281').all()
    session.close()

    all_temps = []
    for date, tobs in results:
    #     temp_obs = {}   
    #     temp_obs["date"] = date
    #     temp_obs["tobs"] = tobs
    #     all_temps.append(temp_obs)    
    
    # return jsonify(all_temps)
        print(date,tobs)

if __name__ == "__main__":
    app.run(debug=True)