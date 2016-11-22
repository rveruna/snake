from flask import Flask, request, render_template, url_for, g, redirect, session, flash, request, jsonify, json
from functools import wraps
import sqlite3
import settings

from main import Main
from login import Login
from music import Music

app = Flask(__name__)

app.secret_key = settings.secret_key


@app.route('/')
def root():
    connection = sqlite3.connect("mydatabase.db")
    connection.row_factory = sqlite3.Row

    rows = connection.cursor().execute("SELECT * FROM categories").fetchall()
    
    return render_template("index.html", rows=rows)


#templates for errors 404, 500
	
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

	
@app.route('/treasures')
@app.route('/treasures/<name>')
def treasures(name):
	sql = ('SELECT * FROM treasures WHERE page_name = ?')
	connection = sqlite3.connect("mydatabase.db")
	connection.row_factory = sqlite3.Row     		
	treasures = connection.cursor().execute(sql,[name]).fetchall()
    
	sql2 = ('SELECT * FROM categories')
	connection = sqlite3.connect("mydatabase.db")
	connection.row_factory = sqlite3.Row     		
	all = connection.cursor().execute(sql2).fetchall()
    
	return render_template('treasures.html',  name=name, all=all, treasures=treasures)  
	connection.close()
    
@app.route('/category')
@app.route('/category/<name>')
def category(name):
	sql = ('SELECT * FROM categories WHERE page_name = ?')
	connection = sqlite3.connect("mydatabase.db")
	connection.row_factory = sqlite3.Row     		
	rows = connection.cursor().execute(sql,[name]).fetchall()
    
	sql2 = ('SELECT * FROM treasures WHERE category = ?')
	connection = sqlite3.connect("mydatabase.db")
	connection.row_factory = sqlite3.Row     		
	treasures = connection.cursor().execute(sql2,[name]).fetchall()
   	all = connection.cursor().execute("SELECT * FROM categories").fetchall()
    
	return render_template('category.html', rows = rows, name=name, all=all, treasures=treasures)  
    
	
	
@app.route('/form', methods=('GET', 'POST'))
def form():
    msg = None
    if request.method == 'POST':
      try:
        name = request.form['name']
        year = request.form['year']
        info = request.form['info']
        location = request.form['location']
        page_name = request.form['page_name']
        category = request.form['category']
        img = request.form['img']
        img2 = request.form['img2']


        if (name and year and info and location and page_name and category and img and img2):
           con = sqlite3.connect("mydatabase.db")
           cur = con.cursor()
           cur.execute("INSERT INTO treasures (name,year,info,location,page_name,category,img,img2) VALUES (?,?,?,?,?,?,?,?)",(name,year,info,location,page_name,category,img,img2) )

           con.commit()
           msg = "Record successfully added"

        else:
           msg = "Please enter details in each field"

      except:
           msg="Something went wrong. Try again."


    return render_template('form.html', msg=msg)
  


	
	
# Routes for login
app.add_url_rule('/',
                 view_func=Main.as_view('main'),
                 methods=["GET"])
app.add_url_rule('/<page>/',
                 view_func=Main.as_view('page'),
                 methods=["GET"])
app.add_url_rule('/login/',
                 view_func=Login.as_view('login'),
                 methods=["GET", "POST"])

app.add_url_rule('/music/',
                 view_func=Music.as_view('music'),
                  methods=["GET", "POST"])

	



if __name__ == "__main__":
 app.run( host ='0.0.0.0', debug = True )
 


