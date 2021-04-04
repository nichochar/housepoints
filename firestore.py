import time
from google.cloud import firestore
from user import User


def document_to_dict(doc):
    if not doc.exists:
        return None
    doc_dict = doc.to_dict()
    doc_dict['id'] = doc.id
    return doc_dict


def get_houses():
    db = firestore.Client()
    query = db.collection(u'houses')
    houses = query.stream()

    return [document_to_dict(house) for house in houses]


def update(data):
    db = firestore.Client()
    house_id = data["house"]
    points = int(data["points"])
    house_ref = db.collection(u'houses').document(house_id)
    house_ref.update({"points": firestore.Increment(points)})

    return document_to_dict(house_ref.get())

def log_entry(house, points_diff, house_points, reason):
    db = firestore.Client()

    ledger_id = str(int(time.time()))
    data = {
        'house': house,
        'points_diff': points_diff,
        'house_points': house_points,
        'reason': reason,
        'time': firestore.SERVER_TIMESTAMP,
    }
    new_ledger = db.collection(u'ledger').document(ledger_id).set(data)

    return data

def get_entries():
    db = firestore.Client()

    query = db.collection(u'ledger')
    entries = query.stream()

    return [document_to_dict(entry) for entry in entries]

def login_and_validate_user(username, password):
    db = firestore.Client()
    query = db.collection(u'users').where(u'username', u'==', username)
    wanted_users = query.get()

    if not wanted_users or len(wanted_users) > 1:
        print("Could not find user")
        return None

    wanted_user = document_to_dict(wanted_users[0])
    if wanted_user['password'] == password:
        return User(username, True)

    print("Found user but password was wrong")
    return None

