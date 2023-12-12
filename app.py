from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'you-will-never-guess'

# create an SQLAlchemy object named `db` and bind it to your app
db = SQLAlchemy(app)


app.app_context().push()

import routes


if __name__ == "__main__":
    app.run()
