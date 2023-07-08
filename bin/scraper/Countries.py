# we can store the country code for teams for which we want to scrape data in a list
# we are including the top 12 ODI ranked teams in the world at the time of making this project
country_list = [
    # "IND",  # India -> 51 Active ODI Players
    # "AUS",  # Australia -> 40 Active ODI Players
    "NZL",  # New Zealand -> 38 Active ODI Players
    # "ENG",  # England -> 44 Active ODI Players
    # "PAK",  # Pakistan -> 47 Active ODI Players
    # "SAF",  # South Africa -> 38 Active ODI Players
    # "BAN",  # Bangladesh -> 31 Active ODI Players
    # "SRL",  # Sri Lanka -> 49 Active ODI Players
    # "AFG",  # Afghanistan -> 34 Active ODI Players
    # "WIN",  # West Indies -> 63 Active ODI Players
    # "IRE",  # Ireland -> 24 Active ODI Players
    # "SCO"   # Scotland -> 26 Active ODI Players
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
