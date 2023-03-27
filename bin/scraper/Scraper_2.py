# This file is used to Trim the Active Players file of a team 
# based on the initial conditions provided
# => Players who have ODI experience
# => Players who have T20 experience
# => Players who have TEST experience
# => Players who have ODI or T20 experience, ... etc
# after trimming the files we should store them in a new folder
# which should be present beforehand
#############################################################################################################

import pandas as pd

# first we need the list of countries to be used
from scraper.Countries import country_list

#############################################################################################################
print("------------------------------------------------------------------------------------------------------")
print("--------------------------------------- [DATA SCRAPING - STAGE 2] ------------------------------------")
print("------------------------------------------------------------------------------------------------------")

# we need to perform this for every country present in the list
for country in country_list:
    # first we need to import the excel file which contains the raw data about the active players
    active_players_df = pd.read_excel(f'./sheets/main_db/active_players/all_formats/ActivePlayers_{country}.xlsx')
    
    # this code needs to be changed for the purpose of changing the output
    # => we are only interested in players who have played at least 1 ODI international
    active_players_df = active_players_df.drop(['TEST', 'T20'], axis=1)
    active_players_df = active_players_df.dropna()

    # now this new data frame needs to be appended to a new file
    with pd.ExcelWriter(f'./sheets/main_db/active_players/odi/ActivePlayers_{country}.xlsx') as writer:
        active_players_df.to_excel(writer, index=False, sheet_name="ODI Active Players")
        print(f"...[LOG]... Added active ODI players for {country} ...")



























