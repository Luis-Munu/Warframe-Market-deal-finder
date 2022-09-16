"""File used to redirect the user depending on which module he wants to use."""

from getpass import getpass
from ducanator import use_ducanator
import settings
import riven_relisting
import utils
import deal_scanner
import url_creation
import riven_requests
import process_data
import buy_scanner
import endo_scanner
import relic_scanner
import part_scanner
import weapon_updater

# file used to ask the user for his search preferences. would love a switch function.


def choose_category():
    """Method used to ask the user for the mode to execute"""

    while True:
        print("Which mode do you want to use?:\n")
        print("1. Riven related actions\n")
        print("2. Market scan\n")
        print("3. Update the database\n")

        try:
            cat = int(input("Introduce a number: "))
        except ValueError:
            print("Write a number between 1 and 2. \n")
        if 0 < cat < 4:
            break
    if cat == 1:
        choose_riven_action()
    elif cat == 2:
        choose_scan_mode()
    elif cat == 3:
        weapon_updater.get_weapons()


def choose_riven_action():
    """Method used to ask the user for the mode to execute"""

    while True:
        print("Which mode do you want to use?:\n")
        print("1. Search for rivens\n")
        print("2. Relist your auctions\n")

        try:
            mode = int(input("Introduce a number: "))
        except ValueError:
            print("Write a number between 1 and 2. \n")
        if 0 < mode < 3:
            break
    if mode == 1:
        settings.init()
        define_search()
    elif mode == 2:
        relist_auctions()


def choose_scan_mode():
    """Method used to ask the user for the mode to execute"""

    while True:
        print("Which mode do you want to use?:\n")
        print("1. Find the best ducat/plat items and sellers\n")
        print("2. Scan the market for deals\n")
        print("3. Find the best spare parts to sell in sets\n")
        print("4. Find the best endo/plat mods\n")
        print("5. Scan the best relics to buy and sell\n")
        print("6. Search for your buy orders\n")
        print("7. Auto-create the best buy orders\n")

        try:
            mode = int(input("Introduce a number: "))
        except ValueError:
            print("Write a number between 1 and 2. \n")
        if 0 < mode < 8:
            break
    if mode == 1:
        use_ducanator(ask_for_ducat_scan())
    elif mode == 2:
        scan_for_deals()
    elif mode == 3:
        part_scanner.part_scanner()
    elif mode == 4:
        endo_scan()
    elif mode == 5:
        relic_scanner.scan_relics()
    elif mode == 6:
        scan_buys()
    elif mode == 7:
        print("To be done")


def ask_for_email():
    """Asks the user for its wfm email"""

    while True:
        try:
            email = str(input("Introduce the email associated to your warframe.market account: "))
        except ValueError:
            print("An error happened when reading your email, please try again. \n")
        if email:
            return email


def ask_for_pass():
    """Asks the user for its wfm password"""

    while True:
        try:
            password = str(getpass("Introduce your password: "))
        except ValueError:
            print("An error happened when reading your password, please try again. \n")
        if password:
            return password


def ask_for_name():
    """Asks the user for its wfm username"""

    while True:
        try:
            name = str(input("Introduce your profile name: "))
        except ValueError:
            print("An error happened when reading your profile name, please try again. \n")
        if name:
            return name


def relist_auctions():
    """Asks the user about its options for relisting"""

    while True:
        print("Do you want to relist all your auctions or only the ones without bids?:\n")
        print("1. All the auctions\n")
        print("2. Only the ones without bid\n")
        try:
            bids = int(input("Introduce a number: "))
        except ValueError:
            print("Write a number between 1 and 2. \n")
        if 0 < bids < 3:
            break

    relist_type = bids == 2
    print("Introduce your warframe.market login credentials:\n")
    email = ask_for_email()
    password = ask_for_pass()
    utils.login(email, password)
    riven_relisting.relist_auctions(relist_type)


# asks the user which kind of search he wants to do.
def define_search():
    """Defines the type of search the user wants to use"""

    while True:
        print("Which search do you want to use?:\n")
        print("1. Fast search (low amount of rivens. specific rolls, unrolleds for wanted weapons, generic godrolls)\n")
        print("2. Medium search (medium amount of rivens. will also search for unrolleds for unwanted weapons)\n")
        print("3. Slow search (high amount of rivens. will also search for godrolls for the wanted weapons)\n")
        print("4. Infinite search (great amount of rivens. will also search for godrolls for all the weapons)\n")
        print("5. Specific search (only searches for a weapon or your specific combinations)\n")
        try:
            search_type = int(input("Introduce a number\n"))
        except ValueError:
            print("Write a number between 1 and 5. \n")
        if 0 < search_type < 6:
            break

    if search_type == 1:
        settings.fast_search = True
    elif search_type == 2:
        settings.medium_search = True
    elif search_type == 3:
        settings.slow_search = True
    elif search_type == 4:
        settings.non_existant_search = True
    elif search_type == 5:
        specific_search()
    rivsearch()


