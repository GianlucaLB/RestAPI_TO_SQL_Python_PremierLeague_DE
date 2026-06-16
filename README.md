# Premier League 2023/24 Standings — ETL Pipeline

Hi there,
Welcome to my first Python project!

## What this project does
This project is an ETL pipeline that:
- **Extracts** Premier League standings data from the SportAPI REST API
- **Transforms** the raw JSON response into a structured format using Pandas
- **Loads** the data into a SQL Server database using SQLAlchemy

## Technologies used
- Python
- Pandas
- SQLAlchemy
- pyodbc
- SQL Server
- REST API (SportAPI via RapidAPI)

## How to run it
1. Clone the repository
2. Install the dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your credentials (see `.env.example`)
4. Run `main.py`

## Credits
Special thanks to Stephen for the clear and inspiring tutorial:
https://www.youtube.com/watch?v=w8Mvb79zRpA&t=3345s

Thanks,

Gianluca
