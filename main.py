import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)

Bootstrap(app)

app.config['SECRET_KEY'] = os.environ['day_56_key']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Integer, nullable=False)
    has_wifi = db.Column(db.Integer, nullable=False)
    has_sockets = db.Column(db.Integer, nullable=False)
    can_take_calls = db.Column(db.Integer, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

class CafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Google Maps Link", validators=[DataRequired(), URL()])
    img_url = StringField("Image Link", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    seats = StringField("Number of Seats", validators=[DataRequired()])
    has_toilet = SelectField('Has Toilets? (0 for no, 1 for yes)', validators=[DataRequired()], choices={0: 0, 1: 1})
    has_wifi = SelectField('Has Wifi? (0 for no, 1 for yes)', validators=[DataRequired()], choices={0: 0, 1: 1})
    has_sockets = SelectField('Has Sockets? (0 for no, 1 for yes)', validators=[DataRequired()], choices={0: 0, 1: 1})
    can_take_calls = SelectField('Can Take Calls? (0 for no, 1 for yes)', validators=[DataRequired()], choices={0: 0, 1: 1})
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    cafes = Cafe.query.all()
    return render_template("home.html", cafes=cafes)

@app.route("/add", methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name = form.name.data,
            map_url = form.map_url.data,
            img_url = form.img_url.data,
            location = form.location.data,
            seats = form.seats.data,
            has_toilet = form.has_toilet.data,
            has_wifi = form.has_wifi.data,
            has_sockets = form.has_sockets.data,
            can_take_calls = form.can_take_calls.data,
            coffee_price = form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_cafe.html', form=form)

@app.route("/edit/<int:cafe_id>", methods=['GET', 'POST'])
def edit_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    form = CafeForm(
        name = cafe.name,
        map_url = cafe.map_url,
        img_url = cafe.img_url,
        location = cafe.location,
        seats = cafe.seats,
        has_toilet = cafe.has_toilet,
        has_wifi = cafe.has_wifi,
        has_sockets = cafe.has_sockets,
        can_take_calls = cafe.can_take_calls,
        coffee_price = cafe.coffee_price,
    )
    if form.validate_on_submit():
        cafe.name = form.name.data
        cafe.map_url = form.map_url.data
        cafe.img_url = form.img_url.data
        cafe.location = form.location.data
        cafe.seats = form.seats.data
        cafe.has_toilet = form.has_toilet.data
        cafe.has_wifi = form.has_wifi.data
        cafe.has_sockets = form.has_sockets.data
        cafe.can_take_calls = form.can_take_calls.data
        cafe.coffee_price = form.coffee_price.data
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add_cafe.html", form=form)

@app.route("/delete/<int:cafe_id>", methods=['GET', 'POST'])
def delete(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)