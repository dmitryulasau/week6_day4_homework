from flask import Flask, request, make_response, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
import json

class Config():
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

app = Flask(__name__)
app.config.from_object(Config)
db= SQLAlchemy(app)
migrate=Migrate(app,db)
basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def verify_password(email, password):
    u = User.query.filter_by(email=email).first()
    if u is None:
        return False
    g.current_user = u
    return u.check_hashed_password(password)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, index=True)
    password = db.Column(db.String)
    recipes = db.relationship("Recipe", backref='author',lazy="dynamic", cascade ='all, delete-orphan')

    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def from_dict(self,data):
        self.email = data['email']
        self.password=self.hash_password(data['password'])

    def to_dict(self):
        return {"user_id": self.user_id, "email":self.email}



class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    user_id = db.Column(db.ForeignKey('user.user_id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def from_dict(self, data):
        self.title = data['title']
        self.body = data['body']
        self.user_id = data['user_id']

    def to_dict(self):
        return {"recipe_id": self.recipe_id, "title":self.title, "body":self.body, "user_id":self.user_id}
##########################################################################################################
#USERS

@app.get('/user')
def get_users():
    """View all users"""
    users = User.query.all()
    return make_response(json.dumps([user.to_dict() for user in users]))

@app.get('/user/<id>')
def get_user(id):
    """View a user by id"""
    user = User.query.filter_by(user_id=id).first()
    return make_response(json.dumps(user.to_dict()))

@app.post('/user')
def post_user():
    """Create a user"""
    data = request.get_json()
    new_user = User()
    new_user.from_dict(data)
    new_user.save()
    return make_response("User is alive!", 200)

@app.put('/user/<id>')
def put_user(id):
    """Edit a user"""
    data = request.get_json()
    user = User.query.filter_by(user_id=id).first()
    if user:
        user.from_dict(data)
        user.save()
        return make_response(f"Success\n{json.dumps(user.to_dict())}", 200)
    return make_response("Error, no user.", 400)

@app.delete("/user/<id>")
def delete_user(id):
    """Delete a user"""
    User.query.filter_by(user_id=id).delete()
    db.session.commit()
    return make_response("User vanished.", 200)

# RECIPES

@app.get('/recipe')
def get_recipes():
    """View all recipes"""
    recipes = Recipe.query.all()
    return make_response(json.dumps([recipe.to_dict() for recipe in recipes]))

@app.get('/recipe-from/<id>')
def get_recipe_from(id):
    """View a recipe from user"""
    recipes = Recipe.query.filter_by(user_id=id)
    return make_response(json.dumps([recipe.to_dict() for recipe in recipes]))

@app.get('/recipe/<id>')
def get_recipe(id):
    """View a recipe by id"""
    recipe = Recipe.query.filter_by(recipe_id=id).first()
    return make_response(json.dumps(recipe.to_dict()))

@app.post('/recipe')
def post_recipe():
    """Add a recipe"""
    data = request.get_json()
    new = Recipe()
    new.from_dict(data)
    new.save()
    return make_response("Recipe was added!", 200)

@app.put('/recipe/<id>')
def put_recipe(id):
    """Edit a recipe"""
    data = request.get_json()
    recipe = Recipe.query.filter_by(recipe_id=id).first()
    if recipe:
        recipe.from_dict(data)
        recipe.save()
        return make_response(f"Success!\n{json.dumps(recipe.to_dict())}", 200)
    return make_response("No recipe!", 400)

@app.delete("/recipe/<id>")
def delete_recipe(id):
    """Delete a recipe"""
    Recipe.query.filter_by(recipe_id=id).delete()
    db.session.commit()
    return make_response("Before deleting recipe was made and eaten", 200)