## UPDATE
The project has been pretty much dead for the last 2 years, I did some small changes due to certain issues arising to make the project remain functional, but that's about it until WFM implements new endpoints so third party apps don't have to bombard them with requests. Hopefully when that happens their performance and speed will be as great as it once was and I'll update the project with the new functionality.

I will repeat it again: DO NOT USE THE SLOW MARKET SCANS AS OF NOW, not only it will take hours to complete but also saturate WFM servers, this includes, but is not limited to, slow riven searches and relic scans.

# Warframe Market deal finder

A personal project created as a compilation of warframe.market tools to learn python.

It's able to scan the market in order to find the best items to convert into ducats, into endo, spare parts to sell in sets, best relics to buy and sell... overall good deals.

It also comes with an experimental deal finder for Rivens, being able to provide a rating based on its stats and grades by using a profile system.

There're several search modes, depending on the speed and accuracy that is needed, however the execution speed is greatly limited (+95%) by the API limits of the website. The recommended modes are the fast search (1-2 minutes, around 8000 rivens) and the slow one (25-30 minutes, 25000-50000 rivens).

## Customization

The user can customize the wanted weapons, rolls and many other settings by editing the files inside the config folder.

The weapon type order used when editing rolls or weapons is this one: 0 primaries, 1 shotguns, 2 pistols, 3 melees, 4 archguns.

To add or remove weapons edit wantedWeapons.csv. To add or remove rolls edit wantedRolls.json

## How to use

It currently uses Python 3.10.7, install the library ratelimit using the command "pip3 install ratelimit" and execute the main file using "python deal_finder.py" on the project folder.


## TODO

As of now there're several things to do, which I may continue some time in the future.
- Add support for rivenhunter.com and riven.market.
   - Translation system for URLs of WFM to the other websites. DONE but RH requests are blocked.
   - Multiprocessing for each website in order to shorten waiting times. 
   - Slight editions on request processing and riven object creation.
- Update the GUI to make the tool accessible for normal people.
   - Finish the remaining screens with Sigma. 
   - Add functionality to the UI. 
- Update ducat values when updating the database.
- Current weightings for the different profiles are mostly picked by gut feeling, a mathematical procedure should be implemented.
- Upgrade the code's quality, which is a hard task as it is mostly spaghetti right now.
