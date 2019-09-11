from datetime import datetime
from exports.webApp import db


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"Author('{self.name}')"


class Post(db.Model):
    id = db.Column(db.String, primary_key=True, unique=True)
    date_posted = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=True)
    author = db.Column(db.Text, nullable=True)
    images = db.relationship("Image")
    videos = db.relationship("Video")
    nested = db.Column(db.Text, nullable=True)
    is_origin = db.Column(db.Boolean, unique=False, default=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"Post('{self.id}')"

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    def __repr__(self):
        return f"Image('{self.id}')"

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    def __repr__(self):
        return f"Image('{self.id}')"