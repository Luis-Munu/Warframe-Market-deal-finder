import settings
#Returns the weapon type given the name.
def getWeaponType(weapon):
    return settings.weaponList[weapon]["weapontype"]