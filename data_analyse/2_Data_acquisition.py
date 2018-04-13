from __future__ import print_function
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.api as sm
from statsmodels.graphics.api import qqplot

from pymongo import MongoClient
import plotly

import plotly.plotly as py
import plotly.graph_objs as go
import plotly


client = MongoClient('mongodb://127.0.0.1:27017/')
db = client.trafic_routier
routiers = db.routiers

Debit=[]
Datetime=[]
for data in routiers.find({'Ident':15}):
    Debit.append(data['Debit'])
    Datetime.append(data['DateTime'])

series=pd.Series(Debit,index=Datetime)
print(series)
# series.to_csv('Ident_15.csv', sep='\t', encoding='utf-8')
#
# d = [go.Scatter(
#         x=series.index,
#         y=series.values)]
# layout = dict(title="Sans prétraitement")
# fig = dict(data=d, layout=layout)
# py.plot(fig, filename="Sans prétraitement")

