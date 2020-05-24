from datetime import datetime

from flask import render_template, request, redirect, url_for
from sqlalchemy import desc

from app import app
from app import db
from .forms import FoodForm, DateForm
from .models import Food, LogDate
from .utils import total_by_food_element, total_by_food_date


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    log_dates: list of entry_date in log_date [(datetime.date(2020, 5, 24),),...]
    log_dates_format: ['May 24, 2020',...]
    food_by_dates: list of food items by date
    total_by_dates: list of dicts totals by food item
    {'date': 'May 24, 2020', 'protein': 0, 'carbohydrates': 0, 'fat': 0, 'calories': 0}
    """
    form = DateForm()
    dates = LogDate.query.all()

    log_dates = db.session.query(LogDate.entry_date) \
        .order_by(desc(LogDate.entry_date)) \
        .all()
    log_dates_format = [datetime.strftime(date[0], '%B %d, %Y') for date in log_dates]

    total_by_dates = [total_by_food_date(date.food, date.entry_date.strftime('%B %d, %Y'))
                      for date in dates]

    print(total_by_dates)
    if request.method == 'POST':
        date = request.form['date']
        log_date = LogDate(entry_date=date)
        db.session.add(log_date)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('base.html',
                           form=form,
                           dates=log_dates_format,
                           total_by_dates=total_by_dates)


@app.route('/total-by-day/<date>', methods=['GET', 'POST'])
def total_by_day(date):
    food_results = Food.query.all()
    log_date = LogDate.query. \
        filter(LogDate.entry_date == date) \
        .first()

    if log_date:
        log_date_format = log_date.entry_date.strftime('%B %d, %Y')
    else:
        log_date_format = datetime.today().strftime('%B %d, %Y')

    if request.method == 'POST':
        food_id = request.form['food-select']
        food = Food.query.filter(Food.id == food_id).first()
        log_date.food.append(food)
        db.session.commit()

    food_by_date = log_date.food
    total = total_by_food_element(food_by_date)
    return render_template('day.html',
                           date=log_date_format,
                           food_results=food_results,
                           food_by_date=food_by_date,
                           total=total)


@app.route('/food', methods=['GET', 'POST'])
def create_food():
    form = FoodForm()
    foods = Food.query.all()
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        protein = int(request.form['protein'])
        carbohydrates = int(request.form['carbohydrates'])
        fat = int(request.form['fat'])
        calories = 4 * protein + 4 * carbohydrates + 9 * fat
        food_item = Food(name=name,
                         protein=protein,
                         carbohydrates=carbohydrates,
                         calories=calories,
                         fat=fat)
        db.session.add(food_item)
        db.session.commit()
        return redirect(url_for('create_food'))
    return render_template('add_food.html', form=form, foods=foods)
