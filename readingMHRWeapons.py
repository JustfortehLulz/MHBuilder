import sqlite3
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
driver = webdriver.Chrome()
driver.maximize_window()


# look for each of the weapons to get the data 
# need to ignore the first few links
driver.get("https://monsterhunterrise.wiki.fextralife.com/Great+Sword+Weapon+Tree")

greatSwordWeapon = driver.find_elements(By.XPATH,"//a[@class='wiki_link']")

# outputs each of the links found 
# goes to each of the link to recieve the data (defense, decorations,)
for gsLink in greatSwordWeapon:
    recLink = gsLink.get_attribute("href")
    print(recLink)
