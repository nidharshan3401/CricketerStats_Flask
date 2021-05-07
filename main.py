from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL 
import MySQLdb.cursors 

app = Flask(__name__) 
  
##Setting up MYSQL
app.secret_key = 'password'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'nidhar@8151'
app.config['MYSQL_DB'] = 'database'
mysql = MySQL(app) 

##Login Page
@app.route('/') 
@app.route('/template')
def template(): 
    query = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query.execute('SELECT * FROM details') 
    return render_template('template.html',players=query.fetchall()) 


@app.route('/details', methods =['GET', 'POST']) 
def details():
    if request.method == 'POST':
        playername = request.form.get('playername')
        print(playername) 
        query = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        query.execute('SELECT * FROM details WHERE pname= %s' , (playername,))
        player_details=query.fetchone() 
        query = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query.execute('SELECT * FROM details') 
        players=query.fetchall()
        return render_template('details.html',players=players,player=player_details)

         

@app.route('/addplayer', methods =['GET', 'POST'])
def addplayer():
    if request.method == 'POST': 
        pname = request.form['pname'] 
        runs = request.form['runs'] 
        wickets = request.form['wickets'] 
        link = request.form['link']
        matches = request.form['matches']  
        average = request.form['average']  
        strike = request.form['strike']  
        query = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query.execute('SELECT * FROM details')
        players = query.fetchall()
        query.execute('INSERT INTO details VALUES (NULL, % s, % s , % s, % s, % s, % s, % s)', (pname,link, runs, wickets,matches,average,strike,))  
        mysql.connection.commit() 
        return render_template('template.html',players=players)
    else: 
        return render_template('addplayer.html') 



if __name__ == "__main__":
    app.run(debug=True)