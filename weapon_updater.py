"""File used to update the weapon list used on the rest of modules.
   Must be greatly improved in the future, by not depending on WFCD's data."""

import os
import json
import requests
import pandas as pd

weapon_categories = ["Primary", "Secondary", "Melee", "Arch-Gun", "SentinelWeapons"]
weapons = {}


def get_weapons_from_wiki():
    "Method used to get weapon data from the wiki, as of now it's only used to get the weapon type"
    tables = pd.read_html("https://warframe.fandom.com/wiki/Weapon_Comparison?so=search")
    tables = [tables[0], tables[9], tables[16], tables[18], tables[19], tables[21]]
    tables = [list(x.T.to_dict().values()) for x in tables]
    tables = [weapon for cat in tables for weapon in cat]

    for weapon in tables:
        weapon["Name"] = weapon["Name"].replace(" ", "_").replace("&", "and").lower()

    return {weapon['Name']: weapon for weapon in tables}


def get_weapon_type(wiki, weapon_name):
    """Method used to get the weapon type from the wiki"""
    if weapon_name in wiki:
        if "Trigger" in wiki[weapon_name] and wiki[weapon_name]["Trigger"] == "Held":
            return "Beam"
        elif "WeaponType" in wiki[weapon_name]:
            return wiki[weapon_name]["WeaponType"]
        else:
            return wiki[weapon_name]["Type"]
    return "Kitgun/Zaw"


def solve_category(weapon):
    """Method used to fill the weapon category of some exceptions"""

    if "kitgun" in weapon["type"]:
        return "Secondary"
    if "Zaw" in weapon["type"]:
        return "Melee"
    if weapon["type"] == "Shotgun":
        return weapon["type"]
    if weapon["type"] == "Exalted Weapon":
        return "Melee"
    if weapon["category"] in ["SentinelWeapons", "Arch-Gun"]:
        return "Primary"
    return weapon["category"]


def get_weapons():
    """Requests, analyzes and stores all the weapons form the WFCD community github.
       This is needed because the wiki doesn't include all the information about weapon attacks on the table.
       Can be improved by using the wiki in a smarter way nonetheless."""

    print("Updating the weapon database\n")
    weapon_request = requests.get("https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json/All.json")
    weapon_request = weapon_request.json()
    weapon_request = [x for x in weapon_request if "omegaAttenuation" in x]

    wiki = get_weapons_from_wiki()

    for weapon in weapon_request:

        weapon["category"] = solve_category(weapon)

        if weapon["category"] not in ["Primary", "Shotgun", "Secondary", "Melee"]:
            continue
        weapon["name"] = weapon["name"].replace(" ", "_").replace("&", "and").lower()

        if not weapon["category"] in weapons:
            weapons[weapon["category"]] = {}

        weapons[weapon["category"]][weapon["name"]] = {}
        newWeapon = weapons[weapon["category"]][weapon["name"]]
        #make the following assignments more efficient
        newWeapon["disposition"] = weapon["omegaAttenuation"]
        newWeapon["critical_chance"] = weapon["criticalChance"]
        newWeapon["critical_damage"] = weapon["criticalMultiplier"]
        newWeapon["status_chance"] = weapon["procChance"]
        newWeapon["type"] = get_weapon_type(wiki, weapon["name"])

        if newWeapon["type"] == "Kitgun/Zaw":
            if weapon["category"] == "Primary":
                newWeapon["critical_chance"], newWeapon["critical_damage"], newWeapon["status_chance"] = 0.28, 2.0, 0.28
            elif weapon["category"] == "Secondary":
                newWeapon["critical_chance"], newWeapon["critical_damage"], newWeapon["status_chance"] = 0.24, 3.0, 0.24
            elif weapon["category"] == "Melee":
                newWeapon["critical_chance"], newWeapon["critical_damage"], newWeapon["status_chance"] = 0.14, 2.2, 0.32

        if "attacks" in weapon:
            for attack in weapon["attacks"]:
                if "damage" in attack:
                    newWeapon["Attacks"] = {}
                    newWeapon["Attacks"][attack["name"]] = {}
                    newWeapon["Attacks"][attack["name"]]["damage_types"] = attack["damage"]
                    if ("slash" in newWeapon["Attacks"][attack["name"]]["damage_types"]):
                        newWeapon["Attacks"][attack["name"]]["slashPercent"] = newWeapon["Attacks"][
                            attack["name"]]["damage_types"]["slash"] / (weapon["totalDamage"] + 0.001)
                    else:
                        newWeapon["Attacks"][attack["name"]]["slashPercent"] = 0
        else:
            newWeapon["Attacks"] = {}
            newWeapon["Attacks"]["No attacks"] = {}
            newWeapon["Attacks"]["No attacks"]["damageTypes"] = {}
            newWeapon["Attacks"]["No attacks"]["slashPercent"] = 0

    with open(os.getcwd() + "\\config\\weapon_list.json", "w", encoding="utf-8") as weapon_file:
        json.dump(weapons, weapon_file)
        print("Succesfully updated the weapon database\n")
