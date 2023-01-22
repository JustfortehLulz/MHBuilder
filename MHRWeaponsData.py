import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests

gsSite = "https://mhrise.kiranico.com/data/weapons?view=0"
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
gsPage = requests.get(gsSite, headers=headers)
soup = BeautifulSoup(gsPage.content, "html.parser")

weaponTable = soup.find("table")

rows = weaponTable.findChildren("tr")

#print(rows)

# go through the entire table going through each row
for elem in rows:
    # get weapon name
    weaponName = elem.find(class_ = "text-sky-500 dark:text-sky-400 group-hover:text-sky-900 dark:group-hover:text-sky-300")
    print(weaponName.get_text())

    # get deco slots and rampage slots
    slots = elem.find_all(class_ = "inline-flex items-center px-2 py-0.5 rounded text-xs font-medium mr-1 bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300")
    deco = slots[0]
    #print(deco.find_all("img", src = True))
    totalDeco = deco.find_all("img", src = True)
    # determine if there are decorations or not and then print how many decorations there are
    if(len(totalDeco) == 0):
        print("THERE ARE NO DECORATIONS")
    else:
        for foundDeco in totalDeco:
            levelDeco = foundDeco['src']
            if("deco1" in levelDeco):
                print("DECORATION LEVEL 1")
            elif("deco2" in levelDeco):
                print("DECORATION LEVEL 2")
            elif("deco3" in levelDeco):
                print("DECORATION LEVEL 3")
            elif("deco4" in levelDeco):
                print("DECORATION LEVEL 4")

    # same process as finding decorations
    rampageDeco = slots[1]
    totalRampageDeco = rampageDeco.find_all("img", src = True)
    if(len(totalRampageDeco) == 0):
        print("THERE ARE NO RAMPAGE DECORATIONS")
    else:
        for foundRampage in totalRampageDeco:
            levelRampage = foundRampage['src']
            if("deco1" in levelRampage):
                print("RAMPAGE LEVEL 1")
            elif("deco2" in levelRampage):
                print("RAMPAGE LEVEL 2")
            elif("deco3" in levelRampage):
                print("RAMPAGE LEVEL 3")
            elif("deco4" in levelRampage):
                print("RAMPAGE LEVEL 4")

    # get attack value
    weaponAttackVal = elem.find("div", {"data-key":"attack"})

    print("Attack Value: " + weaponAttackVal.get_text())

    # get the bonuses and stuff
    # find the defense value
    stuff = elem.find("small", attrs={"div"})
    print(stuff)

    print()