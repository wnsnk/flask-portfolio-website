from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField, SelectMultipleField, BooleanField, SearchField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
import os
from operator import itemgetter
from github_scraper import GithubRepositoryNameScraper

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


@app.route("/")
def homepage():
    all_repos = github_scraper.offline_scrape_test()
    # all_repos = github_scraper.scrape()
    all_repos = sorted(all_repos, key=itemgetter('stars'))
    all_repos.reverse()

    return render_template('index.html', name=full_name, occupation=OCCUPATION, github=github_url, repositories=all_repos)


if __name__ == '__main__':
    app.run(debug=True)
