from flask.ext.security import Security, MongoEngineUserDatastore
from flask import Blueprint, render_template, redirect, url_for, flash
from flask.views import MethodView
from podvesite.models import Role, User, Place
from podvesite import db, app
from podvesite.htmlCalendar import MonthlyCalendar
from wtforms.validators import NumberRange, DataRequired

main = Blueprint('main', __name__, template_folder='templates')
users = Blueprint('users', __name__, template_folder='templates')
calendar = Blueprint('cal', __name__, template_folder='templates')
place = Blueprint('place', __name__, template_folder='templates')

from flask_security.forms import RegisterForm
from wtforms.fields import *


class ExtendedRegisterForm(RegisterForm):
    interests = SelectMultipleField(
        'INTERESNTS', choices=[('math', 'математика'), ('it', 'информатика'), ('literature', 'литература'), ('phylosophy', 'философия'), ('music', 'музыка'), ('languages', 'филология'), ('games', 'игры'), ('art', 'искусство')])

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore,
                    register_form=ExtendedRegisterForm)


class ListView(MethodView):

    def get(self):
        return render_template('index.html')


class UsersView(MethodView):

    def get(self):
        return render_template('users.html')


class CalendarView(MethodView):

    def get(self):
        outputFile = open("templates/calendar.html", 'w')
        calendar = MonthlyCalendar()
        outputFile.write(calendar.create())
        outputFile.close()
        return render_template('calendar.html')

from flask.ext.wtf import Form


class AddNewPlaceForm(Form):
    address = StringField(validators=[DataRequired()])
    contact = StringField(validators=[DataRequired()])
    time = StringField(validators=[DataRequired()])
    capacity = DecimalField(validators=[NumberRange(min=1, message="Please enter the integer number")])
    comment = StringField(validators=[DataRequired()])


class AddNewPlaceView(MethodView):

    def __init__(self):
        self.newPlaceForm = AddNewPlaceForm()

    def get(self):
        return render_template('new_place.html', form=self.newPlaceForm)

    def post(self):
        if self.newPlaceForm.validate():
            place = Place()
            place.address = str(self.newPlaceForm.address.data)
            place.contact = str(self.newPlaceForm.contact.data)
            place.time = str(self.newPlaceForm.time.data)
            place.comment = str(self.newPlaceForm.comment.data)
            place.capacity = int(self.newPlaceForm.capacity.data)
            place.save()
            flash('New place has been successfully registered!')
        else:
            return render_template('new_place.html', form=self.newPlaceForm)
        return redirect(url_for('place.new_place'))


# Register the urls
main.add_url_rule('/', view_func=ListView.as_view('list'))
users.add_url_rule('/users', view_func=UsersView.as_view('users'))
calendar.add_url_rule('/calendar', view_func=CalendarView.as_view('calend'))
place.add_url_rule(
    '/new_place', view_func=AddNewPlaceView.as_view('new_place'))
