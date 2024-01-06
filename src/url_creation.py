"""File used to prepare the urls of the rivens, generating
    combinations of the possible stats and weapons"""
from itertools import combinations

import src.settings as settings
from src.utils import check_variant, get_weapon_type, translate_stat_wfm_rh


def data_creation():
    """Prepares the weapon list"""

    url_list = []

    # creates the url of generic rolls.
    url_list.extend(generic_urls())
    # creates the url of specific rolls
    url_list.extend(specific_urls())

    if settings.specific_weapon:
        # creates the url of a specific weapon search
        url_list.extend(weapon_urls(settings.weapon_name, settings.weapon_stats))

    if settings.search_type:
        # creates the url of generic rolls for wanted weapons.
        url_list.extend(wanted_urls())
        # creates the url of unrolleds
        url_list.extend(unrolled_urls())

    url_list = list(set(url_list))

    print(str(len(url_list)) + " possible riven combinations.")

    if settings.search_type:
        rm_list = [build_url_rh(extract_url_data(url)) for url in url_list]
        rm_list = list(filter(None, rm_list))
        return [url_list, rm_list]

    return url_list


def create_generic_url(stats=[], weapon_type=0):
    """Creates the url of a search with given stats."""
    if stats and "stat3" in stats:
        return [
            "auctions/search?type=riven&positive_stats="
            + stats["stat1"]
            + ","
            + stats["stat2"]
            + ","
            + stats["stat3"]
            + "&negative_stats=has&polarity=any&sort_by=price_asc"
        ]
    return add_positive(
        "auctions/search?type=riven&positive_stats="
        + stats["stat1"]
        + ","
        + stats["stat2"],
        weapon_type,
        stats,
    )


def create_specific_url(weapon, stats=[], unroll=False):
    """Used for specific rolls, given a weapon, it creates a url based on its stats,
    if no stats are given it creates a list of urls with generic godrolls.
    If the unroll parameter is True, it returns an unrolled url"""

    # specific case used to create the url of an unrolled fast.
    if unroll:
        return [
            "auctions/search?type=riven&weapon_url_name="
            + weapon
            + "&polarity=any&re_rolls_max=0&sort_by=price_asc"
        ]
    # if the wanted riven already has a stat list it either adds a
    # third positive or returns a list of urls for it.
    if stats:
        if "stat3" in stats and stats["stat3"] == stats["stat3"]:
            if "negative" in stats and len(stats["negative"]) > 0:
                return [
                    "auctions/search?type=riven&weapon_url_name="
                    + weapon
                    + "&positive_stats="
                    + stats["stat1"]
                    + ","
                    + stats["stat2"]
                    + ","
                    + stats["stat3"]
                    + "&negative_stats="
                    + stats["negative"]
                    + "&polarity=any&sort_by=price_asc"
                ]
            return [
                "auctions/search?type=riven&weapon_url_name="
                + weapon
                + "&positive_stats="
                + stats["stat1"]
                + ","
                + stats["stat2"]
                + ","
                + stats["stat3"]
                + "&negative_stats=has&polarity=any&sort_by=price_asc"
            ]
        if "negative" in stats and len(stats["negative"]) > 0:
            neg = (
                "&negative_stats=" + stats["negative"]
                if "negative" in stats
                else "&negative_stats=has"
            )
            return [
                url + neg
                for url in add_positive(
                    "auctions/search?type=riven&weapon_url_name="
                    + weapon
                    + "&positive_stats="
                    + stats["stat1"]
                    + ","
                    + stats["stat2"],
                    get_weapon_type(weapon),
                    stats,
                )
            ]
    return add_stats(weapon)


def extract_url_data(url):
    """Extracts the weapon and stats from a url."""

    weapon, stats, neg = None, None, None

    if "weapon_url_name" in url:
        weapon = url.split("weapon_url_name=")[1].split("&")[0]
    if "positive_stats" in url:
        stats = []
        sturl = url.split("positive_stats=")[1].split("&negative")[0]
        for stat in sturl.split(","):
            stats.append(stat)
    if "negative_stats" in url:
        neg = url.split("negative_stats=")[1].split("&")[0]
    return [stats, weapon, neg]


