from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
import pandas as pd

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def stuffs():
    t_n = [team_name.append(i) for i in col[0:][::9]]
    y = [year.append(i) for i in col[1:][::9]]
    w = [win.append(i) for i in col[2:][::9]]
    lo = [losses.append(i) for i in col[3:][::9]]
    ot_lo = [ot_losses.append(i) for i in col[4:][::9]]
    wi = [wins.append(i) for i in col[5:][::9]]
    gf = [g_f.append(i) for i in col[6:][::9]]
    ga = [g_a.append(i) for i in col[7:][::9]]
    l_c = [last_col.append(i) for i in col[8:][::9]]


def scrape_all():
    counter = 1

    while counter != 25:
        stuffs()        # Functions that defines the scraping itself
        counter += 1
        pagination = driver.find_element(By.PARTIAL_LINK_TEXT, str(counter))
        pagination.send_keys(keys.Keys.ENTER)


def dataframe():
    da = {
        str(header[0]): team_name,
        str(header[1]): year,
        str(header[2]): wins,
        str(header[3]): losses,
        str(header[4]): ot_losses,
        str(header[5]): win,
        str(header[6]): g_f,
        str(header[7]): g_a,
        str(header[8]): last_col
    }

    data = pd.DataFrame(da)
    return data


team_name = []
year = []
wins = []
losses = []
ot_losses = []
win = []
g_f = []
g_a = []
last_col = []


user = int(input("""
Hello there you can choose between two options:
    1 - You can choose to scrape the entire site
    2 - You can filter based on the teams on the site and then scrape the stats of the team
"""))

if user == 1:
    driver.get("https://www.scrapethissite.com/pages/forms/")
    cols = driver.find_elements(By.TAG_NAME, "td")
    col = [i.text for i in cols]

    head = driver.find_elements(By.TAG_NAME, 'th')
    header = [i.text for i in head]
    scrape_all()
    print(dataframe())
elif user == 2:
    driver.get("https://www.scrapethissite.com/pages/forms/")
    team = input('What team do you wish to scrape?\n-> ')
    search = driver.find_element(By.ID, 'q')
    search.send_keys(team)
    search.send_keys(keys.Keys.RETURN)
    cols = driver.find_elements(By.TAG_NAME, "td")
    col = [i.text for i in cols]

    head = driver.find_elements(By.TAG_NAME, 'th')
    header = [i.text for i in head]

    stuffs()
    print(dataframe())
