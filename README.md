# Football-Match-Outcome-Prediction

## Milestone 1

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

Once the above were complete, the data was analysed again to find any relationships and/or trends, and predict what features will be more important for predicting the outcome of the match. Based on the data provided:
- regardless of the number of matches played in the Premier League season for example, the percentage of Home wins will range between 40 and 45%.
- teams playing in the Premier League generally score more goals when playing at their Home stadium
- the most likely number of goals scored by the Home Team in a match is 1, with a 0.25% to 1.5% chance of a Home team scoring 4+ goals in a match

Whilst manipulating the data can help determine some elements such as the biggest contributor to total home points and a general overview of a team's performance throughout the league, the information found in the link provided for each match is more reliable to predict the outcome of a match.

This milestone was relatively straightforward, but the difficulty depended on the level of knowledge for pandas and matplotlib in order to manipulate and analyse the match data as needed. But when this obstacle was overcome, it was quite rewarding to see how data could be analysed and utilised to record any trends and relationships found.

## Milestone 2

This milestone concerned manipulating the data and extracting specific data from another file, the latter of which was added to a new dataframe so it could be viewed a lot better. 

try: #load ELO data
            self.elo_data = pickle.load(open('elo_dict.pkl', 'rb'))
        except:
            "ELO data failed to load"
	    
def get_elo(self):
        team_elo = []

        for key, value in self.elo_data.items():
            team = key.rsplit("/",4)
            team_elo.append({"Home_Team": team[2].replace("-", " ").title(), "Away_Team": team[3].replace("-", " ").title(), "Elo_Home": value["Elo_home"], 			"Elo_Away": value["Elo_away"] })
        elo_df = pd.DataFrame(team_elo)
        return elo_df
	
	
As for the former, this was pretty much done in Milestone 1 as a result of experimenting with the data to test the capabilities of Pandas and Matplotlib when trying to visualise the data in a graph as well as in a dataframe. This was also done to assist in analysing team performances in a league when each season of the Premier League had their own script for example, which were subsequently removed once a class script was used to save memory and time, although it did somewhat assist in the hypotheses set out above.

	def get_cumulative_data(self): 
		self.get_results()
		self.x["Total_Home_Goals_So_Far"] = self.x.groupby(["Home_Team"])["Home_Goals"].cumsum() #cumulative addition of goals for each home team
		self.x["Total_Away_Goals_So_Far"] = self.x.groupby(["Home_Team"])["Away_Goals"].cumsum() #cumulative addition of goals for each home team
		self.x["Cumulative_Home_Goals"] = self.x["Home_Goals"].cumsum() #cumulative addition of goals for each home team
		self.x["Cumulative_Away_Goals"] = self.x["Away_Goals"].cumsum() #cumulative addition of goals for each home team
		self.x["Total_Home_Points_So_Far"] = self.x.groupby(["Home_Team"])["Home_Points"].cumsum() #cumulative addition of points for each home team
		self.x["Total_Away_Points_So_Far"] = self.x.groupby(["Away_Team"])["Away_Points"].cumsum() #cumulative addition of points for each away team
		self.x["Cumulative_Home_Points"] = self.x["Home_Points"].cumsum() #cumulative sum of home points
		self.x["Cumulative_Away_Points"] = self.x["Away_Points"].cumsum() #cumulative sum of away points

        return self.x

A further method was added to the class to save certain data into a new csv file, including datasets which only included the total points or goals achieved or scored respectively by teams in a certain league and season, and a dataset which showed the cumulative points and goals scored home and away, either per team or wholly. However, the latter dataset could only contain numerical data, so any columns which did not were omitted from the dataset before it was saved as a csv.

	def save_to_csv(self): #save dataset as csv
		self.get_total_team_points()
		self.get_total_team_goals()
		cumulative_data = self.get_cumulative_data()
		data = cumulative_data.drop(["Home_Team", "Away_Team","Result", "Link", "League", "Season", "Home_Match_Outcome", "Away_Match_Outcome"],
				     axis = 1) #remove specified columns from dataframe
		team_points = self.x.groupby(["Home_Team"]).agg({"Home_Points" : ["sum"], "Away_Points" : ["sum"]})
		team_goals = self.x.groupby(["Home_Team"]).agg({"Home_Goals" : ["sum"], "Away_Goals" : ["sum"]})


		folder = rf"cleaned_datasets/{self.league}/{self.year}" #create folder for each league
		#rf"../Football-Match-Outcome-Prediction/cleaned_datasets/{self.league}/{self.year}" - achieves same as above
		if not os.path.exists(folder): #if folder doesn't already exist
		    os.makedirs(folder)
		    team_points.to_csv(f"{folder}/cleaned_dataset_{self.league}_{self.year}_points.csv", encoding='utf-8')
		    team_goals.to_csv(f"{folder}/cleaned_dataset_{self.league}_{self.year}_goals.csv", encoding='utf-8')
		    data.to_csv(f"{folder}/cleaned_dataset_{self.league}_{self.year}.csv", encoding='utf-8') #add index = False to remove index
		elif os.path.exists(folder):
		    #if folder already exists
			team_points.to_csv(f"{folder}/cleaned_dataset_{self.league}_{self.year}_points.csv", encoding='utf-8')
			team_goals.to_csv(f"{folder}/cleaned_dataset_{self.league}_{self.year}_goals.csv", encoding='utf-8')
			data.to_csv(f"{folder}/cleaned_dataset_{self.league}_{self.year}.csv", encoding='utf-8')
        
        return "datasets saved to csv" 
![image](https://user-images.githubusercontent.com/58480783/170560306-45d5811f-08e9-4b37-a868-87b62d7ef041.png)

This milestone was relatively straightforward given some of the objectives were already achieved in the previous milestone; all that was outstanding was extracting the ELO of each team from the pkl file and later saving the new datasets containing the cumulative goals and scores into a csv file. This of course required some of the knowledge gained from developing a webscraper package and some general knowledge of dictionaries.
