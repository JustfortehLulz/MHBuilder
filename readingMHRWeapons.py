import sqlite3
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
driver = webdriver.Chrome()
driver.maximize_window()

gsList = []

# look for each of the weapons to get the data 
# need to ignore the first few links
driver.get("https://monsterhunterrise.wiki.fextralife.com/Great+Sword+Weapon+Tree")

greatSwordWeapon = driver.find_elements(By.XPATH,"//a[@class='wiki_link']")


for gsLink in greatSwordWeapon[4:-9]:
    
    recLink = gsLink.get_attribute("href")
    print(recLink)
    gsList.append(recLink)

print(gsList)

# id gets stale, needs another tab to go through all links
isFirstTab = True

# outputs each of the links found 
# goes to each of the link to recieve the data (defense, decorations,)

for weapon in gsList:
    if isFirstTab:
        driver.get(weapon)
        isFirstTab = False
        # need to find data for the first weapon
    else:
        driver.execute_script("window.open('about:blank', 'secondtab');")
        driver.switch_to.window("secondtab")
        driver.get(weapon)
        # get the link and go to it
        # defense stat
        try:
            defenseStat = driver.find_element(By.XPATH, "//a[@title = 'Monster Hunter Rise Defense']/..")
            defenseStatVal = defenseStat.text
            if "--" in defenseStatVal:
                defenseStatVal = '0'; 
            print(defenseStatVal)
        except:
            defenseStatVal = "N/A"
            print(defenseStatVal)
        # decorations
        try:
            decoration = driver.find_element(By.XPATH,"//a[@title='Monster Hunter Rise Decorations']/..")
            decorationVal = decoration.text
            if "--" in decorationVal:
                decorationVal = "None"
            else:
                availDeco = driver.find_elements(By.XPATH, "//a[@title='Monster Hunter Rise Decorations']/../img")
                for decos in availDeco:
                    decoSlot = decos.get_attribute("alt")
                    if "level 1 rampage" in decoSlot:
                        decoVal = "level 1 rampage"
                    elif "level 2 rampage" in decoSlot:
                        decoVal = "level 2 rampage"
                    elif "level 3 rampage" in decoSlot:
                        decoVal = "level 3 rampage"
        except:
