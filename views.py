from flask.ext.security import Security, MongoEngineUserDatastore, \
    current_user, login_required
from flask.ext.wtf import Form
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask.views import MethodView
from podvesite.models import Role, User, Place
from podvesite import db, app
from podvesite.htmlCalendar import MonthlyCalendar
from wtforms.validators import NumberRange, DataRequired
from flask_security.forms import RegisterForm, LoginForm
from wtforms.fields import *

main = Blueprint('main', __name__, template_folder='templates')
users = Blueprint('users', __name__, template_folder='templates')
calendar = Blueprint('cal', __name__, template_folder='templates')
place = Blueprint('place', __name__, template_folder='templates')
profile = Blueprint('profile', __name__, template_folder='templates')
admin = Blueprint('admin', __name__, template_folder='templates')


class ExtendedRegisterForm(RegisterForm):
    get_array_from_database = [('math', 'математика'),
                               ('it', 'информатика'), ('literature',
                                                       'литература'),
                               ('phylosophy',
                                'философия'), ('music', 'музыка'),
                               ('languages', 'филология'), ('games', 'игры'),
                               ('art', 'искусство')]
    interests = SelectMultipleField(
        'INTERESNTS', choices=get_array_from_database)
    email = TextField('Адрес электронной почты')
    password = PasswordField('Пароль')
    password_confirm = PasswordField('Подтвердите пароль')
    submit = SubmitField('Зарегистрироваться')


class ExtendedLoginForm(LoginForm):
    email = TextField('Адрес электронной почты')
    password = PasswordField('Пароль')
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


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


class ProfileView(MethodView):

    def get(self):
        items = User.objects.get_or_404(email=current_user.email)
        return render_template('profile.html', items=items)


class ProfileViewEdit(MethodView):

    def get(self):

        class ProfileEditForm(Form):
            email = StringField(default=current_user.email)

        self.EditForm = ProfileEditForm()
        return render_template('profile_edit_form.html', form=self.EditForm)


class AddNewPlaceForm(Form):
    address = StringField(validators=[DataRequired()])
    contact = StringField(validators=[DataRequired()])
    time = StringField(validators=[DataRequired()])
    capacity = DecimalField(
        validators=[NumberRange(min=1,
                                message="Please enter the integer number")])
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


class MainRoleForm(Form):
    name = StringField('Роль', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField('Добавить', description="Добавить роль")


class AdminView(MethodView):

    def __init__(self):
        self.RoleForm = MainRoleForm()

    @login_required
    def get(self, slug):

        if slug is None:
            return render_template('admin.html')
        elif slug == 'roles':
            return render_template('roles.html', form=self.RoleForm,
                                   roles=Role.objects.all())
        else:
            abort(404)

    @login_required
    def post(self, slug):
        if slug == 'roles':
            if self.RoleForm.validate():
                roles = Role()
                roles.name = str(self.RoleForm.name.data)
                roles.description = str(self.RoleForm.description.data)
                roles.save()
                flash('Новая роль успешно добавлена.')
            else:
                return render_template('roles.html', form=self.RoleForm)
        return redirect(url_for('admin.admin') + slug)


user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore,
                    register_form=ExtendedRegisterForm,
                    login_form=ExtendedLoginForm)

# Register the urls
main.add_url_rule('/', view_func=ListView.as_view('list'))
users.add_url_rule('/users', view_func=UsersView.as_view('users'))
calendar.add_url_rule('/calendar', view_func=CalendarView.as_view('calend'))
place.add_url_rule(
    '/new_place', view_func=AddNewPlaceView.as_view('new_place'))
profile.add_url_rule(
    '/profile', view_func=ProfileView.as_view('profile'))
profile.add_url_rule(
    '/profile/edit/', view_func=ProfileViewEdit.as_view('profile_edit'))
admin.add_url_rule(
    '/admin/', defaults={'slug': None}, view_func=AdminView.as_view('admin'))
admin.add_url_rule(
    '/admin/<slug>', view_func=AdminView.as_view('some'))
