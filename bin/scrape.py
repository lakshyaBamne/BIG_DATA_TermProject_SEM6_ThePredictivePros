# This is the main script for scraping data in the format required

##################################################################################################
# first we need to execute the Scraper_1.py file to get the ActivPlayers_ file for
# countries of interest
exec(open('./scraper/Scraper_1.py').read())

##################################################################################################
# now we need to trim the active players files to the form which we want
# currently we are interested in players who are active in ODI
exec(open('./scraper/Scraper_2.py').read())

##################################################################################################
# now we need to extract the information about the active odi players and store in 
# files in appropriate locations
# exec(open('./scraper/Scraper_3.py').read())

##################################################################################################
# now we scrape some more extra information about a player's Batting performance
# these are stored in a separate sheet in the same workbook for every player
# exec(open('./scraper/Scraper_4.py').read())

##################################################################################################
# now we scrape some more extra information about a player's Bowling performance
# these are stored in a separate sheet in the same workbook for every player
# exec(open('./scraper/Scraper_5.py').read())
