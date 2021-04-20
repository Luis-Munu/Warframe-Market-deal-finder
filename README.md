# WFM-Riven-Search
A project made to search for godrolls, unrolleds and specific rolls faster and easier, it shows grades and a riven rating along with the stats.
To use it just write the command: "python rivenSearch.py"
Feel free to make changes in the config files and in settings.py.

There're 4 types of search, depending on the speed of the search, the number of rivens received increases or diminishes:
A fast one that will search for generic and specific godrolls and takes a minute to complete.
A medium one that will search for generic godrolls for wanted weapons, specific godrolls and unrolleds for every weapon. Takes 5 minutes to complete.
A slow one that will search for generic godrolls for wanted weapons along with generic godrolls, specific godrolls and unrolleds for every weapon. Takes 15 minutes to complete. 
A terribly slow one that will search for godrolls and unrolleds for every weapon along with specific godrolls. Can take up to infinity.

To change the stats, rolls or weapons being searched for just add or remove them in the config files.
To add or remove weapons edit wantedWeapons.csv
To add or remove rolls edit wantedRolls.json
To add or remove decent positives edit decentPositives.csv
To add or remove negatives edit negatives.csv

If I get the time, I'll try to add stat weighting to the riven rating system, and maybe, in the future, weight them around specific weapon stats.ie a non crit weapon don't want critical damage or critical chance.
