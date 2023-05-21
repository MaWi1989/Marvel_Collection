from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash
import secrets
from flask_login import UserMixin, LoginManager

from flask_marshmallow import Marshmallow


db = SQLAlchemy()


login_manager = LoginManager()
ma = Marshmallow()



class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = False)
    last_name = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(150), nullable = False)
    username = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(150), nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    characters = db.relationship('Marvel_Character', backref = 'user', lazy = True)


    def __init__(self, first_name='', last_name='', email='', username='', password=''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = self.set_password(password)
        self.token = self.set_token(16)  


    def set_token(self, length):
        return secrets.token_hex(length)
        

    def set_id(self):
        return str(uuid.uuid4())
    
    
    def set_password(self, password):
        return generate_password_hash(password)
         

    def __repr__(self):
        return f"User {self.username} has been added to the database!"



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)




class Marvel_Character(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(300), nullable = True)
    series = db.Column(db.String(300))
    powers = db.Column(db.String(500))
    comics_appeared_in = db.Column(db.String(1000))
    first_appeared_in = db.Column(db.String(200))
    year_introduced = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable = False)

    
    
    def __init__(self, name, description, series, powers, comics_appeared_in, first_appeared_in, year_introduced, user_id, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.series = series
        self.powers = powers
        self.comics_appeared_in = comics_appeared_in
        self.first_appeared_in = first_appeared_in
        self.year_introduced = year_introduced
        self.user_id = user_id


    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f'The following Marvel Character has been added: {self.name}'



class Marvel_CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'series', 'powers', 'comics_appeared_in', 'first_appeared_in', 'year_introduced']


character_schema = Marvel_CharacterSchema()
all_characters_schema = Marvel_CharacterSchema(many = True)