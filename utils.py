import settings
#Returns the weapon type given the name.
def getWeaponType(weapon):
    return settings.weaponList[weapon]["weapontype"]
def checkVariant(weaponName):
    if weaponName == "euphona_prime" or weaponName == "dakra_prime" or weaponName == "kuva_ayanga" or weaponName == "reaper_prime": return False
    for weaponVariant in settings.weaponVariants:
        if weaponVariant in weaponName: return True
    return False