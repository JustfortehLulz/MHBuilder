import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

website = "https://mhrise.kiranico.com/data/skills"
skillPage = requests.get(website, headers=headers)
soup = BeautifulSoup(skillPage.content, "html.parser")

createWeaponDB = r"C:\Users\JY\Documents\FlutterProject\mhbuilder\WeaponData.db"

conn = sqlite3.connect(createWeaponDB)

c = conn.cursor()

c.execute('''
            CREATE TABLE IF NOT EXISTS skillTable
            (
                SkillID integer PRMIARY KEY,
                skillName text,
                skillLevel integer,
                description text,
                bonuses text
            );
        ''')

skillTable = soup.find("table")

rows = skillTable.findChildren("tr")

for elem in rows:
    #print(elem)
    skillName = elem.find("p", {"class":"text-sm font-medium text-sky-500 dark:text-sky-400 group-hover:text-sky-900 dark:group-hover:text-sky-300"})
    print(skillName.text)

    skillDesc = elem.find("p", {"class":"truncate"})
    print(skillDesc.text)

    skillLvl = elem.find_all("small")
    for elem in skillLvl:
        if(elem.text != ""):
            wholeDesc = elem.text
            # grabs the level of the skill
            level = wholeDesc[:4]
            level = level.strip()
            # grabs the description of what each level does
            desc = wholeDesc[5:]
            print(level + " " + desc)

    print()