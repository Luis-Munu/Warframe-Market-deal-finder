"""File used to update the weapon list used on the rest of modules.
   Must be greatly improved in the future, by not depending on WFCD's data."""

from io import StringIO

import pandas as pd
import requests
from numpy import NaN

import src.utils as utils


def call_api(slot):
    """Return a table of weapons of a specific slot using MediaWikiAPI."""
    url = "https://warframe.fandom.com/api.php"
    question = (
        "local CSV = require('Module:Weapons/csv') print(CSV._csvGunComparisonTable('{}'))".format(
            slot
        )
        if slot != "Melee"
        else "local CSV = require('Module:Weapons/csv') print(CSV._csvMeleeComparisonTable())"
    )

    params = {
        "action": "scribunto-console",
        "format": "json",
        "title": "Module:Weapons/csv",
        "content": "",
        "question": question,
        "clear": 1,
    }

    response = requests.get(url, params=params).json()["print"]
    response = (
        response.replace("/\\n/gm", "\n")
        .replace("/\\t/gm", "\t")
        .replace('/\\"/gm', '"')
        .split("calculating FireRate from Burst stats for Gorgon Wraith")[-1]
        .split("\n", 1)[1]
        # .split("Name,")[1]
        # .split("+1\n", 1)[1]
    )

    return response


def correct_kitguns(weapons):
    """Corrects the kitgun stats."""
    with open("kitguns.csv", encoding="utf-8") as file:
        exceptions = pd.read_csv(file)
        for name, type in zip(exceptions["name"], exceptions["slot"]):
            for weapon in weapons["name"]:
                if name.lower() in weapon.lower() and type.lower() in weapon.lower():
                    for column in exceptions.columns.tolist():
                        if column not in ["name", "slot", "Unnamed: 0"]:
                            weapons.loc[
                                weapons["name"] == weapon, column
                            ] = exceptions.loc[
                                exceptions["name"] == name, column
                            ].values[
                                0
                            ]
                    break
        for name, type in zip(exceptions["name"], exceptions["slot"]):
            for weapon in weapons["name"]:
                if name.lower() in weapon.lower() and type.lower() in weapon.lower():
                    weapons.loc[weapons["name"] == weapon, "name"] = name.title()
    file.close()
    return weapons


def update_weapons():
    """Updates the weapons.json file."""
    slots = [
        "Primary",
        "Secondary",
        "Melee",
        "Robotic",
        "Arch-Gun",
        "Arch-Gun (Atmosphere)",
        "Amp",
    ]
    print("Updating weapon database.")
    weapons = pd.concat(
        [pd.read_csv(StringIO(call_api(slot))) for slot in slots]
    ).reset_index(drop=True)
    weapons = weapons.loc[weapons.groupby("Name")["TotalDamage"].idxmax()]
    weapons["TotalDamage"] = weapons["TotalDamage"] + 0.1
    slots.insert(1, "Shotgun")
    alternatives = slots[5:]
    slots = slots[:5]
    column_list = [utils.translate_stats_wiki_wfm(x) for x in weapons.columns.tolist()]
    weapons.rename(
        columns=dict(zip(weapons.columns.tolist(), column_list)), inplace=True
    )

    # remove weapons with no disposition
    weapons = weapons[weapons["disposition"] != NaN]
    weapons = correct_kitguns(weapons)
    weapons["weapon_type"] = weapons.apply(
        lambda x: 1
        if (x["class"] == "Shotgun" and x["slot"] == "Primary")
        else (
            slots.index(x["slot"])
            if x["slot"] in slots
            else (5 if x["slot"] in alternatives else (3 if x["class"] != 4 else 4))
        ),
        axis=1,
    )

    weapons = weapons.loc[:, ~weapons.columns.duplicated(keep="last")]
    weapons.to_json("weapons.json", orient="records")
    print("Weapon database updated.")
