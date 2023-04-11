# Importing the required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class Player:
    """
        Represents a player on Howstat.com website.
        Players information is scraped from here by use of various methods

        To instantiate an object for this class, provide a valid player ID
        as an argument while instantiating

        After instantiating the player
    """

    # class variables which represent important information using which information is scraped
    # using these variables, the appropriate methods create the correct url where player information is present
    ROOT_URL = 'http://howstat.com/cricket/Statistics/Players/'
    ROOT_MATCH_SCORECARD = 'http://www.howstat.com/cricket/Statistics/Matches/'

    # the following parts help create the correct URL for some aspect related to the player
    ROOT_ODI_MATCH = 'MatchScorecard_ODI.asp?MatchCode='
    ROOT_T20_MATCH = 'MatchScorecard_T20.asp?MatchCode='

    ROOT_ODI_MATCH_END = '&Print=Y'
    
    ROOT_PLAYER_OVERVIEW = 'PlayerOverviewSummary.asp?PlayerID='

    ROOT_ODI_BAT = 'PlayerProgressBat_ODI.asp?PlayerID='
    ROOT_ODI_BOWL = 'PlayerProgressBowl_ODI.asp?PlayerID='

    ROOT_T20_BAT = 'PlayerProgressBat_T20.asp?PlayerID='
    ROOT_T20_BOWL = 'PlayerProgressBowl_T20.asp?PlayerID='

    # CLASS CONSTRUCTOR only initializes the player ID of a player
    def __init__(self, ID):
        # player ID as used by the website we are trying to scrape
        self.ID = ID

        # to find the name of the player we can make a request to the overview page of the player
        OVERVIEW_PAGE = self.ROOT_URL + self.ROOT_PLAYER_OVERVIEW + f'{self.ID}'
        try:
            r_overview = requests.get(OVERVIEW_PAGE)
            soup = BeautifulSoup(r_overview.content,"html.parser")
            required_table = soup.find_all("table")[0].find_all('table')[0].find_all('table')[0]

            player_name = required_table.find_all('tr')[2].find_all('td')[1].text[11:-11]

            self.NAME = player_name

        except:
            self.NAME = "--Name Not Found--"
            pass

        # initializing the player name as a class variable

    # CLASS METHOD to return a string representation of the instantiated player    
    def __str__(self) -> str:
        return f"{self.NAME} ({self.ID})"

    # OBJECT METHODS to bring functionality to the class objects

    def UTIL_MakeSoup(self, PAGE_URL: str) -> BeautifulSoup:
        """
            Utility Function to make a get request to the given URL 
            and return the parsed string
        """
        
        # we also sleet the function for 1 second to avoid getting timed out
        time.sleep(1)

        r = requests.get(PAGE_URL)
        soup = BeautifulSoup(r.content, "html.parser")

        return soup

    def GET_Overview(self) -> pd.DataFrame:
        """
            method to get the overview page of the player to extract useful information about the player

            returned dataframe with the following fields => "ID, "NAME", "BATTING_HAND", "BOWL_STYLE"
        """

        # first we need to create the correct URL to go to the overview page
        OVERVIEW_PAGE = self.ROOT_URL + self.ROOT_PLAYER_OVERVIEW + f'{self.ID}'

        # creating a new data frame to store the basic information about the player
        player_overview_df = pd.DataFrame()

        # now we need to make a get request to the required page
        try:
            r_overview = requests.get(OVERVIEW_PAGE)

            # using bs4 to parse the recieved html content from the overview page of the player
            soup = BeautifulSoup(r_overview.content,"html.parser")

            required_table = soup.find_all("table")[0].find_all('table')[0].find_all('table')[0]
            
            PLAYER_ID = []
            PLAYER_NAME = []
            BATTING_HAND = []
            BOWL_STYLE = []

            # variables to store the information recieved for the player
            player_name = required_table.find_all('tr')[2].find_all('td')[1].text[11:-11]
            batting_hand = required_table.find_all('tr')[5].find_all('td')[1].text[11:-10]
            bowl_style = required_table.find_all('tr')[6].find_all('td')[1].text[11:-10]

            PLAYER_ID.append(self.ID)
            PLAYER_NAME.append(player_name)
            BATTING_HAND.append(batting_hand)
            BOWL_STYLE.append(bowl_style)

            player_overview_df["ID"] = pd.Series(PLAYER_ID)
            player_overview_df["NAME"] = pd.Series(PLAYER_NAME)
            player_overview_df["BATTING_HAND"] = pd.Series(BATTING_HAND)
            player_overview_df["BOWL_STYLE"] = pd.Series(BOWL_STYLE)

            # returning all the information bundled in a single tuple
            return player_overview_df
            
        except Exception as error:
            # if overview page is not received, the function terminates and nothing is done
            return f"[ERROR] => Overview Page not responding for PlayerID={self.ID}\n[EXCEPTION RAISED] {error}"
        
    def GET_OverviewTemp(self) -> pd.DataFrame:
        pass
    
    def GET_IntlStatus(self, df: pd.DataFrame) -> tuple:
        """
            method returns the number of International matches played in the three formats in order

            returned tuple => (test_matches, odi_matches, t20_matches)
        """

        # to find the correct row, we must make a query to the data frame
        # this query will return a data frame with a single entry
        player = df.query(f"PLAYER_ID == {self.ID}")

        # return player

        # number of matches played by the player in the three formats

        try:    
            num_test = int(list(player['TEST'])[0])
        except:
            num_test = 0
        
        try:    
            num_odi = int(list(player['ODI'])[0])
        except:
            num_odi = 0
        
        try:    
            num_t20 = int(list(player['T20'])[0])
        except:
            num_t20 = 0

        return (num_test, num_odi, num_t20)

    def GET_OdiPlayerMatchDetailsBat(self, MATCH_CODE: list, PLAYER_TEAM: str) -> pd.DataFrame:
        """
            Finds some more attriibutes of a player's batting performance for a particular match
            
            function takes in input the list of matches for which we want to find the attributes
            and the team for which the player plays

            returns a data frame with the required fields
            
            => BATTING_POSITION, NUM_4, NUM_6, PERCENT_RUNS_OF_TOTAL, MAN_OF_MATCH
        """

        # first let us initialize some variables which we can use later in the program

        # data frame to be returned by the method later
        odi_batting_extra_df = pd.DataFrame()

        # we need to populate these lists so that later they can be appended to the data frame
        BATTING_POSITION = []
        NUM_4 = []
        NUM_6 = []
        PERCENT_RUNS_OF_TOTAL = []
        MAN_OF_MATCH = []

        # we make a separate list of URL's to navigate to later and scrape the data
        PAGES = []
        for match_code in MATCH_CODE:
            OVERVIEW_PAGE = self.ROOT_MATCH_SCORECARD + self.ROOT_ODI_MATCH + str(match_code) + self.ROOT_ODI_MATCH_END
            PAGES.append(OVERVIEW_PAGE)

        # now we need to scrape each of the url and get the required information
        count_good_pages = 0
        total_pages = len(MATCH_CODE)

        for page in PAGES:

            # these variables will be updated for each new iteration
            batting_position = None
            num_4 = None
            num_6 = None
            percent_runs = None
            man_of_match = "NO"

            try:
                # using custom function to get the data and parse it
                soup = self.UTIL_MakeSoup(page)

                # some match pages are not returning the complete data about the match
                # so we can only extract the information for some matches of the player
                num_rows_returned = len(soup.find("table", class_="Scorecard").findChildren("tr", recursive=False))

                if num_rows_returned != 38:
                    print("[ERROR] website not responding correctly")
                else:
                    count_good_pages = count_good_pages + 1

                    # this list contains all the import information that we need
                    tr_list = soup.find("table", class_="Scorecard").findChildren("tr", recursive=False)

                    FIRST_BATTING = tr_list[0].contents[1].text[24:-22]
                    SECOND_BATTING = tr_list[19].contents[1].text[24:-36]

                    batter_list = []

                    # now we can get the batting stats of the player using this information
                    if FIRST_BATTING == PLAYER_TEAM:
                        # player's batting comes in the first innings
                        for i in range(1, 12):
                            batter_list.append( str(tr_list[i].contents[1].contents[1].get('href')[-4:]) )
                        
                        # finding the batting position of the player
                        batting_position = batter_list.index(self.ID) + 1

                        # now we can get the other information of the batter
                        # => 4's, 6's, percent runs of total
                        num_4 = tr_list[batting_position].contents[9].text[25:-22]
                        num_6 = tr_list[batting_position].contents[11].text[25:-22]
                        percent_runs = tr_list[batting_position].contents[15].text[3:-35]
                    else:
                        # player's batting comes in the second innings
                        for i in range(20, 30):
                            batter_list.append( str(tr_list[i].contents[1].contents[1].get('href')[-4:]) )
                        
                        # finding the batting position of the player
                        batting_position = batter_list.index(self.ID) + 1

                        # now we can get the other information of the batter
                        # => 4's, 6's, percent runs of total
                        num_4 = tr_list[19 + batting_position].contents[9].text[25:-22]
                        num_6 = tr_list[19 + batting_position].contents[11].text[25:-22]
                        percent_runs = tr_list[19 + batting_position].contents[15].text[3:-35]

                    # now we need to find if the player was the man of the match or not
                    try:
                        outer_table = soup.body.findChildren("table", recursive=False)[1].contents[1].contents[1]
                        match_information_table = outer_table.findChildren("table", recursive=False)[1].findChildren("table", recursive=False)[0]
                        required_tr = match_information_table.findChildren("tr", recursive=False)[6]
                        player_of_match = required_tr.contents[3].contents[1].get('href')[-4:]
                        
                        # checking if the player is the man of the match
                        if player_of_match == self.ID:
                            man_of_match = "YES"
                        else:
                            pass
                    except:
                        pass

                    print(f"---[ADDED INFO]---")

            except:
                print(f'...[ERROR]... Exception occured for {page} ...')

            BATTING_POSITION.append(batting_position)
            NUM_4.append(num_4)
            NUM_6.append(num_6)
            PERCENT_RUNS_OF_TOTAL.append(percent_runs)
            MAN_OF_MATCH.append(man_of_match)

        print(f"Number of pages working correctly => [{count_good_pages} / {total_pages}] => {(count_good_pages/total_pages)*100}")

        # now we can append the lists to the data frame and return it to the user
        odi_batting_extra_df["MATCH_CODE"] = pd.Series(MATCH_CODE)
        odi_batting_extra_df["BATTING_POSITION"] = pd.Series(BATTING_POSITION)
        odi_batting_extra_df["NUM_4"] = pd.Series(NUM_4)
        odi_batting_extra_df["NUM_6"] = pd.Series(NUM_6)
        odi_batting_extra_df["PERCENT_RUNS_OF_TOTAL"] = pd.Series(PERCENT_RUNS_OF_TOTAL)
        odi_batting_extra_df["MAN_OF_MATCH"] = pd.Series(MAN_OF_MATCH)

        return odi_batting_extra_df
        
    def GET_OdiPlayerMatchDetailsBowl(self, MATCH_CODE: list, PLAYER_TEAM: str) -> pd.DataFrame:
        """
            Method returns a data frame with some extra attributes about a player's
            bowling record for the given matches 
        """

        # first let us initialize some variables which we can use later in the program

        # data frame to be returned by the method later
        odi_bowling_extra_df = pd.DataFrame()

        # we need to populate these lists so that later they can be appended to the data frame
        MAIDEN_OVERS = []
        PERCENT_WICKETS_OF_ALL = []

        # we make a separate list of URL's to navigate to later and scrape the data
        PAGES = []
        for match_code in MATCH_CODE:
            OVERVIEW_PAGE = self.ROOT_MATCH_SCORECARD + self.ROOT_ODI_MATCH + str(match_code) + self.ROOT_ODI_MATCH_END
            PAGES.append(OVERVIEW_PAGE)

        # now we need to scrape each of the url and get the required information
        count_good_pages = 0
        total_pages = len(MATCH_CODE)

        for page in PAGES:
            maiden_overs = None
            percent_wickets = None
            
            try:
                # using custom function to get the data and parse it
                soup = self.UTIL_MakeSoup(page)

                # some match pages are not returning the complete data about the match
                # so we can only extract the information for some matches of the player
                num_rows_returned = len(soup.find("table", class_="Scorecard").findChildren("tr", recursive=False))

                if num_rows_returned != 38:
                    print("[ERROR] website not responding correctly")
                else:
                    count_good_pages = count_good_pages + 1

                    # this list contains all the import information that we need
                    tr_list = soup.find("table", class_="Scorecard").findChildren("tr", recursive=False)

                    # when we know who is the first batting side we can find the bowling sides as well
                    FIRST_BOWLING = tr_list[19].contents[1].text[24:-36]

                    bowler_list = []
                    inner_list = []

                    if FIRST_BOWLING == PLAYER_TEAM:
                        # player bowls in the first innings
                        required_table = tr_list[17]
                        inner_list = required_table.contents[1].find("table").findChildren("tr", recursive=False)

                    else:
                        # player bowls in the second innings
                        required_table = tr_list[36]
                        inner_list = required_table.contents[1].find("table").findChildren("tr", recursive=False)    

                    inner_list = inner_list[1:]


                    for tr in inner_list:
                        bowler_list.append( tr.contents[1].contents[1].get('href')[-4:] )

                    required_tr = inner_list[ bowler_list.index(self.ID) ]

                    maiden_overs = required_tr.contents[5].text[30:-28]
                    percent_wickets = required_tr.contents[13].text[3:-30]

                    print(f"...[LOG]... added info ... ")
            except:
                print(f"Exception occured for page : {page}")
            
            # now we can append the information to the list    
            MAIDEN_OVERS.append(maiden_overs)
            PERCENT_WICKETS_OF_ALL.append(percent_wickets)


        print(f"Number of pages working correctly => [{count_good_pages} / {total_pages}] => {(count_good_pages/total_pages)*100}")
        
        # now we can add the lists to the data frame and return to the user
        odi_bowling_extra_df["MATCH_CODE"] = pd.Series(MATCH_CODE)
        odi_bowling_extra_df["MAIDEN_OVERS"] = pd.Series(MAIDEN_OVERS)
        odi_bowling_extra_df["PERCENT_WICKETS_OF_ALL"] = pd.Series(PERCENT_WICKETS_OF_ALL)

        return odi_bowling_extra_df

    def GET_OdiBatPerformance(self) -> pd.DataFrame:
        """
            method which returns a data frame containing the ODI Batting performance of the player.

            If there is some error to get the data, None type is returned
        """
        # making an empty data frame to return
        player_bat_df = pd.DataFrame()

        try:
            # making a request to the appropriate endpoint to get the player's ODI batting statistics
            r_bat = requests.get(self.ROOT_URL + self.ROOT_ODI_BAT + self.ID)

            # using bs4 to parse the html response from the website
            soup_bat = BeautifulSoup(r_bat.content, "html.parser")

            # first let us populate the BATTING CARD
            required_table = soup_bat.find_all("table", class_="TableLined")[0]
            
            # extracting the rows that have information from the table into a list
            all_rows = required_table.find_all("tr")
            all_rows = all_rows[3:len(all_rows)-1]

            # empty lists which will represent one attribute each in the batting card
            MATCH_NUMBER = []
            INNING_NUMBER = []
            MATCH_DATE = []
            MATCH_CODE = []
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
                scorecard_link = self.ROOT_MATCH_SCORECARD + one_row[5].contents[1].get('href')[3:]
                MATCH_CODE.append(scorecard_link[-4:])
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
            player_bat_df['MATCH_CODE'] = MATCH_CODE
            player_bat_df['MATCH_INNING'] = MATCH_INNING
            player_bat_df['OPPONENT'] = OPPONENT
            player_bat_df['VENUE'] = VENUE
            player_bat_df['DISMISSAL'] = DISMISSAL
            player_bat_df['RUNS_SCORED'] = RUNS_SCORED
            player_bat_df['BALLS_FACED'] = BALLS_FACED

            return player_bat_df

        except Exception as error:
            print(f"[ERROR] => ODI Batting Performance Page not responding for PlayerID={self.ID}\n[EXCEPTION RAISED] {error}")
            # exception occurs so we have to return None
            return None

    def GET_OdiBowlPerformance(self) -> pd.DataFrame:
        """
            method which returns a data frame containing the ODI Bowling performance of the player
        """
        player_bowl_df = pd.DataFrame()

        try:
            r_bowl = requests.get(self.ROOT_URL + self.ROOT_ODI_BOWL + self.ID)

            soup_bowl = BeautifulSoup(r_bowl.content, "html.parser")

            # note that it is possible that a player may not have a bowling record
            # this means he is a pure batsman
            try:
                required_table = soup_bowl.find_all("table", class_="TableLined")[0]
            
                # extracting the rows that have information from the table into a list
                all_rows = required_table.find_all("tr")
                all_rows = all_rows[3:len(all_rows)]

                # empty lists that will represent single attributes in the bowling card of the player
                MATCH_NUMBER = []
                MATCH_CODE = []
                MATCH_INNING = []
                OPPONENT = []
                VENUE = []
                OVERS = []
                WICKETS_RUNS = []

                for row in all_rows:
                    # each row is a <tr> which contains the list of <td> that have the information
                    one_row = row.contents

                    try:
                        scorecard_link = self.ROOT_MATCH_SCORECARD + one_row[3].contents[1].get('href')[3:]
                        MATCH_CODE.append(scorecard_link[-4:])
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
                player_bowl_df['MATCH_CODE'] = pd.Series(MATCH_CODE)
                player_bowl_df['MATCH_INNING'] = pd.Series(MATCH_INNING)
                player_bowl_df['OPPONENT'] = pd.Series(OPPONENT)
                player_bowl_df['VENUE'] = pd.Series(VENUE)
                player_bowl_df['OVERS'] = pd.Series(OVERS)
                player_bowl_df['WICKETS_RUNS'] = pd.Series(WICKETS_RUNS)

                # return the bowling data frame if everything goes right
                return player_bowl_df

            except Exception as error:
                print(f"---[NO ODI BOWLING RECORD FOUND] for player {self.NAME} ({self.ID})")
                return None



        except Exception as error:
            print(f"[ERROR] => ODI Bowling Performance Page not responding for PlayerID={self.ID}\n[EXCEPTION RAISED] {error}")
            return None

    def GET_T20BatPerformance(self) -> pd.DataFrame:
        """
            method which returns a data frame containing the T20 Batting performance of the player
        """

        # making an empty data frame to return
        player_bat_df = pd.DataFrame()

        try:
            # making a request to the appropriate endpoint to get the player's ODI batting statistics
            r_bat = requests.get(self.ROOT_URL + self.ROOT_T20_BAT + self.ID)

            # using bs4 to parse the html response from the website
            soup_bat = BeautifulSoup(r_bat.content, "html.parser")

            # first let us populate the BATTING CARD
            required_table = soup_bat.find_all("table", class_="TableLined")[0]
            
            # extracting the rows that have information from the table into a list
            all_rows = required_table.find_all("tr")
            all_rows = all_rows[3:len(all_rows)-1]

            # empty lists which will represent one attribute each in the batting card
            MATCH_NUMBER = []
            INNING_NUMBER = []
            MATCH_DATE = []
            MATCH_CODE = []
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
                scorecard_link = self.ROOT_MATCH_SCORECARD + one_row[5].contents[1].get('href')[3:]
                MATCH_CODE.append(scorecard_link[-4:])
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
            player_bat_df['MATCH_CODE'] = MATCH_CODE
            player_bat_df['MATCH_INNING'] = MATCH_INNING
            player_bat_df['OPPONENT'] = OPPONENT
            player_bat_df['VENUE'] = VENUE
            player_bat_df['DISMISSAL'] = DISMISSAL
            player_bat_df['RUNS_SCORED'] = RUNS_SCORED
            player_bat_df['BALLS_FACED'] = BALLS_FACED

            return player_bat_df

        except Exception as error:
            print(f"[ERROR] => T20 Batting Performance Page not responding for PlayerID={self.ID}\n[EXCEPTION RAISED] {error}")
            # exception occurs so we have to return None
            return None

    def GET_T20BowlPerformance(self) -> pd.DataFrame:
        """
            method which returns a data frame containing the T20 Bowling performance of the player
        """

        player_bowl_df = pd.DataFrame()

        try:
            r_bowl = requests.get(self.ROOT_URL + self.ROOT_T20_BOWL + self.ID)

            soup_bowl = BeautifulSoup(r_bowl.content, "html.parser")

            # note that it is possible that a player may not have a bowling record
            # this means he is a pure batsman
            try:
                required_table = soup_bowl.find_all("table", class_="TableLined")[0]
            
                # extracting the rows that have information from the table into a list
                all_rows = required_table.find_all("tr")
                all_rows = all_rows[3:len(all_rows)]

                # empty lists that will represent single attributes in the bowling card of the player
                MATCH_NUMBER = []
                MATCH_CODE = []
                MATCH_INNING = []
                OPPONENT = []
                VENUE = []
                OVERS = []
                WICKETS_RUNS = []

                for row in all_rows:
                    # each row is a <tr> which contains the list of <td> that have the information
                    one_row = row.contents

                    try:
                        scorecard_link = self.ROOT_MATCH_SCORECARD + one_row[3].contents[1].get('href')[3:]
                        MATCH_CODE.append(scorecard_link[-4:])
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
                player_bowl_df['MATCH_CODE'] = pd.Series(MATCH_CODE)
                player_bowl_df['MATCH_INNING'] = pd.Series(MATCH_INNING)
                player_bowl_df['OPPONENT'] = pd.Series(OPPONENT)
                player_bowl_df['VENUE'] = pd.Series(VENUE)
                player_bowl_df['OVERS'] = pd.Series(OVERS)
                player_bowl_df['WICKETS_RUNS'] = pd.Series(WICKETS_RUNS)

                # return the bowling data frame if everything goes right
                return player_bowl_df

            except Exception as error:
                print(f"---[NO T20 BOWLING RECORD FOUND] for player {self.NAME} ({self.ID})")
                return None



        except Exception as error:
            print(f"[ERROR] => T20 Bowling Performance Page not responding for PlayerID={self.ID}\n[EXCEPTION RAISED] {error}")
            return None


