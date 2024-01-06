"""Module used to store riven-related data and means to calculate it.
Logic and data should be separated but I'm too mongolic to do it yet"""

import src.riven_stuff.riven_rater as riven_rater
import src.settings as settings
import src.utils as utils


class Riven:
    """class used to store all riven-related data and means to calculate it."""

    def __init__(
        self,
        weapon="",
        name="",
        initial_price=-1,
        buyout_price=-1,
        seller="",
        polarity="",
        rerolls=-1,
        mastery_rank=-1,
        riven_rank=-1,
        stats=[],
    ):
        self.weapon_name = weapon  # name of the weapon.
        self.name = name.capitalize()  # name of the riven.
        self.initial_price = initial_price  # starting price of the auction.
        self.buyout_price = buyout_price  # buyout price of the auction.
        self.seller = seller  # name of the seller.
        self.stats = stats  # stats of the riven.
        self.polarity = polarity.capitalize()  # polarity of the riven.
        self.rerolls = rerolls  # number of rerolls.
        self.mastery_rank = mastery_rank  # mastery rank needed to use the riven.
        self.riven_rank = riven_rank  # rank of the riven
        self.buyout_price = (
            buyout_price if buyout_price else 99999
        )  # buyout price of the riven.
        self.riven_type = utils.get_weapon_type(self.weapon_name)
        self.weapon = self.get_stats()
        self.outdated = False  # indicates if the stats are outdated or wrong.
        self.wanted_weapon = (
            self.is_wanted()
        )  # indicates if the riven is in the wanted weapons list.
        self.wanted_roll = False
        self.grades = self.get_grades()  # checks stats grades.
        self.riven_rate = (
            self.check_stats()
        )  # riven rating based on check_stats algorithm.
        self.paths = self.prepare_paths()
        self.real_value = (max(0, self.riven_rate) / self.buyout_price * 100) ** (
            max(0, self.riven_rate) / 100
        )
        self.message = self.riv_to_text()

    def is_wanted(self):
        """checks if the weapon is wanted for godrolls, specific rolls and unrolleds."""

        if self.weapon_name in settings.wanted_unroll:
            return True
        if any(self.weapon_name == x["weapon"] for x in settings.wanted_rv):
            return True
        if any(self.weapon_name == y for x in settings.wanted_rv for y in x):
            return True
        return False

    def get_stats(self):
        """Finds the best version of the weapon, useful to weight stats when rating rivens"""
        name = self.weapon_name.replace("_", " ").title()
        family = [w for w in settings.weapons if w["name"] == name][0]["family"]
        versions = [w for w in settings.weapons if w["family"] == family]
        sorted(versions, key=lambda w: w["disposition"])
        self.disposition = [float(v["disposition"]) for v in versions]

        return versions[0]

    def rate_stats(self):
        """Rates the stats of the riven based on the profiles of the weapon."""
        self.scores = riven_rater.rate_riven(self)
        return self.scores[0][1]

    def check_stats(self):
        """Punctuation system. it checks how good the riven stats are against
        settings. wanted or decent combinations of its types."""

        punctuation = self.rate_stats()

        if self.weapon_name in settings.wanted_rv:
            for wanted_roll in settings.wanted_rv[self.weapon_name]:
                stats = [stat[1] for stat in self.stats]
                if utils.compare_stats(list(wanted_roll["stats"].values()), stats):
                    if self.stats[-1][0] is False:
                        self.wanted_roll = True
                    break

        return punctuation

    def calculate_grade(self, stat, dispo, fakerank):
        """Gets the proper grade of the stat,
        trying every disposition and also checks for fake ranks"""

        # gets the base value of the stat based on the weapon type.
        # find the value of the stat in settings.stat_list
        res = abs(
            float(
                [x for x in settings.stat_list if x["wfm_name"] == stat[1]][0][
                    "value" + str(self.riven_type)
                ]
            )
            * float(dispo)
        )
        res = (res / 9) * (self.riven_rank + 1) if not fakerank else res
        # if there is negative.
        if self.stats[-1][0] is False:
            # if the stat is negative.
            if stat[0] is False:
                res *= 0.5 if len(self.stats) == 3 else 0.7575
            else:
                res *= 1.25 if len(self.stats) == 3 else 0.947
        else:
            # if there is no negative and 3 positives.
            if len(self.stats) == 3:
                res *= 0.7575
        # puts res in a 0-1 scale. formula is (value - minimum) / (maximum - minimum).
        res = (abs(stat[2]) - res * 0.9) / (res * 1.1 - res * 0.9) if res != 0 else 0
        # above calculations should be changed based on the new scale
        # however it's easier to work with this one.
        if stat[1] == "range":
            if 1.1 > res > 1:
                res = 1
            elif 0 > res > -0.1:
                res = 0
        return res

    def calculate_grades(self, fakerank):
        """Calculates the grade of the stat of a riven.
        if the grades aren't compatible with a given disposition it tries with other ones,
        if the weapon has any variant.
        if there is no disposition to which grades are good it returns the closest one
        based on a distance system.
        the formula is: base stat value based on weapon type * disposition * stat system.
        the system calculates res based on these rules:
        if the weapon has 3 positives and a negative the positives are
        weighted *0.947 and the negative *0.7575.
        if the weapon has 2 positives and a negative the positives are
        weighted *1.25 and the negative *0.5.
        if the weapon has 3 positives and no negative the positives are weighted *0.7575.
        if the weapon has 2 positives and no negative the positives stay the same."""

        grades = [0, 0, 0, 0]
        best_distance = 9999

        for dispo in self.disposition:
            distance, buen_grade = 0, 0
            grades_aux = []
            for stat in self.stats:
                res = self.calculate_grade(stat, dispo, fakerank)
                grades_aux.append(res)
                # if res is within the 0-1 scale then the grade is good.
                # otherwise we get the distance to said range.
                if 0 < res < 1:
                    buen_grade += 1
                else:
                    distance += abs(res) if res < 0 else res - 1
            # if all the stats have grades within 0-1 scale it returns them.
            # else if the distance is less than the current best
            # distance it updates the grades and the distance.
            if buen_grade == len(self.stats):
                self.used_disposition = dispo
                return grades_aux
            if distance < best_distance:
                grades = grades_aux
                best_distance = distance

        if best_distance > 30 and fakerank is False:
            return self.calculate_grades(True)

        if any(0 > grade or grade > 1.1 for grade in grades):
            self.outdated = True

        self.used_disposition = self.disposition[0]
        return grades

    def get_grades(self):
        """This module normalizes the grades then calculates
        its punctuation based on simodeus bot."""

        grades = [
            utils.scale_range(grade, 0, 1, -10, 10)
            for grade in self.calculate_grades(False)
        ]
        self.grade_letters = []
        for grade in grades:
            if grade > 9.5:
                self.grade_letters.append("S")
            elif grade > 7.5:
                self.grade_letters.append("A+")
            elif grade > 5.5:
                self.grade_letters.append("A")
            elif grade > 3.5:
                self.grade_letters.append("A-")
            elif grade > 1.5:
                self.grade_letters.append("B+")
            elif grade > -1.5:
                self.grade_letters.append("B")
            elif grade > -3.5:
                self.grade_letters.append("B-")
            elif grade > -5.5:
                self.grade_letters.append("C+")
            elif grade > -7.5:
                self.grade_letters.append("C")
            elif grade > -9.5:
                self.grade_letters.append("C-")
            else:
                self.grade_letters.append("F")
        return grades

    def prepare_paths(self):
        """Creates the paths and files that the riven will write its information in"""

        paths = []
        if self.wanted_weapon is True:
            path = settings.wanted_path
        else:
            path = settings.unwanted_path
        paths.append(path + "\\All rivens.txt")
        if self.rerolls == 0:
            paths.append(path + "\\Unrolleds\\Unrolled list.txt")
            paths.append(
                path
                + "\\Unrolleds\\Unrolled "
                + self.weapon_name.capitalize().replace("_", " ")
                + ".txt"
            )
        if self.wanted_roll:
            paths.append(path + "\\Wanted rolls\\Wanted rolls.txt")
            paths.append(
                path
                + "\\Wanted rolls\\Wanted "
                + self.weapon_name.capitalize().replace("_", " ")
                + ".txt"
            )
        if self.riven_rate >= 95:
            paths.append(path + "\\95-100. Godrolls\\Godrolls.txt")
            paths.append(
                path
                + "\\95-100. Godrolls\\"
                + self.weapon_name.capitalize().replace("_", " ")
                + " Godrolls.txt"
            )
        elif self.riven_rate >= 85:
            paths.append(path + "\\85-95. Good rivens\\Good rivens.txt")
            paths.append(
                path
                + "\\85-95. Good rivens\\Good "
                + self.weapon_name.capitalize().replace("_", " ")
                + ".txt"
            )
        elif self.riven_rate >= 70:
            paths.append(path + "\\70-85. Decent rivens\\Decent rivens.txt")
            paths.append(
                path
                + "\\70-85. Decent rivens\\Decent "
                + self.weapon_name.capitalize().replace("_", " ")
                + ".txt"
            )
        elif self.riven_rate >= 60:
            paths.append(path + "\\60-70. Usable rivens\\Usable rivens.txt")
            paths.append(
                path
                + "\\60-70. Usable rivens\\Usable "
                + self.weapon_name.capitalize().replace("_", " ")
                + ".txt"
            )
        elif self.riven_rate >= 40:
            paths.append(path + "\\40-60. Bad rivens\\Bad rivens.txt")
            paths.append(
                path
                + "\\40-60. Bad rivens\\Bad "
                + self.weapon_name.capitalize().replace("_", " ")
                + ".txt"
            )
        elif self.riven_rate < 40:
            paths.append(path + "\\Trashcan\\Trashcan.txt")
            paths.append(
                path
                + "\\Trashcan\\"
                + self.weapon_name.capitalize().replace("_", " ")
                + " Trash.txt"
            )
        return paths

    def riv_to_text(self):
        """Writes the riven data in specified folders depending on the riven caracteristics."""
        message = (
            "Name: "
            + self.weapon_name.capitalize().replace("_", " ")
            + " "
            + self.name
            + "\n"
        )
        # riven rating.
        message += "Experimental riven rating: " + str(round(self.riven_rate, 2)) + "\n"

        if len(self.stats) == 3 and not self.stats[-1][0]:
            message += "Two stats!\n"

        # best rating profile
        message += "Best profile: " + self.scores[0][0] + "\n"
        # other profiles
        for profile, rating in self.scores[1:]:
            message += profile + ": " + str(rating) + ", "
        # if outdated.
        if self.outdated:
            message += "\nThe stats of this riven don't match its rank, they may be outdated or wrong.\n"
        # stats and grades.
        message += "\nRiven stats: \n"
        for i, stat in enumerate(self.stats):
            message += (
                [x for x in settings.stat_list if x["wfm_name"] == stat[1]][0]["name"]
                + ":  "
                + str(stat[2])
                + "\n"
            )
            if self.outdated is False:
                message += (
                    "\t\tGrade: "
                    + self.grade_letters[i]
                    + " ("
                    + str(round(self.grades[i], 2))
                    + "%)\n"
                )

        message += (
            "\nPolarity: "
            + self.polarity
            + "   Rerolls: "
            + str(self.rerolls)
            + "   MR: "
            + str(self.mastery_rank)
            + "\n"
        )
        message += "Riven rank : " + str(self.riven_rank) + "\n"
        if self.buyout_price != 99999:
            message += (
                "Initial price:  "
                + str(self.initial_price)
                + "   Buyout price: "
                + str(self.buyout_price)
                + "\n"
            )
        else:
            message += (
                "Initial price:  "
                + str(self.initial_price)
                + "   Buyout price: "
                + " infinite \n"
            )
        message += "Seller: " + self.seller + "\n"
        message += "Value/Plat: " + str(round(self.real_value, 2)) + "\n"
        message += "Used disposition: "
        message += str(round(self.used_disposition, 2)) + "\n"
        message += "Real disposition: "
        message += (
            str(round(self.disposition[0], 2))
            + "\n--------------------------------------------------\n"
        )
        return message
