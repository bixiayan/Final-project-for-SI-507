# Final-project-for-SI-507

<!-- Data sources used, including instructions for a user to access the data sources (e.g., API keys or client secrets needed, along with a pointer to instructions on how to obtain these and instructions for how to incorporate them into your program (e.g., secrets.py file format)) -->
Data are generated inside the generate_databse folder. Source data include: API Key of omdbapi, IMDB-Movie-Data.csv daownloaded from the website. 

<!-- Any other information needed to run the program (e.g., pointer to getting started info for plotly) -->
Stay in the directory where app.py exists, run app.py and open  http://localhost:5000/.


<!-- Brief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them. -->
My code is basically consist of database construction and flask running.

Important functions are:
def init_db(db_name)
def insert_ratings(db_name, csv_file, json_file)
def insert_basics(db_name, csv_file, json_file)
def home()


<!-- Brief user guide, including how to run the program and how to choose presentation options. -->
Running instruction:
1. request_with_csv.py(optional)
    NOTE: be careful running this since it override the cache.json. The newly cache.json will contain 4 piece of weired format html data and I delete it manully.
2. get_json.py(optional)
    NOTE: be careful running this since it override the cache.json. The newly cache.json will contain 4 piece of weired format html data and I delete it manully.
3. constuct_db.py(recommened start directly with this step)
    This contruct the database.
4. Go to the upper level folder
5. app.py
    This starts the flask based program, please open http://localhost:5000/ to see the results.