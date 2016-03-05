from application import app
from database import db


app.secret_key = 'some_secret_key!'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = app.secret_key
app.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:///test.db',
    SESSION_TYPE='sqlalchemy',
    SESSION_SQLALCHEMY=db
)
