from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from models.post import Post, db
from dto.post_dto import PostDTO
from getpass import getpass, getuser
from service.json_encoder import CustomJSONEncoder

app = Flask(__name__)


username = 'root'
password = getpass()
host = 'localhost'
database = 'blog'
encoded_password = quote_plus(password)
url = f"mysql://{username}:{encoded_password}@{host}/{database}"

app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.json_encoder = CustomJSONEncoder


db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    db.session.commit()

@app.route('/')
def hello():
    return 'Hello World!'

@app.route("/posts", methods=['POST'])
def create_post():   
    content = request.get_json()
    post = Post(content=content["content"])
    db.session.add(post)
    db.session.commit()
    return jsonify({'id' : post.id}), 201 
    
@app.route("/posts", methods = ['GET'])
def get_posts():
    posts = Post.query.all()
    post_dtos = [PostDTO.from_model(post) for post in posts]    
    return jsonify(post_dtos)
    

if __name__ == '__main__':
    app.run(debug=True)