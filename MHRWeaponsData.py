import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests

# may need to loop together all of the webpages to scrape all of the weapons 
# the following weapons have special exceptions
# bow has coatings Affinity, Recovery, Brace are Arc Shots
# below the 4 levels are for the charge shot
# Compatiable coatings are the next one over. If there is no class value, it is a COMPATIABLE COATING. Else it is not compatiable. If the text is in green, they are enhanced coatings
# gunlance has different shelling types so will have to account for that - add extra code to add in the type of shelling and level
# hunting horn requires data about the music it has - add in extra code to determine each song
# switch axe and charge blade has phials - add extra code to extract phial information
# insect glaive has kinsect levels - add extra code to find kinsect level
# light and heavy bowgun has.... stuff - first column is the deviation, recoil, reload stats. Next column over is how many types of ammo it can shoot with how many shots
# sites go from view=0 to view=13
# 0 Great Sword
# 1 Sword and Shield
# 2 Dual Blades
# 3 Long Sword
# 4 Hammer
# 5 Hunting Horn
# 6 Lance
# 7 Gunlance
# 8 Switch Axe
# 9 Charge Blade
# 10 Insect Glaive
# 11 Bow
# 12 H Bowgun
# 13 L Bowgun

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
iteration = 11

# for loop here iterate by https://mhrise.kiranico.com/data/weapons?view=(i)
gsSite = "https://mhrise.kiranico.com/data/weapons?view=11"
gsPage = requests.get(gsSite, headers=headers)
soup = BeautifulSoup(gsPage.content, "html.parser")

weaponTable = soup.find("table")

rows = weaponTable.findChildren("tr")


# go through the entire table going through each row
for elem in rows:
    # get weapon name
    weaponName = elem.find(class_ = "text-sky-500 dark:text-sky-400 group-hover:text-sky-900 dark:group-hover:text-sky-300")
    #used to find the rampage skills
    weaponLink = weaponName['href']
    print(weaponName.get_text())

    # get deco slots and rampage slots
    slots = elem.find_all(class_ = "inline-flex items-center px-2 py-0.5 rounded text-xs font-medium mr-1 bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300")
    deco = slots[0]
    totalDeco = deco.find_all("img", src = True)
    # determine if there are decorations or not and then print how many decorations there are and the level
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

    # get the elemental damage defense affinity and sharpness level
    bonusesAndSharpness = elem.find_all("small")
    bonuses = bonusesAndSharpness[2]
    #print(bonuses)

    #elemental stats 
    elementalImg = bonuses.find("img")
    elementalVal = bonuses.find("span", {"data-key":"elementAttack"})
    if(elementalImg != None and elementalVal != None):
        elemental = elementalImg['src']
        if("ElementType1" in elemental):
            print("Fireblight: " + str(elementalVal.get_text()))
        elif("ElementType2" in elemental):
            print("Waterblight: " + str(elementalVal.get_text()))
        elif("ElementType3" in elemental):
            print("Thunderblight: "+ str(elementalVal.get_text()))
        elif("ElementType4" in elemental):
            print("Iceblight: " + str(elementalVal.get_text()))
        elif("ElementType5" in elemental):
            print("Dragonblight: " + str(elementalVal.get_text()))
        elif("ElementType6" in elemental):
            print("Poison Element: " + str(elementalVal.get_text()))
        elif("ElementType7" in elemental):
            print("Sleep Element: " + str(elementalVal.get_text()))
        elif("ElementType8" in elemental):
            print("Paralysis Element: " + str(elementalVal.get_text()))
        elif("ElementType9" in elemental):
            print("Blast Element: " + str(elementalVal.get_text()))
    else:
        print("NO ELEMENTAL")
    # both affinity and defense are under the div
    affinityOrDefense = bonuses.find_all("div")
    if(len(affinityOrDefense) != 0):
        # check if the div contains text for affinity or defense
        for elem in affinityOrDefense:
            values = elem.text
            parsedval = " ".join(values.split())
            print(parsedval)
    else:
        print("THERES NOTHING")

    # grabbing sharpness values
    sharpness = bonusesAndSharpness[3]
    isFirstRow = True
    sharpColor = []
    totalSharpness = sharpness.find_all("rect")
    if(len(totalSharpness) != 0):
        for elem in totalSharpness:
            # this is required in order for the max potential of sharpness of a weapon
            if(elem['fill'] in sharpColor):
                print("SECOND ROW NOW")
                isFirstRow = False
            print(elem['fill'] + " " + elem['width'])
            sharpColor.append(elem['fill'])

    # special cases
    # first - hunting horn songs and gunlance 
    if(iteration == 5 or iteration == 7 or iteration == 8 or iteration == 9 or iteration == 10):
        # grab the song names
        songsList = bonusesAndSharpness[4]
        #print(songsList)
        for elem in songsList:
            values = elem.text
            parsedval = " ".join(values.split())
            if(iteration == 5):
                print((elem.text).strip())
            else:
                print(parsedval)
    elif(iteration == 11):
        chargeShot = bonusesAndSharpness[3]
        print(chargeShot)
        bowCoating = bonusesAndSharpness[4]
        print(bowCoating)

    # grab the rampage skills from each weapon click on the link of the weapon(grab the url?)
    # grab url and then use bs4 to look at the skills 
    # skills are in div
    weaponPage = requests.get(weaponLink, headers=headers)
    innerSoup = BeautifulSoup(weaponPage.content, "html.parser")

    detailWeapon = innerSoup.find("table")
    skillsRow = detailWeapon.findChildren("td")
    skills = skillsRow[-1]
    rampageSkills = skills.find_all("a")

    if(len(rampageSkills) != 0):
        for elem in rampageSkills:
            print(elem.text)
    else:
        print("No Rampage Skills")

    
    print()
