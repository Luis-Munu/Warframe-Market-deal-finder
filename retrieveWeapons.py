import requests, os
weaponCategories = ["Primary", "Secondary", "Melee", "Arch-Gun", "Arch-Melee"]
path = os.getcwd() + "\\config"
weapons = {}
for category in weaponCategories:
    weaponRequest = requests.get('https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json/' + category + '.json')
    weaponRequest = weaponRequest.json()
    for weapon in weaponRequest:
        if not weapon["category"] in weapons: weapons[weapon["category"]] = {}
        weapons[weapon["category"]][weapon["name"]] = {}
        weapons[weapon["category"]][weapon["name"]]["disposition"] = weapon["omegaAttenuation"]
        weapons[weapon["category"]][weapon["name"]]["critical_chance"] = weapon["criticalChance"]
        weapons[weapon["category"]][weapon["name"]]["critical_damage"] = weapon["criticalMultiplier"]
        weapons[weapon["category"]][weapon["name"]]["status_chance"] = weapon["procChance"]
        weapons[weapon["category"]][weapon["name"]]["type"] = weapon["type"]
            
        if "damageTypes"in weapon: 
            weapons[weapon["category"]][weapon["name"]]["damageTypes"] = weapon["damageTypes"]
            for key, val in weapons[weapon["category"]][weapon["name"]]["damageTypes"].items():
                if "damage" not in key: weapons[weapon["category"]][weapon["name"]]["damageTypes"][key + "_damage"] = weapons[weapon["category"]][weapon["name"]]["damageTypes"].pop(key)
            if "slash_damage" in weapons[weapon["category"]][weapon["name"]]["damageTypes"]:
                weapons[weapon["category"]][weapon["name"]]["slashPercent"] = weapons[weapon["category"]][weapon["name"]]["damageTypes"]["slash_damage"] / weapon["totalDamage"]
            else: weapons[weapon["category"]][weapon["name"]]["slashPercent"] = 0

with open("weaponList.csv", 'w') as f:
    f.write("Name, Disposition, Critical chance, Critical Damage, Status Chance, Type, Damage Types, Slash Percent")
    for category in weaponCategories:
        for weapon, stats in weapons[category].items():
            f.write(str(weapon)+",")
            for key, val in stats.items():
                f.write(str(val)+ ",")
            f.write("\n")
        f.write("\n")
    f.close()
print("hola")