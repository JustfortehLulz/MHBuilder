import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

# different path
createWeaponDB = r"D:\Coding_Projects\flutter_windows_3.7.3-stable\flutter_code\MHBuilder\MHBuilderWeaponData.db"

conn = sqlite3.connect(createWeaponDB)

c = conn.cursor()

c.execute('''
            CREATE TABLE IF NOT EXISTS armorTable
            (
                armorID integer PRIMARY KEY,
                name text,
                defense integer,
                fire_resistance integer,
                water_resistance integer,
                ice_resistance integer,
                thunder_resistance integer,
                dragon_resistance integer
            );
        ''')

# c.execute('''
#             CREATE TABLE IF NOT EXISTS decorationSlotsTable
#             (
#                 [name] text,
#                 [decoration_level] text,
#                 rampage_level text
#                 weaponID integer,
#                 armorID integer,
#                 PRIMARY KEY (name,decoration_level),
#                 FOREIGN KEY(weaponID) REFERENCES weaponTable(weaponID),
#                 FOREIGN KEY(armorID) REFERENCES armorTable(armorID)
#             )
#         ''')

# there are multiple pages with the armor values view=0 to view=9
i = 0
while i < 10:
    website = "https://mhrise.kiranico.com/data/armors?view=" + str(i)
    armorPage = requests.get(website, headers=headers)
    soup = BeautifulSoup(armorPage.content, "html.parser")

    # order of the resistance values
    resistTable = ["Defense","Fire Resistance","Water Resistance", "Ice Resistance", "Thunder Resistance", "Dragon Resistance"]
    armorTable = soup.find("table")

    rows = armorTable.findChildren("tr")

    for elem in rows:
        #print(elem)

        armorName = elem.find("a", {"class":"text-sky-500 dark:text-sky-400 group-hover:text-sky-900 dark:group-hover:text-sky-300"})
        
        #name of weapon
        print(armorName.text)

        # get defense and elemental resistances and skills
        defAndResist = elem.find_all("div")  
        #print(defAndResist)
        for i in range(len(defAndResist)):
            values = defAndResist[i].text
            if(i > 5):
                print("Now we talking skills")
            print(values.strip())

        deco = elem.find_all("img", src = True)
        #print(deco)
        if(len(deco) == 0):
            print("THERE ARE NO DECORATIONS")
        else:  
            for foundDeco in deco:
                levelDeco = foundDeco['src']
                if("deco1" in levelDeco):
                    print("DECORATION LEVEL 1")
                elif("deco2" in levelDeco):
                    print("DECORATION LEVEL 2")
                elif("deco3" in levelDeco):
                    print("DECORATION LEVEL 3")
                elif("deco4" in levelDeco):
                    print("DECORATION LEVEL 4")
        print()
    i = i + 1