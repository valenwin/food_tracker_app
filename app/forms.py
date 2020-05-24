from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, validators


class FoodForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField('Food Name',
                       validators=[validators.DataRequired(),
                                   validators.Length(min=2, max=80)])
    protein = IntegerField('Protein', validators=[validators.DataRequired()])
    carbohydrates = IntegerField('Carbohydrates', validators=[validators.DataRequired()])
    fat = IntegerField('Fat', validators=[validators.DataRequired()])


class DateForm(FlaskForm):
    class Meta:
        csrf = False

    date = DateField('New Day',
                     validators=[validators.DataRequired()],
                     format='%d-%m-%Y')
