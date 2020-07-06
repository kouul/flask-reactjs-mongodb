from flask import Flask, redirect, url_for
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# mongoClient = MongoClient("MongoDB Atlas connection url needs to be here...")
mongoClient = MongoClient('mongodb://127.0.0.1:27017')
db = mongoClient.get_database('names_db')
names_col = db.get_collection('names_col')

# Addname route
@app.route('/addname/<name>/')
def addname(name):
    names_col.insert_one({"name": name.lower()})
    return redirect(url_for('getnames'))

# GetNames route
@app.route('/getnames/')
def getnames():
    names_json = []
    if names_col.find({}):
        for name in names_col.find({}).sort("name"):
            names_json.append({"name": name['name'], "id": str(name['_id'])})
    return json.dumps(names_json)

# Run app
if __name__ == "__main__":
    app.run()