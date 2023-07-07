from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from urllib.parse import quote_plus

app = Flask(__name__)


username = 'root'
password = 'Wedge8Quantum@'
host = 'localhost'
database = 'blog'
encoded_password = quote_plus(password)
url = f"mysql://{username}:{encoded_password}@{host}/{database}"

app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)



@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)