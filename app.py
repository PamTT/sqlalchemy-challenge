# 1. import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, extract
from flask import Flask, jsonify
import datetime as dt

# 2. create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# 3.1 reflect database and tables
Base = automap_base()
Base.prepare(engine, reflect = True)

#3.2 save table reference
Measurement = Base.classes.measurement
Station = Base.classes.station

#3.3 Create session
session = Session(engine)

# 4. Setup Flask to create an app, being sure to pass __name__
app = Flask(__name__)


#5  / route
@app.route("/")
def home():
    """Return all available routes"""
    print("Server received request for 'Home' page...")
    
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&ltend&gt;"
    )


# 6.  /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """ Return JSON list of dict for {date : precipitation} from the last 12 months"""
    print("Server received request for 'precipitation' page...")
    
    session = Session(engine)
    
    # Query for the dates and precipitation values
    results =   session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

    # Convert date and precipitation to list of dictionaries to jsonify
    prcp_date_list = []
    for date, prcp in results:
        new_dictionary = {}
        new_dictionary[date] = prcp
        prcp_date_list.append(new_dictionary)
    session.close()
    return jsonify(prcp_date_list)

# 7.  /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
    """ Return JSON list stations with a list of dictionaries for id,station, name, lat, long, elevation"""
    print("Server received request for 'stations' page...")
    
    session = Session(engine)

    # query stations list from the Station table
    station_data = session.query(Station).all()

    #create a list of dictionary
    stations_list = []
    for station in station_data:
        stations_dict = {}
        stations_dict["id"]= station.id
        stations_dict["station"]= station.station
        stations_dict["name"]= station.name
        stations_dict["latitude"]= station.latitude
        stations_dict["longitude"]= station.longitude
        stations_dict["elevation"]= station.elevation
        stations_list.append(stations_dict)
    return jsonify(stations_list)

# 8.  /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")
    
    session = Session(engine)

    #query Date
    last_date = session.query(Measurement.date).order_by((Measurement.date).desc()).limit(1).all()
    last_12month = (dt.datetime.strptime(last_date[0][0], '%Y-%m-%d') - dt.timedelta(days=365)).date()
   
    
    temp_results = session.query(Measurement.date, Measurement.tobs).\
	filter(Measurement.date >= last_12month).order_by(Measurement.date).all()
    

    #create a list of dictionary
    tobs_list = []
    for date, tobs in temp_results:
        new_dict = {}
        new_dict[date] = tobs
        tobs_list.append(new_dict)

    session.close()

    return jsonify(tobs_list)

# 9.1 /api/v1.0/<start> 
@app.route("/api/v1.0/<start>")
def start(start):
    """ Return JSON list of min, avg, max temp from start date to end date"""
    print("Server received requeste for start date page...")
    
    session = Session(engine)
    return_list = []

    results = session.query(Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()

    for date, min, avg, max in results:
        new_dict = {}
        new_dict["Date"] = date
        new_dict["TMIN"] = min
        new_dict["TAVG"] = avg
        new_dict["TMAX"] = max
        return_list.append(new_dict)

    session.close()    

    return jsonify(return_list)

#9.2 /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    """ Return JSON list of min, avg, max temp from start date to end date"""
    print("")
    session = Session(engine)

    return_list = []

    results = session.query(Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()

    for date, min, avg, max in results:
        new_dict = {}
        new_dict["Date"] = date
        new_dict["TMIN"] = min
        new_dict["TAVG"] = avg
        new_dict["TMAX"] = max
        return_list.append(new_dict)

    session.close()    

    return jsonify(return_list)


if __name__ == "__main__":
    app.run(debug=True)
