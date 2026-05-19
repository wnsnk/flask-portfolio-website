from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

load_dotenv()


class GithubRepositoryNameScraper():
    def __init__(self, github_username):
        self.username = github_username
        self.url = f'https://github.com/{self.username}?tab=repositories'

    def scrape(self):
        '''scrapes the repositories tab of a user and returns all repositories in a list of dictionaries'''
        self.response = requests.get(self.url, headers={
                                     'User-Agent': os.getenv('USER_AGENT')})
        print(self.response)
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.all_repositories = []

        repositories_div = self.soup.find(
            'div', id='user-repositories-list')
        repositories = repositories_div.find_all('li')

        for repository in repositories:
            name = repository.find('h3').text
            name = name.replace('Public', '')
            name = name.strip()
            try:
                description = repository.find('p', class_='col-9').text
            except AttributeError:
                description = None
            else:
                description = description.strip()

            language = repository.find(
                'span', itemprop='programmingLanguage').text

            last_updated = repository.find('relative-time').text

            try:
                star_amount = repository.find('a', class_='Link--muted').text
            except AttributeError:
                star_amount = 0
            else:
                star_amount = star_amount.strip()
                star_amount = int(star_amount)

            repository_dict = {'name': name,
                               'description': description,
                               'language': language,
                               'last_updated': last_updated,
                               'stars': star_amount}
            self.all_repositories.append(repository_dict)
        return self.all_repositories

    def offline_scrape_test(self):
        with open('github.html', 'r') as github_html:
            github_html = github_html.read()

        self.soup = BeautifulSoup(github_html, 'html.parser')
        repositories_div = self.soup.find(
            'div', id='user-repositories-list')
        print(type(repositories_div))
        repositories = repositories_div.find_all('li')

        for repository in repositories:
            name = repository.find('h3').text
            name = name.replace('Public', '')
            name = name.strip()
            try:
                description = repository.find('p', class_='col-9').text
            except AttributeError:
                description = None
            else:
                description = description.strip()

            language = repository.find(
                'span', itemprop='programmingLanguage').text

            last_updated = repository.find('relative-time').text

            try:
                star_amount = repository.find('a', class_='Link--muted').text
            except AttributeError:
                star_amount = 0
            else:
                star_amount = star_amount.strip()
                star_amount = int(star_amount)
            print(name)
            print(description)
            print(language)
            print(last_updated)
            print('Stars:', star_amount)
            print('')
