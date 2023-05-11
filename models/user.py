from app import db

class User(db.Model):
    id = db.column(db.Integer, primary_key=True)
    email= db.column(db.Integer, nullable=False,unique=True)
    username= db.column (db.String(100),nullable=False, unique=True)
    role= db.column(db.String(100), nullable=False)
    approved = db.column(db.string(100))
    password = db.column(db.String(255), nullable=False)