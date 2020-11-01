from mongoengine.document import Document
from mongoengine.fields import StringField, ObjectIdField, URLField, BooleanField, DateTimeField
import datetime


class User(Document):
    username = StringField(required=True, unique=True)
    name = StringField(required=False)
    password = StringField(required=True)
    role = StringField()

    meta = {
        'strict': False,
        'collection': 'users',
    }


class Photo(Document):
    user_id = ObjectIdField(required=True)
    username = StringField(required=False)
    url = URLField(required=True)
    public = BooleanField(required=True, default=False)

    meta = {
        'strict': False,
        'collection': 'photos',
    }


class Comment(Document):
    user_id = ObjectIdField(required=True)
    username = StringField()
    photo_id = ObjectIdField(required=True)
    content = StringField(required=True)
    created = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'strict': False,
        'collection': 'comments',
    }


class Like(Document):
    user_id = ObjectIdField(required=True)
    photo_id = ObjectIdField(required=True)

    meta = {
        'strict': False,
        'collection': 'likes',
    }
