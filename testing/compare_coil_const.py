# Compare coil constants from file and print matching / not matching signs
# Derek Fujimoto
# May 2025

import pandas as pd
import numpy as np

# files to compare
path1 = 'coil_const/coil_constants.csv'
path2 = 'coil_constants2.csv'

# data cleaning
df_list = []
for path in [path1, path2]:

    # load the file
    df = pd.read_csv(path, comment='#')

    # drop duplicates
    df.drop_duplicates('coil', inplace=True)

    # set index
    df.set_index('coil', inplace=True)

    # get sign
    df['sign'] = df['slope'].apply(np.sign)

    # save
    df_list.append(df['sign'])

# compare
index = np.unique(np.concatenate([df.index for df in df_list]))

for idx in index:
    try:
        print(f'Coil {idx:>2} slope signs match? {df_list[0].loc[idx] == df_list[1].loc[idx]}')
    except KeyError:
        print(f'Coil {idx:>2} missing measurement')

