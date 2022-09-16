# Warframe Market deal finder

A personal project created as a compilation of warframe.market tools to learn python.

It's able to scan the market in order to find the best items to convert into ducats, into endo, spare parts to sell in sets, best relics to buy and sell... overall good deals.

It also comes with an experimental deal finder for Rivens, being able to provide a rating based on its stats and grades by using a profile system.

There're several search modes, depending on the speed and accuracy that is needed, however the execution speed is greatly limited (+95%) by the API limits of the website. The recommended modes are the fast search (1-2 minutes, around 8000 rivens) and the slow one (25-30 minutes, 50000 rivens).

## Customization

The user can customize the wanted weapons, rolls and many other settings by editing the files inside the config folder.

The weapon type order used when editing rolls or weapons is this one: 0 primaries, 1 shotguns, 2 pistols, 3 melees, 4 archguns.

To add or remove weapons edit wantedWeapons.csv. To add or remove rolls edit wantedRolls.json

## How to use

It currently uses Python 3.9.7, install the library ratelimit using the command "pip3 install ratelimit" and execute the main file using "python deal_finder.py" on the project folder.


## TODO

- As of now there're several things to do, which I may continue in the following months.
- Ask for mathematical advice to upgrade the weighting system., may use Xikto's DPS calculator to improve the current profiles.
- Update the GUI with QT to make the tool usable. 
- Create an update method to automatically update all the item databases instead of just weapons.
- Implement a search to create buy orders on the items with better buy/sell ratio if they have decent volume. Buy low, sell high.
- Slightly change the UI to let people search for statsticks or not. As of now they're searched by default, but they can be disabled by editing the lines 121, 155 and 168 removing the "st" of the file names.
- Support for riven.market and rivenhunter.com, the latest being able to provide tons of useful information.
- Convert spaghetti code into real code, a problem to be dealt with in the future, not to gain a speed increase but knowledge.
