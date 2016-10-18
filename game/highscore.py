import sqlite3 as lite

class DbHandler:
    def __init__(self):
        self.conn = lite.connect('highscore.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS HighScore"
                       "(score INT, name TEXT)")

    def insert_highscore(self, score, name):
        """Insert a highscore entry"""
        self.c.execute("INSERT INTO HighScore VALUES (?,?)", (score, name))

    def get_highscore(self):
        """Return highscore as a list of dictionaries"""
        self.c.execute("SELECT * FROM HighScore ORDER BY score DESC LIMIT 15")
        highscore_data = self.c.fetchall()
        highscore = []
        for entry in highscore_data:
            context = {
                "score": entry[0],
                "name": entry[1]
            }
            highscore.append(context)
        return highscore

    def save_changes(self):
        """Save changes to database"""
        self.conn.commit()
