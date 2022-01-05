"""
File used to relist auctions based on the user's preference.
it logins with the user credentials, then retrieves all their auctions.
depending on the user's choice, it will relist all, or only the auctions that doesn't have bids.
"""
import json
from ratelimit import limits, sleep_and_retry
import requests
import utils


# practical information.
WFM_API = "https://api.warframe.market/v1"

# attributes that will get deleted from the auctions in order to relist them.
deleteattr = [
    "visible",
    "owner",
    "created",
    "updated",
    "winner",
    "closed",
    "note_raw",
    "top_bid",
    "platform",
    "id",
    "is_direct_sell",
    "is_marked_for",
    "marked_operation_at",
]


# deletes then list again the selected auctions.
@sleep_and_retry
@limits(calls=3, period=1.5)
def relist_auctions(relist_without_bids):
    """File used to relist auctions based on the user's preference.
    it logins with the user credentials, then retrieves all their auctions.
    depending on the user's choice, it will relist all, or only the auctions
    that doesn't have bids.
    """

    for auction in utils.get_current_auctions():
        if relist_without_bids and not auction["top_bid"] or not relist_without_bids:
            auction_id = auction["id"]
            for attr in deleteattr:
                auction.pop(attr, None)
            # deletes the auctions.
            result = requests.put(
                WFM_API + "/auctions/entry/" + auction_id + "/close",
                stream=True,
                headers=utils.headers,
            )
            if result.status_code == 200:
                print(
                    auction["item"]["weapon_url_name"].capitalize().replace("_", " ")
                    + " "
                    + auction["item"]["name"].capitalize().replace("_", " ")
                    + " succesfully cancelled"
                )
            else:
                print(
                    auction["item"]["weapon_url_name"].capitalize().replace("_", " ")
                    + " "
                    + auction["item"]["name"].capitalize().replace("_", " ")
                    + " not cancelled"
                )
            # relists them.
            result = requests.post(
                WFM_API + "/auctions/create",
                data=json.dumps(auction),
                stream=True,
                headers=utils.headers,
            )
            if result.status_code == 200:
                print(
                    auction["item"]["weapon_url_name"].capitalize().replace("_", " ")
                    + " "
                    + auction["item"]["name"].capitalize().replace("_", " ")
                    + " succesfully posted"
                )
            else:
                print(
                    auction["item"]["weapon_url_name"].capitalize().replace("_", " ")
                    + " "
                    + auction["item"]["name"].capitalize().replace("_", " ")
                    + " not posted"
                )
