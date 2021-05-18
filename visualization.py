import pandas as pd
from pandas import DataFrame
import ast
import matplotlib
import matplotlib.pyplot as plt

df = pd.read_csv('gistJab.csv')
df2 = pd.read_csv('userJab.csv')

language = []
for lang in df['files_language']:
  res = ast.literal_eval(lang)
  if (res == []):
    language.append('NoLanguage')
  else:
    for l in res:
      language.append(l)
# print(language)
# df = DataFrame (language,columns=['files_language'])
# langua = df.groupby(['files_language']).size().sort_values(ascending=False).reset_index(name='count')
# langua.to_csv("files_language.csv", index=False)
# langua = langua.head(15).plot.bar(x='files_language', y='count', figsize=(20, 20))
# plt.show()
# langua.figure.savefig('files_language.png')

# langua = langua.head(15).plot.pie(y='count', x='files_language', figsize=(12, 12))
# plt.show()

# df2 = DataFrame (df2,columns=['login', 'public_gists'])
# df2 = df2.sort_values(by=['public_gists'], ascending=False)
# df2.to_csv("public_gists.csv", index=False)

df = DataFrame (df, columns=['login', 'gist_created_at', 'gist_updated_at', 'files_total_size', 'history_total', 'history_additions', 'history_deletions', 'history_changes'])
df['gist_updated_at'] = pd.to_datetime(df['gist_updated_at'])
df['gist_created_at'] = pd.to_datetime(df['gist_created_at'])
df['gist_difference_at'] = (df['gist_updated_at'] - df['gist_created_at']).dt.days
df = df.sort_values(by=['gist_difference_at'], ascending=False)

df.to_csv("gist_analyzed2.csv", index=False)
