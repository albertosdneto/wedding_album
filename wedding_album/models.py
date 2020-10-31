from mongoengine.document import Document
from mongoengine.fields import StringField


class User(Document):
    username = StringField(required=True)
    password = StringField(required=True)

    meta = {
        'strict': False,
        'collection': 'users',
    }
