from flask import Flask
from flask import request
import sqlite3 as sql
import os as os
import json

database_path = os.getcwd() + "/database.db"
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def hello_world():
    return "Hello world"

@app.route('/patients', methods = ['GET'])
def list_patients():
    try:
        with sql.connect(database_path) as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            cur.execute("SELECT * FROM patients")

            print(cur.description[0])
            rows = [dict((cur.description[i][0], value) \
                    for i, value in enumerate(row)) for row in cur.fetchall()]
            return json.dumps(rows)

    except Exception as e:
        print(e)
        return "F" + str(e)

@app.route('/patients/create', methods = ['POST'])
def new_patient():
    if request.is_json:
        new_patient = request.json

        if not 'name' in new_patient:
            print("Name can't be null")
            return "Name can't be null"

        # Start creating sql command
        command = 'insert into patients(name'

        if 'city' in new_patient:
            command += ',city'
        if 'age' in new_patient:
            command += ',age'

        command += ') values(\"' + new_patient['name'] +'\"'

        if 'city' in new_patient:
            command += ',\"' + str(new_patient['city']) + '\"'
        if 'age' in new_patient:
            command += ',' + str(new_patient['age'])

        command += ')'

        print(command)

        with sql.connect(database_path) as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            cur.execute(command)

            return "success"

    else:
        return "Not json"
