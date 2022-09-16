"""File used to prepare the urls of the rivens, generating
    combinations of the possible stats and weapons"""
from itertools import combinations
import time
import settings
from utils import get_weapon_type, check_variant


def create_generic_url(stats=[], weapon_type=0):
    """Creates the url of a search with given stats."""
    if "stat3" in stats:
        return [
            "/auctions/search?type=riven&positive_stats=" + stats["stat1"] + "," + stats["stat2"] + "," +
            stats["stat3"] + "&negative_stats=has&polarity=any&sort_by=price_asc"
        ]
    return add_positive(
        "/auctions/search?type=riven&positive_stats=" + stats["stat1"] + "," + stats["stat2"],
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
            "/auctions/search?type=riven&weapon_url_name=" + weapon + "&polarity=any&re_rolls_max=0&sort_by=price_asc"
        ]
    # if the wanted riven already has a stat list it either adds a
    # third positive or returns a list of urls for it.
    if stats:
        if "stat3" in stats:
            if "negative" in stats:
                return [
                    "/auctions/search?type=riven&weapon_url_name=" + weapon + "&positive_stats=" + stats["stat1"] +
                    "," + stats["stat2"] + "," + stats["stat3"] + "&negative_stats=" + stats["negative"] +
                    "&polarity=any&sort_by=price_asc"
                ]
            return [
                "/auctions/search?type=riven&weapon_url_name=" + weapon + "&positive_stats=" + stats["stat1"] + "," +
                stats["stat2"] + "," + stats["stat3"] + "&negative_stats=has&polarity=any&sort_by=price_asc"
            ]
        neg = ("&negative_stats=" + stats["negative"] if "negative" in stats else "&negative_stats=has")
        return [
            url + neg for url in add_positive(
                "/auctions/search?type=riven&weapon_url_name=" + weapon + "&positive_stats=" + stats["stat1"] + "," +
                stats["stat2"],
                get_weapon_type(weapon),
                stats,
            )
        ]
    return add_stats(weapon)


def add_stats(weapon):
    """Used to create generic godrolls for a selected weapon."""

    weapon_type = get_weapon_type(weapon)
    res = set()
    for combination in combinations(settings.decent_positives[weapon_type], 3):
        url = "/auctions/search?type=riven&weapon_url_name=" + weapon + "&positive_stats="
        for comb in combination:
            url += comb + "&"
        url += "negative_stats=has&polarity=any&sort_by=price_asc"
        res.add(url)
    return res


def add_positive(url, weapon_type, stats):
    """Adds specific 2 stat rivens to the url and also adds urls with a third positive."""

    result = [
        url + "," + stat + "&negative_stats=has&polarity=any&sort_by=price_asc"
        for stat in settings.decent_positives[weapon_type]
        if stat not in stats.values()
    ]
    # good enough stats to have that aren't too detrimental to your riven.
    result = list(set(result))
    result.append(url)
    return result


def immovable_urls():
    """Extremely long search, not recommended for anyone unless you can wait for many hours."""

    result = set()
    for weapon in list(settings.weapon_list.keys()):
        if check_variant(weapon):
            continue
        for weapon_type in get_weapon_type(weapon):
            for weapon_comb in settings.combinations[weapon_type]:
                for url in create_specific_url(weapon, weapon_comb, False):
                    result.add(url)
    return list(result)


def generic_urls():
    """It creates a list of urls with generic combos with no explicit weapon."""

    result = set()
    for i in range(len(settings.combinations)):
        for weapon_comb in settings.combinations[i]:
            for url in create_generic_url(weapon_comb, i):
                result.add(url)
    return list(result)


def wished_urls():
    """It creates a list of urls with generic godroll combos for wanted weapons.
    it provides better accuraccy."""

    result = set()
    for i in range(len(settings.wished_weapons)):
        for weapon in settings.wished_weapons[i]:
            if check_variant(weapon):
                continue
            for weapon_comb in settings.combinations[i]:
                for url in create_specific_url(weapon, weapon_comb, False):
                    result.add(url)
    return list(result)


def unrolled_urls():
    """It creates a list of urls for unrolleds of selected weapons.
    depending on the kind of search the user chooses,
    it searches for specific wanted weapons or all the weapons."""

    result = set()
    unroll = ([k for d in settings.weapon_list for k in d]
              if settings.non_existant_search or settings.slow_search else settings.wished_unrolleds)
    for weapon in unroll:
        for url in create_specific_url(weapon, [], True):
            result.add(url)
    return list(result)


def specific_urls():
    """It creates a list of urls for specific users inputted by the user in the files."""

    result = set()
    for riv in settings.wished_rivens:
        for wished_roll in settings.wished_rivens[riv]:
            for url in create_specific_url(riv, wished_roll["stats"], False):
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


def data_creation():
    """Prepares the weapon list"""

    url_list = []
    # Should never be used unless you have all the time in the world.
    # it searches for every godroll and unroll.
    if settings.non_existant_search:
        url_list.extend(immovable_urls())
    # creates the url of generic rolls.
    if settings.fast_search or settings.medium_search or settings.slow_search:
        url_list.extend(generic_urls())
    # creates the url of generic rolls for wished weapons.
    if settings.slow_search or settings.medium_search:
        url_list.extend(wished_urls())
    # creates the url of unrolleds
    if settings.slow_search:
        url_list.extend(unrolled_urls())
    # creates the url of specific rolls
    if (settings.specific_search or settings.fast_search or settings.medium_search or settings.slow_search or
            settings.non_existant_search):
        url_list.extend(specific_urls())
    # creates the url of a specific weapon search
    if settings.specific_weapon:
        url_list.extend(weapon_urls(settings.weapon_name, settings.weapon_stats))

    url_list = list(set(url_list))
    time_left = time.strftime("%H:%M:%S", time.gmtime(len(url_list)))
    print(str(len(url_list)) + " possible riven combinations. estimated wait time: " + str(time_left))

    return url_list
