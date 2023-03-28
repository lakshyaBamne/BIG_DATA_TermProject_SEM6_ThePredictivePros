# PAGE - To show active players in the selected team in all the formats
#############################################################################################

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scraper.Countries import country_list

# we must use absolute paths in the streamlit application scripts
from pathlib import Path

#############################################################################################

tab_count = -1

new_list = ["ALL"]

for country in country_list:
    new_list.append(country)

tab_objects = st.tabs(new_list)

for tab in tab_objects:
    tab_count = tab_count + 1
    if tab_count == 0:
        # this is corresponding to the first page that has different information.
        with tab:
            st.write("""
                ## General Statistics about active players
            """)
            
            # we need to get the data first and then we can show it to the web application
            TEST = []
            ODI = []
            T20 = []
            
            # list to store the number of players who play all the formats in the team
            ALL_FORMAT_PLAYERS = []

            for country in country_list:
                # first we should get the active players data of the country 
                absolute_path = Path(__file__).parents[1] / f'sheets/main_db/active_players/all_formats/ActivePlayers_{country}.xlsx'
                active_players = pd.read_excel(absolute_path)
                
                # number of players which are active in atleast one format
                total_players = len(active_players)

                # getting the information for the first plot
                TEST.append(len(list(active_players['TEST'].dropna())))
                ODI.append(len(list(active_players['ODI'].dropna())))
                T20.append(len(list(active_players['T20'].dropna())))

                # getting information for the second plot
                all_format_players = len(active_players.dropna())

                ALL_FORMAT_PLAYERS.append( round((all_format_players/total_players) * 100, 2) )
            
            st.write("""
                ### Active Players in different countries and formats
            """)

            # plot which shows the distribution of players in a country across the three formats
            fig1 = plt.figure(figsize=(10,3))

            plt.plot(country_list, TEST, color='red', marker='.', markersize=10, label='TEST')
            plt.plot(country_list, ODI, color='g',marker='.', markersize=10, label='ODI')
            plt.plot(country_list, T20, color='black', marker='.', markersize=10, label='T20')

            plt.legend()

            st.pyplot(fig1)

            st.write("""
                ---
            """)

            fig2 = plt.figure(figsize=(10,4))
            graph = plt.bar(country_list,ALL_FORMAT_PLAYERS, color='orange', width=0.5)
            
            i = 0
            for p in graph:
                width = p.get_width()
                height = p.get_height()
                x, y = p.get_xy()
                plt.text(x+width/2,
                        y+height*1.01,
                        str(ALL_FORMAT_PLAYERS[i])+'%',
                        ha='center')
                i = i + 1

            st.write("""
                ### Percentage of players who play in all formats
            """)

            st.pyplot(fig2)

        
    else:
        with tab:
            # first we need to know for which country we are making the graphs
            country = country_list[tab_count-1]

            # we want to load the data frame containing the number of active players in a country
            # to show the stats as a pie chart we first need the data

            # we can find the data frame for the selected country from the files scraped by the program
            absolute_path = Path(__file__).parents[1] / f'sheets/main_db/active_players/all_formats/ActivePlayers_{country}.xlsx'
            active_players = pd.read_excel(absolute_path)
            # st.dataframe(active_players)

            # we want to make a pie chart for the number of players in the three formats for this country
            num_test = len(list(active_players['TEST'].dropna()))
            num_odi = len(list(active_players['ODI'].dropna()))
            num_t20 = len(list(active_players['T20'].dropna()))

            # creating a matplotlib figure object which will be displayed in the web app
            fig = plt.figure(figsize=(3,3))

            # parameters taken by the pie chart
            values = [num_test, num_odi, num_t20]
            labels = ["TEST", "ODI", "T20"]
            explode = (0, 0, 0.1)

            # making the plot on the figure canvas 
            plt.pie(values, labels=labels, explode=explode, autopct='%1.1f%%')

            # plotting the figure on the web application
            st.write("""
                #### Player distribution across formats
            """)

            st.pyplot(fig)



# with tab_objects[0]:
    















