import sqlite3
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests

#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
driver = webdriver.Chrome()
driver.maximize_window()

deco = []
rampageDeco = []
bonuses = []

# look for each of the weapons to get the data 
# need to ignore the first few links
# this new link is way better https://mhrise.kiranico.com/
driver.get("https://mhrise.kiranico.com/data/weapons?view=0")

tableRow = driver.find_elements(By.XPATH, "//tbody/tr")
greatSwordName = ''

#print(tableRow)

# go row by row grabbing all the relevant information
for gs in tableRow:
    # gets the weapon name
    greatSwordName = gs.find_element(By.XPATH,"./td/a[@class='text-sky-500 dark:text-sky-400 group-hover:text-sky-900 dark:group-hover:text-sky-300']") # gs.text
    print(greatSwordName.text)

    # gets the deco slots and rampage slots
    decoSlots = gs.find_elements(By.XPATH,"./td/div/span[@class='inline-flex items-center px-2 py-0.5 rounded text-xs font-medium mr-1 bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300']")
    print(decoSlots[0].text)
    print(decoSlots[1].text)
    # decorations for weapon
    deco = decoSlots[0].find_elements(By.XPATH, "./img")
    # rampage decorations for weapons
    rampageDeco = decoSlots[1].find_elements(By.XPATH, "./img")
    # need to determine the level of the decorations
    if(len(deco) == 0):
        print("NO DECORATIONS")
    else:
        print("This how many decorations: " + str(len(deco)))
        for iDeco in deco:
            levelDeco = iDeco.get_attribute("src")
            if("deco1" in levelDeco):
                print("LEVEL 1")
            elif("deco2" in levelDeco):
                print("LEVEL 2")
            elif("deco3" in levelDeco):
                print("LEVEL 3")
            elif("deco4" in levelDeco):
                print("LEVEL 4")
    if(len(rampageDeco) == 0):
        print("NO RAMPAGE")
    else:
        print("This is how many rampage decorations: " + str(len(rampageDeco)))
        for iRampage in rampageDeco:
            levelRampage = iRampage.get_attribute("src")
            if("deco1" in levelRampage):
                print("LEVEL 1")
            elif("deco2" in levelRampage):
                print("LEVEL 2")
            elif("deco3" in levelRampage):
                print("LEVEL 3")
            elif("deco4" in levelRampage):
                print("LEVEL 4")

    # attack value of weapon
    attackStat = gs.find_element(By.XPATH, "./td/div[@data-key='attack']")
    attackVal = attackStat.text
    print(attackVal)

    # defense value, affinity value, elemental damage, status damage 
    # for defense and affinity need to find out if there is 1 or 2 divs
    # then determine if its affinity(use text-red-600 or text-green-500) or defense
    # then extract the defense value
    bonuses = gs.find_elements(By.XPATH, "./td/small/div")
    print(bonuses)
    print("EXTRA GOODS: " +str(len(bonuses)))
    # no def or affinity
    if(len(bonuses) == 0):
        print("NO DEFENSE")
        print("NO AFFINITY")
        print("NO ELEMENTAL")
    elif(len(bonuses) == 1):
        #determine if affinity is present
        try:
            isAffinity = bonuses.find_element(By.XPATH, "./span")
            positiveAffinity = isAffinity.get_attribute("class")
            if(positiveAffinity.Equals("text-green-500")):
                print("This is positive affinity: " + positiveAffinity.text)
            elif(positiveAffinity.Equals("text-red-600")):
                print("This is negative affinity: " + positiveAffinity.text)
            else:
                print("You what m8 no affinity value")
        except NoSuchElementException:
            try:
                #determine if element is present
                elementalOrStatus = bonuses.find_element(By.XPATH, "./img")
                element = elementalOrStatus.get_attribute("src")
                if("ElementType1" in element):
                    print("Fireblight: " + bonuses.find_element(By.XPATH,"./img/../span").text)
                if("ElementType2" in element):
                    print("Waterblight: " + bonuses.find_element(By.XPATH,"./img/../span").text)
                if("ElementType3" in element):
                    print("Thunderblight: " + bonuses.find_element(By.XPATH,"./img/../span").text)
                if("ElementType4" in element):
                    print("Iceblight: " + bonuses.find_element(By.XPATH,"./img/../span").text)
                if("ElementType5" in element):
                    print("Dragonblight: " + bonuses.find_element(By.XPATH,"./img/../span").text)
                if("ElementType6" in element):
                    print("Poison Element: " + bonuses.find_element(By.XPATH,"./img/../span").text)
                if("ElementType7" in element):
                    print("Sleep Element: " + bonuses.find_element(By.XPATH,"./img/../span").text)
                if("ElementType8" in element):
                    print("Paralysis Element: " + bonuses.find_element(By.XPATH,"./img/../span").text)
                if("ElementType9" in element):
                    print("Blast Element: " + bonuses.find_element(By.XPATH,"./img/../span").text)
            except NoSuchElementException or AttributeError:
                defense = bonuses.text
                defVal = defense[13:]
                print("Defense Value: " + defVal)
            
    elif(len(bonuses) == 2):
        #determine if it has elemental/status damage and affinity or defense
        #check for status first
        try:
            elementalOrStatus = bonuses.find_element(By.XPATH, "./img")
            element = elementalOrStatus.get_attribute("src")
            if("ElementType1" in element):
                print("Fireblight: " + bonuses.find_element(By.XPATH,"./img/../span").text)
            if("ElementType2" in element):
                print("Waterblight: " + bonuses.find_element(By.XPATH,"./img/../span").text)
            if("ElementType3" in element):
                print("Thunderblight: " + bonuses.find_element(By.XPATH,"./img/../span").text)
            if("ElementType4" in element):
                print("Iceblight: " + bonuses.find_element(By.XPATH,"./img/../span").text)
            if("ElementType5" in element):
                print("Dragonblight: " + bonuses.find_element(By.XPATH,"./img/../span").text)
            if("ElementType6" in element):
                print("Poison Element: " + bonuses.find_element(By.XPATH,"./img/../span").text)
            if("ElementType7" in element):
                print("Sleep Element: " + bonuses.find_element(By.XPATH,"./img/../span").text)
            if("ElementType8" in element):
                print("Paralysis Element: " + bonuses.find_element(By.XPATH,"./img/../span").text)
            if("ElementType9" in element):
                print("Blast Element: " + bonuses.find_element(By.XPATH,"./img/../span").text)
            #check if its affinity or defense value
            try:
                isAffinity = bonuses.find_element(By.XPATH, "./span")
                positiveAffinity = isAffinity.get_attribute("class")
                if(positiveAffinity.Equals("text-green-500")):
                    print("This is positive affinity: " + positiveAffinity.text)
                elif(positiveAffinity.Equals("text-red-600")):
                    print("This is negative affinity: " + positiveAffinity.text)
                else:
                    print("You what m8 no affinity value")
            except NoSuchElementException:
                defense = bonuses.text
                defVal = defense[13:]
                print("Defense Value: " + defVal)
        # the two bonuses are affinity and defense
        except NoSuchElementException:
            isAffinity = bonuses[0].find_element(By.XPATH, "./span")
            positiveAffinity = isAffinity.get_attribute("class")
            if(positiveAffinity.Equals("text-green-500")):
                print("This is positive affinity: " + positiveAffinity.text)
            elif(positiveAffinity.Equals("text-red-600")):
                print("This is negative affinity: " + positiveAffinity.text)
            else:
                print("You what m8 no affinity value")
            defense = bonuses[1].text
            defVal = defense[13:]
            print("Defense Value: " + defVal)
    
    print()



