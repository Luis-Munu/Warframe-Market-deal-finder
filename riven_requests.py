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


def scan_riven(riven_list):
    """Mode used to scan for specific rolls every 5 minutes.
    it will print a message and save rivens the user want and have a lower or equal
    price than the user's max price for that roll."""

    iteration_counter = 1
    while True:
        timer = time.time()
        print("starting the search number " + str(iteration_counter))
        iteration_counter += 1
        res = mass_riven_request(riven_list)
        res = process_data.process_data(res).values()
        res = sorted(res, key=lambda riven: (riven.buyout_price, riven.initial_price))
        process_data.export_txt(res)
        duration = 1000  # milliseconds
        freq = 440  # hz
        winsound.beep(freq, duration)
        time.sleep(300.0 - ((time.time() - timer) % 60.0))


def mass_riven_request(riven_list):
    """Method used to call for requests for every url, then return the list of results"""

    results = []
    for riven in riven_list:
        received_list = riven_request(riven)
        if received_list:
            results.extend(received_list)
    return results
