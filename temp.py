from tqdm import tqdm
import glob
import numpy as np
import pandas as pd
import os
import pickle
#%%
filename = 'elo_dict.pkl'
with open(filename, 'rb') as f:
    match_dict = pickle.load(f)
​
​
UMLAUTS = {'Ã€': 'À', 'Ã‚': 'Â', 'Ã„': 'Ä',
           'Ã…': 'Å', 'Ã†': 'Æ', 'Ã‡': 'Ç', 'Ãˆ': 'È', 'Ã‰': 'É',
           'ÃŠ': 'Ê', 'Ã‹': 'Ë', 'ÃŒ': 'Ì', 'ÃŽ': 'Î',
           'Ã‘': 'Ñ', 'Ã’': 'Ò', 'Ã“': 'Ó',
           'Ã”': 'Ô', 'Ã•': 'Õ', 'Ã–': 'Ö', 'Ã—': '×', 'Ã˜': 'Ø',
           'Ã™': 'Ù', 'Ãš': 'Ú', 'Ã›': 'Û', 'Ãœ': 'Ü',
           'Ãž': 'Þ', 'ÃŸ': 'ß', 'Ã ': 'à', 'Ã¡': 'á', 'Ã¢': 'â',
           'Ã£': 'ã', 'Ã¤': 'ä', 'Ã¥': 'å', 'Ã¦': 'æ', 'Ã§': 'ç',
           'Ã¨': 'è', 'Ã©': 'é', 'Ãª': 'ê', 'Ã«': 'ë', 'Ã¬': 'ì',
           'Ã®': 'î', 'Ã¯': 'ï', 'Ã°': 'ð', 'Ã±': 'ñ',
           'Ã²': 'ò', 'Ã³': 'ó', 'Ã´': 'ô', 'Ãµ': 'õ', 'Ã¶': 'ö',
           'Ã·': '÷', 'Ã¸': 'ø', 'Ã¹': 'ù', 'Ãº': 'ú', 'Ã»': 'û',
           'Ã¼': 'ü', 'Ã½': 'ý', 'Ã¾': 'þ', 'Ã¿': 'ÿ'}
#%%
def clean_result(x):
    '''
    In some cases, the result will have special characters. By now, let's just remove them
    '''
    if (':' in x) or ('(' in x):
        return None
    return x
​
def get_result(x):
    '''
    Returns the label, the goals for the home team, the
    the goals for the away team
    Parameters
    ----------
    x: str
        Result of the match in the form of X-X
    Returns
    -------
    int:
        Label of the match with 0 being win for the home
        team, 1 being draw, and 2 being lose for the home
        team
    int:
        Number of goals for of the home team
    int:
        Number of goals for of the away team
    '''
    if x is None:
        return None, None, None
    result = x.split('-')
    if len(x) == 3:
        if result[0] > result[1]:
            return 0, int(result[0]), int(result[1])
        elif result[0] == result[1]:
            return 1, int(result[0]), int(result[1])
        else:
            return 2, int(result[0]), int(result[1])
    else:
        return None, None, None
​
​
​
def clean_names(x):
    if any(map(x.__contains__, UMLAUTS.keys())):
        for word, initial in UMLAUTS.items():
            x = x.replace(word, initial)
    return x
​
def get_standings(df):
    # We need to clean the names
    df.loc[:, 'Home_Team'] = df['Home_Team'].map(clean_names)
    df.loc[:, 'Away_Team'] = df['Away_Team'].map(clean_names)
    teams = list(set(df['Home_Team'].unique())
                 | set(df['Away_Team'].unique()))
    df['Number_Teams'] = len(teams)
    n_rounds = df['Round'].max()
    df['Total_Rounds'] = n_rounds
    # Get the result, the goals for and the goals against
    df['Result'] = df['Result'].map(clean_result)
    df['Label'], df['Goals_For_Home'], df['Goals_For_Away'] = \
        zip(*df['Result'].map(get_result))
    df = df[df['Label'].notna()]
