import riven, settings, utils
#Process the auction data from warframe.market and converts it into a list of Riven class objects.
#May add some filtering in the future, in order to increase speed but with an information loss.
#If the user chose to use the scan mode it will actively check if the auctions are specific rolls and their
#price is below the user's price. If all that happens then the riven is created.
def processData(response):
    rivenList = set()
    for auction in response:
        if auction["closed"] == True: continue
        scanFlag = True
        #Converts the dict of riven stats to list in order to get the negative in the last spot.
        #If there's any way to fast check if there's a negative in the stats while using a dict
        #then this would be innecessary.
        stats = [list() for x in range(4)]
        for i, stat in enumerate(auction["item"]["attributes"]):
            stats[i].extend([stat["positive"], stat["url_name"], stat["value"]])
        #Removes empty positions of stats.
        stats = list(filter(None, stats))
        #Sorts the stats list to put the negative stat at the end.
        stats.sort(key=lambda x: x[0] if len(x)>0 else False, reverse=True)
        if settings.scanRiven == True:
            scanFlag = False
            if auction["buyout_price"] and auction["item"]["weapon_url_name"] in settings.wishedRivens:
                statList = [stat[1] for stat in stats]
                for wishedRoll in settings.wishedRivens[auction["item"]["weapon_url_name"]]:
                    listDiff = utils.differenceLists(statList, list(wishedRoll["stats"].values()))
                    if len(listDiff) == 1 and stats[-1][0] == False:
                        if auction["buyout_price"] <= wishedRoll["price"]: 
                            scanFlag = True
                            print("Found a wished roll! " + auction["item"]["weapon_url_name"].capitalize().replace("_", " ") + " " + 
                            auction["item"]["name"].capitalize().replace("_", " ") + " Price: " + str(auction["buyout_price"]))

        if scanFlag == False: continue
        #Adds the riven into the rivenList.
        rivenList.add(riven.Riven(auction["item"]["weapon_url_name"], auction["item"]["name"], 
        auction["starting_price"], auction["buyout_price"], auction["owner"]["ingame_name"], auction["item"]["polarity"], 
        auction["item"]["re_rolls"], auction["item"]["mastery_level"], auction["item"]["mod_rank"], stats))
    return rivenList

def exportTxt(results):
    contentDict = {}
    for riv in results:
        riv.rivToText()
        for path in riv.Paths:
            if path in contentDict: contentDict[path] += riv.Message  
            else: contentDict[path] = riv.Message
    for path, message in contentDict.items():
        ducatList = open(path,'w',encoding='utf-8')
        ducatList.write(message[4:])
            
