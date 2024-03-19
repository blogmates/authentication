from flask import Flask

app = Flask(__name__)

@app.route('/sanity')
def sanity():
    return 'Server is up and running'

