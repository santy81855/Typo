import firebase_admin
from firebase_admin import credentials, firestore
import config

cred = credentials.Certificate("DB/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_user(username):
    result = db.collection("users").document(username).get()
    if result.exists:
        return result.to_dict()
    else:
        return None

def set_user(username, data):
    db.collection('users').document(username).set(data)

def get_user_by_email(email):
    result = db.collection("users").where("email", "==", email).get()
    if result[0].exists:
        return result[0].to_dict()
    else:
        return None

def update_user_results(username, data):
    print("here")
    # get the current results
    curResults = db.collection('users').document(username).get().to_dict()['results']
    print(curResults)
    curResults.append(data)
    db.collection('users').document(username).update({'results' : curResults})