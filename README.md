# WFM-Riven-Search

A personal project created as a compilation of warframe.market tools.
As of now it's able to search automatically for godrolls, unrolleds and specific rolls much faster and easier than manually, it's able to show additional information about the found rivens, such as stat grades and a riven rating.

It also scans the market to search for the best items to convert into ducats, into endo, best relics to buy and sell, good deals.

It currently uses Python 3.9.7, install the library ratelimit using the command "pip install ratelimit" and execute the main file using "python riven_search.py" on the project folder.

There're several search modes, depending on the speed the user needs, but the number of rivens scanned greatly scales with execution time.
As of now it's recommended to do a fast search if you need the results in 2-3 minutes and a slow search which gives a pretty accurate representation of wfm rivens in 30 minutes.

The user can change the wanted weapons, rolls and many other settings editing the files inside the config folder.

The common order to use when editing rolls or weapons is this one: 0 primaries, 1 shotguns, 2 pistols, 3 normal melees, 4 archguns.

To add or remove weapons edit wantedWeapons.csv

To add or remove rolls edit wantedRolls.json

As of now there're several things to do, which I may continue in the following months.

TODO LIST:

Ask for math advice to upgrade the weighting system.

Repair the relic search system, it currently fails at rating a relic.

Create an update method to automatically update all the item databases.

Implement a search to create buy orders on the items with better sell/buy diff ratio if they have decent volume.

Slightly change the UI to let people search for statsticks or not. As of now they're searched by default, but they can be disabled by editing the lines 121, 155 and 168 removing the "st" of the file names.

User interface, although this requires more time than I'm currently able to input on this.

Also there's a need to upgrade the quality of data storage and access, it's difficult to get what the program needs at a certain moment.
