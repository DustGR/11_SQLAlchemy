# 11_SQLAlchemy
SQL Alchemy with Flask

Jupyter Notebook includes analysis of database per assignment readme.

API calls from app.py:
/api/v1.0/precipitation`
JSON showing {date:precipitation} for the last year of data in the dataset
  
/api/v1.0/stations
JSON of stations in the dataset
  
/api/v1.0/tobs
JSON showing {date:temperature observations} for the last year of data in the dataset

/api/v1.0/<start>
JSON of high, low, and average temperature for all days from the start date to the end of the dataset
(<start> given as %Y-%m-%d or YEAR-MO-DA) 

/api/v1.0/<start>/<end>
JSON of high, low, and average temperature for all days from the start date to the end date
(<start> and <end> given as %Y-%m-%d or YEAR-MO-DA) 