# This module can be used to scrape data from HowStat.com about :-
#   1) Active Players in International Cricket (Test, ODI, T20) for any Team
#############################################################################################################
# Importing required libraries and modules

import requests
from bs4 import BeautifulSoup
import pandas as pd

import time

# we need the list of countries to work with the scraping
from scraper.Countries import country_list

#############################################################################################################
print("------------------------------------------------------------------------------------------------------")
print("--------------------------------------- [DATA SCRAPING - STAGE 1] ------------------------------------")
print("------------------------------------------------------------------------------------------------------")

# To get the active players in a team, we have to scrape data from the following endpoint of HowStat.com
active_players_url = "http://www.howstat.com/cricket/Statistics/Players/PlayerListCurrent.asp"

# We can make a data frame for each of these countries and then export it as an excel sheet
# to be used in further scraping and analysis
for country in country_list:
    # this payload needs to be sent to the endpoint along with the POST request
    payload = {"cboCountry" : country}

    # making a request to the website to mimic a select operation on the website
    r = requests.post(active_players_url, data=payload)

    # after making these requests, we should pause the program for some time 
    # so as to avoid getting a timeout response from the website
    time.sleep(1)

    # if the website does not repond with the correct information, loop automatically breaks
    if r.status_code != 200:
        print("\n[ERROR] : CANNOT GET INFORMATION FROM WEBSITE ABOUT THE ACTIVE PLAYERS !!\n")
        break
    
    # if the loop is not broken, it means we have the correct response and can further scrape data
    html_content = r.content

    # creating a beautiful soup object for the html recieved as a response
    soup = BeautifulSoup(html_content, "html.parser")

    # this is the main table that has all the required information
    main_table = soup.find_all("table", class_="TableLined")[0]

    # now we need all the rows of the table to extract the necessary information
    all_rows = []
    
    table_rows = main_table.contents

    for row in table_rows:
        if row.name == 'tr':
            all_rows.append(row)

    # the first 2 rows are headers and extra and the last row gives the count of players
    # thus these three rows are not needed
    # this list now has the <tr> tags as it's elements for each of the players
    all_rows = all_rows[2:len(all_rows)-1]

    # we should create an empty data frame which would become empty after every iteration
    # in which we will store the player information taken from the html table
    active_players_df = pd.DataFrame()

    # these lists are used to initialize the data frame after data collection has completed
    NAME_LIST = []
    PLAYER_ID_LIST = []
    TEST_LIST = []
    ODI_LIST = []
    T20_LIST = []

    # we have to collect information about every player
    for i in range(len(all_rows)):
        # player name
        player_name = all_rows[i].contents[1].contents[1].text
        NAME_LIST.append(player_name)

        # player id which will be used to go to his performance page in next step for scraping
        player_id = all_rows[i].contents[1].contents[1].get('href')[-4:]
        PLAYER_ID_LIST.append(player_id)

        # Test matches played
        test_matches = all_rows[i].contents[7].text
        if len(test_matches) > 10:
            TEST_LIST.append(None)
        else:
            TEST_LIST.append(int(test_matches[1:-1]))

        # ODI matches played
        odi_matches = all_rows[i].contents[9].text
        if len(odi_matches) > 10:
            ODI_LIST.append(None)
        else:
            ODI_LIST.append(int(odi_matches[1:-1]))

        # T20 matches played
        t20_matches = all_rows[i].contents[11].text
        if len(t20_matches) > 10:
            T20_LIST.append(None)
        else:
            T20_LIST.append(int(t20_matches[1:-1]))
    

    # now we should append to the data frame
    active_players_df['NAME'] = NAME_LIST
    active_players_df['PLAYER_ID'] = PLAYER_ID_LIST
    active_players_df['TEST'] = TEST_LIST
    active_players_df['ODI'] = ODI_LIST
    active_players_df['T20'] = T20_LIST

    # now we have the data frame as the table on the website
    # this data frame can be used to get the active players from any format

    # so we should output this data frame as a master sheet from which useful
    # information can be extracted later
    file_name = f"ActivePlayers_{country}.xlsx"

    # the file write path should be relative to the main.py file in the root of the project
    with pd.ExcelWriter(f'./sheets/main_db/active_players/all_formats/ActivePlayers_{country}.xlsx') as writer:
        active_players_df.to_excel(writer, 'all_formats_raw', index=False)

    print(f"...[LOG]... [STAGE-1] ... added {country}")
