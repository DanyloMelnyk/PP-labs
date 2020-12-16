from flask import Flask
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from blueprint import blueprint
from errors import validation_error, not_found_error

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.register_error_handler(ValidationError, validation_error)
app.register_error_handler(NoResultFound, not_found_error)


app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=True)
