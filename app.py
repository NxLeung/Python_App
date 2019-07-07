from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, cast


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end_date><br/>"
    )


@app.route("/api/v1.0/precipitation")

#Convert the query results to a Dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.

def precipitation():
	"""Return the precipitation Dictionary using dates as key."""
	
	maxdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
	maxdate = maxdate[0]
	year_ago = datetime.strptime(maxdate, "%Y-%m-%d") - dt.timedelta(days=366)
	precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between(year_ago, maxdate))
	precipitation_df = pd.DataFrame(precipitation, columns=['date', 'prcp'])	
	precipitation_df.set_index('date', inplace=True)
	precipitation_df = precipitation_df.sort_values('date', ascending=True)
	precipitation_df_grouped = precipitation_df.groupby('date').sum()
	precipitation_dict = precipitation_df_grouped.to_dict("dict")

	return jsonify(precipitation_dict)






@app.route("/api/v1.0/stations")
#Return a JSON list of stations from the dataset.

def stations():
	station_list = session.query(Station.station, Station.name).all()

	return jsonify(station_list)





@app.route("/api/v1.0/tobs")

def tobs():
	maxdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
	maxdate = maxdate[0]
	year_ago = datetime.strptime(maxdate, "%Y-%m-%d") - dt.timedelta(days=366)

	sel = [Measurement.date, func.avg(Measurement.tobs)]
	temperatures = session.query(*sel).filter(Measurement.date.between(year_ago, maxdate)).group_by(Measurement.date).all()
	return jsonify(temperatures)

# # query for the dates and temperature observations from a year from the last data point.
# # Return a JSON list of Temperature Observations (tobs) for the previous year.
 

@app.route("/api/v1.0/<start>")
def date(start):
	sel = [func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)]
	starts = session.query(*sel).filter(Measurement.date >= start).all()

	return jsonify(starts)


@app.route("/api/v1.0/<start>/<end_date>")

def dates(start,end_date):
	sel = [func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)]
	ends = session.query(*sel).filter(Measurement.date.between(start, end_date)).all()
	# starts = session.query(func.max(Measurement.tobs).label('Max')).filter(Measurement.date >= start).all()
	return jsonify(ends)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.


# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.


# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.


if __name__ == "__main__":
    app.run(debug=True)


