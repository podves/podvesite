from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "podvesite"}
app.config["SECRET_KEY"] = "lm+<y]p2|/t+9j|tKd{kKT}x*VfLuNs;^/<:dT_XCIi)+j"
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
app.config[
    'SECURITY_PASSWORD_SALT'] = 'Xy/N!uQ6y4pisRUF%hFq[|p86.AXc.OiR>K<4mP'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_DEFAULT_REMEMBER_ME'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

db = MongoEngine(app)


def register_blueprints(app):
    # Prevents circular imports
    from podvesite.views import main, users, calendar, \
        place, profile, admin
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(calendar)
    app.register_blueprint(place)
    app.register_blueprint(profile)
    app.register_blueprint(admin)

register_blueprints(app)

if __name__ == '__main__':
    app.run()
