import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests


headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

### for rampage skills
website = "https://mhrise.kiranico.com/data/rampage-skills"
skillPage = requests.get(website, headers=headers)
soup = BeautifulSoup(skillPage.content, "html.parser")

skillTable = soup.find("table")

rows = skillTable.findChildren("tr")

for elem in rows:
    # print(elem)
    column = elem.find_all("td")
    skill = column[0]
    effect = column[1]

    skill = skill.text
    effect = effect.text
    print(skill)
    print(effect)
    print()