import os
from flask import Flask
from flask_migrate import Migrate
from model.models import db
from blueprints import kits, login, actuator, sensor, user, log, home


app = Flask(__name__, template_folder="view")
app.secret_key = "ndisanpsaiviwb2983123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'database.db')
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

    app.register_blueprint(login.login, url_prefix="")
    app.register_blueprint(login.logout, url_prefix="")
    app.register_blueprint(kits.kits, url_prefix="")
    app.register_blueprint(actuator.actuator, url_prefix="")
    app.register_blueprint(sensor.sensor, url_prefix="")
    app.register_blueprint(user.user, url_prefix="")
    app.register_blueprint(log.log, url_prefix="")
    app.register_blueprint(home.home, url_prefix="")
app.run(port=8080, debug=True)
