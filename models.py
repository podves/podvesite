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


class Place(db.Document):
    address = db.StringField(max_length=255)
    contact = db.StringField(max_length=255)
    time = db.StringField(max_length=255)
    capacity = db.DecimalField()
    comment = db.StringField(max_length=255)


class Course(db.Document):
    students = db.ListField(db.ReferenceField(User), default=[])
    teacher = db.ReferenceField(User)
    place = db.ReferenceField(Place)
    date = db.ReferenceField(Date)
