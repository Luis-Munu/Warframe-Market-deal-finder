import settings
from utils import getWeaponType, checkVariant

#Can be merged into one module, just didn't thought about it too much.
#Creates the url of a search with given stats. Still doesn't consider negatives which may be a problem in the future. Must fix.
def createGenericUrl(stats=[], weaponType = []):
    if "stat3" in stats: return [settings.WFM_API + "/auctions/search?type=riven&positive_stats=" + stats["stat1"] + "," + stats["stat2"] + "," + stats["stat3"] + "&negative_stats=has&polarity=any&sort_by=price_asc"]
    return addPositive(settings.WFM_API + "/auctions/search?type=riven&positive_stats=" + stats["stat1"] + "," + stats["stat2"], weaponType)

#Used for specific rolls. 
def createSpecificUrl(weapon, stats = [], unroll = False):
    if unroll: return [settings.WFM_API + "/auctions/search?type=riven&weapon_url_name=" + weapon + "&polarity=any&re_rolls_max=0&sort_by=price_asc"]
    if stats:
        if "stat3" in stats: 
            if "negative" in stats: return [settings.WFM_API + "/auctions/search?type=riven&weapon_url_name=" + weapon + "&positive_stats=" + stats["stat1"] + "," + stats["stat2"] + "," + stats["stat3"] +"&negative_stats=" + stats["negative"] + "&polarity=any&sort_by=price_asc"]
            return [settings.WFM_API + "/auctions/search?type=riven&weapon_url_name=" + weapon + "&positive_stats=" + stats["stat1"] + "," + stats["stat2"] + "," + stats["stat3"] + "&negative_stats=has&polarity=any&sort_by=price_asc"]
        else:        
            neg = "&negative_stats=" + stats["negative"] if "negative" in stats else "&negative_stats=has"
            res = []
            for url in addPositive(settings.WFM_API + "/auctions/search?type=riven&weapon_url_name=" + weapon + "&positive_stats=" + stats["stat1"] + "," + stats["stat2"], getWeaponType(weapon)):
                res.append(url + neg  + "&polarity=any&sort_by=price_asc")
            return res
    else:
        return addStats(weapon)

def addStats(weapon):
    weaponType = getWeaponType(weapon)
    res = set()
    for combination in settings.decentPositives[weaponType]:
        for negative in settings.wishedNegatives[weaponType]:
            url = settings.WFM_API + "/auctions/search?type=riven&weapon_url_name=" + weapon + "&positive_stats=" 
            for comb in combination: url += comb + "&"
            url += "negative_stats=" + negative + "&polarity=any&sort_by=price_asc"
            res.add(url)
    return res
#Adds specific 2 stat rivens to the url and also adds urls with a third positive and a negative.
def addPositive(url, weaponType):    
    resultado = [url + "," + pos + "&negative_stats=has&polarity=any&sort_by=price_asc" for wType in weaponType for pos in settings.decentPositives[wType] ]
    #good enough stats to have that aren't detrimental to your riven.
    resultado = list(set(resultado))
    resultado.append(url)
    return resultado


def immovableUrls():
    result = set()
    for weapon in list(settings.weaponList.keys()):
        if checkVariant(weapon): continue
        for weaponType in getWeaponType(weapon):
            for weaponComb in settings.combinations[weaponType]:
                for url in createSpecificUrl(weapon, weaponComb, False): result.add(url)
    return list(result)


def genericUrls():
    result = set()
    for i in range(len(settings.combinations)):
        for weaponComb in settings.combinations[i]:
            for url in createGenericUrl(weaponComb, [i]): 
                result.add(url)
    return list(result)

def wishedUrls():
    result = set()
    for i in range(len(settings.wishedWeapons)):
        for weapon in settings.wishedWeapons[i]:
            if checkVariant(weapon): continue
            for weaponComb in settings.combinations[i]:
                for url in createSpecificUrl(weapon, weaponComb, False): result.add(url)
    return list(result)
def unrolledUrls():
    result = set()
    unroll = list(settings.weaponList.keys()) if settings.nonExistantSearch or settings.slowSearch or settings.mediumSearch else settings.wishedUnrolleds
    for weapon in unroll:
        for url in createSpecificUrl(weapon, [], True): result.add(url)
    return list(result)

def specificUrls():
    result = set()
    for riv in list(settings.wishedRivens.keys()):
        for url in createSpecificUrl(riv, settings.wishedRivens[riv], False): result.add(url)
    return list(result)

def weaponUrls(weapon, stats = []):
    result = set()
    if len(stats)==0: 
        for url in addStats(weapon):result.add(url)
    else: 
        for url in createSpecificUrl(weapon, stats, False): result.add(url)
    return list(result)


#Prepares the weapon list
def dataCreation():
    urlList = []
    if settings.nonExistantSearch:
        #Should never be used unless you have all the time in the world.
        urlList.extend(immovableUrls())
    #Creates the url of generic rolls.
    if settings.fastSearch or settings.mediumSearch or settings.slowSearch:
        urlList.extend(genericUrls())
    #Creates the url of generic rolls for wished weapons.
    if settings.slowSearch or settings.mediumSearch:
        urlList.extend(wishedUrls())
    #Creates the url of unrolleds
    if settings.slowSearch:
        urlList.extend(unrolledUrls())
    #Creates the url of specific rolls
    if settings.specificSearch or settings.fastSearch or settings.mediumSearch or settings.slowSearch or settings.nonExistantSearch:
        urlList.extend(specificUrls())
    #Creates the url of a specific weapon search
    if settings.specificWeapon:
        urlList.extend(weaponUrls(settings.weaponName, settings.weaponStats))
        
    urlList = list(set(urlList))
    print(str(len(urlList)) + " possible riven combinations")

    return urlList