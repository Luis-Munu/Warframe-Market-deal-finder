"""File used to prepare the data for the rest of the functions."""
from csv import reader
from datetime import datetime
import json
import random
import os
import shutil
import rating_profile

##################################################################################################
# settings
delete_previous_folder = True

# set only one as active. determines the accuracy and speed of the search.
# fast search lasts for about a minute.
# it returns a low amount of rivens. used to search unrolleds for wanted weapons.

# medium search lasts for 5 minutes.
# it returns a decent amount of rivens for the wanted weapons
# and a low amount of rivens for unwanted ones.
# it mostly searches for godrolls and unrolleds of wanted weapons.

# slow search lasts for 30 minutes.
# it returns a great amount of rivens both for wanted weapons and unwanted ones.
# it mostly searches for godrolls and unrolleds of wanted weapons and unrolleds for unwanted ones.

# non existant search is an untested search that last for an almost infinite amount of time.
# it returns all the godrolls and unrolleds for both wanted and unwanted weapons.
fast_search = False
medium_search = False
slow_search = False
non_existant_search = False

# variables used to store specific search data from the user's input.
specific_search = False
specific_weapon = False
weapon_name = ""
weapon_stats = {}

################################################################################################
# global variables used around all the files

# creates a directory to place the results in.
path = os.getcwd()
folder_path = ""
wanted_path = ""
unwanted_path = ""

# lists used as database.
weapon_list = {}
weapon_variants = []
special_weapon_names = []
stat_list = {}
combinations = {}
weights_list = {}
equations_list = {}
profile_list = []

# User lists. can be manipulated to change search results.
# based on the weapons, stats and rolls that you want.
# you can make changes in the files in riven_search\\config
wished_weapons = []
wished_unrolleds = []
wished_rivens = {}
wished_negatives = []
decent_positives = []


def init():
    """Calls for the initialization functions."""
    create_directory()
    load_data()


def create_directory():
    """Creates the multiple directories used to write data."""

    global path, folder_path, wanted_path, unwanted_path
    #gets the path to store the results in.
    folder_path = path + "\\Search results\\"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    os.chdir(folder_path)
    #creates a folder with the current date and time.
    date = datetime.today()
    folder = datetime(date.year, date.month, date.day).strftime("%d-%m-%y")
    folder_path = folder_path + folder
    if os.path.exists(folder_path):
        if delete_previous_folder:
            shutil.rmtree(folder_path)
        else:
            folder_path += "(" + str(random.randint(0, 9999)) + ")"
    os.mkdir(folder_path)

    #creates the wanted and unwanted folders along with the rating folders.
    wanted_path = folder_path + "\\Wanted weapons"
    unwanted_path = folder_path + "\\Unwanted weapons"
    for fpath in [wanted_path, unwanted_path]:
        os.mkdir(fpath)
        os.mkdir(fpath + "\\95-100. Godrolls")
        os.mkdir(fpath + "\\85-95. Good rivens")
        os.mkdir(fpath + "\\70-85. Decent rivens")
        os.mkdir(fpath + "\\60-70. Usable rivens")
        os.mkdir(fpath + "\\40-60. Bad rivens")
        os.mkdir(fpath + "\\Unrolleds")
        os.mkdir(fpath + "\\Trashcan")
        os.mkdir(fpath + "\\Wanted rolls")


def load_data():
    """Loads the weapon, stats, rolls and variants database."""

    global weapon_list, stat_list, combinations, wished_weapons, special_weapon_names
    global wished_unrolleds, weapon_variants, wished_rivens, wished_negatives, weights_list
    global equations_list, profile_list, decent_positives

    os.chdir(path + "\\config")
    # stat information, with names and base values for each weapon type.
    with open("stat_values.json", encoding="utf-8") as file:
        stat_list.update(json.loads(file.read()))
        file.close()
    # rolls you want for each weapon type.
    with open("wanted_rolls.json", encoding="utf-8") as file:
        combinations = list(json.loads(file.read()).values())
        file.close()
    # weapons you want for each weapon type.
    with open("wanted_weapons.csv", encoding="utf-8") as file:
        wished_weapons = list(reader(file))
        wished_unrolleds = wished_weapons[-1]
        wished_weapons = wished_weapons[:-1]
        file.close()
    # weapon data with names, stats and attacks.
    with open("weapon_list.json", encoding="utf-8") as file:
        weapon_list = list(json.loads(file.read()).values())
        weapon_list[1], weapon_list[3] = weapon_list[3], weapon_list[1]
        file.close()
    with open("wfcd_exceptions.json", encoding="utf-8") as file:
        content = list(json.loads(file.read()).values())
        for i, w_list in enumerate(content):
            for weapon, stats in w_list.items():
                weapon_list[i][weapon] = stats
        file.close()
    # list with specific rolls you want on a weapon. ie proboscis cernos with ms dmg elec -zoom.
    with open("specific_rolls.json", encoding="utf-8") as file:
        wished_rivens = json.loads(file.read())
        file.close()
    # list with all the weapon variant names. for disposition purposes.
    with open("weapon_variants.csv", encoding="utf-8") as file:
        for weapon in reader(file):
            weapon_variants.append(weapon[0])
        file.close()
    # list with weapons that only exist in a variant form. for disposition purposes.
    with open("special_weapon_names.csv", encoding="utf-8") as file:
        for weapon in reader(file):
            special_weapon_names.append(weapon[0])
        file.close()
    # lists of stat weightings depending on the weapon stats, disposition, etc...
    with open("rating_weights.json", encoding="utf-8") as file:
        weights_list = list(json.loads(file.read()).values())
        decent_positives = [[] for i in range(0, 4)]
        for i, weapon_type in enumerate(weights_list):
            for use in weapon_type.values():
                for stat_name, stat_values in use.items():
                    if stat_values[0] < 10:
                        continue
                    if stat_name not in decent_positives[i]:
                        decent_positives[i].append(stat_name)

        file.close()
    with open("rating_equations.json", encoding="utf-8") as file:
        equations_list = list(json.loads(file.read()).values())
        file.close()
    rating_profile.load_profiles()

    os.chdir(folder_path)
