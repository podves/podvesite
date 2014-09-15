from flask.ext.security import UserMixin, RoleMixin
from podvesite import db


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class Date(db.Document):
    weekDay = db.DateTimeField()
    active = db.BooleanField(default=True)


class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    tariff = db.StringField(max_length=32)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    interests = db.ListField(db.StringField(max_length=255), default=[])
    roles = db.ListField(db.ReferenceField(Role), default=[])


class Course(db.Document):
    teacher = db.ReferenceField(User)
    place = db.StringField(max_length=255)
    date = db.ReferenceField(Date)
