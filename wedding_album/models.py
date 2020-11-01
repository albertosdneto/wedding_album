from mongoengine.document import Document
from mongoengine.fields import StringField, ObjectIdField, URLField, BooleanField


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
