# Importing the required libraries
import requests
from bs4 import BeautifulSoup

import pandas as pd

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

    # the following parts help create the correct URL for some aspect related to the player
    ROOT_MATCH_SCORECARD = 'http://www.howstat.com/cricket/Statistics/'
    
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
    
    def GET_Overview(self) -> tuple:
        """
            method to get the overview page of the player to extract useful information about the player

            returned tuple => (player_fullname, batting_hand, bowling_style)
        """

        # first we need to create the correct URL to go to the overview page
        OVERVIEW_PAGE = self.ROOT_URL + self.ROOT_PLAYER_OVERVIEW + f'{self.ID}'

        # now we need to make a get request to the required page
        try:
            r_overview = requests.get(OVERVIEW_PAGE)

            # using bs4 to parse the recieved html content from the overview page of the player
            soup = BeautifulSoup(r_overview.content,"html.parser")

            required_table = soup.find_all("table")[0].find_all('table')[0].find_all('table')[0]

            # variables to store the information recieved for the player
            player_name = required_table.find_all('tr')[2].find_all('td')[1].text[11:-11]
            batting_hand = required_table.find_all('tr')[5].find_all('td')[1].text[11:-10]
            bowl_style = required_table.find_all('tr')[6].find_all('td')[1].text[11:-10]

            # returning all the information bundled in a single tuple
            return (player_name, batting_hand, bowl_style)
            
        except Exception as error:
            # if overview page is not received, the function terminates and nothing is done
            return f"[ERROR] => Overview Page not responding for PlayerID={self.ID}\n[EXCEPTION RAISED] {error}"
        
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
                MATCH_CARD_LINK.append(self.ROOT_MATCH_SCORECARD + one_row[5].contents[1].get('href')[3:])
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
                        MATCH_CARD_LINK.append(self.ROOT_MATCH_SCORECARD + one_row[3].contents[1].get('href')[3:])
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
                MATCH_CARD_LINK.append(self.ROOT_MATCH_SCORECARD + one_row[5].contents[1].get('href')[3:])
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
                        MATCH_CARD_LINK.append(self.ROOT_MATCH_SCORECARD + one_row[3].contents[1].get('href')[3:])
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

                # return the bowling data frame if everything goes right
                return player_bowl_df

            except Exception as error:
                print(f"---[NO T20 BOWLING RECORD FOUND] for player {self.NAME} ({self.ID})")
                return None



        except Exception as error:
            print(f"[ERROR] => T20 Bowling Performance Page not responding for PlayerID={self.ID}\n[EXCEPTION RAISED] {error}")
            return None


