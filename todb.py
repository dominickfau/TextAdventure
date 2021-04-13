import sys
import sqlite3
import os
import os.path

def main(dbname):
    """Creates a sqlite3 database file with the name given.

    Args:
        dbname (str): The name for the database file to create.
    """
    con = sqlite3.connect(dbname)

    con.execute("CREATE TABLE IF NOT EXISTS rooms(id INTEGER PRIMARY KEY, json TEXT NOT NULL)")
    con.commit()
    ROOMS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'rooms')

    for filename in os.listdir(ROOMS_DIR):
        base, extension = os.path.splitext(filename)
        if extension == '.json':
            with open(os.path.join(ROOMS_DIR, filename), 'r') as f:
                json = f.read()
                
                print("[INFO] Inserting room {0}".format(int(base)))
                
                con.execute("INSERT OR REPLACE INTO rooms(id, json) VALUES(?, ?);",
                            (int(base), json))
                            
                con.commit()

    con.close()

if __name__ == "__main__":
    main('game.db')