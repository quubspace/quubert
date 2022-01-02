from app.database import db


class Hours(db.Model):
    __tablename__ = "hours"

    id = db.Column(db.BIGINT, primary_key=True)
    user_id = db.Column(db.ForeignKey("users.id"))
    quantity = db.Column(db.BIGINT)
    description = db.Column(db.Text)
    date = db.Column(db.Date)
