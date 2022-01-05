"""Class used to scan the market in search of good endo/plat items"""

from datetime import datetime
import os
import json
import settings
import utils

# Endo value of each mod rarity
rarity_value = {
    "Common": 7678,
    "Uncommon": 15355,
    "Peculiar": 15355,
    "Rare": 23033,
    "Amalgam": 23033,
    "Galvanized": 23033,
    "Legendary": 30710,
}

# Sculpture list, with its associated value and rank
sculpture_list = [
    {"name": "Ayatan Anasa Sculpture", "value": 3450, "max_rank": 4},
    {"name": "Ayatan Kitha Sculpture", "value": 3000, "max_rank": 5},
    {"name": "Ayatan Orta Sculpture", "value": 2700, "max_rank": 4},
    {"name": "Ayatan Zambuka Sculpture", "value": 2600, "max_rank": 3},
    {"name": "Ayatan Hemakara Sculpture", "value": 2600, "max_rank": 3},
    {"name": "Ayatan Vaya Sculpture", "value": 1800, "max_rank": 3},
    {"name": "Ayatan Piv Sculpture", "value": 1725, "max_rank": 3},
    {"name": "Ayatan Velana Sculpture", "value": 1575, "max_rank": 3},
    {"name": "Ayatan Sah Sculpture", "value": 1500, "max_rank": 3},
    {"name": "Ayatan Ayr Sculpture", "value": 1425, "max_rank": 3},
]


def get_mods():
    """Method used to read the mod database"""

    with open("mods.json", encoding="utf8") as json_file:
        data = json.load(json_file)
        data = [
            x
            for x in data
            if "fusionLimit" in x and x["fusionLimit"] == 10 and x["rarity"] != "common"
        ]

        return [
            {"name": x["name"], "max_rank": x["fusionLimit"], "rarity": x["rarity"]} for x in data
        ]


def endo_scan(endo_limit=400):
    """Method used to scan the market using the mod database
    Calculates the endo/plat value of each item and writes it if
    it's above the user's endo_limit
    """
    os.chdir(settings.path + "\\config")
    print("The program will look for mods and ayatan sculptures to endo")
    print("Loading database")
    item_list = sculpture_list
    item_list.extend(get_mods())

    while True:
        for item in item_list:
            url = "items/" + item["name"].replace(" ", "_").lower() + "/orders?include=item"
            result = utils.get_request(url)
            if result:
                result = result["orders"]
                result = [
                    x
                    for x in result
                    if x["order_type"] == "sell"
                    and x["platform"] == "pc"
                    and x["mod_rank"] == item["max_rank"]
                    and x["user"]["status"] == "ingame"
                ]
                if not result:
                    continue
                order = sorted(result, key=lambda x: x["platinum"])[0]
                value = (
                    rarity_value[item["rarity"]] / order["platinum"]
                    if "rarity" in item
                    else item["value"] / order["platinum"]
                )
                if value > endo_limit:
                    print(
                        datetime.now().strftime("%H:%M:%S")
                        + " item: "
                        + item["name"]
                        + " endo/plat: "
                        + str(value)
                        + " price: "
                        + str(order["platinum"])
                        + " quantity: "
                        + str(order["quantity"])
                        + " seller: "
                        + order["user"]["ingame_name"]
                    )
                    utils.wfm_string(
                        item["name"],
                        order["user"]["ingame_name"],
                        order["platinum"],
                        order["mod_rank"],
                    )
