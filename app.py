from flask import Flask, redirect, url_for, render_template, jsonify, request
from db import mydb
from main import *
from mysql.connector import errors

app = Flask(__name__)
mycursor = mydb.cursor()

@app.route('/', methods=["POST" , "GET"])
def home():
    if request.method == "POST":
        keyword = request.form['keyword']
        return redirect(url_for('new_table',keyword=keyword))
    else:
        return render_template('index.html')
    

@app.route('/<keyword>', methods=["POST" , "GET"])            
def new_table(keyword):
    if(keyword != "favicon.ico"):
        try:
            sql = "SELECT * FROM %s" % keyword
            mycursor.execute(sql)
            data = mycursor.fetchall()
            return render_template('table.html', data=data)
        except errors.ProgrammingError:
            main(keyword)
            sql = "SELECT * FROM %s" % keyword
            mycursor.execute(sql)
            data = mycursor.fetchall()
            return render_template('table.html', data=data)    
    else:
        return redirect(url_for('home'))
        

if __name__ == "__main__":
    app.run()
