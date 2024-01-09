import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

def get_games():
    driver = webdriver.Chrome()
    driver.get("https://www.pinnacle.com/en/football/nfl/matchups/#period:0")
    wait = WebDriverWait(driver, 10)
    html = driver.page_source

    # Parse the HTML string
    soup = BeautifulSoup(html, 'html.parser')

    urls = set()
    pattern = re.compile(r'/en/football/nfl/([a-z0-9-]+)/(\d+)/')

    for link in BeautifulSoup(html, 'lxml').findAll('a', href=True):
        href = link['href']
        if re.match(pattern, href):
            urls.add(f"https://www.pinnacle.com{href}")


    driver.quit()
    return urls

games = get_games()

def get_players(games):
    for game in games:
        driver = webdriver.Chrome()
        driver.get(game)
        wait = WebDriverWait(driver, 10)
        html = driver.page_source

        # Parse the HTML string
        soup = BeautifulSoup(html, 'html.parser')

        names = set()
        pattern = re.compile(r'/en/football/nfl/([a-z0-9-]+)/(\d+)/')

        for link in BeautifulSoup(html, 'lxml').findAll('a', href=True):
            href = link['href']
            if re.match(pattern, href):
                urls.add(f"https://www.pinnacle.com{href}")


        driver.quit()
        return urls