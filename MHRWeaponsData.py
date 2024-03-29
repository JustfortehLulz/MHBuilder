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
iteration = 0

#different path
createWeaponDB = r"D:\Coding_Projects\flutter_windows_3.7.3-stable\flutter_code\MHBuilder\MHBuilderWeaponData.db"

conn = sqlite3.connect(createWeaponDB)

c = conn.cursor()

#tables to be created inside of the database
c.execute('''
            CREATE TABLE IF NOT EXISTS weaponTable
            (
                weaponID integer PRIMARY KEY,
                weapon_type text,
                name text,
                attack integer,
                elemental_type text,
                elemental_damage integer,
                affinity text,
                defense integer,
                red_sharpness_actual integer,
                orange_sharpness_actual integer,
                yellow_sharpness_actual integer,
                green_sharpness_actual integer,
                blue_sharpness_actual integer,
                white_sharpness_actual integer,
                purple_sharpness_actual integer,
                red_sharpness_potential integer,
                orange_sharpness_potential integer,
                yellow_sharpness_potential integer,
                green_sharpness_potential integer,
                blue_sharpness_potential integer,
                white_sharpness_potential integer,
                purple_sharpness_potential integer,
                shelling_type text,
                phial_type text,
                phial_damage text,
                kinsect_level text,
                arc_shot_type text,
                deviation text,
                recoil text,
                reload text
            );
        ''') 

c.execute('''
            CREATE TABLE IF NOT EXISTS decorationSlotsTable
            (
                weaponID integer,
                armorID integer,
                decoration_level integer,
                rampage_level integer,
                PRIMARY KEY (weaponID,armorID),
                FOREIGN KEY(weaponID) REFERENCES weaponTable(weaponID),
                FOREIGN KEY(armorID) REFERENCES armorTable(armorID)
            )
        ''')

# c.execute('''

#             CREATE TABLE IF NOT EXISTS huntingHornSongs
#             (
#                 weaponID integer,
#                 songName text,
#                 FOREIGN KEY(weaponID) REFERENCES weaponTable(weaponID)
#             )
#         ''')

# c.execute('''
#             CREATE TABLE IF NOT EXISTS chargeShotTypes
#             (
#                 weaponID integer,
#                 name text,
#                 chargeShotType text,
#                 chargeShotLevel integer,
#                 FOREIGN KEY(weaponID) REFERENCES weaponTable(weaponID)
#             )
#         ''')

# c.execute('''
#             CREATE TABLE IF NOT EXISTS bowCoating
#             (
#                 weaponID integer,
#                 name text,
#                 coatingType text,
#                 compatiable integer CHECK (compatiable IN (0,1)),
#                 FOREIGN KEY(weaponID) REFERENCES weaponTable(weaponID)
#             )
#         ''')

# c.execute('''
#             CREATE TABLE IF NOT EXISTS lightOrHeavyBowgunShots
#             (
#                 weaponID integer,
#                 name text,
#                 shotType text,
#                 level integer,
#                 FOREIGN KEY(weaponID) REFERENCES weaponTable(weaponID)
#             )
#     ''')

# c.execute(
#     '''
#         CREATE TABLE IF NOT EXISTS weaponRamapgeSkills
#         (
#             weaponID integer,
#             name text
#             FOREIGN KEY(weaponID) REFERENCES weaponTable(weaponID)
#             FOREIGN KEY(name) REFERENCES rampageSkillTable(name)
#         )
#     '''
# )

#holds the data to be pushed into the database
#have everything be N/A?
weaponData = ["N/A"]*29
decoSlotsData = ["N/A"]*4
huntingHornSongsData = ["N/A"]*2
chargeShotTypesData = []
bowCoatingData = []
lightOrHeavyBowgunShotsData = []
weaponID = 0

