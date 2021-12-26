import json, utils, requests
from ratelimit import limits, sleep_and_retry


"""
File used to relist auctions based on the user's preference.
It logins with the user credentials, then retrieves all their auctions.
Depending on the user's choice, it will relist all, or only the auctions that doesn't have bids.
"""

#Practical information.
WFM_API = "https://api.warframe.market/v1"

relistWithoutBids = False
#Attributes that will get deleted from the auctions in order to relist them.
deleteattr = ["visible","owner","created","updated","winner","closed","note_raw","top_bid","platform","id","is_direct_sell","is_marked_for","marked_operation_at"]


#Deletes then list again the selected auctions.
@sleep_and_retry
@limits(calls=3, period=1.5)
def relistAuctions():
    for auction in utils.getCurrentAuctions():
        if relistWithoutBids and not auction["top_bid"] or not relistWithoutBids:
            id = auction["id"]
            for attr in deleteattr: auction.pop(attr, None)
            #Deletes the auctions.
            result=requests.put(WFM_API +"/auctions/entry/" + id + "/close" ,stream=True, headers=utils.headers)
            if result.status_code == 200: 
                print(auction["item"]["weapon_url_name"].capitalize().replace("_", " ") + " " +  auction["item"]["name"].capitalize().replace("_", " ") + " cancelada con exito")
            else: print(auction["item"]["weapon_url_name"].capitalize().replace("_", " ") + " " +  auction["item"]["name"].capitalize().replace("_", " ") + " no cancelada")
            #Relists them.
            result=requests.post(WFM_API +"/auctions/create" , data = json.dumps(auction), stream=True, headers=utils.headers)
            if result.status_code == 200: 
                print(auction["item"]["weapon_url_name"].capitalize().replace("_", " ") + " " + auction["item"]["name"].capitalize().replace("_", " ") + " posteada con exito")
            else: print(auction["item"]["weapon_url_name"].capitalize().replace("_", " ") + " " +  auction["item"]["name"].capitalize().replace("_", " ") + " no posteada")

