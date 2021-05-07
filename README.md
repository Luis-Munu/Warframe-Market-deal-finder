# WFM-Riven-Search
A personal project that includes some warframe.market utilities. It allows you to relist all your auctions at once, search for godrolls, unrolleds and specific rolls faster and easier while showing grades and a riven rating along with the stats.

It also has a scanner mode that constantly searches for specific rolls behind your price, and alerts you if it finds any auction.

To use it you may need to install some libraries first with the command "pip3 install library", after that just write the command: "python rivenSearch.py" on a cmd/powershell and you're set up.

There're five types of search, depending on the speed of the search, the number of rivens received increases or diminishes:

A fast one that will search for generic and specific godrolls and takes a minute to complete.

A medium one that will search for generic godrolls for wanted weapons, specific godrolls and unrolleds for every weapon. Takes 5 minutes to complete.

A slow one that will search for generic godrolls for wanted weapons along with generic godrolls, specific godrolls and unrolleds for every weapon. Takes 15 minutes to complete. 

A terribly slow one that will search for godrolls and unrolleds for every weapon along with specific godrolls. Can take many hours to complete and it's not recommended.

A specific one, just for the rolls you inputted in the files. It's extremely fast if you don't add lots of specific rolls. It also allows you to search for a specific weapon and combination of stats for it, and you can also use the scan mode to search for your specific rolls every 5 minutes. If the bot finds any auction with your rolls and under your price, it will save the auction and print a message in the console.

To change the stats, rolls or weapons being searched for just add or remove them in the config files.
There's a general rule to edit these files. The rows indicates the type of weapon. 0 primaries, 1 shotguns, 2 pistols, 3 archguns, 4 normal melees, 5 heavy attack melees.

To add or remove weapons edit wantedWeapons.csv

To add or remove decent positives edit decentPositives.csv

To add or remove negatives edit negatives.csv

To add or remove rolls edit wantedRolls.json

If I get the time, I'll try to add stat weighting to the riven rating system, and maybe, in the future, weight them around specific weapon stats.ie a non crit weapon don't want critical damage or critical chance.


TODO LIST:

Add weapon stats to get a better stat weighting, using some presets and specific cases. (Thanks Mutalist)

A decent GUI.

Automatically upload results to a website.
