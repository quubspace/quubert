from app.database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
