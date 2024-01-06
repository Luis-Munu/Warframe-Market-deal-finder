"""Module used to scan the market in search of good ducat/plat ratio items"""

import os
from datetime import datetime

import src.settings as settings
import src.utils as utils

trades = {}


def use_ducanator(limit):
    """It starts the search based on the limit the user has set"""
    os.chdir(settings.path + "\\config")
    get_orders(limit)


def seller_prof(seller):
    """Method used to get the value of a seller"""
    global trades
    if seller not in trades:
        seller_orders = utils.get_wfm_request(
            "profile/" + seller + "/orders?include=profile"
        )["sell_orders"]
        seller_orders = sorted(seller_orders, key=lambda ord: ord["platinum"])
        item_num = 0
        trader = {}
        trader["items"] = []
        trader["price"] = 0
        trader["ducats"] = 0
        for sell in seller_orders:
            if item_num < 6 and "ducats" in sell["item"]:
                item_num += sell["quantity"]
                trader["items"].append(
                    {
                        "name": sell["item"]["url_name"],
                        "price": sell["platinum"],
                        "ducats": sell["item"]["ducats"],
                        "quantity": sell["quantity"],
                    }
                )
                trader["price"] += sell["platinum"]
                trader["ducats"] += sell["item"]["ducats"]
        if item_num >= 6:
            if len(trader["items"]) > 1:
                trades[seller] = trader
                trades[seller]["value"] = (
                    trades[seller]["ducats"] / trades[seller]["price"]
                )
                trades = dict(sorted(trades.items(), key=lambda ord: ord[1]["value"]))


def get_orders(limit):
    """Method used to get the ducats/plat value of the items.
    A dict is created in order to save the data of each item,
    some other useful data is also stored"""

    ducat_dict = {}

    ducat_list = open("ducat_list.csv", "r", encoding="utf-8")

    # Creates a dict with the item name as key and the ducat value as value
    for line in ducat_list.readlines():
        item_name, ducats = line.replace("\n", "").split(",")
        if item_name not in ducat_dict:
            ducat_dict[item_name] = {}
        ducat_dict[item_name]["ducats"] = int(ducats)
        item_data = ducat_dict[item_name]

        # Gets the orders for the items in the dict and calculates the ducat/plat value
        result = utils.get_wfm_request("items/" + item_name + "/orders")["orders"]
        result = [
            x
            for x in result
            if x["user"]["status"] == "ingame"
            and x["user"]["reputation"] > 1
            and x["order_type"] == "sell"
        ]
        if len(result) <= 1:
            continue
        result = sorted(result, key=lambda ord: ord["platinum"])[0]
        item_data["price"] = result["platinum"]
        item_data["seller"] = result["user"]["ingame_name"]
        item_data["quantity"] = result["quantity"]
        item_data["value"] = item_data["ducats"] / item_data["price"]

        # Checks if the item is worth buying and prints its data on real time.
        if item_data["value"] >= limit:
            line = (
                datetime.now().strftime("%H:%M:%S")
                + " item: "
                + item_name.title().replace("_", " ")
                + " ducats/plat: "
                + str(item_data["value"])
                + " price: "
                + str(item_data["price"])
                + " quantity: "
                + str(item_data["quantity"])
                + " seller: "
                + item_data["seller"]
            )
            print(line)

            # Checks the best possible traders for said item and updates their inventory.
            seller_prof(item_data["seller"])
            utils.wfm_string(item_name, item_data["seller"], item_data["price"])
            if len(trades) >= 6:
                print("Best current trades:\n")
                for i in range(1, 7):
                    line = (
                        "Seller: "
                        + str(list(trades)[-i])
                        + " ducats/plat: "
                        + str(trades[list(trades)[-i]]["value"])
                        + " price: "
                        + str(trades[list(trades)[-i]]["price"])
                        + " ducats: "
                        + str(trades[list(trades)[-i]]["ducats"])
                        + "\n"
                    )
                    print(line)

    # Prints the best possible trades on a wfm like string along with the quantities of the items.
    for item in trades[list(trades)[-1]]["items"]:
        utils.wfm_string(item["name"], str(list(trades)[-1]), item["price"])
        print(str(item["quantity"]) + " units of " + item["name"] + "\n")

    ducat_list.close()


def retrieve_list():
    """Method used to get the list of prime parts or sets of wfm."""

    string_set = set()
    result = utils.get_wfm_request("items")
    if result:
        item_list = [item["url_name"] for item in result["items"]]
        result_file = open("item_list.csv", "w", encoding="utf-8")
        for item in item_list:
            if "prime" in item and "set" not in item and "primed" not in item:
                if item + "\n" not in string_set:
                    result_file.write(item + "\n")
                string_set.add(item + "\n")
        result_file.close()


def retrieve_ducats():
    """Method used to get the value in ducats of the item list."""

    item_list = open("item_list.csv", "r", encoding="utf-8")
    ducat_list = open("ducat_list.csv", "w", encoding="utf-8")
    string_set = set()
    lines = item_list.readlines()
    url_list = []
    for line in lines:
        url_list.append("items/" + line.replace("\n", ""))
    for url in url_list:
        result = utils.get_wfm_request(url)
        if result:
            result = result["item"]["items_in_set"]
            for set_item in result:
                if set_item["url_name"] not in string_set:
                    if set_item["ducats"] >= 45:
                        ducat_list.write(
                            set_item["url_name"] + "," + str(set_item["ducats"]) + "\n"
                        )
                        string_set.add(set_item["url_name"])
    item_list.close()
    ducat_list.close()


def update_ducats():
    """Method used to update the item and ducat lists"""

    os.chdir(settings.path + "\\config")
    retrieve_list()
    retrieve_ducats()
