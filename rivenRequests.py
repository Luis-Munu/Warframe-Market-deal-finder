from ratelimit import limits, sleep_and_retry
import time, requests, processData
#Modules needed to do the requests to the server.
#They are provided a list of urls created in urlCreation.
#The api call rate used right now is a call each 0.5s. Increasing it may causes the server to ban you.

@sleep_and_retry
@limits(calls=3, period=1.5)
def rivenRequest(url):
    result=requests.get(url,stream=True)
    if result.status_code == 200: return result.json()["payload"]["auctions"]

#Mode used to scan for specific rolls every 5 minutes. It will print a message and save rivens the user want
#and have a lower or equal price than the user's max price for that roll.
def scanMode(rivenList):
    iterationCounter = 1
    while True:
        timer = time.time()
        print("Starting the search number " + str(iterationCounter))
        iterationCounter+=1
        res = massRivenRequest(rivenList)
        res = processData.processData(res)                      
        res = sorted(res, key=lambda riven: (riven.BuyoutPrice, riven.InitialPrice)) 
        processData.exportTxt(res)
        time.sleep(300.0 - ((time.time() - timer) % 60.0))

def massRivenRequest(rivenList):
    results = []
    for riven in rivenList:
        receivedList=rivenRequest(riven)
        if receivedList: results.extend(receivedList)
    return results