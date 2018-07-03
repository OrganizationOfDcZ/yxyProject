from __future__ import print_function


import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import os.path


work_path = '/Users/yang/PycharmProjects/FirstProjet/Github/yxyProject/PublicTransport'
file_name = "bus63.csv"
encoding = "UTF-8"

df = pd.read_csv(os.path.join(work_path, file_name),
                          encoding=encoding,
                          engine='python', header=None)

df.drop([0],inplace=True)
df = df[0].str.split("\t", expand=True)
df[0] = pd.to_datetime(df[0])
df[1]=pd.to_numeric(df[1])

temp_df = pd.Series(data=df[1].values, index=df[0].values)
temp_df.dropna(inplace=True)
print(temp_df.values)

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(temp_df.values.squeeze(), lags=40, ax=ax1)

ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(temp_df.values, lags=40, ax=ax2)
plt.show()