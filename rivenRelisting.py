import json
from ratelimit import limits, sleep_and_retry
import requests


"""
File used to relist auctions based on the user's preference.
It logins with the user credentials, then retrieves all their auctions.
Depending on the user's choice, it will relist all, or only the auctions that doesn't have bids.
"""

#Practical information.
WFM_API = "https://api.warframe.market/v1"
jwt_token = None
headers = {}
ingame_name = None
relistWithoutBids = False
#Attributes that will get deleted from the auctions in order to relist them.
deleteattr = ["visible","owner","created","updated","winner","closed","note_raw","top_bid","platform","id","is_direct_sell","is_marked_for","marked_operation_at"]

#Login function, copied from the wfm discord.
def login(user_email: str, user_password: str, platform: str = "pc", language: str = "en"):
    global jwt_token, ingame_name, headers
    headers = {
        "Content-Type": "application/json; utf-8",
        "Accept": "application/json",
        "Authorization": "JWT",
        "platform": platform,
        "language": language,
    }
    content = {"email": user_email, "password": user_password, "auth_type": "header"}
    response = requests.post(f"{WFM_API}/auth/signin", data=json.dumps(content), headers=headers)
    if response.status_code != 200:
        print("Couldn't login with those credentials")
        return
    print("Logged succesfully")
    ingame_name = response.json()["payload"]["user"]["ingame_name"]
    jwt_token = response.headers["Authorization"]
    headers["authorization"]= jwt_token
    headers["auth_type"] = "header"

#Returns the current auctions of the user.
def getCurrentAuctions():
    if ingame_name:
        result=requests.get(WFM_API +"/profile/" + ingame_name + "/auctions",stream=True)
        if result.status_code == 200: return result.json()["payload"]["auctions"]
    else: return None

#Deletes then list again the selected auctions.
@sleep_and_retry
@limits(calls=3, period=1.5)
def relistAuctions():
    for auction in getCurrentAuctions():
        if relistWithoutBids and not auction["top_bid"] or not relistWithoutBids:
            id = auction["id"]
            for attr in deleteattr: auction.pop(attr, None)
            result=requests.put(WFM_API +"/auctions/entry/" + id + "/close" ,stream=True, headers=headers)
            if result.status_code == 200: 
                print(auction["item"]["weapon_url_name"].capitalize().replace("_", " ") + " " +  auction["item"]["name"].capitalize().replace("_", " ") + " cancelada con exito")
            else: print(auction["item"]["weapon_url_name"].capitalize().replace("_", " ") + " " +  auction["item"]["name"].capitalize().replace("_", " ") + "no cancelada")
            result=requests.post(WFM_API +"/auctions/create" , data = json.dumps(auction), stream=True, headers=headers)
            if result.status_code == 200: 
                print(auction["item"]["weapon_url_name"].capitalize().replace("_", " ") + " " + auction["item"]["name"].capitalize().replace("_", " ") + " posteada con exito")
            else: print(auction["item"]["weapon_url_name"].capitalize().replace("_", " ") + " " +  auction["item"]["name"].capitalize().replace("_", " ") + "no posteada")

