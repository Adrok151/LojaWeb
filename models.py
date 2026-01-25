from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), nullable=False)
    preco = db.Column(db.Integer, nullable=False)
    imagem = db.Column(db.String(128), nullable=False)
    descricao = db.Column(db.String(256), nullable=False)
    categoria = db.Column(db.String(64), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash =  generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)