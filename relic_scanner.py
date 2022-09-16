"""Module used to scan the market in search of good relics to buy and sell."""

import os
import requests
import settings
import utils

item_dict = {}


def scan_relics():
    """Method used to retrieve the relics the market in search of good relics to buy and sell."""

    os.chdir(settings.path + "\\config")

    print("Updating relic database.")
    url = "https://drops.warframestat.us/data/relics.json"
    relic_list = requests.get(url, stream=True)
    if relic_list.status_code != 200:
        return
    relic_list = relic_list.json()["relics"]
    analyzed_relics = []

    with open("best_sell_relics.csv", "w+") as sell_relic:
        with open("best_buy_relics.csv", "w+") as buy_relic:
            #takes the intact and radiant relics and searches for its stats and orders
            relic_list = [relic for relic in relic_list if relic["state"] in ("Intact", "Radiant")]
            print("Analyzing " + str(len(relic_list)) + " relics and " + str(len(relic_list) * 5) + " items.")
            for relic in relic_list:
                relic_stats = utils.get_request("items/" + relic["tier"].lower() + "_" +
                                                relic["relicName"].replace(" ", "_").lower() + "_relic/statistics")
                relic_orders = utils.get_request("items/" + relic["tier"].lower() + "_" +
                                                 relic["relicName"].replace(" ", "_").lower() + "_relic/orders")

                if not relic_stats or (relic_stats and len(relic_stats["statistics_closed"]["90days"]) < 20 or
                                       not relic_orders):
                    continue

                relic_orders = [order for order in relic_orders["orders"] if order["subtype"] == relic["state"].lower()]
                #gets the average value of each relic and updates the value of parts of the dict
                analyzed_relics.append(analyzeRelic(relic, relic_orders))
            #sorts the relics by real value removing empty ones
            analyzed_relics = [relic for relic in analyzed_relics if relic]
            analyzed_relics = sorted(analyzed_relics, key=lambda relic: (relic["value"] / relic["price"]))

            #writes the best relics to sell and buy
            print("Best relics to sell")
            for relic in analyzed_relics[:10]:
                print(relic["name"] + " Price: " + str(relic["price"]) + " Value: " + str(relic["value"]) +
                      " Value/Price: " + str(relic["value"] / relic["price"]))
                sell_relic.write(relic["name"] + " Price: " + str(relic["price"]) + " Value: " + str(relic["value"]) +
                                 " Value/Price: " + str(relic["value"] / relic["price"]))
            print("\nBest relics to buy")
            for relic in analyzed_relics[-10:]:
                print(relic["name"] + " Price: " + str(relic["price"]) + " Value: " + str(relic["value"]) +
                      " Value/Price: " + str(relic["value"] / relic["price"]))
                buy_relic.write(relic["name"] + " Price: " + str(relic["price"]) + " Value: " + str(relic["value"]) +
                                " Value/Price: " + str(relic["value"] / relic["price"]))


def analyzeRelic(relic, relic_orders):
    """Method used to extract the real value of a relic and update its parts."""
    relic_orders = [
        order["platinum"] for order in relic_orders if order["subtype"] == relic["state"].lower() and
        order["order_type"] == "sell" and order["user"]["status"] == "ingame"
    ]
    if not relic_orders:
        return
    relic_orders.sort()
    analyzed_relic = {}
    analyzed_relic["name"] = relic["tier"] + " " + relic["relicName"] + " " + relic["state"]
    analyzed_relic["price"] = relic_orders[0]
    reward_values = []

    for reward in relic["rewards"]:
        reward["itemName"] = reward["itemName"].replace(" Blueprint", "")

        if "forma" in reward["itemName"]:
            reward_values.append(5 * reward["chance"] * 0.01)
            continue

        if reward["itemName"] not in item_dict:
            reward_data = utils.get_request("items/" + reward["itemName"].replace(" ", "_").lower() + "/orders")
            if reward_data:
                reward_orders = sorted([
                    order["platinum"]
                    for order in reward_data["orders"]
                    if order["order_type"] == "sell" and order["user"]["status"] == "ingame"
                ])
                if reward_orders:
                    reward_values.append(reward_orders[0] * reward["chance"] * 0.01)
                    item_dict[reward["itemName"]] = reward_orders[0]
        else:
            reward_values.append(item_dict[reward["itemName"]] * reward["chance"] * 0.01)
    analyzed_relic["value"] = sum(reward_values)
    return analyzed_relic
