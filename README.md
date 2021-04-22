# WFM-Riven-Search
A project made to search for godrolls, unrolleds and specific rolls faster and easier, it shows grades and a riven rating along with the stats.

To use it you will need the library ratelimit. To get it use the command "pip3 install ratelimit"

After that just write the command: "python rivenSearch.py" in the project folder and wait for the results.

There're 4 types of search, depending on the speed of the search, the number of rivens received increases or diminishes:

A fast one that will search for generic and specific godrolls and takes a minute to complete.

A medium one that will search for generic godrolls for wanted weapons, specific godrolls and unrolleds for every weapon. Takes 5 minutes to complete.

A slow one that will search for generic godrolls for wanted weapons along with generic godrolls, specific godrolls and unrolleds for every weapon. Takes 15 minutes to complete. 

A terribly slow one that will search for godrolls and unrolleds for every weapon along with specific godrolls. Can take up to infinity.

There's no way to speed this up as far as I'm concerned, as warframe.market returns a size-capped response, missing results if you do a broad search.

To change the stats, rolls or weapons being searched for just add or remove them in the config files.
There's a general rule to edit these files. The rows indicates the type of weapon. 0 primaries, 1 shotguns, 2 pistols, 3 archguns, 4 normal melees, 5 heavy attack melees.

To add or remove weapons edit wantedWeapons.csv

To add or remove decent positives edit decentPositives.csv

To add or remove negatives edit negatives.csv

To add or remove rolls edit wantedRolls.json

If I get the time, I'll try to add stat weighting to the riven rating system, and maybe, in the future, weight them around specific weapon stats.ie a non crit weapon don't want critical damage or critical chance.


TODO LIST:
User interface
Ability to search for just one weapon or specific combo on the go.
Stat weighting.
Add weapon stats to get a better stat weighting.
Automatically upload results to a website.
