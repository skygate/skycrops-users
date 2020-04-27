from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    orchards = db.relationship('Orchard', backref='author', lazy='dynamic')

    def __repr__(self):
        return f"<ID: {self.id} User: {self.username}>"


class Orchard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rows = db.Column(db.Integer)
    trees = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Orchard ID: {self.id} Rows: {self.rows}, Trees: {self.trees}>"
