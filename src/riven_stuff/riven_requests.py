"""
    Modules used to do requests to the server.
    they are feeded with a list of urls created in url_creation.
    the api call rate used right now is a call each 0.5s.
    increasing it may causes the server to ban you.
"""

import src.settings as settings
import src.utils as utils


def wfm_riven_request(url):
    """Retrieves the list of auctions from the url if the request works"""
    result = utils.get_wfm_request(url)
    if result:
        return result["auctions"]


def rh_riven_request(url):
    """Retrieves the list of auctions from the url if the request works"""
    result = utils.get_rh_request(url)
    if result:
        return result


def mass_riven_request(riven_list):
    """Method used to call for requests for every url, then return the list of results"""
    if settings.search_type:
        results = [[], []]
        for riven in riven_list[0]:
            results[0].extend(wfm_riven_request(riven))
        for riven in riven_list[1]:
            results[1].extend(rh_riven_request(riven))
        return results
    else:
        results = []
        for riven in riven_list:
            rs = wfm_riven_request(riven)
            if rs:
                results.extend(rs)
        return results
