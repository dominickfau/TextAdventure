import json
import sqlite3

def get_room(id, dbfile):
    """Find and return a room by ID.

    Args:
        id (int): ID of room to retrieve.
        dbfile (Path Like): Path to sqlite3 database file.

    Raises:
        RuntimeError: Raised if room not found.

    Returns:
        Room Object: Returns a Room object for the ID given.
    """
    
    roomObject = None
    
    con = sqlite3.connect(dbfile)
    data = con.execute("select json from rooms where id=?",(id,))
    if not data: raise RuntimeError(f"Could not find room with ID: {id}.")
    for row in data:
        jsontext = row[0]
        d = json.loads(jsontext)
        d['id'] = id
        roomObject = Room(**d)
        break
    con.close()
    return roomObject

class Room():
    def __init__(self, id=0, name="A Room", description="An empty room", neighbors={}):
        """Create a Room object.

        Args:
            id (int, optional): Room Id. Defaults to 0.
            name (str, optional): Room name. Defaults to "A Room".
            description (str, optional): Room description. Defaults to "An empty room".
            neighbors (dict, optional): Dictionary where key = direction, value = corresponding room ID. Defaults to {}.
        """
        self.id = id
        self.name = name
        self.description = description
        self.neighbors = neighbors
        
    def neighbor(self, direction):
        """Method for finding neighboring room ID.

        Args:
            direction (str): Direction to find neboring room.

        Returns:
            int: Retruns corresponding room ID for the direction. None if room does not have a neighbor in that direction.
        """
        if direction in self.neighbors:
            return self.neighbors[direction]
        else:
            return None
