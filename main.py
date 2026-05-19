from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField, SelectMultipleField, BooleanField, SearchField, EmailField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
import os
from operator import itemgetter
from modules.github_scraper import GithubRepositoryNameScraper

load_dotenv()

FIRST_NAME = os.getenv('FIRST_NAME')
LAST_NAME = os.getenv('LAST_NAME')
OCCUPATION = os.getenv('OCCUPATION')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
GITHUB_USERNAME = ' [REMOVED]'


full_name = f'{FIRST_NAME} {LAST_NAME}'
github_url = f'https://github.com/{GITHUB_USERNAME}'

github_scraper = GithubRepositoryNameScraper(GITHUB_USERNAME)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
Bootstrap = Bootstrap5(app=app)


class ContactForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired()])
    message = CKEditorField('Message', validators=[DataRequired()])
    submit = SubmitField('Contact me!')


@app.route("/")
def homepage():
    all_repos = github_scraper.offline_scrape_test()
    # all_repos = github_scraper.scrape()
    all_repos = sorted(all_repos, key=itemgetter('stars'))
    all_repos.reverse()

    return render_template('index.html', name=full_name, occupation=OCCUPATION, github=github_url, repositories=all_repos)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        flash('Thanks for reaching out! I\'ll be in contact soon!')

    return render_template('contact.html', form=contact_form, name=full_name)


@app.route('/about')
def about_me():
    with open('about_me.txt', 'r') as about_me_txt:
        about_me_txt = about_me_txt.read()
    about_me_txt = about_me_txt.split('\n')
    return render_template('about.html', message=about_me_txt, name=full_name)


if __name__ == '__main__':
    app.run(debug=True)
