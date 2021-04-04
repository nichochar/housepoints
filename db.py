from google.cloud import firestore as gcloud_firestore
import firestore
import time
from user import User


class DB:
    def __init__(self):
        pass

    def get_houses(self):
        """ Return all houses """
        pass

    def update_house(self, house, points):
        """ Update the points for one house """
        pass

    def log_entry(self, house, points_diff, house_points, reason):
        """ Log a points change """
        pass

    def get_entries(self):
        """ Returns all entries of the ledger """
        pass

    def login_and_validate_user(self, username, password):
        """ Returns a User if correctly logged in, None if not """
        pass


class FirestoreDB(DB):
    def __init__(self):
        super().__init__()
        self.db = gcloud_firestore.Client()
        print("using FirestoreDB() for the Database")

    def get_houses(self):
        return firestore.get_houses(self.db)

    def update_house(self, house, points):
        return firestore.update_house(self.db, house, points)

    def log_entry(self, house, points_diff, house_points, reason):
        return firestore.log_entry(self.db, house, points_diff, house_points, reason)

    def get_entries(self):
        return firestore.get_entries(self.db)

    def login_and_validate_user(self, username, password):
        return firestore.login_and_validate_user(self.db, username, password)


class MemoryDB(DB):
    def __init__(self):
        super().__init__()
        self.db = {
            "houses": {
                "gryffindor": 10,
                "slytherin": 8,
                "hufflepuff": 6,
                "ravenclaw": 42
            },
            "users": {
                "headmaster": "password",
                "nichochar": "password"
            },
            "entries": [
                {
                    "house": "gryffindor",
                    "points_diff": 10,
                    "house_points": 10,
                    "reason": "really good reason",
                    "time": time.time()
                }
            ],
        }
        print("using MemoryDB() for the Database")

    def get_house(self, house):
        return {"name": house, "points": self.db["houses"][house]}

    def get_houses(self):
        return [{"name": name, "points": points} for name, points in self.db["houses"].items()]

    def update_house(self, house, points):
        self.db["houses"][house] += points
        return self.get_house(house)

    def log_entry(self, house, points_diff, house_points, reason):
        entry = {
            "house": house,
            "points_diff": points_diff,
            "house_points": house_points,
            "reason": reason,
            "time": time.time()
        }
        self.db["entries"].append(entry)
        return entry

    def get_entries(self):
        return self.db["entries"]

    def login_and_validate_user(self, username, password):
        for db_username, db_password in self.db["users"].items():
            if db_username == username and db_password == password:
                return User(username, True)
        return None


def get_db(debug):
    if debug is True:
        return MemoryDB()
    else:
       return FirestoreDB()
