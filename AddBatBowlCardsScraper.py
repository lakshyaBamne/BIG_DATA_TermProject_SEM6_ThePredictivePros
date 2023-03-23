# In this scraping step, we want to get the stats for matches played by any player
# both batting and bowling stats are required
##########################################################################################################
# Importing the required libraries

import pandas as pd

import requests
from bs4 import BeautifulSoup

import time
##########################################################################################################
# these parts help us to re create the URL endpoint to which we have to 
# make the appropriate request
root_url = 'http://howstat.com/cricket/Statistics/Players/'
root_match_scorecard = 'http://www.howstat.com/cricket/Statistics/'

root_bat = 'PlayerProgressBat_ODI.asp?PlayerID='
root_bowl = 'PlayerProgressBowl_ODI.asp?PlayerID='

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

##########################################################################################################

# we need to get the player_id of a player to send the appropriate requests
# to get his batting and bowling statistics cards to then scrape

# dictionary to store the playerID of those players across countries which only have a batting record
# i.e. people who have never bowled a single over through their entire careers
PURE_BATSMEN = pd.DataFrame()

# we need data for each player of each country
for country in country_list:
    # list to store the exceptions of a single country
    BATSMEN = []

    # first we need to fetch the data about the active players in the country
    active_players_df = pd.read_excel(f'./sheets/active_players/ActivePlayers_{country}.xlsx')

    PLAYER_ID = []

    # let us append the player id of each active player in a list to later use
    for i in range(len(active_players_df)):
        PLAYER_ID.append( active_players_df.loc[i, ["PLAYER_ID"]][0] )

    # now we can start the process of making requests and getting the data for each player
    # two requests are made per player
    for player in PLAYER_ID:
        # time out of one second before the next request to avoid getting timed out
        time.sleep(1)
            
        # request to get the batting card
        r_bat = requests.get(root_url + root_bat + str(player))
        # request to get the bowling card
        r_bowl = requests.get(root_url + root_bowl + str(player))

        # creating a bs4 object for the obtained response
        soup_bat = BeautifulSoup(r_bat.content, "html.parser")
        soup_bowl = BeautifulSoup(r_bowl.content, "html.parser")

        # Let us create the batting data frame and the bowling data frame that will be exported
        # these empty data frames will be filled with data onnce the html response is parsed
        player_bat_df = pd.DataFrame()
        player_bowl_df = pd.DataFrame()

        # first let us populate the BATTING CARD
        required_table = soup_bat.find_all("table", class_="TableLined")[0]
        
        # extracting the rows that have information from the table into a list
        all_rows = required_table.find_all("tr")
        all_rows = all_rows[3:len(all_rows)-1]

        # empty lists which will represent one attribute each in the batting card
        MATCH_NUMBER = []
        INNING_NUMBER = []
        MATCH_DATE = []
        MATCH_CARD_LINK = []
        MATCH_INNING = []
        OPPONENT = []
        VENUE = []
        DISMISSAL = []
        RUNS_SCORED = []
        BALLS_FACED = []

        for row in all_rows:
            one_row = row.contents
            MATCH_NUMBER.append(one_row[1].text[22:-20])
            INNING_NUMBER.append(one_row[3].text[22:-20])
            MATCH_DATE.append(one_row[5].contents[1].text)
            MATCH_CARD_LINK.append(root_match_scorecard + one_row[5].contents[1].get('href')[3:])
            MATCH_INNING.append(one_row[7].text[12:-20])
            OPPONENT.append(one_row[9].text[22:-20])
            VENUE.append(one_row[11].text[22:-20])
            DISMISSAL.append(one_row[13].text[22:-20])
            RUNS_SCORED.append(one_row[15].text[22:-20])
            BALLS_FACED.append(one_row[17].text[12:-20])
        
        # now we can populate the batting data frame
        player_bat_df['MATCH_NUMBER'] = MATCH_NUMBER 
        player_bat_df['INNING_NUMBER'] = INNING_NUMBER
        player_bat_df['MATCH_DATE'] = MATCH_DATE
        player_bat_df['MATCH_CARD_LINK'] = MATCH_CARD_LINK
        player_bat_df['MATCH_INNING'] = MATCH_INNING
        player_bat_df['OPPONENT'] = OPPONENT
        player_bat_df['VENUE'] = VENUE
        player_bat_df['DISMISSAL'] = DISMISSAL
        player_bat_df['RUNS_SCORED'] = RUNS_SCORED
        player_bat_df['BALLS_FACED'] = BALLS_FACED

        # now let us populate the BOWLING CARD of the player
        # some players might not have a bowling card... these are the pure BATSMEN
        try:
            required_table = soup_bowl.find_all("table", class_="TableLined")[0]
            
            # extracting the rows that have information from the table into a list
            all_rows = required_table.find_all("tr")
            all_rows = all_rows[3:len(all_rows)]

            # empty lists that will represent single attributes in the bowling card of the player
            MATCH_NUMBER = []
            MATCH_CARD_LINK = []
            MATCH_INNING = []
            OPPONENT = []
            VENUE = []
            OVERS = []
            WICKETS_RUNS = []

            for row in all_rows:
                # each row is a <tr> which contains the list of <td> that have the information
                one_row = row.contents

                try:
                    MATCH_CARD_LINK.append(root_match_scorecard + one_row[3].contents[1].get('href')[3:])
                    MATCH_NUMBER.append(one_row[1].text[22:-20])
                    MATCH_INNING.append(one_row[5].text[12:-20])
                    OPPONENT.append(one_row[7].text[22:-20])
                    VENUE.append(one_row[9].text[22:-20])
                    OVERS.append(one_row[13].text[22:-20])
                    WICKETS_RUNS.append(one_row[15].text[22:-20])
                except:
                    pass

            # now let us push the fileds in the data frame
            player_bowl_df['MATCH_NUMBER'] = pd.Series(MATCH_NUMBER)
            player_bowl_df['MATCH_CARD_LINK'] = pd.Series(MATCH_CARD_LINK)
            player_bowl_df['MATCH_INNING'] = pd.Series(MATCH_INNING)
            player_bowl_df['OPPONENT'] = pd.Series(OPPONENT)
            player_bowl_df['VENUE'] = pd.Series(VENUE)
            player_bowl_df['OVERS'] = pd.Series(OVERS)
            player_bowl_df['WICKETS_RUNS'] = pd.Series(WICKETS_RUNS)
        except:
            # if the player does not have a bowling record, we inser an empty data frame
            # to the BOWLING card of the player because he might bowl in the future
            player_bowl_df['MATCH_NUMBER'] = []
            player_bowl_df['MATCH_CARD_LINK'] = []
            player_bowl_df['MATCH_INNING'] = []
            player_bowl_df['OPPONENT'] = []
            player_bowl_df['VENUE'] = []
            player_bowl_df['OVERS'] = []
            player_bowl_df['WICKETS_RUNS'] = []

            # but we should add this information to the dictionary for later use
            BATSMEN.append(player)
            pass


        # now we should export this data frame to an excel sheet in the required location 
        with pd.ExcelWriter(f"./sheets/teams/{country}/PlayerStatistics_{player}.xlsx") as writer:
            player_bat_df.to_excel(writer, f"BATTING_{player}", index=False)
            player_bowl_df.to_excel(writer, f"BOWLING_{player}", index=False)
            print(f"...[LOG]... [STAGE-3] ... Added batting and bowling stats of : {player} ({country})")

    # now we should add the only batsmen list of the country to the data frame
    # which store the only batsment data of every country
    PURE_BATSMEN[f"{country}"] = pd.Series(BATSMEN)

# now let us export the data frame as another utility excel file for later use
with pd.ExcelWriter(f'./sheets/utility/PureBatsmen.xlsx') as writer:
    PURE_BATSMEN.to_excel(writer, "Pure Batsmen", index=False)
    print(f"...[LOG]... [STAGE-3] ... added the UTILITY EXCEL file of Pure batsmen ...")
