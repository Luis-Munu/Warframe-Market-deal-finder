"""Module used to scan the market in search of good ducat/plat ratio items"""

from datetime import datetime
import os
import settings
import utils


def use_ducanator(options):
    """It starts the search based on the scan option introduced by the user"""
    os.chdir(settings.path + "\\config")
    if options[0] is False:
        while True:
            get_orders(options[1])
    else:
        get_orders(options[1])


def get_orders(limit):
    """Method used to get the ducats/plat value of the items.
    A dict is created in order to save the data of each item,
    some other useful data is also stored"""

    ducat_dict = {}

    ducat_list = open("ducat_list.csv", "r", encoding="utf-8")
    ducanator = open("ducanated.csv", "a+", encoding="utf-8")
    for line in ducat_list.readlines():
        item_name, ducats = line.replace("\n", "").split(",")
        if item_name not in ducat_dict:
            ducat_dict[item_name] = {}
        ducat_dict[item_name]["ducats"] = int(ducats)
        item_dict = ducat_dict[item_name]
        result = utils.get_request("items/" + item_name + "/orders")
        if not result:
            continue
        result = sorted(result["orders"], key=lambda ord: ord["platinum"])
        for order in result:
            if order["user"]["status"] == "ingame" and order["order_type"] == "sell":
                if "sell" not in item_dict:
                    item_dict["sell"] = []
                item_dict["sell"].append(
                    [order["platinum"], order["user"]["ingame_name"], order["quantity"]]
                )
        if "sell" in item_dict and len(item_dict["sell"]) >= 1:
            item_dict["prices"] = sorted(item_dict["sell"], key=lambda x: x[0])[0]
        else:
            continue
        item_dict["value"] = item_dict["ducats"] / item_dict["prices"][0]
        if item_dict["value"] >= limit:
            line = (
                datetime.now().strftime("%H:%M:%S")
                + " item: "
                + item_name.title().replace("_", " ")
                + " ducats/plat: "
                + str(item_dict["value"])
                + " price: "
                + str(item_dict["prices"][0])
                + " quantity: "
                + str(item_dict["prices"][2])
                + " seller: "
                + item_dict["prices"][1]
            )
            print(line)
            utils.wfm_string(item_name, item_dict["prices"][1], item_dict["prices"][0])
            ducanator.write(line)
    ducanator.close()
    ducat_list.close()


def retrieve_list():
    """Method used to get the list of prime parts or sets of wfm."""

    string_set = set()
    result = utils.get_request("items")
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
        url_list.append("/items/" + line.replace("\n", ""))
    for url in url_list:
        result = utils.get_request(url)
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
