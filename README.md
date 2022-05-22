# Football-Match-Outcome-Prediction

Milestone 1

This milestone required downloading Football Match Data from various leagues for the 1990 to 2021 seasons.
The data was subsequently manipulated by assigning points to teams depending on their match outcome for example and whether they were playing Home or Away, which required splitting the match results and then adding if statements to determine whether the game ended in a win, loss or draw.

	home_goal = []
        away_goal = []
        home_match_outcome = []
        away_match_outcome = []
        home_points = []
        away_points = []
            
        split_result = data["Result"].str.split("-") #split results at '-' to separate numbers

        for res in split_result:
            #print("Home goals: ", res[0][0])    
            home_goal.append(int(res[0][0])) #convert to int to add goals together -- default type is str
            #print("Away goals: ", res[1][0])
            away_goal.append(int(res[1][0]))
                
            #Determine match outcomes
            #Win
            if int(res[0][0]) > int(res[1][0]):
                home_match_outcome.append("Win")
                home_points.append(3) #3 points for a win 

                away_match_outcome.append("Loss")   
                away_points.append(0)           
            #Draw
            elif int(res[0][0]) == int(res[1][0]):
                home_match_outcome.append("Draw")
                home_points.append(1) #1 point for a draw

                away_match_outcome.append("Draw")  
                away_points.append(1)   
            #Loss    
            else:
                home_match_outcome.append("Loss")
                home_points.append(0) #0 points for a loss

                away_match_outcome.append("Win")  
                away_points.append(3)  
								
Although different methods were being used to manipulate and analyse the data, it was much more practical to move these into a class where they could be called as and when needed, rather than creating separate scripts and calling all the methods (or commenting out those which were not being used) which would be using a lot of disk memory. For a more streamlined user experience, a condition was added so that a user could select a league and season if wanting to review match/league data only, or also select a team from that league in order to review team info. Any functions added to the class were named according to the method(s) they contained.

	def __init__(self, match = True):
        #allow user to select league and year without manually changing file path
        
        try:
            self.league = input("Select league: ").replace(" ", "_").lower()
            if match == True:    
                self.year = input("Select year: ")
                self.league_ = self.league
                #dataframes
                pd.set_option('display.max_rows', None) #display all rows in table
                self.file = f"Football-Dataset/{self.league}/Results_{self.year}_{self.league_}.csv"
                self.x = pd.read_csv(self.file)

            #self.x.head() #display 5 rows of dataset
        except:
            "File failed to load"

        try:
            if match == True:
                self.team_info = pd.read_csv("Team_Info.csv")
            else:
                self.team = input(f"Select team from {self.league}").lower().title()
                self.team_info = pd.read_csv("Team_Info.csv")
        except:
            "Team_Info failed to load"

        try:
            if match == True:
                self.match_info = pd.read_csv("Match_Info.csv")
            else:
                self.year = input("Select year: ")
                self.team = input(f"Select team from {self.league}").lower().title()
                self.match_info = pd.read_csv("Match_Info.csv")
        except:
            "Match_Info failed to load"

This is yet to be done for analysing additional match data (including the date, referee and number of yellow or red cards handed out) as the current input methods are not sufficient to filter the data to show the chosen team and season.

Once the above were complete, some hypotheses were added to a report based on any relationships and/or trends found, and predict what features will be more important for predicting the outcome of the match.

This milestone was relatively straightforward, but the difficulty depended on the amount of knowledge for pandas and matplotlib in order to manipulate and analyse the match data as needed. But when this obstacle was overcome, it was quite rewarding to see how data could be analysed and utilised to record any trends and relationships found.
