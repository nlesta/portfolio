import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

player_points = pd.DataFrame(columns=['Player Name', 'Anytime TD Yes', 'Anytime TD No', 'Interceptions Over', 'Interceptions Under', 'Interceptions Line', 'Passing Yards Over', 'Passing Yards Under', 'Passing Yards Line', 'Rushing Yards Over', 'Rushing Yards Under', 'Rushing Yards Line', 'TD Passes Over', 'TD Passes Under', 'TD Passes Line', 'Receiving Yards Over', 'Receiving Yards Under', 'Receiving Yards Line', 'Receptions Over', 'Receptions Under', 'Receptions Line'])

def get_players():
    driver = webdriver.Chrome()
    driver.get("https://www.pinnacle.com/en/football/nfl/seattle-seahawks-vs-dallas-cowboys/1582399805/#all")
    wait = WebDriverWait(driver, 10)
    any_clickable_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[not(@disabled) and not(@aria-disabled)]")))
    html = driver.page_source

    # Parse the HTML string
    soup = BeautifulSoup(html, 'html.parser')
###
    # Extracting the name 'Brandin Cooks (Anytime TD)'
    name_element = soup.find_all('span', class_='')

    # Extracting the Money Line values
    #money_line_yes = soup.find('button', {'title': 'Yes'}).text
    #money_line_no = soup.find('button', {'title': 'No'}).text
    # Find all span elements with class=""
    #player_spans = soup.find_all('span', class_='')

    # Extract player names
    #player_names = []
    #for span in player_spans:
    #    match = re.search(r'(.*?) \(Anytime TD\)', span.text)
    #    if match:
    #        player_names.append(match.group(1))

    driver.quit()
    return name_element

#player_names_set = get_players()

#for player_name in player_names_set:
    #player_points = player_points.append({'Player Name': player_name}, ignore_index=True)

print(get_players())

<div data-collapsed="false" data-test-id="Collapse" class="style_primary__uMCOh style_marketGroup__rIPR4" style="order: 1;"><div class="style_title__2wOdP collapse-title style_collapseTitle__3EXI2"><span class="">Brandin Cooks (Receiving Yards)</span><span class="style_icon__3XP0a collapse-icon style_collapseIcon__GYHPV"><i class="icon-chevron-right-sml style_arrow__2EsIx style_expanded__3VpHF"></i></span></div><div class="style_content__23pgc collapse-content"><div class="style_buttons__2X8Y7 style_specials__13Hfh style_default__8VH8n style_twoColumns__Cdpo-"><div class="style_buttonRow__33Vfj"><div class="style_button-wrapper__2u2GV"><button title="Over 41.5 ReceivingYards" aria-label="Money Line -116" class="market-btn style_button__G9pbN style_pill__2U30o style_horizontal__3vGxa"><span class="style_label__3BBxD">Over 41.5 ReceivingYards</span><span class="style_price__3Haa9">1.862</span></button></div><div class="style_button-wrapper__2u2GV"><button title="Under 41.5 ReceivingYards" aria-label="Money Line -114" class="market-btn style_button__G9pbN style_pill__2U30o style_horizontal__3vGxa"><span class="style_label__3BBxD">Under 41.5 ReceivingYards</span><span class="style_price__3Haa9">1.877</span></button></div></div></div></div></div>