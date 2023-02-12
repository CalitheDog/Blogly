from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from dateutil import tz

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://static.vecteezy.com/system/resources/thumbnails/002/318/271/small/user-profile-icon-free-vector.jpg"


def connect_db(app):
    """Connect to app to database"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """SQLAlchemy Users model"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    @property
    def full_name(self):

        if self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return self.first_name


class Post(db.Model):
    """SQLAlchemy posts model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(40),
                      nullable=False)

    content = db.Column(db.String(),
                        nullable=False)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship('User', backref=db.backref(
        'posts', cascade='all, delete-orphan'))

    def convert_created_at(self):
        f = "%b %d %Y %r"

        timestamp = self.created_at

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        timestamp = timestamp.replace(tzinfo=from_zone)
        timestamp = timestamp.astimezone(to_zone)

        return timestamp.strftime(f)

    @classmethod
    def recent_posts(cls):
        """Returns 5 most recent posts"""

        return cls.query.order_by(Post.created_at.desc()).limit(5).all()
