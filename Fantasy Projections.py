def rb_wr_te():
    td_true = float(input("Enter odds for Anytime Touchdown Yes: "))
    td_false = float(input("Enter odds for Anytime Touchdown No: "))
    td_proj = 6*((1/td_true)/((1/td_true)+(1/td_false)))
    rec_yards_over = float(input("Enter the odds for Over Receiving Yards: "))
    rec_yards_under = float(input("Enter the odds for Under Receiving Yards: "))
    rec_yards = float(input("Enter the Receiving Yards line: "))
    rec_yards_proj = (rec_yards/10)*((1/rec_yards_over)/((1/rec_yards_over)+(1/rec_yards_under)) + .5)
    recep_over = float(input("Enter the odds for Receptions Over: "))
    recep_under = float(input("Enter the odds for Receptions Under: "))
    recep = float(input("Enter the Receptions line: "))
    recep_proj = recep*((1/recep_over)/((1/recep_over)+(1/recep_under)) + .5)
    rush_yards_over = float(input("Enter the odds for Over Rushing Yards: "))
    rush_yards_under = float(input("Enter the odds for Under Rushing Yards: "))
    rush_yards = float(input("Enter the Rushing Yards line: "))
    rush_yards_proj = (rush_yards/10)*((1/rush_yards_over)/((1/rush_yards_over)+(1/rush_yards_under)) + .5)
    total_proj = td_proj + rec_yards_proj + rush_yards_proj + recep_proj
    return "The projected fantasy points for this player is: " + str(round(total_proj, 2))

def qb():
    td_true = float(input("Enter odds for Anytime Touchdown Yes: "))
    td_false = float(input("Enter odds for Anytime Touchdown No: "))
    td_proj = 6*((1/td_true)/((1/td_true)+(1/td_false)))
    int_true = float(input("Enter the odds for Over Interceptions: "))
    int_false = float(input("Enter the odds for Under Interceptions: "))
    int_proj = -2*((1/int_true)/((1/int_true)+(1/int_false)))
    pass_yards_over = float(input("Enter the odds for Over Passing Yards: "))
    pass_yards_under = float(input("Enter the odds for Under Passing Yards: "))
    pass_yards = float(input("Enter the Passing Yards line: "))
    pass_yards_proj = (pass_yards*.04)*((1/pass_yards_over)/((1/pass_yards_over)+(1/pass_yards_under)) + .5)
    rush_yards_over = float(input("Enter the odds for Over Rushing Yards: "))
    rush_yards_under = float(input("Enter the odds for Under Rushing Yards: "))
    rush_yards = float(input("Enter the Rushing Yards line: "))
    rush_yards_proj = (rush_yards/10)*((1/rush_yards_over)/((1/rush_yards_over)+(1/rush_yards_under)) + .5)
    td_passes_over = float(input("Enter the odds for TD Passes Over: "))
    td_passes_under = float(input("Enter the odds for TD Passes Under: "))
    td_passes = float(input("Enter the TD Passes line: "))
    td_passes_proj = (td_passes*4)*((1/td_passes_over)/((1/td_passes_over)+(1/td_passes_under)) + .5)
    total_proj = td_proj + int_proj + pass_yards_proj + rush_yards_proj + td_passes_proj
    return "The projected fantasy points for this player is: " + str(round(total_proj, 2))


import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

driver = webdriver.Chrome()

driver.get("https://www.pinnacle.com/en/football/nfl/matchups/#period:0:spread")

title = driver.title

driver.implicitly_wait(10)

text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

text_box.send_keys("Selenium")
submit_button.click()

text = message.text

driver.quit()

# Now you can use BeautifulSoup to parse the page_html
from bs4 import BeautifulSoup

soup = BeautifulSoup(page_html, 'html.parser')

# Now you can work with the soup object as you would with BeautifulSoup
# For example, print the title of the page
print(soup.title.text)

def scrape_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    urls = []
    for link in soup.findAll('a', href=True):
        href = link['href']
        if href and href.startswith('/en/football'):
            urls.append(f"https://www.pinnacle.com{href}")

    return urls

# Replace 'https://example.com/en/football' with the actual URL of the website
starting_url = "https://www.pinnacle.com/en/football/nfl/matchups/"

urls = scrape_urls(starting_url)
print(urls)