# for loop here iterate by https://mhrise.kiranico.com/data/weapons?view=(i)
while iteration < 14:
    #reset data for each entry
    weaponData = ["N/A"]*29
    decoSlotsData = ["N/A"]*4
    huntingHornSongsData = ["N/A"]*2
    chargeShotTypesData = []
    bowCoatingData = []
    lightOrHeavyBowgunShotsData = []

    gsSite = "https://mhrise.kiranico.com/data/weapons?view=" + str(iteration)
    gsPage = requests.get(gsSite, headers=headers)
    soup = BeautifulSoup(gsPage.content, "html.parser")

    weaponType = soup.find("h1", {"class" : "font-display text-3xl tracking-tight text-slate-900 dark:text-white"})
    weaponTypeName = weaponType.text
    weaponTypeName = weaponTypeName.strip()
    print(weaponTypeName)
    #add weaponID and weaponName for weaponTable
    weaponData[0] = weaponID
    weaponData[1] = weaponTypeName


    weaponTable = soup.find("table")

    rows = weaponTable.findChildren("tr")


    # go through the entire table going through each row
    for elem in rows:
        #reset data after each row
        weaponData = ["N/A"]*30
        decoSlotsData = ["N/A"]*5
        #unique ID for each weapon
        weaponData[0] = weaponID
        decoSlotsData[3] = weaponID
        # get weapon name
        #print(elem)

        weaponName = elem.find("a" , {"class": "text-sky-500 dark:text-sky-400 group-hover:text-sky-900 dark:group-hover:text-sky-300"})
        #weaponName = elem.find(class_ = "text-sky-500 dark:text-sky-400 group-hover:text-sky-900 dark:group-hover:text-sky-300")
        #used to find the rampage skills

        #print(weaponName)
        if(weaponName == None):
            continue
        weaponLink = weaponName['href']
        print(weaponName.text)
        weaponData[2] = weaponName.text
        decoSlotsData[0] = weaponName.text
        #print(weaponName.get_text())

        # get deco slots and rampage slots
        slots = elem.find_all(class_ = "inline-flex items-center px-2 py-0.5 rounded text-xs font-medium mr-1 bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300")
        deco = slots[0]
        totalDeco = deco.find_all("img", src = True)
        # determine if there are decorations or not and then print how many decorations there are and the level
        if(len(totalDeco) == 0):
            print("THERE ARE NO DECORATIONS")
            # do not push any data to the database
        else:
            for foundDeco in totalDeco:
                # reset each time to clear the data
                decoSlotsData = ["N/A"]*4
                levelDeco = foundDeco['src']
                if("deco1" in levelDeco):
                    print("DECORATION LEVEL 1")
                    decoSlotsData[2] = 1
                elif("deco2" in levelDeco):
                    print("DECORATION LEVEL 2")
                    decoSlotsData[2] = 2
                elif("deco3" in levelDeco):
                    print("DECORATION LEVEL 3")
                    decoSlotsData[2] = 3
                elif("deco4" in levelDeco):
                    print("DECORATION LEVEL 4")
                    decoSlotsData[2] = 4
                # push the data everytime here
                decoSlotsData[0] = weaponID
                # decoSlotsData[1] is for the armorID, there is no armor here
                decoSlotsData[1] = 0
                # decoSlotsData[3] is for the rampage level, there is no rampage level (deal with that in the following for loop)
                decoSlotsData[3] = None

                decorationSlots_query = """INSERT INTO decorationSlotsTable
                    (
                        weaponID integer,
                        armorID integer,
                        decoration_level integer,
                        rampage_level integer,
                    )
                    VALUES
                    (?,?,?,?,?)"""
                try:
                    c.execute(decorationSlots_query,decoSlotsData)
                    conn.commit()
                except sqlite3.Error as error:
                    print("UH OH WE FAILED " , error)

        # rampage decorations same process as finding decorations
        rampageDeco = slots[1]
        totalRampageDeco = rampageDeco.find_all("img", src = True)
        if(len(totalRampageDeco) == 0):
            print("THERE ARE NO RAMPAGE DECORATIONS")
        else:
            for foundRampage in totalRampageDeco:
                decoSlotsData = ["N/A"]*4
                levelRampage = foundRampage['src']
                if("deco1" in levelRampage):
                    print("RAMPAGE LEVEL 1")
                    decoSlotsData[3] = 1
                elif("deco2" in levelRampage):
                    print("RAMPAGE LEVEL 2")
                    decoSlotsData[3] = 2
                elif("deco3" in levelRampage):
                    print("RAMPAGE LEVEL 3")
                    decoSlotsData[3] = 3
                elif("deco4" in levelRampage):
                    print("RAMPAGE LEVEL 4")
                    decoSlotsData[3] = 4

                decoSlotsData[0] = weaponID
                # decoSlotsData[1] is zero because that is reserved for armorID 
                decoSlotsData[1] = 0
                # decoSlotsData[2] is None since that is for normal slots level
                decoSlotsData[2] = None

                # push the data everytime here
                decorationSlots_query = """INSERT INTO decorationSlotsTable
                    (
                        weaponID integer,
                        armorID integer,
                        decoration_level integer,
                        rampage_level integer,
                    )
                    VALUES
                    (?,?,?,?,?)"""
                try:
                    c.execute(decorationSlots_query,decoSlotsData)
                    conn.commit()
                except sqlite3.Error as error:
                    print("UH OH WE FAILED " , error)

        # get attack value
        weaponAttackVal = elem.find("div", {"data-key":"attack"})
        print("Attack Value: " + weaponAttackVal.get_text())
        weaponData[3] = weaponAttackVal.get_text()

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
                weaponData[4] = "Fireblight"
            elif("ElementType2" in elemental):
                print("Waterblight: " + str(elementalVal.get_text()))
                weaponData[4] = "Waterblight"
            elif("ElementType3" in elemental):
                print("Thunderblight: "+ str(elementalVal.get_text()))
                weaponData[4] = "Thunderblight"
            elif("ElementType4" in elemental):
                print("Iceblight: " + str(elementalVal.get_text()))
                weaponData[4] = "Iceblight"
            elif("ElementType5" in elemental):
                print("Dragonblight: " + str(elementalVal.get_text()))
                weaponData[4] = "Dragonblight"
            elif("ElementType6" in elemental):
                print("Poison Element: " + str(elementalVal.get_text()))
                weaponData[4] = "Poison"
            elif("ElementType7" in elemental):
                print("Sleep Element: " + str(elementalVal.get_text()))
                weaponData[4] = "Sleep"
            elif("ElementType8" in elemental):
                print("Paralysis Element: " + str(elementalVal.get_text()))
                weaponData[4] = "Paralysis"
            elif("ElementType9" in elemental):
                print("Blast Element: " + str(elementalVal.get_text()))
                weaponData[4] = "Blast"
            # get the elemental damage value
            weaponData[5] = elementalVal.get_text()
        else:
            print("NO ELEMENTAL")
            weaponData[4] = "N/A"
            weaponData[5] = 0
        # both affinity and defense are under the div
        affinityOrDefense = bonuses.find_all("div")
        if(len(affinityOrDefense) != 0):
            # check if the div contains text for affinity or defense
            for elem in affinityOrDefense:
                values = elem.text
                parsedval = " ".join(values.split())
                if("Affinity" in parsedval):
                    print("Affinity")
                    weaponData[6] = parsedval[9:]
                elif("Defense" in parsedval):
                    print("Defense")
                    weaponData[7] = parsedval[14:]
                print(parsedval)
        else:
            print("THERES NOTHING")
            weaponData[6] = 0
            weaponData[7] = 0

        # grabbing sharpness values
        sharpness = bonusesAndSharpness[3]
        isFirstRow = True
        sharpColor = []
        i = 0
        totalSharpness = sharpness.find_all("rect")
        if(len(totalSharpness) != 0):
            for elem in totalSharpness:
                # this is required in order for the max potential of sharpness of a weapon
                if(elem['fill'] in sharpColor):
                    print("SECOND ROW NOW")
                    if(isFirstRow):
                        i = 0
                    isFirstRow = False
                print(elem['fill'] + " " + elem['width'])
                sharpColor.append(elem['fill'])
                # insert the sharpness value for each colour
                # However, some weapons do not have sharpness for certain colours
                if(isFirstRow):
                    weaponData[8+i] = elem['width']
                else:
                    weaponData[15+i] = elem['width']
                i = i + 1

        # special cases
        # first - hunting horn songs and gunlance 
        # iteration 5 = hunting horn
        # iteration 7 = gunlance 
        # iteration 8 = switch axe
        # iteration 9 = charge blade
        # iteration 10 = insect glaive
        if(iteration == 5 or iteration == 7 or iteration == 8 or iteration == 9 or iteration == 10):
            # grab the song names
            songsList = bonusesAndSharpness[4]
            #print(songsList)
            for elem in songsList:
                values = elem.text
                parsedval = " ".join(values.split())
                parsedval = parsedval.strip()
                if(iteration == 5):
                    print((elem.text).strip())
                else:
                    if(iteration == 7):
                        weaponData[22] = parsedval
                    elif(iteration == 8 or iteration == 9):
                        if(not (parsedval == "")):
                            print(parsedval)
                            switchAxe = parsedval.split()
                            #type of phial
                            print(switchAxe[0])
                            weaponData[23] = switchAxe[0]
                            #check if there is a damage value of phial
                            print(switchAxe[-1])
                            if(switchAxe[-1].isdigit()):
                                weaponData[24] = switchAxe[-1]
                    elif(iteration == 10):
                        if(not (parsedval == "")):
                            print(parsedval)
                            insectGlaive = parsedval.split()
                            # level of kinsect
                            print(insectGlaive[-1])
                            weaponData[25] = insectGlaive[-1]
                    print(parsedval)
        #bow stuff
        elif(iteration == 11):
            chargeShot = bonusesAndSharpness[3]
            chargeShot = chargeShot.find_all("div")
            isArcShot = True
            chargeLevel = 1
            #print(chargeShot)
            for elem in chargeShot:
                if(isArcShot):
                    print("Arc Shot: " + elem.text)
                    weaponData[26] = elem.text
                    isArcShot = False
                else:
                    print("Charge Shot " + str(chargeLevel) + ": " + elem.text)
                    chargeLevel = chargeLevel + 1

            # get coatings
            bowCoating = bonusesAndSharpness[4]
            compatiableCoating = bowCoating.find_all("div", {"class": ""})
            uncompatiableCoating = bowCoating.find_all("div", {"class": "text-gray-400"})
            enhancedCoating = bowCoating.find_all("div", {"class":"text-green-500"})
            # print(compatiableCoating)
            # print(uncompatiableCoating)
            # print(enhancedCoating)

            if(len(compatiableCoating) != 0):
                for elem in compatiableCoating:
                    print("Compatiable Coating: " + elem.text)
            else:
                print("NO COMPATIABLE COATING")
            if(len(uncompatiableCoating) != 0):
                for elem in uncompatiableCoating:
                    print("Incompatiable Coating: " + elem.text)
            else:
                print("NO INCOMPATIABLE COATING")
            if(len(enhancedCoating) != 0):
                for elem in enhancedCoating:
                    print("Enhanced Coating: " + elem.text)
            else:
                print("NO ENHANCED COATING")
            #bowCoating = bowCoating.find_all("div")
            #print(bowCoating)
        elif(iteration == 12 or iteration == 13):
            #light and heavy bowgun
            shotStats = bonusesAndSharpness[3]
            #shotTypes = bonusesAndSharpness[4]
            #print(shotStats)
            shotStatsVal = shotStats.find_all("div")
            shotTypes = shotStats.find_all("td")
            shotTypesAgain = shotStats.find_all("table")
            for elem in shotStatsVal:
                #Deviation, Recoil, Reload
                values = elem.text
                parsedval = values.split("\n")
                #print(parsedval)
                i = 0
                while i < len(parsedval):
                    parsedval[i] = parsedval[i].strip()
                    i = i + 1
                #print(parsedval)
                parsedval = " ".join(parsedval)
                parsedval = parsedval.strip()
                if("Deviation" in parsedval):
                    weaponData[27] = parsedval[9:]
                elif("Recoil" in parsedval):
                    weaponData[28] = parsedval[7:]
                elif("Reload" in parsedval):
                    weaponData[29] = parsedval[7:]
                print(parsedval)
            #print(shotStatsVal)
            shotTypes = shotTypes[1:2]
            # gets the first column of shots
            #print(shotTypes)
            levelNum = 1
            for i in range(len(shotTypes)):
                data = shotTypes[i].find_all("td")
                shotName = ""
                levelNum = 1
                for j in range(len(data)):
                    if("Nrm" in data[j].text):
                        shotName = "Normal Ammo"
                        levelNum = 1
                    elif("Prc" in data[j].text):
                        shotName = "Pierce Ammo"
                        levelNum = 1
                    elif("Spr" in data[j].text):
                        shotName = "Spread Ammo"
                        levelNum = 1
                    elif("Shr" in data[j].text):
                        shotName = "Shrapnel Ammo"
                        levelNum = 1
                    elif("Sti" in data[j].text):
                        shotName = "Sticky Ammo"
                        levelNum = 1
                    elif("Clu" in data[j].text):
                        shotName = "Cluster Bomb"
                        levelNum = 1
                    else:
                        print(shotName + " " + str(levelNum) + " " + data[j].text)
                        levelNum = levelNum + 1
            #print(shotTypesAgain[2:4])
            print("OTHER SHOTS")
            shotTypesAgain = shotTypesAgain[2:5]
            for i in range(len(shotTypesAgain)):
                data = shotTypesAgain[i].find_all("td")
                shotName = ""
                levelNum = 1
                isFire = False
                isWater = False
                isThunder = False
                isIce = False
                isDragon = False
                for j in range(len(data)):
                    if("Fir" in data[j].text):
                        shotName = "Flaming Ammo"
                        isFire = True
                        #shotName = "Piercing Fire Ammo"
                    elif("Wat" in data[j].text):
                        shotName = "Water Ammo"
                        isWater = True
                        #shotName = "Piercing Water Ammo"
                    elif("Thn" in data[j].text):
                        shotName = "Thunder Ammo"
                        isThunder = True
                        #shotName = "Piercing Thunder Ammo"
                    elif("Ice" in data[j].text):
                        shotName = "Freeze Ammo"
                        isIce = True
                        #shotName = "Piercing Ice Ammo"
                    elif("Dra" in data[j].text):
                        shotName = "Dragon Ammo"
                        isDragon = True
                        #shotName = "Piercing Dragon Ammo"
                    elif("Poi" in data[j].text):
                        shotName = "Poison Ammo"
                    elif("Par" in data[j].text):
                        shotName = "Paralysis Ammo"
                        levelNum = 1
                    elif("Sle" in data[j].text):
                        shotName = "Sleep Ammo"
                        levelNum = 1
                    elif("Exh" in data[j].text):
                        shotName = "Exhaust Ammo"
                        levelNum = 1
                    elif("Rec" in data[j].text):
                        shotName = "Recover Ammo"
                        levelNum = 1
                    elif("Dem" in data[j].text):
                        shotName = "Demon Ammo"
                        levelNum = 1
                    elif("Amr" in data[j].text):
                        shotName = "Armor Ammo"
                        levelNum = 1
                    elif("Tra" in data[j].text):
                        shotName = "Tranq Ammo"
                        levelNum = 1
                    elif("Wyv" in data[j].text):
                        shotName = "Wyvern Ammo"
                        levelNum = 1
                    elif("Sli" in data[j].text):
                        shotName = "Slicing Ammo"
                        levelNum = 1
                    else:
                        if(isFire):
                            if(levelNum == 1):
                                print(shotName + " " + data[j].text)
                                levelNum = levelNum + 1
                            else:
                                print("Piercing Fire Ammo " + data[j].text)
                                isFire = False
                                levelNum = 1
                        elif(isWater):
                            if(levelNum == 1):
                                print(shotName + " " + data[j].text)
                                levelNum = levelNum + 1
                            else:
                                print("Piercing Water Ammo " + data[j].text)
                                isWater = False
                                levelNum = 1
                        elif(isThunder):
                            if(levelNum == 1):
                                print(shotName + " " + data[j].text)
                                levelNum = levelNum + 1
                            else:
                                print("Piercing Thunder Ammo " + data[j].text)
                                isThunder = False
                                levelNum = 1
                        elif(isIce):
                            if(levelNum == 1):
                                print(shotName + " " + data[j].text)
                                levelNum = levelNum + 1
                            else:
                                print("Piercing Ice Ammo " + data[j].text)
                                isIce = False
                                levelNum = 1
                        elif(isDragon):
                            if(levelNum == 1):
                                print(shotName + " " + data[j].text)
                                levelNum = levelNum + 1
                            else:
                                print("Piercing Dragon Ammo " + data[j].text)
                                isDragon = False
                                levelNum = 1
                        else:
                            if(shotName == "Demon Ammo" or shotName == "Armor Ammo" or shotName == "Tranq Ammo" or shotName == "Wyvern Ammo" or shotName == "Slicing Ammo"):
                                print(shotName + " " + data[j].text)
                            else:
                                print(shotName + " " + str(levelNum) + " " + data[j].text)
                            levelNum = levelNum + 1



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
        print(weaponData)
        # incrementing for the next weapon
        weaponID = weaponID + 1
        # inserting values into database
        weaponTable_query = """INSERT INTO weaponTable 
                ( 
                    weaponID,
                    weapon_type,
                    name,
                    attack,
                    elemental_type,
                    elemental_damage,
                    affinity,
                    defense,
                    red_sharpness_actual,
                    orange_sharpness_actual,
                    yellow_sharpness_actual,
                    green_sharpness_actual,
                    blue_sharpness_actual,
                    white_sharpness_actual,
                    purple_sharpness_actual,
                    red_sharpness_potential,
                    orange_sharpness_potential,
                    yellow_sharpness_potential,
                    green_sharpness_potential,
                    blue_sharpness_potential,
                    white_sharpness_potential,
                    purple_sharpness_potential,
                    shelling_type,
                    phial_type,
                    phial_damage,
                    kinsect_level,
                    arc_shot_type,
                    deviation,
                    recoil,
                    reload
                )
                VALUES
                (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""

        # decorationSlots_query = """INSERT INTO decorationSlotsTable
        #                         (
        #                             name,
        #                             decoration_level,
        #                             rampage_level,
        #                             weaponID,
        #                             armorID
        #                         )
        #                         VALUES
        #                         (?,?,?,?,?)"""
        huntingHornSongs_query = """INSERT INTO huntingHornSongs
                                (
                                    weaponID,
                                    name,
                                    songName,
                                )
                                VALUES
                                (?,?,?)"""
        chargeShotTypes_query = """INSERT INTO chargeShotTypes
                                (
                                    weaponID,
                                    name,
                                    chargeShotType,
                                    chargeShotLevel
                                )
                                VALUES
                                (?,?,?,?)
                                """
        bowCoating_query = """INSERT INTO bowCoating
                           (
                                weaponID,
                                name,
                                coatingType,
                                compatiable
                           ) 
                           VALUES
                           (?,?,?,?)
                           """
        lightOrHeavyBowgunShots_query = """INSERT INTO lightOrHeavyBowgunShots
                                        (
                                            weaponID,
                                            name,
                                            shotType,
                                            level
                                        )
                                        VALUES
                                        (?,?,?,?)
                                        """
        try:
            c.execute(weaponTable_query,weaponData)
            #c.execute(decorationSlots_query,decoSlotsData)
            c.execute(huntingHornSongs_query,huntingHornSongsData)
            c.execute(bowCoating_query,bowCoatingData)
            c.execute(lightOrHeavyBowgunShots_query,lightOrHeavyBowgunShotsData)
            conn.commit()
        except sqlite3.Error as error:
            print("UH OH WE FAILED " , error)

        weaponID = weaponID + 1

    iteration = iteration + 1

conn.close()