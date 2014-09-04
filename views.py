from flask.ext.security import Security, MongoEngineUserDatastore
from flask import Blueprint, render_template
from flask.views import MethodView
from podvesite.models import Role, User
from podvesite import db, app

posts = Blueprint('posts', __name__, template_folder='templates')

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)


class ListView(MethodView):

    def get(self):
        return render_template('index.html')


# Register the urls
posts.add_url_rule('/', view_func=ListView.as_view('list'))
