import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

palette=[
    '#838a96',
    #Tatum
    '#007A33',
    #Luka
    '#00538C',
    #Joker
    '#FEC524',
    #Gianni
    '#EEE1C6',
    #Book
    '#E56020'
]


def gen_cats(data, rows):
    r_df = pd.DataFrame()
    i = 0
    for row in rows:
        r = pd.DataFrame()
        r['data'] = data[row]
        r['idx'] = i
        r_df = pd.concat([r_df, r], axis=0)
        i += 1
    r_df['player_id']=0
    return r_df

def add_player_info(data, player, rows):
    r_df = data
    max_player_id = data['player_id'].max()+1
    i = 0
    for row in rows:
        r = pd.DataFrame()
        r['data'] = player[row]
        r['idx'] = i
        r['player_id'] = max_player_id
        r_df = pd.concat([r_df, r], axis=0)
        i += 1

    return r_df

COUNTING_STATS = ['PTS', 'TRB', 'AST']

mvp = pd.read_csv('mvps.csv')
SCAT = gen_cats(mvp, COUNTING_STATS)
tatum = pd.read_csv('tatum.csv')
luka = pd.read_csv('luka.csv')
joker = pd.read_csv('joker.csv')
gianni = pd.read_csv('gianni.csv')
book = pd.read_csv('book.csv')



SCAT = add_player_info(SCAT, tatum, COUNTING_STATS)
SCAT = add_player_info(SCAT, luka, COUNTING_STATS)
SCAT = add_player_info(SCAT, joker, COUNTING_STATS)
SCAT = add_player_info(SCAT, gianni, COUNTING_STATS)
SCAT = add_player_info(SCAT, book, COUNTING_STATS)
print(mvp.sort_values(by=['TRB']))
counting_stats = sns.scatterplot(data=SCAT, x='idx', y='data', hue='player_id', palette=palette, s=500, marker='o')
plt.legend(labels=['legend', 'Previous MVPs', 'Jayson Tatum', "Luka Donic", "Nikola Jokic", "Giannis Antetokounmpo", "Devin Booker"])
counting_stats.set_xticks([0, 1, 2])
counting_stats.set_yticks(range(0, 40))
counting_stats.set_xticklabels(COUNTING_STATS)
plt.show()