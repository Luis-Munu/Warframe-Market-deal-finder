"""Common methods used by all modules"""

import json
import requests
import settings

JWT_TOKEN = None
HEADERS = {}
INGAME_NAME = None
WFM_API = "https://api.warframe.market/v1/"


def get_request(url):
    """Executes a wfm query"""
    request = requests.get(WFM_API + url, stream=True)
    if request.status_code == 200:
        return request.json()["payload"]
    return None


def get_weapon(weapon_name):
    """Returns the weapon data given a name"""
    for wtype in settings.weapon_list:
        for wep, stats in wtype.items():
            if weapon_name == wep:
                return stats
    return None


def get_weapon_type(weapon_name):
    """Returns the weapon type given the name."""

    for index, wtype in enumerate(settings.weapon_list):
        if weapon_name in wtype.keys():
            return index
    return None


def check_variant(weapon_name):
    """Returns the weapon variants given the name."""

    if "_" not in weapon_name:
        return False
    if weapon_name in settings.special_weapon_names:
        return False
    for weapon_variant in settings.weapon_variants:
        if weapon_variant in weapon_name:
            return True
    return False


def scale_range(actual, actual_min, actual_max, wanted_min, wanted_max):
    """Scales a value from within a range to another range"""

    return (wanted_max - wanted_min) * (
        (actual - actual_min) / (actual_max - actual_min)
    ) + wanted_min


def compare_stats(little_list, big_list):
    """Returns if the first list is a subset of the second one."""

    return set(little_list).issubset(big_list)


def difference_lists(stat_list1, stat_list2):
    """Returns the values that are in the first list and aren't in the second"""

    return list(set(stat_list1) - set(stat_list2))


def login(user_email: str, user_password: str, platform: str = "pc", language: str = "en"):
    """Login function, copied from the wfm discord."""

    global JWT_TOKEN, INGAME_NAME, HEADERS
    HEADERS = {
        "content-type": "application/json; utf-8",
        "accept": "application/json",
        "authorization": "jwt",
        "platform": platform,
        "language": language,
    }
    content = {"email": user_email, "password": user_password, "auth_type": "header"}
    response = requests.post(f"{WFM_API}/auth/signin", data=json.dumps(content), HEADERS=HEADERS)
    if response.status_code != 200:
        print("couldn't login with those credentials")
        return None
    print("logged succesfully")
    INGAME_NAME = response.json()["payload"]["user"]["INGAME_NAME"]
    JWT_TOKEN = response.HEADERS["authorization"]
    HEADERS["authorization"] = JWT_TOKEN
    HEADERS["auth_type"] = "header"
    return [HEADERS, INGAME_NAME, JWT_TOKEN]


def get_current_auctions():
    """Returns the current auctions of the user."""
    if INGAME_NAME:
        result = get_request(WFM_API + "/profile/" + INGAME_NAME + "/auctions")
        if result:
            return result["auctions"]
    return None


def wfm_string(item_name, seller_name, price, rank=None):
    """Writes a message that can be copied directly as if the user came from wfm"""
    if rank is not None:
        print(
            "/w "
            + str(seller_name)
            + " hi! i want to buy: "
            + item_name.title().replace("_", " ")
            + " (rank "
            + str(rank)
            + ") for "
            + str(price)
            + " platinum. (warframe.market)\n"
        )
    else:
        print(
            "/w "
            + str(seller_name)
            + " hi! i want to buy: "
            + item_name.title().replace("_", " ")
            + " for "
            + str(price)
            + " platinum. (warframe.market)\n"
        )
