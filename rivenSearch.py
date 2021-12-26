import settings, urlCreation, rivenRequests, processData, userCommands, rivenRelisting, ducanator


#Speed could be vastly improved if warframe.market responses didn't have a size cap or I filtered the search.
#However I prefer information over speed, it's better to spend 30 minutes waiting than to lose thousands of plats.

#Things to do: 
#Add weight to the stats. Useful for many weapons but maybe terrible for others.
#Add weapon stats to weight the stats better.
#Calculate weapon grades on different ranks, as of now it just calculates rank 8.
#Automatically upload results to a website.
#Convert dirty modules into something readable.



def createEverything():

    res = urlCreation.dataCreation()                        #Gets the urls for the searches we have to do.
    if settings.scanRiven:
        rivenRequests.scanRiven(res)
    else:
        res = rivenRequests.massRivenRequest(res)               #Requests said searches to the server and returns them.
        res = processData.processData(res)                      #Processes the requests and converts them into Riven objects.

        res = sorted(res, key=lambda riven: (riven.BuyoutPrice, riven.InitialPrice))    #Sorts them by price.
        processData.exportTxt(res)              #Exports them into txt files.

        print("Rivens searched: " + str(len(res)))

settings.init()
if userCommands.chooseMode()==1: createEverything()
#settings.fastSearch = True


