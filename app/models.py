from functools import partial

from slugify import slugify
from sqlalchemy import Column

from app import db

NotNullColumn = partial(Column, nullable=False)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = NotNullColumn(db.String(500))
    protein = NotNullColumn(db.Integer)
    carbohydrates = NotNullColumn(db.Integer)
    fat = NotNullColumn(db.Integer)
    calories = NotNullColumn(db.Integer)
    slug = db.Column(db.String, nullable=True)

    def __init__(self, *args, **kwargs):
        if 'slug' not in kwargs:
            kwargs['slug'] = slugify(kwargs.get('name', ''))
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<Food: {}>'.format(self.name)


class LogDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date)
    food = db.relationship('Food',
                           secondary='food_date',
                           backref=db.backref('food', cascade='delete', lazy='dynamic'))

    def __repr__(self):
        return '<Date: {}>'.format(self.entry_date)


food_date = db.Table('food_date',
                     db.Column('food_id', db.Integer, db.ForeignKey('food.id')),
                     db.Column('log_date_id', db.Integer, db.ForeignKey('log_date.id'))
                     )