# print(gsList)

# # id gets stale, needs another tab to go through all links
# isFirstTab = True

# # outputs each of the links found 
# # goes to each of the link to recieve the data (defense, decorations,)

# for weapon in gsList:
#     if isFirstTab:
#         driver.get(weapon)
#         isFirstTab = False
#         # need to find data for the first weapon
#     else:
#         driver.execute_script("window.open('about:blank', 'secondtab');")
#         driver.switch_to.window("secondtab")
#         driver.get(weapon)
#         # get the link and go to it
#         # defense stat
#         try:
#             defenseStat = driver.find_element(By.XPATH, "//a[@title = 'Monster Hunter Rise Defense']/..")
#             defenseStatVal = defenseStat.text
#             if "--" in defenseStatVal:
#                 defenseStatVal = '0'; 
#             print(defenseStatVal)
#         except:
#             defenseStatVal = "N/A"
#             print(defenseStatVal)
#         # decorations
#         try:
#             decoration = driver.find_element(By.XPATH,"//a[@title='Monster Hunter Rise Decorations']/..")
#             decorationVal = decoration.text
#             if "--" in decorationVal:
#                 decorationVal = "None"
#             else:
#                 availDeco = driver.find_elements(By.XPATH, "//a[@title='Monster Hunter Rise Decorations']/../img")
#                 for decos in availDeco:
#                     decoSlot = decos.get_attribute("alt")
#                     if "level 1 rampage" in decoSlot:
#                         decoVal = "level 1 rampage"
#                     elif "level 2 rampage" in decoSlot:
#                         decoVal = "level 2 rampage"
#                     elif "level 3 rampage" in decoSlot:
#                         decoVal = "level 3 rampage"
#         except:
