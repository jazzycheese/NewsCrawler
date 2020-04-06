import os
import pandas as pd

directory = "/Users/soyeon/dev/NewsCrawler/1990-01-01_2019-12-31"

df = pd.DataFrame()
for root,dirs,files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            _df =  pd.read_csv(os.path.join(directory,file),index_col =0)
            df = df.append(_df,ignore_index=True)
            
df.to_csv(os.path.join(directory,"all.csv"))