"""
    Modules used to do requests to the server.
    they are feeded with a list of urls created in url_creation.
    the api call rate used right now is a call each 0.5s. 
    increasing it may causes the server to ban you.
"""

import time
import process_data
import winsound
import utils


def riven_request(url):
    """Retrieves the list of auctions from the url if the request works"""

    result = utils.get_request(url)
    if result:
        return result["auctions"]


def mass_riven_request(riven_list):
    """Method used to call for requests for every url, then return the list of results"""

    results = []
    for riven in riven_list:
        received_list = riven_request(riven)
        if received_list:
            results.extend(received_list)
    return results