def specific_search():
    """Gets data needed to execute an specific search"""

    while True:
        print("Do you want to search for a specific weapon or your specific combos? \n")
        print("1. A specific weapon\n")
        print("2. My specific combos\n")
        try:
            specific = int(input())
        except ValueError:
            print("Write a number between 1 and 2\n")
        if specific == 1:
            settings.specific_weapon = True
            weapon_combo()
            break
        if specific == 2:
            settings.specific_search = True
            break


def weapon_combo():
    """Asks the user if he wants a broad search with generic godroll combinations
    or a specific one for the selected weapon."""

    while True:
        try:
            weapon_name = str(input("Which weapon do you want to search? write a non variant name\n"))
        except ValueError:
            print("Write the name of the weapon you want to search for \n")
        weapon_name = weapon_name.lower().replace(" ", "_")
        if (weapon_name in settings.weapon_list[utils.get_weapon_type(weapon_name)].keys() and
                utils.check_variant(weapon_name) is False):
            settings.weapon_name = weapon_name
            break
        print("Name not valid")

    while True:
        print("Do you want the riven to have specific stats or a generic combo?\n")
        print("1. Specific stats\n")
        print("2. Generic combo\n")
        try:
            stats_type = int(input())
        except ValueError:
            print("Introduce a number between 1 and 2 \n")
        if stats_type == 1:
            ask_for_stats()
            break
        if stats_type == 2:
            break


def ask_for_stats():
    """Asks for the stats to search for the selected weapon.
    A restart option should be added in case the user makes a mistake"""

    print("The list of stats: \n")
    stat_list = [value["name"] for value in settings.stat_list.values()]
    order = ["first positive", "second positive", "third positive", "negative"]
    stat_name = ["stat1", "stat2", "stat3", "negative"]
    thirdpos, neg = 0, 0

    for i, stat in enumerate(stat_list):
        print(str(i) + ". " + stat)
    stat_list = list(settings.stat_list.keys())
    for i in range(4):
        if i == 2:
            while thirdpos not in (1, 2):
                print("Do you want a third positive? \n")
                print("1. Yes")
                print("2. No")
                try:
                    thirdpos = int(input())
                except ValueError:
                    print("Introduce a number between 1 and 2")
                if thirdpos in (1, 2):
                    break
            if thirdpos == 2:
                continue
        if i == 3:
            while neg not in (1, 2):
                print("Do you want a negative? \n")
                print("1. Yes")
                print("2. No")
                try:
                    neg = int(input())
                except ValueError:
                    print("Introduce a number between 1 and 2")
            if neg == 2:
                break
        try:
            statnum = int(input("Write the number of the " + order[i] + "\n"))
        except ValueError:
            print("Introduce a number between 1 and " + str(len(stat_list)))
        if statnum < len(stat_list):
            settings.weapon_stats[stat_name[i]] = stat_list[statnum].lower().replace(" ", "_")


def ask_for_ducat_scan():
    """Asks the user about his ducat limit and the scanning"""

    print("The program will scan the market for items with a ducat value higher than your limit.\n")
    print("At the end of the scan, it'll provide you with a list of the best sellers to buy off the market.\n")
    while True:
        print("Write the ducats/plat ratio you want to search for.\n")
        try:
            ducat_ratio = float(input())
        except ValueError:
            print("Introduce a number between 1 and 2")
        if ducat_ratio >= 0:
            return ducat_ratio


def rivsearch():
    """Process used to search for rivens, step by step"""

    # gets the urls for the searches we have to do.

    res = url_creation.data_creation()
    # requests said searches to the server and returns them.
    res = riven_requests.mass_riven_request(res)
    # processes the requests and converts them into riven objects.
    res = process_data.process_data(res).values()
    # sorts them by price.
    res = sorted(res, key=lambda riven: (-riven.real_value, riven.buyout_price, riven.real_value))
    # exports them into txt files.
    process_data.export_txt(res)

    print("Rivens found: " + str(len(res)))


def scan_for_deals():
    """Searches for deals in the market"""

    deal_scanner.deal_finder()


def scan_buys():
    """Searches for good prices the user wants"""

    buy_scanner.scan_buys(ask_for_name())


def endo_scan():
    """Searches for good endo/plat deals in the market"""

    while True:
        print("If the program finds an item with a good endo/plat ratio it will save it and show a message.")
        print("Type the endo/plat to look for. (default 400)")
        try:
            endo = int(input())
        except ValueError:
            print("Introduce a number between 1 and 2")
        if endo > 0:
            endo_scanner.endo_scan(endo)
