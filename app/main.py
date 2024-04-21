from flask import Flask, request, jsonify, Response, abort
import dataclasses
import jwt
import time
from datetime import datetime, timedelta  
app = Flask(__name__)

@app.route('/sanity')
def sanity():
    return 'Server is up and running'

password_db = {"vlad.visan87@gmail.com" : "manele manele"}
token_db = {}
secret_key = "delta_charlie"
valid_emails = ['@gmail.', '@yahoo.', '@ymail.']

@app.route("/auth", methods=["POST"])
def add_accounts():
    payload = request.get_json(silent=True)
    username = payload.get("username")
    password = payload.get("password")

    if not username or not password:
        error_message = 'error: field empty'
        print(error_message)
        #abort(401, description=error_message)
        return jsonify({error_message}), 400
    email_flag = 0
    for elem in valid_emails:
        if elem in username:
            email_flag = 1

    if not email_flag:
        error_message = "error: invalid email format"
        print(error_message)
        #abort(401, description=error_message)
        return jsonify({"error" : error_message}), 401 

    if username in password_db.keys():
        error_message = "error: email already in use"
        print(error_message)
        #abort(401, description=error_message)
        return jsonify({"error" : error_message}), 402
    
    password_db[username] = password

    return Response(status=201)

def generate_token(email):
    present_time = datetime.now()   
    exp_time = present_time + timedelta(hours=1) 
    return jwt.encode({
  "id": email,
  "email": email,
  "nbf": present_time,
  "exp": exp_time,
  "iat": present_time,
#   "iss": "https://my.app",
#   "aud": "https://my.app"
    },
  secret_key,
  algorithm="HS256",
  headers = {"alg": "HS256", "typ": "JWT"}), exp_time

@app.route("/login", methods=["POST"])
def validate_account():
    payload = request.get_json(silent=True)
    username = payload.get("username")
    password = payload.get("password")
    
    if username in password_db.keys():
        if not password_db[username] == password:
            error_message = "error: invalid credentials"
            print(error_message)
            #abort(401, description=error_message)
            return jsonify({"error" : error_message}), 401
        elif password_db[username] == password:
            token_db[username] = generate_token(username)
            return jsonify({"token": token_db[username][0], "time" : token_db[username][1]}), 201
    
    else:
        error_message = "error: invalid login"
        print(error_message)
        #abort(401, description=error_message)
        return jsonify({"error" : error_message}), 404
    
    error_message = "error: unknown error"
    print(error_message)
    #abort(401, description=error_message)
    return jsonify({"error" : error_message}), 405

def validate_token(token):
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        return jsonify({"status" : True}), 201
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({'error': 'Invalid Token', 'details': str(e)}), 402
    

@app.route("/validate", methods=["GET"])
def check_token():
    payload = request.get_json(silent=True)
    return validate_token(payload.get("token"))
    
@app.route("/refresh", methods=["POST"])
def refresh_token():
    payload = request.get_json(silent=True)
    username = payload.get("username")
    (_, check) = validate_token(payload.get("token"))
    if check == 401:
        token_db[username] = generate_token(username)
        return jsonify({"status" : "refreshed"}), 201
    return jsonify({"status" : "not refreshed"}), 201
