import requests, settings, os
WFM_API = "https://api.warframe.market/v1"
#Method used to get the list of prime parts or sets of wfm.
def retrieveList():
    stringSet = set()
    result=requests.get(WFM_API + "/items",stream=True)
    if result.status_code == 200: 
        itemList = [x["url_name"] for x in result.json()["payload"]["items"]]
        resultFile = open("itemList.csv",'w',encoding='utf-8')
        for x in itemList:
            if "prime" in x and "set" not in x and "primed" not in x: 
                if x + "\n" not in stringSet: resultFile.write(x + "\n")
                stringSet.add(x + "\n")
        resultFile.close()
        
#Method used to get the value in ducats of the items list.
def retrieveDucats():
    itemList = open("itemList.csv",'r',encoding='utf-8')
    ducatList = open("ducatList.csv",'w',encoding='utf-8')
    stringSet = set()     
    lines = itemList.readlines()
    urlList = []
    for line in lines: urlList.append(WFM_API + "/items/" + line.replace("\n", ""))
    for url in urlList:
        result=requests.get(url,stream=True)
        if result.status_code == 200:
            result = result.json()["payload"]["item"]["items_in_set"]
            for setItem in result:
                if setItem["url_name"] not in stringSet:
                    if setItem["ducats"] >= 45: 
                        ducatList.write(setItem["url_name"] +"," + str(setItem["ducats"])+"\n")
                        stringSet.add(setItem["url_name"])
    itemList.close()
    ducatList.close()

#Method used to get the ducats/plat value of the items.
#We create a dict in order to save the data of each item. We also save the seller and the price.
#The scanItems parameter makes it instantly write good deals on the file and print them in console.
#Otherwise it will write the list of all the items with their ducat/plat, seller and price values.
def getOrders(scanItems):
    ducatDict = {}

    ducatList = open("ducatList.csv",'r',encoding='utf-8')
    ducanator = open("ducanated.csv",'a+',encoding='utf-8') if scanItems else open("ducanated.csv",'w',encoding='utf-8')
    for line in ducatList.readlines():
        itemName, ducats = line.replace("\n", "").split(",")
        if itemName not in ducatDict: ducatDict[itemName] = {}
        ducatDict[itemName]["ducats"] = int(ducats)
        result=requests.get(WFM_API + "/items/" + itemName +"/orders",stream=True)
        if result.status_code == 200:
            result = result.json()["payload"]["orders"]
            for order in result:
                if order["user"]["status"] == "ingame" and order["order_type"] == "sell":
                    if "sell" not in ducatDict[itemName]: ducatDict[itemName]["sell"] = []
                    ducatDict[itemName]["sell"].append([order["platinum"], order["user"]["ingame_name"]])
            if len(ducatDict[itemName]["sell"]) >= 1:
                ducatDict[itemName]["prices"] = sorted(ducatDict[itemName]["sell"] ,key=lambda x: x[0])[0]
            else: 
                ducatDict[itemName]["value"] = 0
                continue
            ducatDict[itemName]["value"] = ducatDict[itemName]["ducats"] / ducatDict[itemName]["prices"][0]
            if scanItems and ducatDict[itemName]["value"] > 30: 
                line = itemName.capitalize().replace("_", " ") + " Ducats/Plat: " + str(ducatDict[itemName]["value"]) + " Price: " + str(ducatDict[itemName]["prices"][0]) + " Seller: " + ducatDict[itemName]["prices"][1] + "\n"
                print(line)
                ducanator.write(line)
    if not scanItems:
        listxd = [[x, ducatDict[x]["value"], ducatDict[x]["prices"][0], ducatDict[x]["prices"][1]] for x in ducatDict]
        listxd = sorted(listxd, key=lambda x: x[1], reverse=True)
            
        for item in listxd: ducanator.write(item[0].capitalize().replace("_", " ") + " Ducats/Plat: " +  
        str(item[1]) + " Price: " + str(item[2]) + " Seller: " + item[3] + "\n")
    ducanator.close()
    ducatList.close()
def updateDucats():
    os.chdir(settings.path + "\\config")
    retrieveList()
    retrieveDucats()
def scanDucats():
    while(True):
        getOrders(True)
def useDucanator():
    os.chdir(settings.path + "\\config")
    if settings.scanDucats: 
        while(True):
            getOrders(True)
    else: getOrders(False)



