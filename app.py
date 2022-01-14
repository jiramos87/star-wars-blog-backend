from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager


app = Flask(__name__, static_folder='static', static_url_path='')
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///starwars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config["JWT_SECRET_KEY"] = "serverkey"
jwt = JWTManager(app)

CORS(app)

db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

if __name__ == "__main__":  
    from views import *
    app.run()