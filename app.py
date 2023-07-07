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
def get_all_posts():
    posts = Post.query.all()
    post_dtos = [PostDTO.from_model(post) for post in posts]    
    return jsonify(post_dtos)

@app.route("/posts/<int:id>", methods = ['GET'])
def get_post(id):
    post = Post.query.get(id)
    if post:
        post_dto = PostDTO.from_model(post)
        return jsonify(post_dto)
    else:
        return jsonify({'message': 'Post not found'}), 404

@app.route("/posts/<int:id>", methods = ['PUT'])
def update_post(id):
    post = Post.query.get(id)
    if post:
        content = request.get_json()
        post.content = content['content']
        db.session.commit()
        return '', 204
    else:
        return jsonify({'message': 'Post not found'}), 404

@app.route("/posts/<int:id>", methods = ['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return '', 204
    else:
        return jsonify({'message': 'Post not found'}), 404        

 
    

if __name__ == '__main__':
    app.run(debug=True)