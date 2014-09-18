from flask.ext.security import Security, MongoEngineUserDatastore
from flask import Blueprint, render_template
from flask.views import MethodView
from podvesite.models import Role, User
from podvesite import db, app

main = Blueprint('main', __name__, template_folder='templates')
users = Blueprint('users', __name__, template_folder='templates')

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


# Register the urls
main.add_url_rule('/', view_func=ListView.as_view('list'))
users.add_url_rule('/users', view_func=UsersView.as_view('users'))
