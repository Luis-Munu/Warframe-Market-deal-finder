"""Class used to calculate the best grades for each riven,
the punctuation system is based off pricings on different
platforms and trade chat.
It uses the weapon, its type, class, uses, stats...
"""
import settings
import utils


class Profile:
    """Class used to calculate the best grades for each riven,
    the punctuation system is based off pricings on different
    platforms and trade chat.
    It uses the weapon, its type, class, uses, stats...
    """

    def __init__(self, name, weapon_type, stat_weights, equations):
        self.name = name
        self.weapon_type = weapon_type
        self.stat_weights = stat_weights
        self.equations = equations

    def evaluate_stats(self, riven):
        """The method searches for the weight of the stats based on the
        weapon class, type and stats and its equation, then calculates
        a total rating for the riven"""

        punctuation = 0
        for stat, grade in zip(riven.stats, riven.grades):
            weight = self.stat_weights[stat[1]][not stat[0]]
            punctuation += eval(self.equations[stat[1]])
            if -10 < grade < 11:
                punctuation += weight * grade * 0.01 if stat[0] else weight * -grade * 0.01
        return punctuation


def load_profiles():
    """Method used to load the profiles that'll be used"""

    for i, w_type in enumerate(settings.weights_list):
        for key, val in w_type.items():
            settings.profile_list.append(Profile(key, i, val, settings.equations_list[i][key]))


def find_profiles(riven):
    """Method used to find the profiles that'll be used for the weapon, should rework it"""

    weapon_profiles = []
    for prof in settings.profile_list:
        if prof.weapon_type == riven.riven_type:
            weapon_profiles.append(prof)
    return weapon_profiles


def profile_management(riven, prof, punct):
    """Method used to filter the profiles punctuation"""

    if riven.riven_type == 3:
        if prof.name in ["Heavy", "Gunblade"] and (
            riven.weapon["type"]
            not in [
                "Gunblade",
                "Scythe",
                "Two-handed nikana",
                "Dual daggers",
                "Dagger",
                "Rapier",
                "Claws",
                "Hammer",
                "Machete",
            ]
        ):
            punct /= 2
        if prof.name in ["Heavy", "General use"] and "Gunblade" in riven.weapon["type"]:
            punct /= 3
        if prof.name == "Gunblade" and "Gunblade" not in riven.weapon["type"]:
            punct = -20
        if riven.disposition < 1.1 and "statstick" in prof.name:
            punct = punct * riven.disposition / 2
    if (
        riven.riven_type == 2
        and prof.name == "Co-primer"
        and riven.weapon_name not in ["epitaph", "kuva_nukor", "tenet_cycron"]
    ):
        punct = -20
    if ("Rubico" in prof.name and "rubico" not in riven.weapon_name) or (
        "Vectis" in prof.name and "vectis" not in riven.weapon_name
    ):
        punct = -20
    elif (
        "rubico" in riven.weapon_name or "vectis" in riven.weapon_name
    ) and prof.name == "General use":
        punct /= 2

    return punct


def rate_riven(riven):
    """Searches for the weapon profiles, then executes them and chooses
    the best out of them, returning the best riven punctuation"""
    weapon_profiles = find_profiles(riven)
    initial_punct = 0
    if not riven.stats[-1][0]:
        initial_punct += 15
    punct_list = []
    for prof in weapon_profiles:
        punct_list.append(
            [
                prof.name,
                round(
                    utils.scale_range(
                        profile_management(riven, prof, initial_punct + prof.evaluate_stats(riven)),
                        -20,
                        100,
                        0,
                        100,
                    ),
                    2,
                ),
            ]
        )

    return sorted(punct_list, key=lambda punct: punct[1], reverse=True)
