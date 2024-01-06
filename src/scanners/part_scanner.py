import src.utils as utils
import json
import os
import random

""" This file is used to scan the market in order to find the best spare parts to buy
in order to sell them as sets for a profit."""


def part_scanner():
    """Main method"""
    item_dict = check_for_price_db()
    item_dict = {k: v for k, v in item_dict.items() if v["price"] != 9999}
    item_dict = get_diffs(item_dict)
    item_dict = dict(
        sorted(item_dict.items(), key=lambda item: item[1]["price_diff"], reverse=True)
    )
    print_items(item_dict)


def upvote_farmer(email, password):
    utils.login(email, password)
    item_dict = get_items()
    votes = vote_loop(item_dict)
    print("Upvoted " + str(votes) + " users")


def get_items():
    # if file exists, load it
    if os.path.isfile("config/items.json"):
        with open("config/items.json", "r") as file:
            return json.load(file)
    """Gets the items from wfm and returns a dict with the item name as key and a list of components as value"""
    item_list = utils.get_wfm_request("items")["items"]
    set_urls = [x["url_name"] for x in item_list if "set" in x["url_name"][-4:]]
    item_dict = {}

    print("Searching for " + str(len(set_urls)) + " sets, it will take some minutes.")

    for set_item in set_urls:
        req = utils.get_wfm_request("items/" + set_item)
        if req:
            item_dict[set_item] = {}
            item_dict[set_item]["components"] = req["item"]["items_in_set"]
    # store the item dict on a file called items.json
    with open("config/items.json", "w") as file:
        json.dump(item_dict, file)

    return item_dict


def check_for_price_db():
    """Checks if the price database exists, if it does, it loads it, otherwise it creates it"""
    if os.path.isfile("config/previous_prices.json"):
        with open("config/previous_prices.json", "r") as file:
            item_dict = json.load(file)
            item_dict = {k: v for k, v in item_dict.items() if v["price"] != 9999}
            # update only the most profitable items
            item_dict = get_diffs(item_dict)
            profit = dict(
                sorted(
                    item_dict.items(),
                    key=lambda item: item[1]["price_diff"],
                    reverse=True,
                )[:20]
            )

            profit = value_items(profit)
            for item, stats in profit.items():
                item_dict[item]["price_diff"] = stats["price_diff"]
                item_dict[item]["price"] = stats["price"]
    else:
        item_dict = value_items(get_items())
    with open("config/previous_prices.json", "w") as file:
        json.dump(item_dict, file)
    return item_dict


def value_items(item_dict):
    """Updates the value of each set in the dict"""
    for item, comps in item_dict.items():
        item_dict[item]["price"] = get_price(item)
        for i, compo in enumerate(comps["components"]):
            if "set_root" in compo and compo["set_root"] is True:
                item_dict[item]["components"][i]["price"] = 0
                continue
            quantity = compo["quantity_for_set"] if "quantity_for_set" in compo else 1
            item_dict[item]["components"][i]["price"] = (
                get_price(compo["url_name"]) * quantity
            )
            quantity = 0

    return item_dict


def get_names(item_dict):
    names = []
    for item_name, comps in item_dict.items():
        """Gets the names of sellers of buyers of orders of an item from wfm"""
        orders = utils.get_wfm_request("items/" + item_name + "/orders")
        if not orders or len(orders["orders"]) < 1:
            continue

        names.extend(
            [
                order["user"]["ingame_name"]
                for order in orders["orders"]
                if order["user"]["reputation"] > 1 and random.randint(0, 7) < 2
            ]
        )
    return names


def vote_loop(item_dict):
    i = 0
    e = 0
    for item_name, comps in item_dict.items():
        """Gets the names of sellers of buyers of orders of an item from wfm"""
        orders = utils.get_wfm_request("items/" + item_name + "/orders")
        if not orders or len(orders["orders"]) < 1:
            continue
        names = [
            order["user"]["ingame_name"]
            for order in orders["orders"]
            if order["user"]["reputation"] > 1 and random.randint(0, 7) < 2
        ]
        for name in names:
            if utils.upvote_wfm_user(name):
                i += 1
            else:
                e += 1

            if i > 15 or e > 3:
                break
    return i


def get_price(item_name):
    """Gets the price of an item from wfm"""
    orders = utils.get_wfm_request("items/" + item_name + "/orders")
    if not orders or len(orders["orders"]) < 1:
        return 9999
    orders = [
        order
        for order in orders["orders"]
        if order["order_type"] == "sell" and order["user"]["status"] == "ingame"
    ]
    if not orders:
        return 9999
    order = sorted(orders, key=lambda order: order["platinum"])[0]
    return order["platinum"]


def get_diffs(item_dict):
    """Gets the difference between the price of the set and the price of the parts"""
    for item, comps in item_dict.items():
        total = 0
        for component in comps["components"]:
            total += component["price"]
        item_dict[item]["price_diff"] = item_dict[item]["price"] - total
    return item_dict


def print_items(item_dict):
    """Prints the best sets to buy"""

    print("Best sets to buy parts of")
    i = 0
    for set_name, stats in item_dict.items():
        if i == 10:
            break
        i += 1
        print(
            "Item name: "
            + str(set_name.replace("_", " ").title())
            + ", Price Difference: "
            + str(stats["price_diff"])
            + ", Price: "
            + str(stats["price"])
        )
