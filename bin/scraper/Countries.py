# we can store the country code for teams for which we want to scrape data in a list
# we are including the top 12 ODI ranked teams in the world at the time of making this project
country_list = [
    "IND",  # India
    # "AUS",  # Australia
    # "NZL",  # New Zealand
    # "ENG",  # England
    # "PAK",  # Pakistan
    # "SAF",  # South Africa
    # "BAN",  # Bangladesh
    # "SRL",  # Sri Lanka
    # "AFG",  # Afghanistan
    # "WIN",  # West Indies
    # "IRE",  # Ireland
    # "SCO"   # Scotland
]

espn_country_list = {
    "IND" : ("India", "https://www.espncricinfo.com/cricketers/team/india-6"),
    "AUS" : ("Australia", "https://www.espncricinfo.com/cricketers/team/australia-2"),
    "NZL" : ("New Zealand", "https://www.espncricinfo.com/cricketers/team/new-zealand-5"),
    "ENG" : ("England", "https://www.espncricinfo.com/cricketers/team/england-1"),
    "PAK" : ("Pakistan", "https://www.espncricinfo.com/cricketers/team/pakistan-7"),
    "SAF" : ("South Africa", "https://www.espncricinfo.com/cricketers/team/south-africa-3"),
    "BAN" : ("Bangladesh", "https://www.espncricinfo.com/cricketers/team/bangladesh-25"),
    "SRL" : ("Sri Lanka", "https://www.espncricinfo.com/cricketers/team/sri-lanka-8"),
    "AFG" : ("Afghanistan", "https://www.espncricinfo.com/cricketers/team/afghanistan-40"),
    "WIN" : ("West Indies", "https://www.espncricinfo.com/cricketers/team/west-indies-4"),
    "IRE" : ("Ireland", "https://www.espncricinfo.com/cricketers/team/ireland-29"),
    "SCO" : ("Scotland", "https://www.espncricinfo.com/cricketers/team/scotland-30")
}
