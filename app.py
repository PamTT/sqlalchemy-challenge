# 1. import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, extract
from flask import Flask, jsonify
import datetime

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

# 5. #Create a function that gets minimum, average, and maximum temperatures for a range of dates
        # This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
        # and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# 6.1 Define what to do when users hit / route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


# 6.2. Define what to do when a user hits the /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")
    
    #find precipitation data for the last year.  First we find the last date in the database
    final_date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    max_date_string = final_date_query[0][0]
    max_date = datetime.datetime.strptime(max_date_string, "%Y-%m-%d")

    #set beginning of search query
    begin_date = max_date - datetime.timedelta(366)

    #find dates and precipitation amounts
    precip_data = session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.prcp).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= begin_date).all()
    
    #prepare the dictionary with the date as the key and the prcp value as the value
    prcp_results_dict = {}
    for result in precip_data:
        prcp_results_dict[result[0]] = result[1]
    return jsonify(prcp_results_dict)
    

# 8. Define what to do when a user hits the /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")

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

# 9. Define what to do when a user hits the /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")

    #query Date
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    





    return "1 Query the dates and temperature observations of the most active station for the last year of data. 2.Return a JSON list of temperature observations (TOBS) for the previous year."


if __name__ == "__main__":
    app.run(debug=True)
