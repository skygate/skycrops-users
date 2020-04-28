from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    orchards = db.relationship("Orchard", backref="author", lazy="dynamic")

    def __repr__(self):
        return f"<ID: {self.id}, User: {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Orchard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rows = db.Column(db.Integer)
    trees = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Orchard ID: {self.id}, Rows: {self.rows}, Trees in each row: {self.trees}>"