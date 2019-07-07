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
#Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Building date parameters
maxdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
maxdate = maxdate[0]
year_ago = datetime.strptime(maxdate, "%Y-%m-%d") - dt.timedelta(days=366)

# Precipitation Query
precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between(year_ago, maxdate))

# Dataframe build
precipitation_df = pd.DataFrame(precipitation, columns=['date', 'prcp'])
precipitation_df.set_index('date', inplace=True)
precipitation_df = precipitation_df.sort_values('date', ascending=True)

# Plot and save
precipitation_df.plot.bar(title="Precipitation", figsize=(20,10))
plt.xticks([])
plt.tight_layout()
plt.savefig("precipitation_chart.png", bbox_inches="tight")
plt.show()

#precipitation_df.describe()

station_count = session.query(Station).count()
#station_count

counts = func.count(Measurement.station)
active_stations = session.query(Measurement.station,counts).group_by(Measurement.station).order_by(counts.desc()).all()
#active_stations

# Temperature Query
sel = [Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
most_active = session.query(*sel).    filter(Measurement.station == 'USC00519281').    all()

temperatures = session.query(Measurement.date, Measurement.tobs).    filter(Measurement.date.between(year_ago, maxdate)).    filter(Measurement.station == 'USC00519281')

temperature_df = pd.DataFrame(temperatures, columns=['date', 'tobs'])
temperature_df.plot.hist(title="Temperatures for Most Active Station", figsize = (20,10), bins = 12)
plt.tight_layout()
plt.savefig("temperature_histogram.png", bbox_inches="tight")
plt.show()















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
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation/<date>")

#Convert the query results to a Dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.

def precipitation(date):
    """Return the precipitation Dictionary using dates as key."""

    precipitation_df.to_dict("precipitation_dict")

    return jsonify(precipitation_dict), 404






# @app.route("/api/v1.0/stations")
# #Return a JSON list of stations from the dataset.






# @app.route("/api/v1.0/tobs")


# # query for the dates and temperature observations from a year from the last data point.
# # Return a JSON list of Temperature Observations (tobs) for the previous year.




# @app.route("/api/v1.0/<start>") 





# @app.route("/api/v1.0/<start>/<end>")

# def dates():
# 	return ""

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.


# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.


# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

# @app.route("/api/v1.0/justice-league/superhero/<superhero>")
# def justice_league_by_superhero__name(superhero):
#     """Fetch the Justice League character whose superhero matches
#        the path variable supplied by the user, or a 404 if not."""

#     canonicalized = superhero.replace(" ", "").lower()
#     for character in justice_league_members:
#         search_term = character["superhero"].replace(" ", "").lower()

#         if search_term == canonicalized:
#             return jsonify(character)

#     return jsonify({"error": "Character not found."}), 404

if __name__ == "__main__":
    app.run(debug=True)


