import json
import sqlite3
from sqlite3 import Error
from flask import Flask
from flask import request, render_template

DB_NAME = "db.sqlite"
users = [
    {
        "id": 1,
        "username": "john",
        "password": "P@ssw0rd@1234",
        "message": "You are a h4ck3r!"
    },
    {
        "id": 2,
        "username": "bob",
        "password": "P@ssw0rd@4321",
        "message": "Pwned"
    }
]
""" SQLite3"""
def seed():
    try:
        con = sqlite3.connect(DB_NAME)
        cursor = con.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id integer primary key, username text, pass_without_hash text);")
        cursor.execute("CREATE TABLE IF NOT EXISTS hidden_messages (id integer primary key, message text);")
        for user in users:
            cursor.execute("INSERT INTO users VALUES (?, ?, ?);", (user["id"], user["username"], user["password"]))
            cursor.execute("INSERT INTO hidden_messages VALUES (?, ?);", (user["id"], user["message"]))
            print("user added")
        rows = cursor.execute("SELECT * FROM users;").fetchall()
        con.commit()
    except Error as error:
        print(error)
    finally:
        con.close()

seed()

def login_sqli(password):
    try:
        con = sqlite3.connect(DB_NAME)
        cursor = con.cursor()
        sql = 'SELECT * FROM users WHERE pass_without_hash is "%s";'%password
        print(f"SQLInjection try with [{sql}]")
        rows = cursor.execute(sql).fetchall()
        response = []
        for row in rows:
            for el in row:
                response.append(el)
        print(response)
        return len(rows) > 0, response, sql
    except Error as error:
        print(error)
    finally:
        con.close()

app = Flask(__name__, template_folder='')

@app.route('/')
def login_get():
    return render_template("index.html")


@app.route('/', methods=['POST',])
def login_post():
    password = request.form.get('password')
    logged, rows, sql = login_sqli(password)
    return render_template("index.html", data={
        "logged": logged,
        "rows": rows,
        "sql": sql
    })
