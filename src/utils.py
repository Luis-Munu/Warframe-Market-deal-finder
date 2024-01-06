"""Common methods used by all modules"""

import json
import re

import random

import requests
from ratelimit import limits, sleep_and_retry

import src.settings as settings

jwt_token = None

headerss = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Accept": "application/json",
    "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://warframe.market/",
    "content-type": "application/json",
    "language": "en",
    "platform": "pc",
    "Origin": "https://warframe.market",
    "DNT": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "TE": "trailers",
}

cookies = {
    "language": "en",
    "sessionid": "yoursessionid",
    "csrftoken": "yourtoken",
}
headers = {
    "x-csrftoken": "yourtoken",
    "Connection": "keep-alive",
}
params = {
    "interval": "7 day",
}

ingame_name = None
WFM_API = "https://api.warframe.market/v1/"
RH_API = "https://rivenhunter.com/api/v1/rivensearch/?itemtype="
session = requests.Session()


@sleep_and_retry
# @limits(calls=3, period=1.2)
def get_wfm_request(url):
    """Executes a wfm query"""
    request = session.get(WFM_API + url, stream=True, headers=headerss)
    if request.status_code == 200:
        return request.json()["payload"]
    return None


@sleep_and_retry
def get_rh_request(url):
    """Executes a rh query"""
    request = session.get(
        RH_API + url, params=params, cookies=cookies, headers=headers
    ).json()
    if len(request) != 0 and len(request["data"]) != 0:
        return request["data"]
    return None


def get_weapon(weapon_name):
    """Returns the weapon data given a name"""
    weapon_name = weapon_name.replace("_", " ").title()
    weapon = [x for x in settings.weapons if x["name"] == weapon_name]
    if len(weapon) == 0:
        return None
    return weapon[0]


def get_weapon_type(weapon_name):
    """Returns the weapon type given the name."""
    weapon = get_weapon(weapon_name)
    if weapon is None:
        return 3
    return weapon["weapon_type"]


def check_variant(weapon_name):
    """Returns if the weapon is a variant given the name."""
    weapon_name = weapon_name.replace("_", " ").title()
    family = [w for w in settings.weapons if w["name"] == weapon_name][0]["family"]
    if family == weapon_name:
        return False
    return True


def scale_range(actual, actual_min, actual_max, wanted_min, wanted_max):
    """Scales a value from within a range to another range"""

    return (wanted_max - wanted_min) * (
        (actual - actual_min) / (actual_max - actual_min)
    ) + wanted_min


def compare_stats(little_list, big_list):
    """Returns if the first list is a subset of the second one."""

    return set(little_list).issubset(big_list)


def login(
    user_email: str, user_password: str, platform: str = "pc", language: str = "en"
):
    """Login function, copied from the wfm discord."""

    global jwt_token, ingame_name, headers
    headers = {
        "content-type": "application/json; utf-8",
        "accept": "application/json",
        "authorization": "jwt",
        "platform": platform,
        "language": language,
    }
    content = {"email": user_email, "password": user_password, "auth_type": "header"}
    response = requests.post(
        f"{WFM_API}/auth/signin", data=json.dumps(content), headers=headers
    )
    if response.status_code != 200:
        print("couldn't login with those credentials")
        return None
    print("logged succesfully")
    ingame_name = response.json()["payload"]["user"]["ingame_name"]
    jwt_token = response.headers["authorization"]
    headers["authorization"] = jwt_token
    headers["auth_type"] = "header"
    return [headers, ingame_name, jwt_token]


def get_current_auctions():
    """Returns the current auctions of the user."""
    if ingame_name:
        url = "profile/" + ingame_name + "/auctions"
        result = get_wfm_request(url)
        if result:
            return result["auctions"]
    return None


@sleep_and_retry
@limits(calls=3, period=1.2)
def upvote_wfm_user(user_name):
    # We'll do a positive review of the user, the URL is like this https://api.warframe.market/v1/profile/{user_name}/review
    # But we have to add the fields review_type = 1 and text = "Good seller"
    url = "profile/" + user_name + "/review"
    texts = [
        "Nice trader!",
        "Fast trader",
        "Good prices",
        "Generous trader",
        "Good trader",
        "Nice trader",
        "+1",
    ]
    data = {"review_type": 1, "text": random.choice(texts)}
    result = requests.post(WFM_API + url, data=json.dumps(data), headers=headers)
    if result.status_code == 200:
        print("upvoted " + user_name)
        return True
    return False


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


def translate_stat_rh_wfm(stat):
    return [x["wfm_name"] for x in settings.stat_list if stat in x["rh_names"]][0]


def translate_stat_wfm_rh(stat, type):
    return [x["rh_names"][type] for x in settings.stat_list if stat == x["wfm_name"]][0]


def translate_stats_wiki_wfm(stat):
    res = [stat2 for stat2 in settings.stat_list if stat2["wiki_name"] == stat]
    if len(res) != 0:
        return str(res[0]["wfm_name"])
    return str(re.sub("([a-z0-9])([A-Z])", r"\1_\2", stat).lower())
