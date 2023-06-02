# Import the dependencies.
from matplotlib import style
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, func
from sqlalchemy.orm import sessionmaker
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

# 2. Create an app, being sure to pass_name_
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
        f"Welcome to Surf Up! Analyze the climate in Hawaii! <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
    )

# 4. Define what to do when a user hits the /about route
# Save reference to the table

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create a query
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).order_by(Measurement.date).all()

    session.close()

	# Create a dictionary 

    precipitation_data = {}
    for date, prcp in query:
        precipitation_data[date] = prcp

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():

    # Create a query
    active_stations = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).order_by(Station.station).all()
   
    session.close()

	# Create a dictionary

    station_data = {}
    for station, name, latitude, longtitude, elevation in active_stations:
        station_data[station] = name

    return jsonify(station_data)

if __name__ == "__main__":
    app.run(debug=True)