from flask import Flask, redirect, url_for, render_template, jsonify, request
from main import *
import mysql.connector
from mysql.connector import errors

app = Flask(__name__)


@app.route('/', methods=["POST" , "GET"])
def home():
    if request.method == "POST":
        keyword = request.form['keyword']
        return redirect(url_for('new_table',keyword=keyword))
    else:
        return render_template('index.html')
    

@app.route('/table/<keyword>', methods=["POST","GET"])            
def new_table(keyword):
    if keyword != "favicon.ico":
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM storage WHERE parent = '%s'" % keyword)
        data = mycursor.fetchall()
        if data:
            mycursor.close()
            return render_template('table.html', data=data)
        main(keyword)
        return new_table(keyword)
    else:
        return redirect(url_for('home'))    

@app.route('/delete/<keyword>/<id>', methods=["POST"])
def delete_table_row(id, keyword):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM storage WHERE id = %s" % id)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('new_table', keyword=keyword))

if __name__ == "__main__":
    app.run()
