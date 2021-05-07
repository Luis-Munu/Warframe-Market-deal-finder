import settings, rivenRelisting

#File used to ask the user for his search preferences. The code seems dirty but until python adds a switch function
#I see no other way.


def chooseMode():
    while True:
        print("Which mode do you want to use?:\n")
        print("1. Search rivens\n")
        print("2. Relist my auctions\n")
        try: mode= int(input("Introduce a number: "))
        except ValueError:
            print("Write a number between 1 and 2. \n")
        if 0 < mode  < 3: break
    if mode == 1: 
        defineSearch()
    elif mode == 2: 
        askForCredentials()
    return mode
        

def askForCredentials():
    while True:
        print("Do you want to relist all your auctions or only the ones without bids?:\n")
        print("1. All the auctions\n")
        print("2. Only the ones without bid\n")
        try: bids= int(input("Introduce a number: "))
        except ValueError:
            print("Write a number between 1 and 2. \n")
        if 0 < bids  < 3: break
    if bids == 2: rivenRelisting.relistWithoutBids=True
    print("Introduce your warframe.market login credentials:\n")
    while True:
        try: email= str(input("Introduce the email associated to your warframe.market account: "))
        except ValueError:
            print("An error happened when reading your email, please try again. \n")
        if email: break
    while True:
        try: password= str(input("Introduce your password: "))
        except ValueError:
            print("An error happened when reading your password, please try again. \n")
        if password: break
    rivenRelisting.login(email, password)
    rivenRelisting.relistAuctions()

#Asks the user which kind of search he wants to do.
def defineSearch():

    while True:
        print("Which search do you want to use?:\n")
        print("1. Fast search (Low amount of rivens. Specific rolls, unrolleds for wanted weapons, generic godrolls)\n")
        print("2. Medium search (Medium amount of rivens. Will also search for unrolleds for unwanted weapons)\n")
        print("3. Slow search (High amount of rivens. Will also search for godrolls for the wanted weapons)\n")
        print("4. Infinite search (Great amount of rivens. Will also search for godrolls for all the weapons)\n")
        print("5. Specific search (Only searches for a weapon or your specific combinations)\n")
        try: searchType = int(input("Introduce a number\n"))
        except ValueError:
            print("Write a number between 1 and 5. \n")
        if 0 < searchType  < 6: break
    #Python its time to give us a switch.
    if searchType == 1: settings.fastSearch = True
    elif searchType == 2: settings.mediumSearch = True
    elif searchType == 3: settings.slowSearch = True
    elif searchType == 4: settings.nonExistantSearch = True
    elif searchType == 5: specificSearch()
    
def specificSearch():

    while True:
        print("Do you want to search for a specific weapon or your specific combos? \n")
        print("1. A specific weapon\n")
        print("2. My specific Combos\n")
        try: specific = int(input())
        except ValueError:
            print("Write a number between 1 and 2\n")
        if specific == 1: 
            settings.specificWeapon = True
            weaponCombo()
            break
        elif specific == 2: 
            settings.specificSearch = True
            scanMode()
            break

#Asks the user if he wants a broad search with generic godroll combinations or a specific one for the selected weapon.
def weaponCombo():
    while True:
        try: weaponName = str(input("Which weapon do you want to search? Write a non variant name\n"))
        except ValueError:
            print("Write the name of the weapon you want to search for \n")
        weaponName = weaponName.lower().replace(" ", "_")
        if weaponName in settings.weaponList: 
            settings.weaponName = weaponName
            break
        else: print("Name not valid")

    while True:
        print("Do you want the riven to have specific stats or a generic combo?\n")
        print("1. Specific Stats\n")
        print("2. Generic Combo\n")
        try: wantStats = int(input())
        except ValueError:
            print("Introduce a number between 1 and 2 \n")
        if wantStats == 1:
            askForStats()
            break
        elif wantStats == 2:
            break

#Asks for the stats to search for the selected weapon. Should add a restart option in case you make a mistake.
def askForStats():
    print ("The list of stats: \n")
    statList = [value["name"] for value in settings.statList.values()]
    order = ["first positive", "second positive", "third positive", "negative"]
    thirdpos = 1
    neg = 1
    for i, stat in enumerate(statList):
        print(str(i) + ". " + stat)
    statList = list(settings.statList.keys())
    for i in range(4):
        while True:
            if i == 2 :
                while True:
                    print("Do you want a third positive? \n")
                    print("1. Yes")
                    print("2. No")
                    try: thirdpos = int(input())
                    except ValueError:
                        print("Introduce a number between 1 and 2")
                    if thirdpos == 1 or thirdpos == 2 : break
            if i == 3 :
                while True:
                    print("Do you want a negative? \n")
                    print("1. Yes")
                    print("2. No")
                    try: neg = int(input())
                    except ValueError:
                        print("Introduce a number between 1 and 2")
                    if neg == 1 or neg == 2 : break
            if neg == 2 or thirdpos == 2: break
            try: statnum = int(input("Write the number of the " + order[i] + "\n"))
            except ValueError:
                print("Introduce a number between 1 and " + str(len(statList)))
            if statnum < len(statList) :
                if i == 0:
                    settings.weaponStats["stat1"] = statList[statnum].lower().replace(" ", "_")
                if i == 1:
                    settings.weaponStats["stat2"] = statList[statnum].lower().replace(" ", "_")
                if i == 2 and thirdpos:
                    settings.weaponStats["stat3"] = statList[statnum].lower().replace(" ", "_")
                if i == 3 and neg:
                    settings.weaponStats["negative"] = statList[statnum].lower().replace(" ", "_")      
                break
    
def scanMode():
    while True:
        print("Would you like the program to keep searching your specific rivens every 5 minutes?\n")
        print("If the program finds an auction with the price below your maximum price it will save it and show a message.\n")
        print("1. Yes\n")
        print("2. No\n")
        try: scan = int(input())
        except ValueError:
            print("Introduce a number between 1 and 2")
        if scan == 1:
            settings.scanMode = True
            break
        elif scan == 2 : break

