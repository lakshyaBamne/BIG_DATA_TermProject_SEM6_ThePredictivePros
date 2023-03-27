# Extracting statistics of the active odi players using the Player class
# and it's methods

##########################################################################################################
# Importing the required libraries

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# we need to import the list of countries to be used in the scraping 
from scraper.Countries import country_list

# importing the Player class
from classes.player import Player

#############################################################################################################
print("------------------------------------------------------------------------------------------------------")
print("--------------------------------------- [DATA SCRAPING - STAGE 3] ------------------------------------")
print("------------------------------------------------------------------------------------------------------")

# this data frame would store all the players who do not have a bowling record and hence are pure batsmen
PURE_BATSMEN = pd.DataFrame()

# we want to get the data for each player in each country
for country in country_list:
    BATSMEN = []

    # first we should get the active players in the country
    active_players_df = pd.read_excel(f'./sheets/main_db/active_players/all_formats/ActivePlayers_{country}.xlsx')

    # We should get the data for players who have played at least one ODI game and not retired
    active_players_df = active_players_df.drop(['TEST','T20'], axis=1)
    active_players_df = active_players_df.dropna()    

    # in order to use the Player class and it's methods we need to get all the player id's
    PLAYER_ID = []

    # let us append the player id of each active player in a list to later use
    indexes = list(active_players_df.index)

    for i in indexes:
        id = str(active_players_df.loc[i, ['PLAYER_ID']][0])
        PLAYER_ID.append(id)

    # now we can find the information of players using the Player class methods
    for id in PLAYER_ID:
        # we need to instantiate the Player class for each player whose information we require
        one_player = Player(id)

        # since we only want the ODI information about the players
        # we use the following two methods only
        odi_bat_df = one_player.GET_OdiBatPerformance()
        odi_bowl_df = one_player.GET_OdiBowlPerformance()

        # now we can store this obtained information in an excel sheet
        with pd.ExcelWriter(f'./sheets/main_db/teams/{country}/PlayerPerformance_{id}.xlsx') as writer:
            # batting record of the player is always present
            odi_bat_df.to_excel(writer, index=False, sheet_name="ODI Batting")
            
            # bowling record may not be present for some player
            try:
                odi_bowl_df.to_excel(writer, index=False, sheet_name="ODI Bowling")
            except:
                # if bowling record is not found, then we can be sure that this is a pure batsman
                BATSMEN.append(id)
                pass
            
            # logging is done to console
            print(f"...[LOG]... added performance of {id} ...")
    
    # we should append the pure batsmen list of this country to the Data frame
    PURE_BATSMEN[f'{country}'] = pd.Series(BATSMEN)
    
# we should export the pure batsmen data frame as a utility file
with pd.ExcelWriter(f'./sheets/main_db/utility/PureBatsmen_ODI.xlsx') as writer:
    PURE_BATSMEN.to_excel(writer, index=False, sheet_name="ODI Pure Batsmen")
    print(f"...[LOG]... added a utility file => Pure Batsmen in ODI ...")



