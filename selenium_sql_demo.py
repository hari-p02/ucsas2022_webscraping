from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
import time
import sqlite3

def highlight(element, color, border):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    original_style = element.get_attribute('style')
    apply_style("border: {0}px solid {1};".format(border, color))
    time.sleep(0.01)
    apply_style(original_style)

conn = sqlite3.connect("quarter_backs.db")

cur = conn.cursor()

cur.execute("""CREATE TABLE player_stats (
            name TEXT,
            Pass_Yds REAL,
            Yds_Att	REAL,
            Att	REAL,
            Cmp	REAL,
            Cmp_percent	REAL,
            TD	REAL,
            INT	REAL,
            Rate REAL,
            First REAL,
            First_percent REAL,
            twenty_plus	REAL,
            forty_plus	REAL,
            Lng	REAL,
            Sck	REAL,
            SckY REAL
        )""")

cur.execute("""CREATE TABLE player_info (
            name TEXT,
            team TEXT,
            height TEXT,
            weight REAL,
            arms TEXT,
            hands REAL,
            experience REAL,
            college TEXT,
            age REAL,
            hometown TEXT
        )""")

PATH = 'chromedriver_win32\chromedriver.exe'
service = Service(PATH)
driver = webdriver.Chrome(service=service)
driver.get('https://www.nfl.com/stats/player-stats/')
time.sleep(2)


popup_later = driver.find_element(By.CSS_SELECTOR, "#onesignal-slidedown-cancel-button")
highlight(popup_later, "red", 5)
popup_later.click()

driver.execute_script("window.scrollTo(0, 450)")

def get_all_info(selector, exe_lst, info_lst):
    temp_lst = []
    row = driver.find_element(By.CSS_SELECTOR, selector)
    highlight(row, "red", 5)
    player_link = row.find_element(By.CSS_SELECTOR, "a")
    highlight(player_link, "red", 5)
    temp_lst.append(player_link.text)
    allc = row.find_elements(By.CSS_SELECTOR, "td")
    for val in allc[1::]:
        highlight(val, "red", 5)
        temp_lst.append(val.text)
    exe_lst.append(tuple(temp_lst))

    if player_link.text.strip() == "Ben Roethlisberger":
        return

    highlight(player_link, "red", 5)
    temp_lst2 = []
    temp_lst2.append(player_link.text)
    player_link.click()
    # time.sleep(2)
    team_name = driver.find_element(By.CSS_SELECTOR, "#main-content > div > div > section > div > div > div > div.nfl-c-player-header__team.nfl-u-hide-empty > a")
    # print(team_name.text)
    highlight(team_name, "red", 5)
    # print(team_name.text)
    temp_lst2.append(team_name.text)
    gen_vals = driver.find_elements(By.CSS_SELECTOR, ".nfl-c-player-info__value")
    for val in gen_vals:
        highlight(val, "red", 5)
        temp_lst2.append(val.text)
    info_lst.append(tuple(temp_lst2))
    driver.back()
    return

exe_lst = []
info_lst = []
for i in range(1, 26):
    selector = f"#main-content > section.d3-l-grid--outer.d3-l-section-row > div > div > div > div > table > tbody > tr:nth-child({i})"
    get_all_info(selector, exe_lst, info_lst)

cur.executemany("INSERT INTO player_stats VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", exe_lst)
cur.executemany("INSERT INTO player_info VALUES (?,?,?,?,?,?,?,?,?,?)", info_lst)
conn.commit()
conn.close()
time.sleep(2)

driver.close()

