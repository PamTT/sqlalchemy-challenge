# sqlalchemy-challenge

Climate Analysis and Exploration:
I  began with using Python and SQLAlchemy to do basic climate analysis and data exploration of my climate database. All of the following analysis were completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.
I used the provided starter notebook and hawaii.sqlite files to complete my climate analysis and data exploration.
Choose a start date and end date for your trip. Make sure that your vacation range is approximately 3-15 days total.
Use SQLAlchemy create_engine to connect to your sqlite database.
Use SQLAlchemy automap_base() to reflect your tables into classes and save a reference to those classes called Station and Measurement.

Precipitation Analysis
Design a query to retrieve the last 12 months of precipitation data.
Select only the date and prcp values.
Load the query results into a Pandas DataFrame and set the index to the date column.
Sort the DataFrame values by date.
Plot the results using the DataFrame plot method.
Use Pandas to print the summary statistics for the precipitation data.

Station Analysis
Designed a query to calculate the total number of stations.
Designed a query to find the most active stations.
Listed the stations and observation counts in descending order.
Determined station with the highest number of observations
I needed to use a function such as func.min, func.max, func.avg, and func.count in your queries.
Designed a query to retrieve the last 12 months of temperature observation data (TOBS).
Filtered by the station with the highest number of observations.
Ploted the results as a histogram with bins=12.


