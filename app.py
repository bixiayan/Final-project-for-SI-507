from flask import Flask, render_template, url_for
from flask import *
import sqlite3


app = Flask(__name__, template_folder='templates')
DBNAME = 'movies.db'

@app.route('/')
def home():
    years=[2006, 2007, 2008, 2009, 2012, 2011, 2012, 2013, 2014, 2015, 2016]
    return render_template('index.html', years=years)

@app.route('/allMovies')
def show_years():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Exception as ex:
        print(ex)
    if request.method == 'GET':
        year = int(request.args.get('year'))
        statement = "SELECT mdbID, Title FROM Basics WHERE Year={}".format(year)
        cur.execute(statement)
        result = cur.fetchall()
    cur.close()
    return render_template('allMovies.html', year=year, result=result)


@app.route('/averageMovies')
def show_average():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Exception as ex:
        print(ex)
    if request.method == 'GET':
        year = int(request.args.get('year'))
        statement = "SELECT AVG(MetaScore), AVG(imdbRating), AVG(imdbVotes) FROM Ratings "
        statement += "JOIN Basics on Basics.mdbID = Ratings.mdbID "
        statement += "WHERE BAsics.Year='{}'".format(year)
        cur.execute(statement)
        result = cur.fetchone()
    cur.close()
    return render_template('averageMovies.html', result=result, year=year)



@app.route('/highestMovies')
def show_highest():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Exception as ex:
        print(ex)
    if request.method == 'GET':
        year = int(request.args.get('year'))
        statement = "SELECT MAX(Ratings.MetaScore), Basics.Title, Basics.mdbID FROM Ratings "
        statement += "JOIN Basics on Basics.mdbID = Ratings.mdbID "
        statement += "WHERE Basics.Year={}".format(year)
        print(statement)
        cur.execute(statement)
        MetaMax = cur.fetchone()
        
        statement = "SELECT MAX(Ratings.imdbRating),  Basics.Title, Basics.mdbID FROM Ratings "
        statement += "JOIN Basics on Basics.mdbID = Ratings.mdbID "
        statement += "WHERE Basics.Year={}".format(year)
        cur.execute(statement)
        imdbRatingMax = cur.fetchone()

        statement = "SELECT MAX(Ratings.imdbVotes), Basics.Title, Basics.mdbID FROM Ratings "
        statement += "JOIN Basics on Basics.mdbID = Ratings.mdbID "
        statement += "WHERE Basics.Year={}".format(year)
        cur.execute(statement)
        imdbVotesMax = cur.fetchone()
    cur.close()
    return render_template('highestMovies.html', year=year, MetaMax=MetaMax, imdbRatingMax=imdbRatingMax, imdbVotesMax=imdbVotesMax)



@app.route('/details')
def show_details():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Exception as ex:
        print(ex)
    if request.method == 'GET':
        mdbID = request.args.get('mdbID')
        statement = "SELECT Basics.*, Ratings.* FROM Basics "
        statement += "JOIN Ratings on Basics.mdbID = Ratings.mdbID "
        statement += "WHERE Basics.mdbID='{}'".format(mdbID)
        cur.execute(statement)
        result = cur.fetchall()
    cur.close()
    return render_template('details.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)