from market import app
from market import route
from market import db
from os import path
from market import DB_NAME
def create_database(app):
    if not path.exists('FlaskMarket/instance'+ DB_NAME):
        db.create_all(app=app)
if __name__ == '__main__':
    app.run(host='0.0.0.0')