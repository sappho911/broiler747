# Code
from flask import Flask
from flask_cors import CORS
from api.api import register_routes


app = Flask(__name__)
CORS(app)
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

