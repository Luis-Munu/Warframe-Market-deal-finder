"""Module used to scan the market in search of good deals."""

from datetime import datetime
from ratelimit import limits, sleep_and_retry
import utils


@sleep_and_retry
@limits(calls=3, period=1.5)
def deal_finder():
    """Method used to scan the market in search of good prices.
    The conditions used are:
        -Be below 70% of the average price
        -Be below 70% of the other 3 best sells
    """

    print("Looking for deals")
    item_list = utils.get_request("items")
    if not item_list:
        return
    item_list = [x["url_name"] for x in item_list["items"]]
    while True:
        for item in item_list:
            item_stats = utils.get_request("items/" + item + "/statistics")
            if item_stats is None:
                continue
            item_stats = item_stats["statistics_closed"]["48hours"]
            if not item_stats:
                continue
            if "mod_rank" in item_stats[0]:
                stat_list = analyze_mod(item, item_stats)
            else:
                stat_list = [analyze_part(item, item_stats)]

            item_orders = utils.get_request("items/" + item + "/orders?include=item")
            if item_orders is None:
                continue

            item_orders = [x for x in item_orders["orders"] if x["user"]["status"] == "ingame"]
            item_orders.sort(key=lambda x: x["platinum"])
            sell_orders = [x for x in item_orders if x["order_type"] == "sell"]

            if sell_orders == 0:
                continue

            for i in (0, 1):
                for rank_stats in stat_list:
                    sell_rank = ([
                        x for x in sell_orders if "mod_rank" in x and x["mod_rank"] == rank_stats["mod_rank"]
                    ] if "mod_rank" in rank_stats else sell_orders)
                    if len(sell_rank) < [1, 4][i]:
                        continue

                    order = sell_rank[0]
                    if not i:
                        rank_stat = (next(x for x in rank_stats if order["mod_rank"] == x["mod_rank"]) if isinstance(
                            type(rank_stats), list) else rank_stats)

                    if (comparator(order, [rank_stat, sell_rank][i], i) and order["platinum"] > 10 and
                        (rank_stats["volume"] > 5 or order["platinum"] > 100)):
                        print_deal(
                            item,
                            order["user"]["ingame_name"],
                            order["platinum"],
                            order["quantity"],
                            ["first", "second"][i],
                            [
                                rank_stats["lowest_2d_average"],
                                sum([c["platinum"] for c in sell_rank[0:3]]) / 3,
                            ][i],
                            order.get("mod_rank"),
                        )


def analyze_mod(item, item_stats):
    """Method used to analyze a mod item.
    It gets the stats of every rank of the mod.
    """
    mod_stats = []
    timestamps_rank = {}
    for timestamp in item_stats:
        if timestamp["mod_rank"] not in timestamps_rank:
            timestamps_rank[timestamp["mod_rank"]] = []
        timestamps_rank[timestamp["mod_rank"]].append([
            timestamp["avg_price"],
            timestamp["min_price"],
            timestamp["volume"],
        ])
    for key, rank_stats in timestamps_rank.items():
        mod_stats.append({
            "name": item,
            "mod_rank": key,
            "item_2d_average": sum([tmp[0] for tmp in rank_stats]) / len(rank_stats),
            "lowest_2d_average": sum([tmp[1] for tmp in rank_stats]) / len(rank_stats),
            "latest_average": rank_stats[0][0],
            "latest_lowest": rank_stats[0][1],
            "volume": sum([tmp[2] for tmp in rank_stats]),
        })
    return mod_stats


def analyze_part(item, item_stats):
    """Method used to analyze a tradable item that isn't a mod."""

    return {
        "name": item,
        "item_2d_average": sum([timestamp["avg_price"] for timestamp in item_stats]) / len(item_stats),
        "lowest_2d_average": sum([timestamp["min_price"] for timestamp in item_stats]) / len(item_stats),
        "latest_average": item_stats[0]["avg_price"],
        "latest_lowest": item_stats[0]["min_price"],
        "volume": sum([timestamp["volume"] for timestamp in item_stats]),
    }


def comparator(order, item_stats, mode):
    """Checks if the item satisfies the conditions."""
    if mode:
        return order["platinum"] < (sum([c["platinum"] for c in item_stats[0:3]]) / 3 * 0.7)
    return order["platinum"] < item_stats["lowest_2d_average"] * 0.7


def print_deal(item_name, seller_name, price, quantity, approach, benefit, rank=None):
    """Simple print function."""
    if rank is not None:
        print(datetime.now().strftime("%H:%M:%S") + " item: " + item_name.replace("_", " ").title() + ", rank: " +
              str(rank) + ", price: " + str(price) + "p, seller: " + str(seller_name) + ", quantity: " + str(quantity) +
              " " + approach + " approach, normal value: " + str(benefit))
    else:
        print(datetime.now().strftime("%H:%M:%S") + " item: " + item_name.replace("_", " ").title() + " price: " +
              str(price) + "p seller: " + str(seller_name) + " quantity: " + str(quantity) + " " + approach +
              " approach, normal value: " + str(benefit))
    utils.wfm_string(
        item_name.replace("_", " ").title(),
        seller_name,
        price,
        rank,
    )
