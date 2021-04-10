import mysql.connector
from mysql.connector import errorcode

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database = "google_searches"
)


#mycursor.execute("CREATE DATABASE google_searches")

