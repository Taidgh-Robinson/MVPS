from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
#from basketball_reference_scraper.players import get_stats, get_game_logs, get_player_headshot

import pandas as pd 
import csv

def gen_ids():
    df = pd.read_csv('data/mvps.csv')
    names = set(df['Player'].tolist())
    
    d = {}
    for name in names:
        d[name] = players.find_players_by_full_name(name)[0]['id']

    pdf = pd.DataFrame(d.items(), columns=['name', 'id'])
    pdf.to_csv('data/ids.csv')



def download_player_career_stats():
    df = pd.read_csv('data/ids.csv')
    ids = df['id'].tolist()
    for id in ids:
        print(id)
        career = playercareerstats.PlayerCareerStats(player_id=id)
        pdf = career.get_data_frames()[0] 
        pdf.to_csv('data/player_career_stats/{}.csv'.format(str(id)))

def calculate_per_game_stat(row, stat):
    row[stat+'_PER_GAME'] = row[stat]/row['GP']
    return row

#gen_ids()
#download_player_career_stats()
#download_advanced_stats()


def create_mvp_data_table():
    mvps = pd.read_csv('data/mvps.csv')    
    mvp_ids = pd.read_csv('data/ids.csv')
    data_frame = pd.DataFrame()
    for index, row in mvps.iterrows():
        print(row['Season'] + ':' +row['Player'])
        id = int((mvp_ids.loc[mvp_ids['name'] == row['Player']])['id'])
        print(id)
        data = pd.read_csv('data/player_career_stats/{}.csv'.format(str(id)))
        advanced = pd.read_csv('data/player_advanced_stats/{}.csv'.format(str(id)))
        data_row = data.loc[data['SEASON_ID'] == row['Season']]
        data_row['PLAYER'] = row['Player']
        advanced_row = advanced.loc[advanced['SEASON'] == row['Season']]
        print(advanced_row)
        data_row = calculate_per_game_stat(data_row, 'PTS')
        data_row = calculate_per_game_stat(data_row, 'REB')
        data_row = calculate_per_game_stat(data_row, 'AST')
        data_row = calculate_per_game_stat(data_row, 'BLK')
        data_row = calculate_per_game_stat(data_row, 'STL')

        data_frame = pd.concat([data_row, data_frame])

    return data_frame


def download_advanced_stats():
    df = pd.read_csv('data/ids.csv')
    for index, row in df.iterrows():
        name = row['name']
        #Issue with Shaq, just gonna download that one manually, created an issue with the package we'll see if I have the heart to fix it: 
        if(name != "Shaquille O'Neal"):
            stats = get_stats(name, stat_type='ADVANCED', playoffs=False, career=False)        
            stats.to_csv('data/player_advanced_stats/{}.csv'.format(str(row['id'])))

print(create_mvp_data_table())