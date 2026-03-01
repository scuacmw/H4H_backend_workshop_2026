# flask imports
from flask import Flask, jsonify, request, render_template
import os
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

# firebase setup
import firebase_admin
from firebase_admin import credentials, firestore

cred_path = os.environ.get("FIREBASE_CREDENTIALS")

if not firebase_admin._apps: #if firebase has not been initialized yet

    cred = credentials.Certificate(cred_path) #load credentials
    firebase_admin.initialize_app(cred) #python app connects to firebase with the credentials

db = firestore.client()

# frontend folder at project root - so Flask can find our index.html
_frontend = Path(__file__).resolve().parent.parent.parent / "frontend"
app = Flask(__name__, template_folder=str(_frontend))


@app.route("/")
def index():
    return render_template("index.html")

# MAKE SURE to initialize collection in firestore called "users" for these methods to work
# method to get users from firestore
@app.route("/getUsers" , methods=["GET"])
def firebase_get():
    docs = db.collection("users").get()  # returns a list of documents
    if not docs:
        return jsonify({"error": "No documents found"}), 404
    return jsonify([doc.to_dict() for doc in docs])

# method to add users to firestore
@app.route("/addUsers", methods=["POST"])
def firebase_set():
    user_input = request.form.get('my_data')
    # Create the dictionary to store
    data = {"content": user_input}
    # Use .add() on the collection
    db.collection("users").add(data)
    return jsonify({"message": "User added successfully"}), 201

if __name__ == "__main__":
    app.run(port=8080,debug=True)
