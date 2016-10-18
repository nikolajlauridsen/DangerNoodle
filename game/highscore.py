import sqlite3 as lite


class DbHandler:
    """Class handling database interaction"""
    def __init__(self):
        """Connect to database, create cursor and tables"""
        self.conn = lite.connect('highscore.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS HighScore"
                       "(score INT, name TEXT)")

    def insert_highscore(self, score, name):
        """Insert a highscore entry"""
        self.c.execute("INSERT INTO HighScore VALUES (?,?)", (score, name))

    def get_highscore(self):
        """Return highscore as a list of dictionaries"""
        # Select and fetch the 15 highest high scores
        self.c.execute("SELECT * FROM HighScore ORDER BY score DESC LIMIT 15")
        highscore_data = self.c.fetchall()
        # List for containing high score
        highscore = []
        for entry in highscore_data:
            context = {                 # Put the data in to context
                "score": entry[0],
                "name": entry[1]
            }
            highscore.append(context)   # Append it to the list

        return highscore

    def save_changes(self):
        """Save changes to database"""
        self.conn.commit()
