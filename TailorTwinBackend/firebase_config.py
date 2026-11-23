
import firebase_admin
from firebase_admin import credentials, firestore

# Connect to Firebase only if it is not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

# Firestore database connection
db = firestore.client()

print("Firebase connected successfully!")
