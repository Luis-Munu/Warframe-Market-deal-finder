"""File used to update the weapon list used on the rest of modules"""

import os
import json
import requests

weapon_categories = ["primary", "secondary", "melee", "arch-gun", "sentinel_weapons"]
path = os.getcwd() + "\\config"
weapons = {}


def solve_category(weapon):
    """Method used to fill the weapon category of some exceptions"""

    if "kitgun" in weapon["type"]:
        weapon["category"] = "secondary"
    if "zaw" in weapon["type"]:
        weapon["category"] = "melee"
    if weapon["type"] == "shotgun":
        weapon["category"] = weapon["type"]
    if weapon["category"] in ["sentinel_weapons", "arch-gun"]:
        weapon["category"] = "primary"
    return weapon


def get_weapons():
    """Requests, analyzes and stores all the weapons form the WFCD community github."""

    weapon_request = requests.get(
        "https://raw.githubusercontent.com/wfcd/warframe-items/master/data/json/all.json"
    )
    weapon_request = weapon_request.json()
    weapon_request = [x for x in weapon_request if "omega_attenuation" in x]
    for weapon in weapon_request:
        weapon = solve_category(weapon)
        if weapon["category"] not in ["primary", "shotgun", "secondary", "melee"]:
            continue
        weapon["name"] = weapon["name"].replace(" ", "_").replace("&", "and").lower()

        if not weapon["category"] in weapons:
            weapons[weapon["category"]] = {}
            weapons[weapon["category"]][weapon["name"]] = {}
            weapons[weapon["category"]][weapon["name"]]["disposition"] = weapon["omega_attenuation"]
            weapons[weapon["category"]][weapon["name"]]["critical_chance"] = weapon[
                "critical_chance"
            ]
            weapons[weapon["category"]][weapon["name"]]["critical_damage"] = weapon[
                "critical_multiplier"
            ]
            weapons[weapon["category"]][weapon["name"]]["status_chance"] = weapon["proc_chance"]
            weapons[weapon["category"]][weapon["name"]]["type"] = weapon["type"]

        if "attacks" in weapon:
            for attack in weapon["attacks"]:
                if "damage" in attack:
                    weapons[weapon["category"]][weapon["name"]]["attacks"] = {}
                    weapons[weapon["category"]][weapon["name"]]["attacks"][attack["name"]] = {}
                    weapons[weapon["category"]][weapon["name"]]["attacks"][attack["name"]][
                        "damage_types"
                    ] = attack["damage"]
                    if (
                        "slash"
                        in weapons[weapon["category"]][weapon["name"]]["attacks"][attack["name"]][
                            "damage_types"
                        ]
                    ):
                        weapons[weapon["category"]][weapon["name"]]["attacks"][attack["name"]][
                            "slash_percent"
                        ] = weapons[weapon["category"]][weapon["name"]]["attacks"][attack["name"]][
                            "damage_types"
                        ][
                            "slash"
                        ] / (
                            weapon["total_damage"] + 0.001
                        )
                    else:
                        weapons[weapon["category"]][weapon["name"]]["attacks"][attack["name"]][
                            "slash_percent"
                        ] = 0
        else:
            weapons[weapon["category"]][weapon["name"]]["attacks"] = {}
            weapons[weapon["category"]][weapon["name"]]["attacks"][attack["name"]] = {}
            weapons[weapon["category"]][weapon["name"]]["attacks"][attack["name"]][
                "damage_types"
            ] = {}
            weapons[weapon["category"]][weapon["name"]]["attacks"][attack["name"]][
                "slash_percent"
            ] = 0

    with open("weapon_list.json", "w", encoding="utf-8") as weapon_file:
        json.dump(weapons, weapon_file)
