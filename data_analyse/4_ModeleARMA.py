from __future__ import print_function


import matplotlib.pyplot as plt
import statsmodels.api as sm
import sys
import pandas as pd
import os.path
import numpy as np


work_path = '/Users/yang/PycharmProjects/FirstProjet/Test/third_month'
file_name = "Ident_15_new.csv"
encoding = "UTF-8"

df = pd.read_csv(os.path.join(work_path, file_name),
                          encoding=encoding,
                          engine='python', header=None)

df.drop([0],inplace=True)
df = df[0].str.split("\t", expand=True)
df[0] = pd.to_datetime(df[0])
df[1]=pd.to_numeric(df[1])

temp_df = pd.Series(data=df[1].values, index=df[0].values)
print(temp_df)

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(temp_df.values.squeeze(), lags=40, ax=ax1)

ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(temp_df, lags=40, ax=ax2)
plt.show()

# arma_mod20 = sm.tsa.ARMA(dta, (2,0)).fit(disp=False)
# print(arma_mod20.params)
#
# arma_mod30 = sm.tsa.ARMA(dta, (3,0)).fit(disp=False)
# print(arma_mod20 .aic, arma_mod20.bic, arma_mod20.hqic)
#
# print(arma_mod30.params)
# print(arma_mod30.aic, arma_mod30.bic, arma_mod30.hqic)
#
# sm.stats.durbin_watson(arma_mod30.resid.values)
#
# fig = plt.figure(figsize=(12,8))
# ax = fig.add_subplot(111)
# ax = arma_mod30.resid.plot(ax=ax);
#
# resid = arma_mod30.resid
# stats.normaltest(resid)
#
# fig = plt.figure(figsize=(12,8))
# ax = fig.add_subplot(111)
# fig = qqplot(resid, line='q', ax=ax, fit=True)
#
# fig = plt.figure(figsize=(12,8))
# ax1 = fig.add_subplot(211)
# fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=40, ax=ax1)
# ax2 = fig.add_subplot(212)
# fig = sm.graphics.tsa.plot_pacf(resid, lags=40, ax=ax2)
#
# r,q,p = sm.tsa.acf(resid.values.squeeze(), qstat=True)
# data = np.c_[range(1,41), r[1:], q, p]
# table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
# print(table.set_index('lag'))
#
# predict_sunspots = arma_mod30.predict('1990', '2012', dynamic=True)
# print(predict_sunspots)
#
# fig, ax = plt.subplots(figsize=(12, 8))
# ax = dta.ix['1950':].plot(ax=ax)
# fig = arma_mod30.plot_predict('1990', '2012', dynamic=True, ax=ax, plot_insample=False)
