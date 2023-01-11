import pandas as pd
import numpy as np
import sklearn
import matplotlib
import matplotlib.pylab as plt
import missingno as msno
import plotly.io as pio
from sklearn import datasets, svm
from sklearn.model_selection import train_test_split #split data
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier 
from joblib import dump, load
import pickle
import time


class TrainTestModel:
    def __init__(self, single = False):
        pio.renderers.default = "vscode" #set default renderer to 'notebook' or 'vscode'
        self.season_start = 2010
        self.season_end = 2022
        season = range(self.season_start, self.season_end) 
        league = ["premier_league","2_liga", "bundesliga", "championship", "eerste_divisie", "ligue_1", "ligue_2", "eredivisie",
                "primeira_liga", "primera_division", "segunda_division", "segunda_liga", "serie_a", "serie_b"]
        
        #allow user to select league without manually changing file path
        try: #load football dataset
            pd.set_option('display.max_rows', None) #display all rows in table
            if single == True:
                self.league = input(f"Select league: {league}").replace(" ", "_").lower()
                for i in season:
                    if self.league in league:
                        self.file = f"cleaned_datasets/{self.league}/cleaned_dataset_{self.league}.csv"
                        self.x = pd.read_csv(self.file)
                    else:
                        print("Select league from list to load file")
                
            else:
                self.file = f"cleaned_datasets/cleaned_dataset_{self.season_start}-{self.season_end}.csv"
                self.x = pd.read_csv(self.file)

            #rename index column to Match_Number and apply to DataFrames
            self.x = self.x.rename({"Unnamed: 0": "Match_Number"}, axis= 'columns') 

            #self.x.head() #display 5 rows of dataset
        except:
            f"{self.file} failed to load"
        
        self.values = [key for key in self.x] #use to print current values in DataFrame
        self.drop_values = []
        
        return None

    def display_data(self): #display dataset
        return self.x 
    
    def describe_dataset(self): #generate descriptive statistics
        return self.x.describe()
    
    def display_data_types(self):
        return self.x.info() #return columns and value data types

    def display_unique_rows(self):
        return self.x.value_counts() #return a Series containing counts of unique rows in Dataframe

    def check_null_values(self):
        return self.x.isnull().sum() #check for null values in each column
    
    def check_missing_data(self):
        return msno.matrix(self.x) #check for columns with missing data

    def get_missing_value_sum(self):
        return self.x.isna().sum() #check for sum of any missing values in Series
    
    def calculate_sum(self):
        return self.x.sum() #calculate sum of values in each column
    
    def display_dataframe_shape(self):
        #Return a tuple representing the dimensionality of the DataFrame
        return self.x.shape
    
    ## Split & Join Values to DataFrame ##
    def split_away_points(self):
        #present linear relationship of away_points
        self.away_points = pd.get_dummies(self.x["Away_Points"], prefix="Away_Points") 
            #add drop_first = True to get rid of first column in modified DataFrame
        return self.away_points

    def split_home_points(self):
        #present linear relationship of home_points
        self.home_points = pd.get_dummies(self.x["Home_Points"], prefix="Home_Points") 
            #add drop_first = True to get rid of first column in modified DataFrame
        return self.home_points
    
    def join_points(self):
        self.x = self.x.join(self.away_points).join(self.home_points)
        return self.x
    
    def split_away_match_outcome(self):
        self.away_match_outcome = pd.get_dummies(self.x["Away_Match_Outcome"], prefix="Away_Match_Outcome") 
            #add drop_first = True to get rid of first column in modified DataFrame
        return self.away_match_outcome
    
    def split_home_match_outcome(self):
        self.home_match_outcome = pd.get_dummies(self.x["Home_Match_Outcome"], prefix="Home_Match_Outcome") #add drop_first = True to get rid of first column in modified DataFrame
        return self.home_match_outcome
    
    def join_outcomes(self):
        self.x = self.x.join(self.away_match_outcome).join(self.home_match_outcome)
        return self.x
    
    def split_away_goals(self):
        self.away_goals = pd.get_dummies(self.x["Away_Goals"], prefix="Away_Goals") 
            #add drop_first = True to get rid of first column in modified DataFrame
        return self.away_goals
    
    def split_home_goals(self):
        self.home_goals = pd.get_dummies(self.x["Home_Goals"], prefix="Home_Goals") 
            #add drop_first = True to get rid of first column in modified DataFrame
        return self.home_goals
    
    def join_goals(self):
        self.x = self.x.join(self.away_goals).join(self.home_goals)
        return self.x

    ## Drop Values ##
    def drop_away_match_outcome(self):
        self.x = self.x.drop(["Away_Match_Outcome"], axis= 1)
        self.drop_values.append("Away_Match_Outcome")
        return f"Dropped Away_Match_Outcome. Remaining values: {self.values}"
    
    def drop_home_match_outcome(self):
        self.x = self.x.drop(["Home_Match_Outcome"], axis= 1)
        self.drop_values.append("Home_Match_Outcome")
        return f"Dropped Home_Match_Outcome. Remaining values: {self.values}"
    
    def drop_away_goals(self):
        self.x = self.x.drop(["Away_Goals"], axis = 1)
        self.drop_values.append("Away_Goals")
        return f"Dropped Away_Goals. Remaining values: {self.values}"
    
    def drop_home_goals(self):
        self.x = self.x.drop(["Home_Goals"], axis = 1)
        self.drop_values.append("Home_Goals")
        return f"Dropped Home_Goals. Remaining values: {self.values}"
    
    def drop_goals_so_far(self):
        self.x = self.x.drop(["Total_Home_Goals_So_Far", "Total_Away_Goals_So_Far"], axis= 1)
        self.drop_values.append("Total_Home_Goals_So_Far", "Total_Away_Goals_So_Far")
        return f"Dropped Away_Goals_So_Far and Home_Goals_So_Far. Remaining values: {self.values}"
    
    def drop_away_points(self):
        self.x = self.x.drop(["Away_Points"], axis= 1)
        self.drop_values.append("Away_Points")
        return f"Dropped Away_Points. Remaining values: {self.values}"
    
    def drop_home_points(self):
        self.x = self.x.drop(["Home_Points"], axis= 1)
        self.drop_values.append("Home_Points")
        return f"Dropped Home_Points. Remaining values: {self.values}"

    def drop_cumulative_points(self):
        self.x = self.x.drop(["Cumulative_Home_Points", "Cumulative_Away_Points"], axis= 1)
        self.drop_values.append("Cumulative_Home_Points")
        self.drop_values.append("Cumulative_Away_Points")
        return f"Dropped Cumulative_Away_Points and Cumulative_Home_Points. Remaining values: {self.values}"
    
    def drop_points_so_far(self):
        self.x = self.x.drop(["Total_Home_Points_So_Far", "Total_Away_Points_So_Far"], axis= 1)
        self.drop_values.append("Total_Home_Points_So_Far")
        self.drop_values.append("Total_Away_Points_So_Far")
        return f"Dropped Total_Away_Points_So_Far and Total_Home_Points_So_Far. Remaining values: {self.values}"
    
    def drop_match_number(self):
        self.x = self.x.drop(["Match_Number"], axis= 1)
        self.drop_values.append("Match_Number")
        return f"Dropped Match_Number. Remaining values: {self.values}"
    
    def drop_rounds(self):
        self.x = self.x.drop(["Round"], axis= 1)
        self.drop_values.append("Round")
        return f"Dropped Round. Remaining values: {self.values}"
    
    def show_dropped_values(self):
        return "Dropped values: ", self.drop_values

    ## Train & Test Model ##
    def train_test_model(self):
        start = True
        while start:
            select_values_to_drop = input(f"Select values to drop: {self.values}. Type 'stop' to train and test model: ").lower().title().replace(" ", "_")
            if select_values_to_drop in self.values:
                self.x = self.x.drop([select_values_to_drop], axis= 1)
                self.values.remove(select_values_to_drop)
                self.drop_values.append(select_values_to_drop)
            elif select_values_to_drop not in self.values and select_values_to_drop != "Stop":
                print("Please select a value to drop") 
            else:
                if select_values_to_drop == "Stop":
                    start = False
                    if "Home_Match_Outcome" in self.values:
                        self.X = self.x.drop(["Home_Match_Outcome"], axis=1) 
                        self.y = self.x["Home_Match_Outcome"] #variable to be predicted
                        print("Home_Match_Outcome used")
                    else:
                        self.X = self.x.drop(["Away_Match_Outcome"], axis=1) 
                        self.y = self.x["Away_Match_Outcome"] #variable to be predicted
                        print("Away_Match_Outcome used")
                    time.sleep(1.5)
                    self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42) #add data, features and labels
                    self.ss = StandardScaler()
                    self.X_train = self.ss.fit_transform(self.X_train)
                    self.X_test = self.ss.transform(self.X_test)
                    time.sleep(1.5)
                    self.select_model = input("Select lr or rf to test model: ").lower()

                    #Logistic Regression
                    if self.select_model == "lr":
                        #only add features which will not leak any information, such as points for both teams at the end of each match 
                        self.lr = LogisticRegression()
                        self.lr.fit(self.X_train, self.y_train)  #fit model according to given training data
                        self.y_pred = self.lr.predict(self.X_test) #predict class labels for samples in X

                    #Random Forest Classifier
                    elif self.select_model == "rf":
                        self.rf = RandomForestClassifier(n_estimators = 30, random_state = 42)
                        self.rf.fit(self.X_train, self.y_train)
                        self.y_pred = self.rf.predict(self.X_test) #predict class labels for samples in X
                    else:
                        "Please select either lr or rf to test model"
                    return f"Model tested using {self.select_model} - accuracy %: {accuracy_score(self.y_test, self.y_pred)}", f"Values used: {self.values}" #%print accuracy %
                break
    

    ## Save Model ## 
    def save_to_csv(self, single = True):
        round = self.x["Round"]
        X_submission = self.x.drop(["Round"], axis=1)
        X_scale_sub = self.ss.transform(X_submission)
        y_submission = self.rf.predict(X_scale_sub) #lr = LogisticRegression #rf = RandomForestClassifier
        my_dict = {"Round": round, "Home_Match_Outcome": y_submission}
        if single == True:
            submission = pd.DataFrame(my_dict).to_csv(f"submission_{self.league}.csv", index=False) #load dictionary in DataFrame and save to csv
        else:
            submission = pd.DataFrame(my_dict).to_csv("full_dataset_submission.csv", index=False) #load dictionary in DataFrame and save to csv
        return "Model saved to csv"
    
    def save_baseline_pickle(self):
        ##SAVE MODEL USING PICKLE##
        self.clf = svm.SVC()
        self.X, self.y= datasets.load_iris(return_X_y=True)
        self.clf.fit(self.X, self.y)
        #SVC()

        s = pickle.dumps(self.clf)
        clf2 = pickle.loads(s)
        clf2.predict(self.X[0:1])
        dump(self.clf, f'baseline_{self.select_model}.joblib') 
        return "Baseline saved using Pickle"

    def save_model_pickle(self):
        ##SAVE MODEL USING PICKLE##
        self.clf = svm.SVC()
        self.X, self.y= datasets.load_iris(return_X_y=True)
        self.clf.fit(self.X, self.y)
        #SVC()

        s = pickle.dumps(self.clf)
        clf2 = pickle.loads(s)
        clf2.predict(self.X[0:1])

        dump(self.clf, f'model_{self.select_model}.joblib') 
        return "Model saved using Pickle"
    
    def load_pickle_baseline(self):
        #load pickled model
        self.clf = load(f'baseline.joblib') 
        return self.clf
    
    def load_pickle_model(self):
        #load pickled model
        self.clf = load('model.joblib') 
        return self.clf


if __name__ == "__main__": #will only run methods below if script is run directly
    model = TrainTestModel()