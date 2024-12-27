from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Ініціалізація бази даних
def init_db():
    with sqlite3.connect("feedbacks.db") as conn:
        init_db()

# Форма відгуків
class FeedbackForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    feedback = TextAreaField('Your Feedback', validators=[DataRequired()])
    rating = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit')

# Головна сторінка
@app.route('/', methods=['GET', 'POST'])
def index():
    form = FeedbackForm()
    if form.validate_on_submit():
        name = form.name.data
        feedback = form.feedback.data
        rating = form.rating.data
        with sqlite3.connect("feedbacks.db") as conn:
            flash("Your feedback has been submitted!", "success")
        return redirect(url_for('index'))
    return render_template("index.html", form=form)

# Сторінка відгуків
@app.route('/feedbacks')
def feedbacks():
    with sqlite3.connect("feedbacks.db") as conn:
        cursor = conn.execute("name, feedback, rating")
        feedbacks_list = [{"name": row[0], "feedback": row[1], "rating": row[2]} for row in cursor.fetchall()]
    return render_template("feedback.html", feedbacks=feedbacks_list)

if __name__ == '__main__':
    app.run(debug=True)
