#importing all the libraries neccesarie
import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from datetime import datetime

#Created an .env file to store all the private information and the use load_dotenv() to load it into the main.py file
load_dotenv()

#REST_API info
API_KEY  = os.getenv('API_KEY')
API_HOST = os.getenv('API_HOST')
SEASON = os.getenv('SEASON')
LEAGUE_ID = os.getenv('LEAGUE_ID')

#SQL Info
DB_DRIVER   = os.getenv('DB_DRIVER')
DB_SERVER   = os.getenv('DB_SERVER')
DB_DATABASE = os.getenv('DB_DATABASE')


#Loading the REST_API


url = f"https://sportapi7.p.rapidapi.com/api/v1/unique-tournament/{LEAGUE_ID}/season/{SEASON}/standings/total"

headers = {
	"x-rapidapi-key": f"{API_KEY}",
	"x-rapidapi-host": F"{API_HOST}",
	"Content-Type": "application/json"
}

#Using a try/excpet to control the status of the API call
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status() # If there is an error with the requestes,it will close the request and  go straight to the except
    payload = response.json()
except requests.exceptions.RequestException as e: #it will print the error number.
    print(f'Error API: {e}')


#Extacting from the JSON file all the data needed
rows = payload["standings"][0]["rows"]

column_name = ['rank' , 'team' , 'played' , 'wins' , 'draws' , 'losses' , 'goals_for' , 'goals_against' , 'goals_diff' , 'points']
standings_list = []


for row in rows:
    standings_list.append({
        "rank": row["position"],
        "team": row["team"]["name"],
        "played": row["matches"],
        "wins": row["wins"],
        "draws": row["draws"],
        "losses": row["losses"],
        "goals_for": row["scoresFor"],
        "goals_against": row["scoresAgainst"],
        "goals_diff": row["scoreDiffFormatted"],
        "points": row["points"]
    })

#Creating the DataFrame
df = pd.DataFrame(standings_list)


#Creating the connection to SQL Server through sqlalchemy

engine = create_engine(
    "mssql+pyodbc:///?odbc_connect="
    f"DRIVER={DB_DRIVER};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_DATABASE};"
    "Trusted_Connection=yes;"
)

#Loading the data to SQL
df['loaded_at'] = datetime.now()

df.to_sql(
    name='Premier_League_24_25',
    con=engine,
    if_exists='replace',
    index=False
)


#Running a query to see the top 5 teams by goals for.
df_check = pd.read_sql("SELECT TOP 5* \
                       FROM Premier_League_24_25 \
                       ORDER BY goals_for  DESC ", engine)
print(df_check)