def build_url_rh(info):
    url = ""
    stats, weapon, neg = info
    if weapon:
        weapon_name = weapon.replace("_", " ").title()
        weapon_name = [w for w in settings.weapons if w["name"] == weapon_name][0][
            "internal_name"
        ]
        weapon_type = 1 if get_weapon_type(weapon_name) != 3 else 0
        url += weapon_name + "&interval=3 day&buffs="
        if stats:
            url += ",".join(
                [translate_stat_wfm_rh(stat, weapon_type) for stat in stats]
            )
        if neg:
            if neg != "has":
                url += "&curses=" + translate_stat_wfm_rh(neg, weapon_type)
            url += "&exact=1&needsCurse=1"
        else:
            url += "&exact=1&needsCurse=0"
        return url
    return None


def add_stats(weapon):
    """Used to create generic godrolls for a selected weapon."""

    weapon_type = get_weapon_type(weapon)
    res = set()
    for combination in combinations(settings.positives[weapon_type], 3):
        url = (
            "auctions/search?type=riven&weapon_url_name=" + weapon + "&positive_stats="
        )
        for comb in combination:
            url += comb + ","
        url = url[:-1] + "&negative_stats=has&polarity=any&sort_by=price_asc"
        res.add(url)
    return res


def add_positive(url, weapon_type, stats):
    """Adds specific 2 stat rivens to the url and also adds urls with a third positive."""

    result = [
        url + "," + stat + "&negative_stats=has&polarity=any&sort_by=price_asc"
        for stat in settings.positives[weapon_type]
        if stat not in stats.values()
    ]
    # good enough stats to have that aren't too detrimental to your riven.
    result = list(set(result))
    result.append(url)
    return result


def generic_urls():
    """It creates a list of urls with generic combos with no explicit weapon."""

    result = set()
    for i, weapon_type in enumerate(settings.combinations.values()):
        for weapon_comb in weapon_type:
            for url in create_generic_url(weapon_comb, i):
                result.add(url)
    return list(result)


def wanted_urls():
    """It creates a list of urls with generic godroll combos for wanted weapons.
    it provides better accuraccy."""

    result = set()
    for i, weapon_type in enumerate(settings.wanted_wp):
        for weapon in weapon_type:
            for url in create_specific_url(weapon):
                result.add(url)
            if check_variant(weapon):
                continue
            for weapon_t in settings.combinations.values():
                for weapon_comb in weapon_t:
                    for url in create_generic_url(weapon_comb, i):
                        result.add(url)
    return list(result)


def unrolled_urls():
    """It creates a list of urls for unrolleds of all the weapons."""

    result = set()
    for weapon in settings.wanted_unroll:
        for url in create_specific_url(weapon, [], True):
            result.add(url)
    return list(result)


def specific_urls():
    """It creates a list of urls for specific users inputted by the user in the files."""

    result = set()
    for weapon_comb in settings.wanted_rv:
        for url in create_specific_url(
            weapon_comb["weapon"],
            {
                "stat1": weapon_comb["stat1"],
                "stat2": weapon_comb["stat2"],
                "stat3": weapon_comb["stat3"],
                "negative": weapon_comb["negative"],
            },
            False,
        ):
            result.add(url)

    return list(result)


def weapon_urls(weapon, stats=[]):
    """Module used in the specific situation the user just want
    to search for combos for a single weapon.
    if a stat list is provided it searches just for it, otherwise
    it searches for generic godrolls."""

    result = set()
    if not stats:
        for url in add_stats(weapon):
            result.add(url)
    else:
        for url in create_specific_url(weapon, stats, False):
            result.add(url)
    return list(result)
