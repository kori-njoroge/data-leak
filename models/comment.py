from .. import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact= db.Column(db.String(100), nullable=False,unique=True)
    comment= db.Column(db.String(100), nullable=False,unique=True)