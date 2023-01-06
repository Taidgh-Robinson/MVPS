import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def gen_cats_pg(data, rows):
    r_df = pd.DataFrame()
    i = 0
    for row in rows:
        r = pd.DataFrame()
        r['data'] = data[row]/data['GP']
        r['idx'] = i
        r['player'] = data['PLAYER']
        r_df = pd.concat([r_df, r], axis=0)
        i += 1
    r_df['player_id']=0
    return r_df

def gen_by_year_dataset(data, tag):
    dtm =[]
    i=0
    for index, row in data.iterrows():
        dtpm =[i, str(row['SEASON_ID']), float(row[tag]/row['GP'])]
        i+=1
        print(dtpm)
        dtm.append(dtpm)

    r_df = pd.DataFrame(dtm, columns=['idx', 'season', tag])
    return r_df

mvp = pd.read_csv('data/mvps_downloaded.csv')
O_COUNTING_STATS = ['PTS', 'REB', 'AST']

SCAT=gen_by_year_dataset(mvp, 'PTS')
counting_stats = sns.scatterplot(data=SCAT, x='idx', y='PTS')
plt.show()