from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField, SelectMultipleField, BooleanField, SearchField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5


NAME = 'name'
OCCUPATION = 'job'
GITHUB_LINK = 'https://github.com/wnsnk'

app = Flask(__name__)
app.secret_key = 'super secret key'
Bootstrap = Bootstrap5(app=app)


@app.route("/")
def homepage():
    return render_template('index.html', name=NAME, occupation=OCCUPATION, github=GITHUB_LINK)


if __name__ == '__main__':
    app.run(debug=True)