​
    print(f'Getting info about \tSeason: {df.loc[0]["Season"]}'
          + f'\n\t\t\tLeague: {df.loc[0]["League"]}')
    # Create a dataframe to accumulates the results during the season
    # throughout the rounds
    list_standings = ['Team', 'Position', 'Points', 'Win',
                      'Draw', 'Lose', 'Win_Home', 'Win_Away',
                      'Draw_Home', 'Draw_Away', 'Lose_Home',
                      'Lose_Away', 'Goals_For', 'Goals_For_When_Home',
                      'Goals_For_When_Away', 'Goals_Against',
                      'Goals_Against_When_Home',
                      'Goals_Against_When_Away',
                      'Streak', 'Streak_When_Home', 'Streak_When_Away']
    dict_standings = {x: [] for x in list_standings}
    df_standings = pd.DataFrame(dict_standings)
    df_standings['Team'] = teams
    df_standings.iloc[:, 1:-3] = 0
    df_standings.iloc[:, -3:] = ''
​
    # Add new columns that can potentially increase the performan5ce of
    # a model
    new_cols = ['Position_Home', 'Points_Home', 'Total_Wins_Home',
                'Total_Draw_Home', 'Total_Lose_Home',
                'Total_Goals_For_Home_Team',
                'Total_Goals_Against_Home_Team', 'Total_Streak_Home',
                'Wins_When_Home', 'Draw_When_Home', 'Lose_When_Home',
                'Goals_For_When_Home', 'Goals_Against_When_Home',
                'Position_Away', 'Points_Away', 'Total_Wins_Away',
                'Total_Draw_Away', 'Total_Lose_Away',
                'Total_Goals_For_Away_Team',
                'Total_Goals_Against_Away_Team', 'Total_Streak_Away',
                'Wins_When_Away', 'Draw_When_Away', 'Lose_When_Away',
                'Goals_For_When_Away', 'Goals_Against_When_Away',
                'Streak_When_Home', 'Streak_When_Away',
                ]
​
    df[new_cols] = 0
    # If a team wins it adds 3 points, 1 point if it draws and
    # 0 points if it loses
    dict_points_home = {0: 3, 1: 1, 2: 0}
​
    for r in tqdm(range(n_rounds)):
        cur_round = df[df['Round'] == (r + 1)]
        for _, row in df_standings.iterrows():
            team = row['Team']
            # If the selected team is in the Home Team column
            # we should add the variables concerning their
            # overall performance and only the performance
            # when it plays at home
​
            # Let's write the performance of the Home team
            if (cur_round['Home_Team'] == team).sum() >= 1:
                indices = list(cur_round.loc[cur_round['Home_Team']
                                             == team].index.values)
​
                # First the position of the team
                for idx in indices:
                    cur_round.loc[idx, 'Points_Home'] = \
                        row['Points']
​
            # Let's write the performance of the Away team when
            # it plays Away
            elif (cur_round['Away_Team'] == team).sum() >= 1:
                indices = list(cur_round.loc[cur_round['Away_Team']
                                             == team].index.values)
​
                # First the position of the team
                for idx in indices:
                    cur_round.loc[idx, 'Points_Away'] = \
                        row['Points']
            else:
                pass
        df.loc[cur_round.index] = cur_round
        for _, rows in cur_round.iterrows():
            # If a team wins it adds 3 points, 1 point if it draws and
            # 0 points if it loses
​
            df_standings.loc[df_standings['Team']
                             == rows['Home_Team'],
                             'Points'] += \
                                 dict_points_home[rows['Label']]
    return df
​
​
def clean_database():
    leagues = [x.split('/')[-1] for x in glob.glob('./Data/Results/*')]
    for league in leagues:
        os.makedirs(f"./Data/Results_Cleaned/{league}", exist_ok=True)
        seasons = glob.glob(f'./Data/Results/{league}/*')
        seasons.sort()
        for season in seasons:
            # Load the data
            df = pd.read_csv(season)
            if len(df) == 0:
                print(f'No available data for season {season} of {league}')
                continue
            filename = f'./Data/Results_Cleaned/{league}/Cleaned_{df.loc[0]["Season"]}' \
                        + f'_{df.loc[0]["League"]}.csv'
            df = get_standings(df)
​
            df.to_csv(filename, index=False)
​
​
if __name__ == '__main__':
    clean_database()