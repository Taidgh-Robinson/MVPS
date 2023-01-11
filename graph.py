import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def gen_labels(seasons):
    seasons = ["'"+x.split("-")[1] for x in seasons]
    labels = []
    xticks = [0]
    labels.append(seasons[0])
    xt=4
    for x in seasons[4::5]:
        labels.append(x)
        xticks.append(xt)
        xt+=5
    labels.append("'23")
    xticks.append(len(seasons))
    return (labels, xticks)

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

def gen_by_year_by_game_dataset(data, tag):
    dtm =[]
    i=0
    for index, row in data.iterrows():
        dtpm =[i, str(row['SEASON_ID']), float(row[tag]/row['GP'])]
        i+=1
        dtm.append(dtpm)

    r_df = pd.DataFrame(dtm, columns=['idx', 'season', tag])
    return r_df

def gen_by_year_dataset(data, tag):
    dtm =[]
    i=0
    for index, row in data.iterrows():
        dtpm =[i, str(row['SEASON_ID']), float(row[tag])]
        i+=1
        dtm.append(dtpm)

    r_df = pd.DataFrame(dtm, columns=['idx', 'season', tag])
    return r_df


O_COUNTING_STATS = ['PTS', 'REB', 'AST']
D_COUNTING_STATS = ['STL', 'BLK']
EFFICENCY_METRICS = ['FG_PCT', 'FG3_PCT', 'TS%']

tag_to_label = {"PTS": "Points", "REB" : "Rebounds", "AST" : "Assits", "STL" : "Steals", "BLK" : "Blocks", "FG_PCT": "Field Goal Percentage", "FG3_PCT" : "3 Point Percentage", "TS%" : "True Shooting Percentage"}

def beep(tag):
    if(tag=='REB'):
        return 'TRB'
    if(tag=='FG_PCT'):
        return 'FG%'
    if(tag=='FG3_PCT'):
        '3P%'
    return tag

def add_player_to_scat(scat, name, tag, sub_cat):
    player = pd.read_csv('data/this_year/{}.csv'.format(name))
    new_row = {'idx':67, 'season':'2022-23', tag:float(player[beep(tag)]), 'sub_cat':sub_cat}
    scat = scat.append(new_row, ignore_index=True)
    return scat

def gen_scatter_plot_by_year(tag, per_game):
    mvp = pd.read_csv('data/mvps_downloaded.csv')
    if(per_game):
        SCAT=gen_by_year_by_game_dataset(mvp, tag)
    else:
        SCAT=gen_by_year_dataset(mvp, tag)
    
    (labels, xticks) = gen_labels(SCAT['season'])


    SCAT['sub_cat'] = 0
    SCAT = add_player_to_scat(SCAT, 'tatum', tag, 1)
    SCAT = add_player_to_scat(SCAT, 'luka', tag, 2)

    sp = sns.scatterplot(data=SCAT, x='idx', y=tag, hue='sub_cat')
    sp.set_title("{} per game by the MVP".format(tag_to_label[tag]))
    sp.set_xticks(xticks)
    sp.set_xticklabels(labels)
    sp.set_xlabel("Season")
    sp.set_ylabel("{} per game".format(tag_to_label[tag]))
    plt.savefig('data/graphs/per_game/{}.png'.format(tag))
    plt.clf()

for stat in O_COUNTING_STATS:
    gen_scatter_plot_by_year(stat, True)

for stat in D_COUNTING_STATS:
    gen_scatter_plot_by_year(stat, True)

for stat in EFFICENCY_METRICS:
    gen_scatter_plot_by_year(stat, False)

