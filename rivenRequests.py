from ratelimit import limits, sleep_and_retry
import  requests
#Modules needed to do the requests to the server.
#They are provided a list of urls created in urlCreation.
#The api call rate used right now is a call each 0.5s. Increasing it may causes the server to ban you.

@sleep_and_retry
@limits(calls=3, period=1.5)
def rivenRequest(url):
    result=requests.get(url,stream=True)
    if result.status_code == 200: return result.json()["payload"]["auctions"]


def massRivenRequest(rivenList):
    results = []
    for riven in rivenList:
        receivedList=rivenRequest(riven)
        if receivedList: results.extend(receivedList)
    return results