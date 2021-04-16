# git_for_dbikes
# URL to access the website: 54.87.129.140:5000

This is an explanation of each file in the main repository:

flaskapp: A folder that contains all the code relating to the front end application. A seperate read me file has been included in this folder.

availability.ipynb: A file that contains all the code used to examine the linear models and test the implementation of both the charts and the linear model building packages.

credentials.py: A file that contains the password to access the main ec2 database

dbinfo.py: A file that contains the credentials to access the main ec2 database

mae_rmse_figures.zip: A zip file used to review the MAE and RMSE figures obtained from preparing the models.

main.py: This contains the scrappers used to gather data from the JCDecaux. This data populates the Stations and Occupancy tables

Unitttest(backend).ipynb: Test file to ensure that users can connect to the Database and that the database structure has not been comprimised

weather.py: The weather data scrapper collecting information from open weather maps

weather_predict.py: The function used to collect weather prediciton information in reation to the occupancy predictive modeling. This information has been built into the flask applicaiton. This is here as it is used to perform edits and test new features for the weather prediction applicaiton
