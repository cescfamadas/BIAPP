from pandas import read_csv
from pandas import read_sql
import sqlite3
from sqlalchemy import create_engine
df = read_csv('data.csv')
engine = create_engine("sqlite:///test.db", echo=True)
sqlite_connection = engine.connect()
sqlite_table = "User"
df.to_sql(sqlite_table, sqlite_connection, if_exists='fail')
sqlite_connection.close()
