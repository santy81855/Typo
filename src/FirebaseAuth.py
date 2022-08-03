import pyrebase, config, FirebaseDB

firebaseConfig = {
    'apiKey': "AIzaSyC9njlNqWr7JqfLgc2QPXxc8mqeOA_O-qI",
    'authDomain': "typo-f6f11.firebaseapp.com",
    'projectId': "typo-f6f11",
    'storageBucket': "typo-f6f11.appspot.com",
    'messagingSenderId': "435838278921",
    'appId': "1:435838278921:web:069c9a7f58cbed38ae07d8",
    'measurementId': "G-DLKKF9481M",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

def signup(email, password, first, last, username):
    try:
        user = auth.create_user_with_email_and_password(email.lower(), password)
        config.settings.setValue("user", user)
        config.settings.setValue("username", username)
        # give each new user an empty results page
        data = {'email' : email, 'first' : first, 'last' : last, 'username' : username, 'results' : []}
        FirebaseDB.set_user(username, data)
        return True
    except Exception as e:
        print(e)
        return False

def signin(email, password):
    try:
        config.settings.setValue("user", auth.sign_in_with_email_and_password(email.lower(), password))
        config.settings.setValue("username", FirebaseDB.get_user_by_email(email.lower())['username'])
        return True
    except Exception as e:
        print(e)
        return False
    
    