from flask import Flask, request, jsonify, Response, abort
import dataclasses

import time
import psycopg2
from psycopg2 import OperationalError
from datetime import datetime, timedelta  
app = Flask(__name__)


@app.route('/sanity')
def sanity():
    return 'Server is up and running'

password_db = {"vlad.visan87@gmail.com" : "manele manele"}
token_db = {}
secret_key = "delta_charlie"
valid_emails = ['@gmail.', '@yahoo.', '@ymail.']
url = "localhost"
port ="5432"

@app.route("/auth", methods=["POST"])
def add_accounts():
    try:
    # Connect to the default PostgreSQL database
        connection = psycopg2.connect(
            database="authDB",
            user="user",
            password="password",
            host=url,
            port=port
        )
    
        cursor = connection.cursor()

        payload = request.get_json(silent=True)
        username = payload.get("username")
        password = payload.get("password")

        sql = """
        INSERT INTO users (email, password, hash)
        VALUES (%s, %s, %s)        
        """
        vals = (username, password, None)
        cursor.execute(sql, vals)
        connection.commit()

        cursor.close()
        connection.close()

        return Response(status=201)
    except OperationalError as e:
        return Response(status=500), e


@app.route("/login", methods=["POST"])
def validate_account():
    payload = request.get_json(silent=True)
    username = payload.get("username")
    password = payload.get("password")
    try:
    # Connect to the default PostgreSQL database
        connection = psycopg2.connect(
            database="authDB",
            user="user",
            password="password",
            host=url,
            port=port
        )

        sql = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor = connection.cursor()


        # Execute the SQL statement
        cursor.execute(sql, (username, password))

        # Fetch the result
        result = cursor.fetchone()

        if result is not None:
            return Response(status=200)
        return Response(status=500)
    
    except OperationalError as e:
        return Response(status=500), e


# def validate_token(token):
#     try:
#         decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
#         return jsonify({"status" : True}), 201
#     except jwt.ExpiredSignatureError:
#         return jsonify({'error': 'Token has expired'}), 401
#     except jwt.InvalidTokenError as e:
#         return jsonify({'error': 'Invalid Token', 'details': str(e)}), 402
    

# @app.route("/validate", methods=["GET"])
# def check_token():
#     payload = request.get_json(silent=True)
#     return validate_token(payload.get("token"))
    
# @app.route("/refresh", methods=["POST"])
# def refresh_token():
#     payload = request.get_json(silent=True)
#     username = payload.get("username")
#     (_, check) = validate_token(payload.get("token"))
#     if check == 401:
#         token_db[username] = generate_token(username)
#         return jsonify({"status" : "refreshed"}), 201
#     return jsonify({"status" : "not refreshed"}), 201
