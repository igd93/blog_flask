from flask import Flask, request
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

class Post(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text)

    def __repr__(self):
        return f"<Post id = {self.id}>"

@app.before_first_request
def create_tables():
    db.create_all()
    db.session.commit()

@app.route('/')
def hello():
    return 'Hello World!'

@app.route("/posts", methods=['GET', 'POST'])
def create_post():
    content = request.get_json()
    post = Post(content=content["content"])
    db.session.add(post)
    db.session.commit()
    return 'Post created succesfully'




if __name__ == '__main__':
    app.run(debug=True)