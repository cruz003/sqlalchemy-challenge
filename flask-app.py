import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"api/v1.0/<start date><br/>"
        f"api/v1.0/<start date>/<end date><br/>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation for Honolulu, Hawaii"""
    # Query all passengers
    all_prcp = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Weather Statons for Honolulu, Hawaii"""
    # Query all passengers
    all_stations = session.query(Station.station, Station.name).all()

    session.close()

    # Convert list of tuples into normal list
#    all_names = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Temperature Obesrvations for Honolulu, Hawaii from 8/23/2016 to 8/23/2017"""
    # Query all passengers
    precip_data = session.query(Measurement.date, Measurement.tobs).filter((Measurement.date >= '2016-08-23')).order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
#    all_names = list(np.ravel(results))

    return jsonify(precip_data)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return Temperature Min, Max and Average for all dates since <start date>"""
    start_wtr = session.query(Measurement.date, func.min(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).group_by(Measurement.date).all()

    start_data_rtn=list(start_wtr)

    return jsonify(start_data_rtn)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return Temperature Min, Max and Average for all dates since <start date>"""
    start_end_wtr = session.query(Measurement.date, func.min(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).group_by(Measurement.date).all()

    start_end_data_rtn=list(start_end_wtr)

    return jsonify(start_end_data_rtn)

    
if __name__ == '__main__':
    app.run(debug=True)