import settings
from utils import getWeaponType 

#Can be merged into one module, just didn't thought about it too much.
#Creates the url of a search with given stats. Still doesn't consider negatives which may be a problem in the future. Must fix.
def createUrl(stats=[], weaponType = []):
    if "stat3" in stats: return [settings.WFM_API + "/auctions/search?type=riven&positive_stats=" + stats["stat1"] + "," + stats["stat2"] + "," + stats["stat3"] + "&negative_stats=has&polarity=any&sort_by=price_asc"]
    return addPositive(settings.WFM_API + "/auctions/search?type=riven&positive_stats=" + stats["stat1"] + "," + stats["stat2"], weaponType)

#Used for specific rolls. 
def createSpecificUrl(weapon, stats = [], unroll = False):
    if unroll: return [settings.WFM_API + "/auctions/search?type=riven&weapon_url_name=" + weapon + "&polarity=any&re_rolls_max=0&sort_by=price_asc"]
    if "stat3" in stats: 
        if "negative" in stats: return [settings.WFM_API + "/auctions/search?type=riven&weapon_url_name=" + weapon + "&positive_stats=" + stats["stat1"] + "," + stats["stat2"] + "," + stats["stat3"] +"&negative_stats=" + stats["negative"] + "&polarity=any&sort_by=price_asc"]
        return [settings.WFM_API + "/auctions/search?type=riven&weapon_url_name=" + weapon + "&positive_stats=" + stats["stat1"] + "," + stats["stat2"] + "," + stats["stat3"] + "&negative_stats=has&polarity=any&sort_by=price_asc"]
    else:        
        neg = "&negative_stats=" + stats["negative"] if "negative" in stats else "&negative_stats=has"
        res = []
        for url in addPositive(settings.WFM_API + "/auctions/search?type=riven&weapon_url_name=" + weapon + "&positive_stats=" + stats["stat1"] + "," + stats["stat2"], getWeaponType(weapon)):
            res.append(url + neg  + "&polarity=any&sort_by=price_asc")
        return res

#Adds specific 2 stat rivens to the url and also adds urls with a third positive and a negative.
def addPositive(url, weaponType):    
    resultado = []
    resultado = [url + "," + pos + "&negative_stats=has&polarity=any&sort_by=price_asc" for wType in weaponType for pos in settings.decentPositives[wType] ]
    #good enough stats to have that aren't detrimental to your riven.
    resultado = list(set(resultado))
    resultado.append(url)
    return resultado



#Prepares the weapon list
def dataCreation():
    urlList = []
    if settings.search:
        if settings.nonExistantSearch:
            #Should never be used unless you have all the time in the world.
            for weaponCombs in settings.combinations:
                for weapon in list(settings.weaponList.keys()):
                    for comb in weaponCombs:
                        for url in createSpecificUrl(weapon, comb, False):
                            if not any(url  == auxUrl for auxUrl in urlList): urlList.append(url)

        #Creates the url of generic rolls.
        for i, weaponCombs in enumerate(settings.combinations):
            for comb in weaponCombs:
                for url in createUrl(comb, [i]): 
                    if not any(url  == auxUrl for auxUrl in urlList): urlList.append(url)
        #Creates the url of generic rolls for wished weapons.
        if settings.nonExistantSearch or settings.slowSearch:
            for weaponCombs in settings.combinations:
                for weapon in settings.wishedWeapons[i]:
                    for comb in weaponCombs:
                        for url in createSpecificUrl(weapon,comb, False): 
                            if not any(url  == auxUrl for auxUrl in urlList): urlList.append(url)
        #Creates the url of unrolleds
        unroll = list(settings.weaponList.keys()) if settings.nonExistantSearch or settings.slowSearch or settings.mediumSearch else settings.wishedUnrolleds
        for weapon in unroll:
            for url in createSpecificUrl(weapon, [], True): 
                    if not any(url  == auxUrl for auxUrl in urlList): urlList.append(url)
        #Creates the url of specific rolls
        for riv in list(settings.wishedRivens.keys()):
            for url in createSpecificUrl(riv, settings.wishedRivens[riv], False):
                if not any(url  == auxUrl for auxUrl in urlList): urlList.append(url)
        print(str(len(urlList)) + " possible riven combinations")

    else:
        for url in addPositive(settings.WFM_API + "/auctions/search?type=riven&weapon_url_name=" + "glaive" + "&positive_stats=" + "fire_rate_/_attack_speed" + "," + "range", getWeaponType("glaive")):
            urlList.append(url)
    return urlList