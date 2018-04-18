import sqlite3
import csv
import json
import ast

DBNAME = 'movies.db'
MOVIECSV = 'IMDB-Movie-Data.csv'

CACHE_FNAME = "imdb.json"

# read bars from csv
def create_database():
    init_db(DBNAME)
    insert_data(DBNAME, MOVIECSV, CACHE_FNAME)
    


def insert_data(db_name, csv_file, json_file):
    insert_basics(db_name, csv_file, json_file)
    insert_ratings(db_name, csv_file, json_file)



def init_db(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
    except Exception as ex:
        print(ex)
        print("Created...")
    # create Countries table
    try:
        statement = 'SELECT * FROM Basics'
        ### only works if there is a table, else would return an error, then go to the exception part
        cur.execute(statement)
        user_input = input("Basics Table already exists. Drop table? yes/no: ")
        while True:
            #if user input is yes, drop table. Else, use move on and use existing table
            if user_input == "yes":
                statement = "DROP TABLE IF EXISTS Basics"
                cur.execute(statement)
                conn.commit()
                # imdbID year actors directors genre description
                statement = '''CREATE TABLE 'Basics' (
                    'mdbID' TEXT PRIMARY KEY,
                    'Title'  TEXT NOT NULL,
                    'Year'  INTEGER NOT NULL,
                    'Actors'  TEXT NOT NULL,
                    'Director'  TEXT NOT NULL,
                    'Genre'  TEXT NOT NULL,
                    'Description'  TEXT NOT NULL
                    )
                    '''
                cur.execute(statement)
                conn.commit()
                break  
            elif user_input == "no":
                break
            else:
                user_input = input("Basics Table already exists. Drop table? yes/no: ")
    except Exception as ex:
        print("Created...")
        statement = '''CREATE TABLE 'Basics' (
                    'mdbID' TEXT PRIMARY KEY,
                    'Title'  TEXT NOT NULL,
                    'Year'  INTEGER NOT NULL,
                    'Actors'  TEXT NOT NULL,
                    'Director'  TEXT NOT NULL,
                    'Genre'  TEXT NOT NULL,
                    'Description'  TEXT NOT NULL
                    )
                    '''
        # print(statement)
        cur.execute(statement)
    conn.commit()

    # create bars table
    try:
        statement = 'SELECT * FROM Ratings'
        ### only works if there is a table, else would return an error, then go to the exception part
        cur.execute(statement)
        user_input = input("Ratings Table already exists. Drop table? yes/no: ")
        while True:
            #if user input is yes, drop table. Else, use move on and use existing table
            if user_input == "yes":
                statement = "DROP TABLE IF EXISTS Ratings"
                cur.execute(statement)
                conn.commit()
                # imdbID score, ratings, rank
                statement = '''CREATE TABLE 'Ratings' (
                    'mdbID' TEXT REFERENCES Basics('mdbID'),
                    'MetaScore'  INTEGER NOT NULL,
                    'imdbRating' REAL NOT NULL,
                    'imdbVotes' INTEGER NOT NULL
                    )
                    '''
                cur.execute(statement)
                conn.commit()
                break  
            elif user_input == "no":
                break
            else:
                user_input = input("Ratings Table already exists. Drop table? yes/no: ")
    except Exception as ex:
        print("Created...")
        statement = '''CREATE TABLE 'Ratings' (
            'mdbID' TEXT REFERENCES Basics('mdbID'),
            'MetaScore'  INTEGER NOT NULL,
            'imdbRating' REAL NOT NULL,
            'imdbVotes' INTEGER NOT NULL
            )
            '''
        cur.execute(statement)
    conn.commit()

def insert_ratings(db_name, csv_file, json_file):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
    except Exception as ex:
        print(ex)

    data = json.load(open(json_file))

    # 'Title' TEXT REFERENCES Basics('Title'),
    # 'Rating'  Real NOT NULL,
    # 'Ranking' INTEGER NOT NULL

    for key, value in data.items():
        value = ast.literal_eval(value)
        if value['Metascore'] == 'N/A':
            value['Metascore'] = 0
        if value["imdbRating"] == 'N/A':
            value["imdbRating"] = 0.0
        if value["imdbVotes"] == 'N/A':
            value["imdbVotes"] = ",0"
        
        insertion = (value['imdbID'], value["Metascore"], value["imdbRating"], value["imdbVotes"].replace(',', ''))

        statement = 'INSERT INTO "Ratings" '
        statement += 'VALUES (?, ?, ?, ?)'
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()


def insert_basics(db_name, csv_file, json_file):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
    except Exception as ex:
        print(ex)
    
    data = json.load(open(json_file))
    imdb_ids = []
    for key, value in data.items():
        value = ast.literal_eval(value)
        insertion = (value["imdbID"], value["Title"], int(value["Year"][0:4]), value["Actors"], value["Director"], value["Genre"], value["Plot"])
        statement = 'INSERT INTO "Basics" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?) '
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()

        

if __name__=="__main__":
    create_database()