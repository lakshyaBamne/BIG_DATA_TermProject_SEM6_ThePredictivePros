# This script performs EDA on the Players and shows a dashboard for review

print("----------------------------------------------------------------------")
print("--------------------------[STARTING EDA]------------------------------")
print("----------------------------------------------------------------------")

# we are using the streamlit library to perform EDA and dashboarding
# for all the data we have collected in the scraping step

import streamlit as st

############################################################################################

# Putting a title using markdown language
st.write("""
    ## The Predictive Pros :sunglasses:

    ---

    ### Welcome to the Data dashboard for our project

    ---

    * Navigate to the different pages present on the sidebar to view the data in various formats.
        * ***Active Players*** - to view the various active players in a country in various formats of cricket.

    ---
        
""")

