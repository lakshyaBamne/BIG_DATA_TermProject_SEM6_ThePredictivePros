# we wish to add more fields about a player in a team
# this would help in further analysis

# 1) Replace the NAME field with the Full Names of the Players
# 2) Add fields like ['BATTING_HAND', 'BOWL_STYLE']

# Later we will add the field giving information about the 
# ROLE of the player in the team ['BATSMAN', 'BOWLER', 'ALL-ROUNDER'] etc.
############################################################################
# Importing required libraries
import requests
from bs4 import BeautifulSoup

import pandas as pd

import time

############################################################################
# To do this we first need to open the currently existing excel file
# and import it as a data frame to work with it
# then we can edit the data frame and over write the new data frame
############################################################################

# these parts help us to re create the URL endpoint to which we have to 
# make the appropriate request
root_url = 'http://howstat.com/cricket/Statistics/Players/'
root_overview = 'PlayerOverviewSummary.asp?PlayerID='

# countries for which this scraping procedure would be performed
country_list = [
    "IND",  # India
    "AUS",  # Australia
    "NZL",  # New Zealand
    "ENG",  # England
    "PAK",  # Pakistan
    "SAF",  # South Africa
    "BAN",  # Bangladesh
    "SRL",  # Sri Lanka
    "AFG",  # Afghanistan
    "WIN",  # West Indies
    "IRE",  # Ireland
    "SCO"   # Scotland
]

# observe the file name to import is of the form :-
# => ActivePlayers_{COUNTRY_CODE}.xlsx

# we have to perform the procedure for all the countries in the country list
for country in country_list:
    # let us create a data frame to store the excel file
    # using relative paths to import the excel sheets
    active_players_df = pd.read_excel(f'./sheets/active_players/ActivePlayers_{country}.xlsx')

    NAME = []
    BATTING_HAND = []
    BOWL_STYLE = []

    for i in range(len(active_players_df)):
        # first we need to find the player ID of the player to send further requests
        player_id = str(active_players_df.loc[i,["PLAYER_ID"]][0])

        # sending request to the appropriate endpoint on the website
        # for now we only want the overview information
        r_overview = requests.get(root_url + root_overview + player_id)

        # after making these requests, we should pause the program for some time 
        # so as to avoid getting a timeout response from the website
        time.sleep(1)


        soup = BeautifulSoup(r_overview.content,"html.parser")

        required_table = soup.find_all("table")[0].find_all('table')[0].find_all('table')[0]

        player_name = required_table.find_all('tr')[2].find_all('td')[1].text[11:-11]
        batting_hand = required_table.find_all('tr')[5].find_all('td')[1].text[11:-10]
        bowl_style = required_table.find_all('tr')[6].find_all('td')[1].text[11:-10]

        NAME.append(player_name)
        BATTING_HAND.append(batting_hand)
        BOWL_STYLE.append(bowl_style)

        print(f"...[LOG]... [STAGE-2] ... updated {player_name} ({country})")


    # first we should drop the NAME column which already exists in the data frame
    active_players_df = active_players_df.drop(['NAME'], axis=1)

    # adding the fields
    active_players_df['BOWL_STYLE'] = pd.Series(BOWL_STYLE)
    active_players_df['BATTING_HAND'] = pd.Series(BATTING_HAND)
    active_players_df['NAME'] = pd.Series(NAME)

    # now we should export and re write the updated data frame to the same location
    with pd.ExcelWriter(f'./sheets/active_players/ActivePlayers_{country}.xlsx') as writer:
        active_players_df.to_excel(writer,'Sheet 1', index=False)
        print(f"----------------------------------- UPDATED {country}----------------------------")







