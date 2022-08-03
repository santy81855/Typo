import pyrebase, config

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

def signup(email, password):
    try:
        config.settings.setValue("user", auth.create_user_with_email_and_password(email.lower(), password))
        print(config.settings.value("user"))
        return True
    except Exception as e:
        print(e)
        return False

def signin(email, password):
    try:
        config.settings.setValue("user", auth.sign_in_with_email_and_password(email.lower(), password))
        print(auth.get_account_info(config.settings.value("user")['idToken']))
        return True
    except Exception as e:
        print(e)
        return False
    
    