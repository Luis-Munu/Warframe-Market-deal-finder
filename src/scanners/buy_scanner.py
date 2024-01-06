"""Class used to scan the market in search of prices near the ones the user's looking for"""

import src.utils as utils


def scan_buys(name):
    """Method used to retrieve the list of auctions from the user,
    then search for them and apply some conditions and print them
    """

    print("Looking for cheap buys")
    url = "profile/" + name + "/orders?include=profile"
    if (item_list := utils.get_wfm_request(url)) is not None and len(
        list(item_list["buy_orders"])
    ) != 0:
        item_list = list(item_list["buy_orders"])
        while True:
            for product in item_list:
                url = "items/" + product["item"]["url_name"] + "/orders?include=item"
                if (orders := utils.get_wfm_request(url)) is None:
                    continue
                orders = [
                    x
                    for x in orders["orders"]
                    if x["user"]["status"] == "ingame"
                    and x["order_type"] == "sell"
                    and (
                        "mod_rank" not in x
                        or ("mod_rank" in x and x["mod_rank"] == product["mod_rank"])
                    )
                ]
                if not orders:
                    continue
                order = sorted(orders, key=lambda x: x["platinum"])[0]
                if order["platinum"] <= (product["platinum"] * 1.1):
                    utils.wfm_string(
                        product["item"]["url_name"],
                        order["user"]["ingame_name"],
                        str(order["platinum"]),
                    )
    else:
        print("No buy orders found")
