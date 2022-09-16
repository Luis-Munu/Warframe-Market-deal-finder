import utils
""" This file is used to scan the market in order to find the best spare parts to buy in order to sell them as sets for a profit."""


def part_scanner():
    """Main method"""
    item_dict = get_items()
    item_dict = value_items(item_dict)
    item_dict = {k: v for k, v in item_dict.items() if v["price"] != 9999}
    item_dict = get_diffs(item_dict)
    item_dict = dict(sorted(item_dict.items(), key=lambda item: item[1]["price_diff"], reverse=True))
    print_items(item_dict)


def get_items():
    """Gets the items from wfm and returns a dict with the item name as key and a list of components as value"""
    item_list = utils.get_request("items")["items"]
    set_urls = [x["url_name"] for x in item_list if "set" in x["url_name"][-4:]]
    item_dict = {}

    print("Searching for " + str(len(set_urls)) + " sets, it'll take some minutes.")

    for set_item in set_urls:
        req = utils.get_request("items/" + set_item)
        if req:
            item_dict[set_item] = {}
            item_dict[set_item]["components"] = req["item"]["items_in_set"]
    return item_dict


def value_items(item_dict):
    """Updates the value of each set in the dict"""
    for item, comps in item_dict.items():
        item_dict[item]["price"] = get_price(item)
        for i, compo in enumerate(comps["components"]):
            if "set_root" in compo and compo["set_root"] == True:
                item_dict[item]["components"][i]["price"] = 0
                continue
            quantity = compo["quantity_for_set"] if "quantity_for_set" in compo else 1
            item_dict[item]["components"][i]["price"] = get_price(compo["url_name"]) * quantity
            quantity = 0
    return item_dict


def get_price(item_name):
    """Gets the price of an item from wfm"""
    orders = utils.get_request("items/" + item_name + "/orders")
    if not orders or len(orders["orders"]) < 1:
        return 9999
    orders = [
        order for order in orders["orders"] if order["order_type"] == "sell" and order["user"]["status"] == "ingame"
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
        print("Item name: " + str(set_name.replace("_", " ").title()) + ", Price Difference: " +
              str(stats["price_diff"]) + ", Price: " + str(stats["price"]))
