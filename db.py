import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database = "google_searches"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE DATABASE google_searches")