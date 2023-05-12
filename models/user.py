from .. import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(100), nullable=False,unique=True)
    username= db.Column (db.String(100),nullable=False, unique=True)
    role= db.Column(db.String(100), nullable=False)
    approved = db.Column(db.String(100))
    password = db.Column(db.String(255), nullable=False)