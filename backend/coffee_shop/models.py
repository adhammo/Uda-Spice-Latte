from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, String, Integer
import json


def database_path(database_name):
    return f'postgresql://postgres:admin@localhost:5432/{database_name}'


db = SQLAlchemy()
migrate = Migrate(db=db)


def setup_db(app, database_name='coffee_shop'):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path(database_name)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    migrate.app = app
    migrate.init_app(app)


class Drink(db.Model):
    __tablename__ = 'drinks'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    recipe = Column(String, nullable=False)

    def __init__(self, title, recipe):
        self.title = title
        self.recipe = recipe

    def format_short(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': [{'color': r['color'], 'parts': r['parts']} for r in json.loads(self.recipe)]
        }

    def format_long(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }
