import settings, requests, json

jwt_token = None
headers = {}
ingame_name = None
WFM_API = "https://api.warframe.market/v1"

#Returns the weapon type given the name.
def getWeaponType(weapon):
    return settings.weaponList[weapon]["weapontype"]
def checkVariant(weaponName):
    if weaponName in settings.specialWeaponNames: return False
    for weaponVariant in settings.weaponVariants:
        if weaponVariant in weaponName: return True
    return False
    
#Returns if the list 1 is a subset of the list 2.
def compareStats(littleList, bigList):
    return set(littleList).issubset(bigList)

def differenceLists(statList1, statList2):
    return list(set(statList1)-set(statList2))

#Login function, copied from the wfm discord.
def login(user_email: str, user_password: str, platform: str = "pc", language: str = "en"):
    global jwt_token, ingame_name, headers
    headers = {
        "Content-Type": "application/json; utf-8",
        "Accept": "application/json",
        "Authorization": "JWT",
        "platform": platform,
        "language": language,
    }
    content = {"email": user_email, "password": user_password, "auth_type": "header"}
    response = requests.post(f"{WFM_API}/auth/signin", data=json.dumps(content), headers=headers)
    if response.status_code != 200:
        print("Couldn't login with those credentials")
        return
    print("Logged succesfully")
    ingame_name = response.json()["payload"]["user"]["ingame_name"]
    jwt_token = response.headers["Authorization"]
    headers["authorization"]= jwt_token
    headers["auth_type"] = "header"
    return [headers, ingame_name, jwt_token]

#Returns the current auctions of the user.
def getCurrentAuctions():
    if ingame_name:
        result=requests.get(WFM_API +"/profile/" + ingame_name + "/auctions",stream=True)
        if result.status_code == 200: return result.json()["payload"]["auctions"]
    else: return None