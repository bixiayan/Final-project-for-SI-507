from app import *
import unittest

class TestDatabase(unittest.TestCase):

    def test_basics_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT COUNT(DISTINCT(Year)) FROM Basics '
        results = cur.execute(sql)
        result = results.fetchone()
        self.assertEqual(result[0], 11)

        sql = 'SELECT MAX(Year) FROM Basics '
        results = cur.execute(sql)
        result = results.fetchone()
        self.assertEqual(result[0], 2016)

        sql = 'SELECT MIN(Year) FROM Basics '
        results = cur.execute(sql)
        result = results.fetchone()
        self.assertEqual(result[0], 2006)

        sql = 'SELECT Year FROM Basics '
        sql += "WHERE Title='Ted'"
        results = cur.execute(sql)
        result = results.fetchone()
        self.assertEqual(result[0], 2012)

        sql = '''
            SELECT Title
            FROM Basics
            WHERE Year=2016
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('La La Land',), result_list)
        self.assertEqual(len(result_list), 268)

        conn.close()

    def test_ratings_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT mdbID
            FROM Ratings
            WHERE imdbRating>8
        '''
        results = cur.execute(sql)
        count = len(results.fetchall())
        self.assertEqual(count, 47)

        sql = '''
            SELECT MAX(imdbVotes)
            FROM Ratings
        '''
        results = cur.execute(sql)
        result = results.fetchone()
        self.assertEqual(result[0], 1896843)

        sql = '''
            SELECT MAX(imdbRating)
            FROM Ratings
        '''
        results = cur.execute(sql)
        result = results.fetchone()
        self.assertEqual(result[0], 9.0)

        sql = '''
            SELECT MAX(metaScore)
            FROM Ratings
        '''
        results = cur.execute(sql)
        result = results.fetchone()
        self.assertEqual(result[0], 100)

        sql = '''
            SELECT AVG(metaScore)
            FROM Ratings
        '''
        results = cur.execute(sql)
        result = results.fetchone()
        self.assertEqual(result[0], 55.53041622198506)

        conn.close()

    def test_joins(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = '''
            SELECT Title
            FROM Basics
            JOIN Ratings on Basics.mdbId = Ratings.mdbId
            ORDER BY Ratings.imdbVotes DESC
            LIMIT 1
        '''
        results = cur.execute(sql)
        result = results.fetchone()
        self.assertEqual(result[0], "The Dark Knight")

        sql = '''
            SELECT MAX(Ratings.MetaScore) 
            FROM Ratings
            JOIN Basics on Basics.mdbId = Ratings.mdbId
            WHERE Year=2016
        '''
        results = cur.execute(sql)
        result = results.fetchone()
        self.assertEqual(result[0], 99)

        conn.close()

unittest.main()
