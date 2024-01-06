"""File used to prepare the data for the rest of the functions."""
import csv
import json
import os
import random
import shutil
from ast import literal_eval
from datetime import datetime

import src.riven_stuff.riven_rater as riven_rater

##################################################################################################
# settings
delete_previous_folder = True

# Determines the accuracy and speed of the search.
# 0 = fast, 1 = slow.
# fast search lasts for about a minute.
# it returns a low amount of rivens. used to search unrolleds for wanted weapons.

# slow search lasts for 30 minutes.
# it returns a great amount of rivens both for wanted weapons and unwanted ones.
# it mostly searches for godrolls and unrolleds of wanted weapons and unrolleds for unwanted ones.

search_type = False

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
weapons = {}
stat_list = {}
combinations = {}
weights = {}
equations = {}
profiles = []

# User lists. can be manipulated to change search results.
# based on the weapons, stats and rolls that you want.
# you can make changes in the files in riven_search\\config
wanted_wp = []
wanted_unroll = []
wanted_rv = {}
positives = []


def init():
    """Calls for the initialization functions."""
    create_directory()
    load_data()


def create_directory():
    """Creates the multiple directories used to write data."""

    global path, folder_path, wanted_path, unwanted_path

    # gets the path to store the results in.
    folder_path = path + "\\Search results\\"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    os.chdir(folder_path)

    # creates a folder with the current date and time.
    date = datetime.today()
    folder = datetime(date.year, date.month, date.day).strftime("%d-%m-%y")
    folder_path = folder_path + folder

    if os.path.exists(folder_path):
        if delete_previous_folder:
            shutil.rmtree(folder_path)
        else:
            folder_path += "(" + str(random.randint(0, 9999)) + ")"
    os.mkdir(folder_path)

    # creates the wanted and unwanted folders along with the rating folders.
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


def load_stats():
    """Loads the stats from the stats.csv file."""
    global stat_list
    with open("stat_values.csv", encoding="utf-8") as file:
        stat_list = list(csv.DictReader(file))
        for stat in stat_list:
            stat["rh_names"] = literal_eval(stat["rh_names"])
            for i in range(5):
                stat["value" + str(i)] = float(stat["value" + str(i)])
        file.close()


def load_roll_info():
    """Loads the combinations of decent rolls for each weapon type."""
    global combinations
    with open("wanted_rolls.json", encoding="utf-8") as file:
        combinations = json.load(file)
        file.close()


def load_specific_search():
    """Loads specific weapons and rolls the user wants to search for."""
    global wanted_rv, wanted_wp, wanted_unroll
    with open("specific_rolls.csv", encoding="utf-8") as file:
        wanted_rv = list(csv.DictReader(file))
        file.close()
    with open("wanted_weapons.json", encoding="utf-8") as file:
        wanted_wp = json.load(file)
        wanted_unroll = wanted_wp["wanted_unroll"]
        wanted_wp.pop("wanted_unroll")
        wanted_wp = list(wanted_wp.values())
        file.close()


def load_weapon_data():
    """Loads all the information related with weapons and its stats."""
    global weapons
    with open("weapons.json", encoding="utf-8") as file:
        weapons = json.loads(file.read())
        file.close()


def load_profile_data():
    """Loads the weighting profiles data for the scoring system."""
    global weights, equations, positives

    with open("rating_weights.json", encoding="utf-8") as file:
        weights = list(json.loads(file.read()).values())
        positives = [[] for i in range(0, 4)]
        positives.append(positives[0])

        for i, weapon_type in enumerate(weights):
            for use in weapon_type.values():
                for stat_name, stat_values in use.items():
                    if stat_values[0] < 10:
                        continue
                    if stat_name not in positives[i]:
                        positives[i].append(stat_name)
        file.close()

    with open("rating_equations.json", encoding="utf-8") as file:
        equations = list(json.loads(file.read()).values())
        file.close()


def load_data():
    """Calls for the loading functions."""

    os.chdir(path + "\\config")

    load_stats()
    load_roll_info()
    load_specific_search()
    load_weapon_data()
    load_profile_data()

    riven_rater.generate_profiles()
