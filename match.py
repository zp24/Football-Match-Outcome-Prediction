import pandas as pd
import numpy as np
import seaborn as sns
import scipy.stats as ss
import matplotlib.pylab as plt
import json
from json import JSONEncoder
import csv
import plotly.express as px
import plotly.io as pio

class match_outcome_data:

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

        #display graphs
        pio.renderers.default = "notebook" #set default renderer to 'notebook' or 'vscode'
        return None

    def display_data(self):
        return self.x #display dataset
    
    def get_data_types(self):
        return self.x.dtypes #print data types

    def get_teams(self): #confirm number of teams in league and list of teams
        self.x["Home_Team"][self.x["Home_Team"]!= "Away Team"].unique()
        return f'Number of teams in {self.league}: {len(set(self.x["Home_Team"]))}', set(self.x["Home_Team"])

    def find_team(self, text): 
        return self.x[self.x["Home_Team"].str.contains(text.lower().title())] #display data of specified team using "text"

    def get_team_info(self):
        return self.team_info[self.team_info["Team"].str.contains(f"{self.team}")] #display data for specified team
    
    def get_match_info(self):
        '''myList = [self.team.lower(), self.year]
        str = self.match_info["Link"]
        if any(x in str for x in myList):
            return str
        else:
            return "Did not work"'''
        return self.match_info[self.match_info["Link"].str.contains(f"{self.team}".lower(), f'{self.year}')] #display match info dataset
    
    def split_results(self): #split results
        result = self.x["Result"].astype("category")
        #set(result) #display results in a set

        result_df = pd.DataFrame(result, columns=["Result"])
        result_df["Count"] = result_df["Result"].map(self.x["Result"].value_counts()) #count frequency of each result
        return result_df #display results frequency

    def get_results(self): 
        #split results and add to lists
        home_goal = []
        away_goal = []
        home_match_outcome = []
        away_match_outcome = []
        home_points = []
        away_points = []
            
        split_result = self.x["Result"].str.split("-") #split results at '-' to separate numbers

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
            '''
            #determine match outcome without iterating and populate dataset
            self.x['Home_Win'] = (self.x['Home_Goals'] > self.x['Away_Goals']).astype(int)
            self.x['Home_Loss'] = (self.x['Home_Goals'] < self.x['Away_Goals']).astype(int)
            self.x['Draw'] = (self.x['Home_Goals'] == self.x['Away_Goals']).astype(int)
            '''
        
        #add lists to existing dataframe/set
        self.x["Home_Goals"] = home_goal
        self.x["Away_Goals"] = away_goal
        self.x["Home_Match_Outcome"] = home_match_outcome
        self.x["Home_Points"] = home_points
        self.x["Away_Match_Outcome"] = away_match_outcome
        self.x["Away_Points"] = away_points 
        
        return self.x #display modified dataset


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
    
    def get_total_team_goals(self):
        self.get_results()
        return self.x.groupby(["League","Season","Home_Team"]).agg({"Home_Goals" : ["sum"], "Away_Goals" : ["sum"]})
    
    '''
        def get_total_home_goals(self):
        self.get_results()
        return self.x.groupby(["Home_Team"]).agg({"Home_Goals" : ["sum"]})

        def get_total_away_goals(self):
        self.get_results()
        return self.x.groupby(["Away_Team"]).agg({"Away_Goals" : ["sum"]})'''
    
    def get_total_team_points(self):
        self.get_results()
        return self.x.groupby(["League","Season","Home_Team"]).agg({"Home_Points" : ["sum"], "Away_Points" : ["sum"]}) #show total points per Round per Home Team only

    '''def get_total_away_points(self):
        self.get_results()
        return self.x.groupby(["Away_Team"]).agg({"Away_Points" : ["sum"]}) #show total points per Round per Home Team only'''
    def get_team_stats(self):
        self.get_results()
        return self.x.groupby(["League", "Season", "Home_Team"]).agg({"Home_Match_Outcome": ["sum"], "Away_Match_Outcome": ["sum"]})
    
    def get_home_goal_stats(self):
        self.get_results()
        #calculate mean, sum and standard deviation of home goals
        grp = self.x.groupby('Home_Team')
        score_sum = []
        score_mean = []
        score_std = []
        #for gr in grp:
        score_mean.append(grp['Home_Goals'].agg(np.mean)) #calculate mean 
        score_sum.append(grp['Home_Goals'].agg(np.sum)) #calculate sum
        score_std.append(grp['Home_Goals'].agg(np.std)) #calculate standard deviation

        return 'sum: ',score_sum, 'mean: ', score_mean, 'standard deviation: ', score_std

    def get_away_goal_stats(self):
        self.get_results()
        #calculate mean, sum and standard deviation of away goals
        grp = self.x.groupby('Away_Team')
        self.score_sum = []
        score_mean = []
        score_std = []
        #for gr in grp:

        score_mean.append(grp['Away_Goals'].agg(np.mean)) #calculate mean 
        self.score_sum.append(grp['Away_Goals'].agg(np.sum)) #calculate sum
        score_std.append(grp['Away_Goals'].agg(np.std)) #calculate standard deviation
        return 'sum: ', self.score_sum, 'mean: ', score_mean, 'standard deviation: ', score_std

    ############ GRAPHS ############
    def show_res_freq(self):
        result = self.split_results()
        return px.histogram(result, "Result", labels={"value": "Result"}, title="Counts of League Match Results") #print all game results
    
    def check_home_res(self):
        self.get_results()

        result = self.x.sort_values(by=["Result"])

        fig = px.bar(result, "Result", 
                    color="Home_Team",
                    title="Counts of Overall Results Achieved by Home Team",
                    labels={ "Home_Team": "Home Team", "Result": "Result"},
                    height=1000, facet_col_wrap=4, 
                    facet_col_spacing=0.1
                    )

        fig.update_layout(showlegend=True, xaxis={'categoryorder':'total descending'})
        fig.update_yaxes(matches=None, showticklabels=True)

        return fig


    '''def get_test(self):
        self.get_results()
        #show number of individual scores for home teams in League
        fig = px.bar(self.score_sum, "Home_Match_Outcome", 
                    color="Home_Team",
                    title="Counts of Individual Score Frequency per Home Team",
                    labels={"Home_Team": "Home Team", "Home_Match_Outcome": "Home Match Outcome"},
                    height=2000, 
                    facet_col_wrap=2, 
                    facet_col_spacing=0.1)

        fig.update_layout(showlegend=True) #False to hide
        fig.update_xaxes(showticklabels=True, tickangle=45)
        fig.update_yaxes(matches=None, showticklabels=True)

        return fig'''

    def get_home_scores(self):
        self.get_results()
        #show number of individual scores for home teams in League
        fig = px.bar(self.x, "Home_Match_Outcome", 
                    color="Home_Team",
                    title="Counts of Individual Score Frequency per Home Team",
                    labels={"Home_Team": "Home Team", "Home_Match_Outcome": "Home Match Outcome"},
                    height=2000, 
                    facet_col_wrap=2, 
                    facet_col_spacing=0.1)

        fig.update_layout(showlegend=True) #False to hide
        fig.update_xaxes(showticklabels=True, tickangle=45)
        fig.update_yaxes(matches=None, showticklabels=True)

        return fig

    def get_away_scores(self):
        self.get_results()
        #show number of individual scores for away teams in League
        fig = px.bar(self.x, "Away_Match_Outcome", 
                    color="Away_Team",
                    title="Counts of Away Team Match Outcomes",
                    labels={"Away_Team": "Away Team", "Away_Match_Outcome": "Away Match Outcome"},
                    height=1000, 
                    facet_col_wrap=2, 
                    facet_col_spacing=0.1)

        fig.update_layout(showlegend=True, barmode="group") #False to hide legend, remove barmode to stack data
        fig.update_xaxes(showticklabels=True, tickangle=45)
        fig.update_yaxes(matches=None, showticklabels=True)
        return fig

    def get_away_goals(self):
        self.get_results()
        #show number of individual scores for each home team in League
        self.x.sort_values(by=["Away_Goals"])
        fig = px.pie(self.x, "Away_Goals",
                    color="Away_Goals",
                    title="Counts of Away Goals in League",
                    labels={"Away_Goals": "Away Goals", "Away_Team": "Away Team"},
                    height=500,  
                    )

        fig.update_layout(showlegend=True, legend_title_text='Number of Goals')
        fig.update_xaxes(showticklabels=True, tickangle=45)
        fig.update_yaxes(matches=None, showticklabels=True)
        
        return fig

if __name__ == "__main__": #will only run methods below if script is run directly
    m_data = match_outcome_data()