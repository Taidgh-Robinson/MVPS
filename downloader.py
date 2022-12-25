from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd 
import csv

def gen_ids():
    df = pd.read_csv('mvps.csv')
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

#gen_ids()
#download_player_career_stats()

df = pd.read_csv('mvps.csv')
df1 = pd.read_csv('data/ids.csv')
for index, row in df.iterrows():
    print(row['Season'] + ':' +row['Player'])
    id = int((df1.loc[df1['name'] == row['Player']])['id'])
    print(id)
    data = pd.read_csv('data/player_career_stats/{}.csv'.format(str(id)))
    rrrr = data.loc[data['SEASON_ID'] == row['Season']]
    print(rrrr)