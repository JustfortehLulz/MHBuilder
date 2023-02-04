import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

### for rampage skills
website = "https://mhrise.kiranico.com/data/rampage-decorations"
skillPage = requests.get(website, headers=headers)
soup = BeautifulSoup(skillPage.content, "html.parser")

skillTable = soup.find("table")

rows = skillTable.findChildren("tr")

for elem in rows:
    # print(elem)
    column = elem.find_all("td")

    name = column[0]
    skill = column[1]
    desc = column[2]

    name = name.text
    print(name)
    skillName = skill.text
    print(skillName)
    link = skill.find("a")
    link = link['href']
    #print(link)

    # grabbing the true description of the skills by going into each pages
    if(link != ""):
        jewelPage = requests.get(link, headers=headers)
        innerSoup = BeautifulSoup(jewelPage.content, "html.parser")

        detailDescription = innerSoup.find("header", {"class" : "mb-9 space-y-1"})
        trueDesc = detailDescription.findChildren("p")
        trueDesc = trueDesc[1]
        trueDesc = trueDesc.text
        # contains what the skill really is
        print(trueDesc)


    # check if skill is only for certain weapons
    desc = desc.text

    openBracket = 0
    closeBracket = 0
    try:
        openBracket = desc.index('(')
        closeBracket = desc.index(')')
        #print(desc[openBracket+1:closeBracket])
        # determine if / is in there
        slash = desc.index('/')
        firstWeapon = desc[openBracket+1:slash]
        secondWeapon = desc[slash+1:closeBracket-5]
        print(firstWeapon)
        print(secondWeapon)
    except ValueError:
        # means that there is no /
        if(closeBracket != 0):
            weapon = desc[openBracket+1:closeBracket-5]
            print(weapon)
    print(desc)
    print()