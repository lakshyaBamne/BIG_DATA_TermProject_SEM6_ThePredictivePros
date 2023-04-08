import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time

from classes.player import Player
from scraper.Countries import country_list, espn_country_list

#############################################################################################################
print("------------------------------------------------------------------------------------------------------")
print("--------------------------------------- [DATA SCRAPING - STAGE 5] ------------------------------------")
print("------------------------------------------------------------------------------------------------------")

for country in country_list:
    # we should get the name of the team for which the player plays
    PLAYER_TEAM = str(espn_country_list[f'{country}'][0])
    
    # first we need to get the active odi players in the team
    PLAYER_LIST = list(map(
        str, 
        pd.read_excel(
            f'./sheets/main_db/active_players/odi/ActivePlayers_{country}.xlsx'
        )["PLAYER_ID"]
    ))

    # now for each player in this list we want to first
    # => read their performance workbook
    # => get the match codes of the matches they have played
    # => scrape the match scorecards for the matches which are available
    # => create a data frame for the new information scraped
    # => append a new worksheet in the existing workbook

    for player in PLAYER_LIST:
        # first we need to instantiate the player as an object of the Player class
        one_player = Player(player)
        
        try:
            # getting the list of matches played by the player in ODI
            MATCH_CODE = list(map(
                str,
                pd.read_excel(
                    f'./sheets/main_db/teams/{country}/PlayerPerformance_{player}.xlsx', 
                    sheet_name='ODI Bowling'
                )['MATCH_CODE']
            ))

            if len(MATCH_CODE) >= 20:
                odi_batting_extra_df = one_player.GET_OdiPlayerMatchDetailsBowl(MATCH_CODE[-20:], PLAYER_TEAM)
                
                # we should first test if the returned data frame is empty or not
                if len(odi_batting_extra_df) == 0:
                    print(f'... [ERROR] ... extra batting info not found for {player} ({country}) ...')
                else:
                    path = f'./sheets/main_db/teams/{country}/PlayerPerformance_{player}.xlsx'

                    with pd.ExcelWriter(path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                        odi_batting_extra_df.to_excel(writer, sheet_name='ODI Bowling Extra', index=False)
                        print(f'... [LOG] ... added info for {player} ({country}) ...')
            else:
                print(f'... [IGNORED] ... not enought matches for {player} ({country})')
        except:
            print(f"...[EXCEPTION]... no bowling record found for {player} ({country})")


print("------------------------------------------------------------------------------------------------------")
print("--------------------------------------------- [SCRAPING END] -----------------------------------------")
print("------------------------------------------------------------------------------------------------------")


