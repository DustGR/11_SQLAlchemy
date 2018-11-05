##SQL_Alchmey with Flask
##Coding Bootcamp Week 11 Homework
##Dustin Rice 11/4/2018


from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify

# # Reflect Tables into SQLAlchemy ORM
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

lastrecord = session.query(Measurement).order_by(Measurement.date.desc()).first()  #Retrieves most recent date
lastdate = dt.datetime.strptime(lastrecord.date, '%Y-%m-%d') #converts to datetime object lastdate
oneyear = dt.timedelta(365)   #Amount of days in a year - Doesn't take leap years into account.
firstdate = lastdate - oneyear

app = Flask(__name__)
@app.route("/api/v1.0/precipitation")
def year_precip():
    # Perform a query to retrieve the data and precipitation scores
    # Save the query results as a Pandas DataFrame and set the index to the date column
    year_precip_df = pd.read_sql(session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= firstdate).statement, session.bind,index_col='date') 
    # Sort the dataframe by date
    year_precip_df.sort_values(by='date', inplace=True)
    year_precip_dict = year_precip_df.to_dict(orient='dict')['prcp']
    return jsonify(year_precip_dict)


# Design a query to show how many stations are available in this dataset?
@app.route("/api/v1.0/stations")
def station_quantity():
    station_q = session.query(Station).all()
    stationlist = []
    for st in station_q:
        stationlist.append(st.station)
    return jsonify(stationlist)

@app.route('/api/v1.0/tobs')
def year_temp():
    year_temp_df = pd.read_sql(session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= firstdate).statement, session.bind,index_col='date') 
    # Sort the dataframe by date
    year_temp_df.sort_values(by='date', inplace=True)
    year_temp_dict = year_temp_df.to_dict(orient='dict')['tobs']
    return jsonify(year_temp_dict)



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
    engine = create_engine("sqlite:///Resources/hawaii.sqlite") 
    session = Session(engine) ##I had to reconnect to the database to avoid errors
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


@app.route('/api/v1.0/<start>')
def temp_from_start(start):
    lastdate_str = (lastdate-dt.timedelta(days=1)).strftime('%Y-%m-%d')
    try:
        averages = calc_temps(start, lastdate_str)[0]
        output_dict = {"High Temp" : averages[2],
                        "Low Temp" : averages[0],
                        "Avg Temp" : averages[1]}
        return jsonify(output_dict)
    except:
        return "Date Time Conversion Failure"

@app.route('/api/v1.0/<start>/<end>')
def temp_range(start, end):
    try:
        averages = calc_temps(start, end)[0]
        output_dict = {"High Temp" : averages[2],
                        "Low Temp" : averages[0],
                        "Avg Temp" : averages[1]}
        return jsonify(output_dict)
    except:
        return "Date Time Conversion Failure"

if __name__ == "__main__":
    # @TODO: Create your app.run statement here
    app.run(debug=True)

