import riven
#Process the auction data from warframe.market and converts it into a list of Riven class objects.
#May add some filtering in the future.
def processData(response):
    rivenList = set()
    for auction in response:

        if auction["closed"] == True: continue
        #Gets the stats of the riven.
        stats = [list() for x in range(4)]
        for i, stat in enumerate(auction["item"]["attributes"]):
            stats[i].extend([stat["positive"], stat["url_name"], stat["value"]])
        #Removes empty positions of stats.
        stats = list(filter(None, stats))
        #Sorts the stats list to put the negative stat at the end.
        stats.sort(key=lambda x: x[0] if len(x)>0 else False, reverse=True)

        #Adds the riven into the rivenList.
        rivenList.add(riven.Riven(auction["item"]["weapon_url_name"], auction["item"]["name"], 
        auction["starting_price"], auction["buyout_price"], auction["owner"]["ingame_name"], auction["item"]["polarity"], 
        auction["item"]["re_rolls"], auction["item"]["mastery_level"], auction["item"]["mod_rank"], stats))
    return rivenList

def exportTxt(results):
    for riv in results: riv.printData()