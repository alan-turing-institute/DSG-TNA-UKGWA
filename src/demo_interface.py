# Script to run the demo in the local repository

import sqlite3
import os
import pandas as pd
import json
import plotly.graph_objects as go
from db_utils import db_connect


# %%
years = ['2013','2014', '2015','2016','2017', '2018','2019']
years_cleaned = ['2012','2013','2014', '2015','2016','2017', '2018']


def get_freq(token):
    freq = []
    if token in all_weighted_ents:
      db = all_weighted_ents
      for year in years:
        if year in db[token]:
            f = db[token][year]
        else:
            f = 0
        freq.append(f)
    else:
      db = all_weighted_words
      token = token.lower()
      for year in years:
          if year+"0101000000" in db[token]:
              f = db[token][year+"0101000000"]
          else:
              f = 0
          freq.append(f)
    return freq

with open("all_weighted_ents.json") as json_file:
    all_weighted_ents = json.load(json_file)
with open("all_weighted_words.json") as json_file:
    all_weighted_words = json.load(json_file)


# %%
# terms to be searched in the database (temporary json file)
# to be replaced for database
query = set(["Olympics","sports","UKSA"])

fig_list = []
check = True
for el in query:
  try:
      fig_list.append(go.Bar(name=el, x=years_cleaned, y=get_freq(el)))
  except Exception as e:
    print ("Sorry, the term",e, "does not appear in the corpus.")
    check = False
    continue
if check == True:
    fig = go.Figure(data=fig_list)
    # Change the bar mode
    fig.update_layout(barmode='stack')
    fig.show()

# %%
# instance the database file for constante queries
DEFAULT_PATH = os.path.join(os.path.dirname('__file__'), 'search_data.db')
def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con
con = db_connect() # connect to the database

# term to search in db simulation a drill down from stack bar
term = ('UKSA', 2019)

df = pd.read_sql_query(f"""SELECT doc, count(*) as cnt FROM documententity \
                        where ent = '{term[0]}' \
                        and year = {term[1]}
                        group by doc \
                        order by cnt desc """, con)
df.head(10)
