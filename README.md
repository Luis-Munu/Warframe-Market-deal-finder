# WFM-Riven-Search
A project made to search for godrolls, unrolleds and specific rolls faster and easier, it shows grades and a riven rating along with the stats.

To use it just write the command: "python rivenSearch.py" and follow the command guide.

There're 4 types of search, depending on the speed of the search, the number of rivens received increases or diminishes, the times listed here are done with a 10 year old computer, your times will probably be way faster.

A fast one that will search for generic and specific godrolls and takes 2 minutes to complete.

A medium one that will search for generic godrolls for wanted weapons, specific godrolls and unrolleds for every weapon. Takes 15 minutes to complete.

A slow one that will search for generic godrolls for wanted weapons along with generic godrolls, specific godrolls and unrolleds for every weapon. Takes 30 minutes to complete. 

A terribly slow one that will search for godrolls and unrolleds for every weapon along with specific godrolls. Can take many hours to complete.

To change the stats, rolls or weapons being searched for just add or remove them in the config files.
There's a general rule to edit these files. The rows indicates the type of weapon. 0 primaries, 1 shotguns, 2 pistols, 3 archguns, 4 normal melees, 5 heavy attack melees.

To add or remove weapons you want to search rivens for edit wantedWeapons.csv

To edit the list of decent positives make changes in decentPositives.csv

To edit the list of decent negatives make changes in negatives.csv

To edit the list of rolls you want to search for make changes in wantedRolls.json

If I get the time, I'll try to add stat weighting to the riven rating system, and maybe, in the future, weight them around specific weapon stats.ie a non crit weapon don't want critical damage or critical chance.


TODO LIST:
Stat weighting.
Add weapon stats to get a better stat weighting.
Automatically upload results to a website.
