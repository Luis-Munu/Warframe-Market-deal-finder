"""Process the auction data from warframe.market and converts
it into a list of riven class objects.
If the user chooses to use the scan mode it will actively check if the auctions are specific
rolls and their price is below the user's price."""

import riven
import settings
import utils


def process_data(response):
    """Process the auction data from warframe.market and converts
    it into a list of riven class objects.
    If the user chooses to use the scan mode it will actively check if the auctions are specific
    rolls and their price is below the user's price."""

    riven_list = {}
    for auction in response:
        if auction["closed"] is True:
            continue
        if (auction["item"]["weapon_url_name"] + auction["item"]["name"] + auction["owner"]["ingame_name"]
                in riven_list):
            continue
        # converts the dict of riven stats to list in order to get the negative in the last spot.
        # if there's any way to fast check if there's a negative in the stats while using a dict
        # then this would be innecessary.
        stats = [list() for x in range(4)]
        for i, stat in enumerate(auction["item"]["attributes"]):
            stats[i].extend([stat["positive"], stat["url_name"], stat["value"]])
        # removes empty positions of stats.
        stats = list(filter(None, stats))
        # sorts the stats list to put the negative stat at the end.
        stats.sort(key=lambda x: x[0] if len(x) > 0 else False, reverse=True)

        # adds the riven into the riven_list.
        riv = riven.Riven(
            auction["item"]["weapon_url_name"],
            auction["item"]["name"],
            auction["starting_price"],
            auction["buyout_price"],
            auction["owner"]["ingame_name"],
            auction["item"]["polarity"],
            auction["item"]["re_rolls"],
            auction["item"]["mastery_level"],
            auction["item"]["mod_rank"],
            stats,
        )
        riven_list[auction["item"]["weapon_url_name"] + auction["item"]["name"] + auction["owner"]["ingame_name"]] = riv
    return riven_list


def export_txt(results):
    """Writes every riven message on their respective folders"""

    content_dict = {}
    for riv in results:
        for path in riv.paths:
            if path in content_dict:
                content_dict[path] += riv.message
            else:
                content_dict[path] = riv.message
    for path, message in content_dict.items():
        ducat_list = open(path, "w", encoding="utf-8")
        ducat_list.write(message)
