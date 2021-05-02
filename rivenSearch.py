import settings, urlCreation, rivenRequests, processData, userCommands


#This Speed won't work until warframe.market uncap the auction responses.

#Things to do: 
#Add weight to the stats. Useful for many weapons but maybe terrible for others.
#Calculate weapon grades on different ranks. 
#Convert dirty modules into something readable.
#Add weapon stats to weight the stats better.
#Automatically upload results to website.
#GUI. 



def createEverything():

    res = urlCreation.dataCreation()        #Gets the urls for the searches we have to do.
    res = rivenRequests.massRivenRequest(res)  #Requests said searches to the server and returns them.
    res = processData.processData(res)      #Processes the requests and converts them into Riven objects.

    res = sorted(res, key=lambda riven: (riven.BuyoutPrice, riven.InitialPrice))    #Sorts them by price.
    processData.exportTxt(res)              #Exports them into txt files.

    print("Rivens searched: " + str(len(res)))

settings.init()
userCommands.greatSearch()
createEverything()
