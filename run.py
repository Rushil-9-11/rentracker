from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routes import main

app = Flask(__name__, template_folder='app/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app/rentracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
