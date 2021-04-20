import os, shutil, random, json, glob
from csv import reader
from datetime import datetime

#File used to prepare the data for the rest of the functions.

########################################################################################################
#SETTINGS
deletePreviousFolder = True


#Set only one as active. Determines the accuracy and speed of the search.
#Fast search lasts for about a minute. 
#It returns a low amount of rivens. Used to search unrolleds for wanted weapons.

#Medium search lasts for 5 minutes. 
#It returns a decent amount of rivens for the wanted weapons and a low amount of rivens for unwanted ones.
#It mostly searches for godrolls and unrolleds of wanted weapons.

#Slow search lasts for 15 minutes.
#It returns a great amount of rivens both for wanted weapons and unwanted ones.
#It mostly searches for godrolls and unrolleds of wanted weapons and unrolleds for unwanted ones.

#Non Existant search is an untested search that last for an almost infinite amount of time.
#It returns all the godrolls and unrolleds for both wanted and unwanted weapons.

#Set all to false to get fastSearch

mediumSearch = False
slowSearch = False
nonExistantSearch = False

#Used for debugs.
search = True

########################################################################################################
#GLOBAL VARIABLES USED AROUND ALL THE FILES

WFM_API = "https://api.warframe.market/v1"

#Creates a directory to place the results in.
path = ""
folderPath= ""
wantedPath=""
unwantedPath=""

#Lists used as database.
weaponList = {}
weaponVariants = []
statList = {}
combinations = {}

#User lists. Can be manipulated to change search results. Based on the weapons, stats and rolls that you want.
#You can make changes in the files in RivenSearch\\config 
wishedWeapons = []
wishedUnrolleds = []
wishedRivens = {}
wishedNegatives = []
decentPositives = []

def init():
    createDirectory()
    loadData()

#Creates the multiple directories used to write data.
def createDirectory():
    global path, folderPath, wantedPath, unwantedPath

    path = os.getcwd()
    folderPath = path + "\\RivenSearch\\"
    if not os.path.exists(folderPath): os.mkdir(folderPath)
    os.chdir(folderPath)
    date = datetime.today()
    folder = datetime(date.year, date.month, date.day).strftime("%d-%m-%Y")
    folderPath = folderPath +  folder
    if os.path.exists(folderPath):
        if deletePreviousFolder: shutil.rmtree(folderPath)
        else: folderPath += "(" + str(random.randint(0,9999)) + ")"
    os.mkdir(folderPath)
    wantedPath = folderPath + "\\Wanted Weapons"
    unwantedPath = folderPath + "\\Unwanted Weapons"
    for fpath in [wantedPath, unwantedPath]:
        os.mkdir(fpath)
        os.mkdir(fpath + "\\Godrolls")
        os.mkdir(fpath + "\\Decents")
        os.mkdir(fpath + "\\Good_ones")
        os.mkdir(fpath + "\\Unrolleds")
        os.mkdir(fpath + "\\Trashcan")

#Load the weapon, stats, rolls and variants database.
def loadData():
    global weaponList, statList, combinations, wishedWeapons
    global wishedUnrolleds, weaponVariants, wishedRivens, wishedNegatives, decentPositives

    os.chdir(path+"\\config")
    #Stat information, with names and base values for each weapon type.
    with open("statValues.json") as f:
        data = json.loads(f.read())
        statList.update(data) 
        f.close()
    #Rolls you want for each weapon type.
    with open("wantedRolls.json") as f:
        combinations = list(json.loads(f.read()).values())
        f.close()
    #Weapons you want for each weapon type.
    with open("WantedWeapons.csv") as f:
        wishedWeapons = list(reader(f))
        wishedUnrolleds = wishedWeapons[-1]
        wishedWeapons = wishedWeapons[:-1]
        f.close()
    #List of all weapons in the game with their dispositions. May add stats in the future.
    for file in glob.glob("*Dispo.json"):
        with open(file) as f:
            data = json.loads(f.read())
            weaponList.update(data) 
            f.close()
    #Prepares the weapon types for heavy attack melees.
    for weapon, stats in list(weaponList.items()):
        if stats["weapontype"] == [4] and weapon in wishedWeapons[5]:
            stats["weapontype"] = [4,5]
    #List with specific rolls you want on a weapon. ie Proboscis Cernos with ms dmg elec -zoom.
    with open("specificRolls.json") as f:
        wishedRivens = json.loads(f.read())
        f.close()
    #List with negatives that weapon can use. May be weighted in the future.
    with open("negatives.csv") as f:
        wishedNegatives = list(reader(f))
        f.close()
    #List with decent positives. May be weighted in the future.
    with open("positives.csv") as f:
        decentPositives = list(reader(f))
        f.close()
    #List with all the weapon variant names. For disposition purposes.
    with open("weaponVariants.csv") as f:
        weaponVariants = [""]
        for weapon in reader(f): weaponVariants.append(weapon[0])
        f.close()
    """with open("decentPositives.csv") as f:
        decentPositives = list(reader(f))
        f.close()"""
    """with open("decentNegatives.csv") as f:
        decentNegatives = list(reader(f))
        f.close()"""
    os.chdir(folderPath)
