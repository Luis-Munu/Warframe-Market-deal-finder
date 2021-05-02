import settings
from utils import getWeaponType, checkVariant
import os
#Class used to store all riven-related data and means to calculate it.

class Riven:

    #Defines a method used by set to be able to compare rivens by hash in order to ignore possible duplicates.
    def __eq__(self, other):
        return self.Weapon == other.Weapon and self.Name == other.Name and self.Seller == other.Seller
        
    #Defines a method used by set to be able to compare rivens by hash in order to ignore possible duplicates.
    def __hash__(self):
        return hash((self.Weapon, self.Name, self.Seller))

    def __init__(self, Weapon="", Name="", InitialPrice=-1, BuyoutPrice=-1, Seller="", Polarity="", Rerolls=-1, MasteryRank=-1, Stats=[]):
        self.Weapon = Weapon                                    #Name of the weapon.
        self.Name= Name.capitalize()                            #Name of the riven.
        self.InitialPrice = InitialPrice                        #Starting price of the auction.
        self.BuyoutPrice = BuyoutPrice                          #Buyout price of the auction.
        self.Seller = Seller                                    #Name of the seller.
        self.Stats = Stats                                      #Stats of the riven.
        self.Polarity = Polarity.capitalize()                   #Polarity of the riven.
        self.Rerolls = Rerolls                                  #Number of rerolls.
        self.MasteryRank = MasteryRank                          #Mastery rank needed to use the riven.
        self.BuyoutPrice = BuyoutPrice if BuyoutPrice else 99999#Buyout price of the riven.
        self.Outdated = False                                   #Indicates if the stats are outdated or wrong.
        self.Disposition = [self.getDisposition(x) for x in self.getOcurrences()] #Riven possible dispositions
        self.WantedWeapon = False                               #Indicates if the riven is in the wanted Weapons list.

        for i in getWeaponType(Weapon):
            if len(settings.wishedWeapons) < i: continue
            if Weapon in settings.wishedWeapons[i]:
                self.WantedWeapon = True 
                break
        
        if Weapon in settings.wishedUnrolleds: self.WantedWeapon = True 
        if any(Weapon == x for x  in settings.wishedRivens): self.WantedWeapon = True 

        self.RivenRate = self.checkStats()                      #Riven rating based on checkStats algorithm.
        self.Grades = self.calculateGrades()                    #Checks stats grades.

    #Returns the disposition of a weapon given the name.
    def getDisposition(self, weapon):
        return settings.weaponList[weapon]["disposition"]
    #Finds any variants a weapon may have. Dirty but fast code.
    #Check conditions for each weapon that has self.Weapon inside their name.
    #The conditions are:
    #1: It starts with the weapon name.
    #2: It contains the weapon name and also a a variant name.
    #Only one condition is needed to be true
    def getOcurrences(self):
        #gets a list with all weapons that contain given weapon in the name.
        WeaponList = [weapon3 for weapon3 in settings.weaponList.keys() if self.Weapon in weapon3] 
        res = []
        for weaponName in WeaponList: 
            flag = False
            bool1 = weaponName.startswith(self.Weapon)
            if checkVariant(weaponName): flag = True
            bool2 = flag and self.Weapon in weaponName
            if  bool1 or bool2:
                res.append(weaponName)
        return res

    #Rates the stats of the riven, given a weapon type and a combination of good stats for the weaponType
    #As of now the punctuation goes as follows:
    #+25 per settings.wished positive
    #+10 per decent positive
    #-20 per wasted positive
    #+25 per settings.wished negative
    #-100 if negative is on the settings.wished positives list
    #-20 per wasted negative
    #I want to try to add different weights to the stat in the future. So that a -reload speed neg isn't as bad as -dmg.
    def rateStats(self, combination, weaponType):
        puntuacion = 0
        stats = self.Stats
        if self.Stats[-1][0]== False: stats = self.Stats[:-1]
        for stat in stats:
            if stat[1] in combination: puntuacion+=25
            elif stat[1] in list(set(combination+ settings.decentPositives[weaponType])): puntuacion+=10
            else: puntuacion -= 20
        if self.Stats[-1][0]== False:
            if self.Stats[-1][1] in settings.wishedNegatives[weaponType]: puntuacion += 25
            elif self.Stats[-1][1] in list(set(combination+ settings.decentPositives[weaponType])): puntuacion -= 100
            else: puntuacion -= 20
        else: 
            puntuacion -= 20
        return puntuacion
 

    #Punctuation system. It checks how good the riven stats are against settings.wished or decent combinations of they type.
    def checkStats(self):
        mejorPuntuacion = -9999
        for weaponType in getWeaponType(self.Weapon):
            #Little band-aid for heavy attack weapons.
            for i in range(4,5):
                if weaponType == i and len(settings.wishedWeapons) >= i and self.Weapon not in settings.wishedWeapons[i]: continue
            for combination in settings.combinations[weaponType]:
                puntuacion = self.rateStats(list(combination.values()), weaponType)
                if puntuacion > mejorPuntuacion: mejorPuntuacion = puntuacion 
            if self.Weapon in settings.wishedRivens:
                puntuacion = self.rateStats(list(settings.wishedRivens[self.Weapon].values()), weaponType)
                if puntuacion > mejorPuntuacion: mejorPuntuacion = puntuacion 
        return mejorPuntuacion


    #Calculates the grade of the stat of a riven. 
    #If the grades aren't compatible with a given disposition it tries with other ones, if the weapon has any variant.
    #If there is no disposition to which grades are good it returns the closest one based on a distance system.
    #The formula is: base stat value based on weapon type * disposition * stat system.
    #The system calculates res based on these rules:
    #If the weapon has 3 positives and a negative the positives are weighted *0.947 and the negative *0.7575
    #If the weapon has 2 positives and a negative the positives are weighted *1.25 and the negative *0.5
    #If the weapon has 3 positives and no negative the positives are weighted *0.7575
    #If the weapon has 2 positives and no negative the positives stay the same.
    def calculateGrades(self):
        grades = [0,0,0,0]
        bestDistance = 9999

        for dispo in self.Disposition:
            distance = 0
            buenGrade = 0
            gradesAux = []
            for stat in self.Stats:
                #Gets the base value of the stat based on the weapon Type.
                res = abs(settings.statList[stat[1]]["value" + str(getWeaponType(self.Weapon)[0])]) * dispo
                #If there is negative
                if self.Stats[-1][0] == False: 
                    #If the stat is negative
                    if stat[0] == False:
                        #If 2 positives
                        if len(self.Stats) == 3: res *= 0.5
                        #If 3 positives
                        else: res *= 0.7575
                    #If 2 positives
                    elif len(self.Stats) == 3: res *=  1.25 
                    #If 3 positives
                    else: res *= 0.947 
                #If there is no negative
                else: 
                    #If 2 positives
                    if len(self.Stats) == 4: res *= 0.7575
                #Puts res in a 0-1 scale. Formula is (Value - Minimum) / (Maximum - Minimum) 
                res = (abs(stat[2])-res*0.9)/(res*1.1-res*0.9) if res !=0 else 0
                #For reader ease.
                gradesAux.append(res*10)
                #If res is within the 0-1 scale then the grade is good.Otherwise we get the distance to said range.
                if res < 1 and res > 0 : buenGrade+=1
                else: 
                    if res < 0: distance += abs(res)
                    else: distance+= res -1
            #If all the stats have grades within range it returns them. 
            #Else if the distance is less than the current best distance it updates the grades and the distance.
            if buenGrade == len(self.Stats): return gradesAux
            elif distance < bestDistance:
                grades = gradesAux
                bestDistance = distance
        
        if any(0 < grade < 10.5 for grade in grades): self.Outdated = True

        return grades
        
    #Writes the riven data in specified folders depending on the riven caracteristics.
    def printData(self):
        paths = []

        if self.WantedWeapon == True:
            path = settings.wantedPath  
        else: path = settings.unwantedPath
        paths.append(path + "\\All rivens.txt")
        if self.Rerolls == 0: 
            paths.append(path + "\\Unrolleds\\Unrolled list.txt")
            paths.append(path + "\\Unrolleds\\Unrolled " + self.Weapon.capitalize().replace("_", " ") + ".txt")
        if self.RivenRate >= 90: 
            paths.append(path + "\\Godrolls\\Godrolls.txt")
            paths.append(path + "\\Godrolls\\" + self.Weapon.capitalize().replace("_", " ") + " godrolls.txt")
        elif self.RivenRate >= 60: 
            paths.append(path + "\\Good_ones\\Good ones.txt")
            paths.append(path + "\\Good_ones\\Good " + self.Weapon.capitalize().replace("_", " ") + ".txt")
        elif self.RivenRate >= 40: 
            paths.append(path + "\\Decents\\Decents.txt")
            paths.append(path + "\\Decents\\Decent " + self.Weapon.capitalize().replace("_", " ") + ".txt")
        elif self.RivenRate < 40: 
            paths.append(path + "\\Trashcan\\Trash.txt")
            paths.append(path + "\\Trashcan\\" + self.Weapon.capitalize().replace("_", " ") + " trash.txt")

        #The format is:
        #Riven name
        #Riven rating
        #Shows if stats are outdated
        #Stats + grades
        #Polarity + Rerolls + MR
        #Initial price + Buyout price
        #Dispositions
        for fpath in paths:
            resultFile = open(fpath,'a+')

            #if it's not the first riven of the file, it adds some newlines to separate it from the previous ones.
            if os.stat(fpath).st_size != 0:
                resultFile.write("\n")
                resultFile.write("\n")
            #Name
            resultFile.write(("Name: " + self.Weapon.capitalize().replace("_", " ") + " " + self.Name + "\n"))
            #Riven rating
            resultFile.write("Experimental riven rating: " + str(self.RivenRate) + "\n")
            #If outdated
            if self.Outdated: resultFile.write("The stats of this riven seem outdated or it's not rank 8, grades can be incorrect\n")
            #Stats and grades
            for i in range(len(self.Stats)):
                resultFile.write(settings.statList[self.Stats[i][1]]["name"] + ":  " + str(self.Stats[i][2]) + "\n")
                resultFile.write("\t\tGrade (0-10): " + str(round(self.Grades[i],4)) +"\n")
            
            resultFile.write("Polarity: " + self.Polarity + "   Rerolls: " + str(self.Rerolls) + "   MR: " + str(self.MasteryRank) + "\n")
            
            if self.BuyoutPrice != 99999: resultFile.write("Initial Price:  " + str(self.InitialPrice) + "   Buyout price: " + str(self.BuyoutPrice) + "\n")
            else: resultFile.write("Initial Price:  " + str(self.InitialPrice) + "   Buyout price: " +" Infinite \n")
            resultFile.write("Seller: " + self.Seller + "\n")

            resultFile.write("Dispositions: ")
            for dispo in self.Disposition[:-1]: resultFile.write( str(dispo) + ", ")
            resultFile.write( str(self.Disposition[-1]) + "\n")
            resultFile.close()
