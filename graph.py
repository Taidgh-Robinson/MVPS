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

tag_to_label = {"PTS": "Points", "REB" : "Rebounds", "AST" : "Assits", "STL" : "Steals", "BLK" : "Blocks", "FG_PCT": "Field Goal Percentage", "FG3_PCT" : "3 Point Percentage", "TS%" : "True Shooting Percentage", 'OWS' : 'OWS', 'TOV' : 'Turnovers', 'PF':'Personal Fouls', 'PER':'PER','OWS':'OWS',
                'DWS':'DWS','WS':'WS','OBPM':'OBPM','DBPM':'DBPM','BPM':'BPM','VORP':'VORP'}

def beep(tag):
    ret_map = {'REB':'TRB', 'FG_PCT':'FG%', 'FG3_PCT':'3P%'}
    if(tag in ret_map.keys()):
        return ret_map[tag]
    return tag

def add_player_to_scat(scat, name, tag, sub_cat):
    player = pd.read_csv('data/this_year/{}.csv'.format(name))
    player_tag = beep(tag)
    new_row = {'idx':67, 'season':'2022-23', tag:float(player[player_tag]), 'sub_cat':sub_cat}
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
    if(per_game):
        sp.set_title("{} per game by the MVP".format(tag_to_label[tag]))
    else:
        sp.set_title("{} by the MVP".format(tag_to_label[tag]))
    sp.set_xticks(xticks)
    sp.set_xticklabels(labels)
    sp.set_xlabel("Season")
    if(per_game):
        sp.set_ylabel("{} per game".format(tag_to_label[tag]))
    else:
        sp.set_ylabel("{}".format(tag_to_label[tag]))
    plt.savefig('data/graphs/by_year/{}.png'.format(tag))
    plt.clf()

def gen_scatter_plot_by_cat(cats, per_game, label):
    mvp = pd.read_csv('data/mvps_downloaded.csv')
    i = 0
    r_df = pd.DataFrame()
    for cat in cats:
        r = pd.DataFrame()
        if(per_game):
            r['data'] = mvp[cat]/mvp['GP']
        else:
            r['data'] = mvp[cat]
        r['idx'] = i
        r['player_id'] = 0
        r_df = pd.concat([r_df, r], axis=0)
        i += 1

    tatum = pd.read_csv('data/this_year/tatum.csv')
    luka = pd.read_csv('data/this_year/luka.csv')

    r_df = add_player_info_to_cat(r_df, tatum, cats, per_game)
    r_df = add_player_info_to_cat(r_df, luka, cats, per_game)

    sp = sns.scatterplot(data=r_df, x='idx', y='data', hue='player_id', marker='_', s=200)
    sp.set_xticks(list(range(len(cats))))
    sp.set_xticklabels([tag_to_label[c] for c in cats])
    plt.tight_layout()
    plt.savefig('data/graphs/by_cat/{}.png'.format(label))
    plt.clf()

def add_player_info_to_cat(data, player, rows, per_game):
    r_df = data
    max_player_id = data['player_id'].max()+1
    i = 0
    for row in rows:
        r = pd.DataFrame()
        if(per_game):
            r['data'] = player[row]/player['G']
        else:
            r['data'] = player[row]
        r['idx'] = i
        r['player_id'] = max_player_id
        r_df = pd.concat([r_df, r], axis=0)
        i += 1

    return r_df

BASIC_OFFENSIVE_COUNTING_STATS = (['PTS', 'REB', 'AST'], 'Offensive Counting Stats')
BASIC_DEFENSIVE_COUNTING_STATS = (['BLK', 'STL'], 'Defensive Counting Stats')
BASIC_BAD_STATS = (['TOV', 'PF'], 'Negative Counting Stats')
ADVANCED_STATS = (['OWS','DWS','WS','OBPM','DBPM','BPM','VORP', 'PER'], 'Advanced Stats')


gen_scatter_plot_by_cat(ADVANCED_STATS[0], False, ADVANCED_STATS[1])
