import matplotlib.pyplot as plt
import pandas as pd
import os
import plotly
work_path = '/Users/yang/PycharmProjects/FirstProjet/Github/yxyProject/PublicTransport'
file_bus = "bus2017.csv"
file_tram='tram2017.csv'
encoding = "UTF-8"


bus=pd.read_csv(os.path.join(work_path,file_bus),encoding=encoding,engine='python', header=None)
bus.drop([0],inplace=True)
bus = bus[0].str.split("\t", expand=True)
bus[0] = pd.to_datetime(bus[0])
bus[1]=pd.to_numeric(bus[1])





tram=pd.read_csv(os.path.join(work_path,file_tram),encoding=encoding,engine='python', header=None)
tram.drop([0],inplace=True)
tram = tram[0].str.split("\t", expand=True)
tram[0] = pd.to_datetime(tram[0])
tram[1]=pd.to_numeric(tram[1])



bus[2]=tram[1]
bus[3]=(bus[2]-bus[1])/(bus[2]+bus[1])
plt.plot(bus[0][40:50],bus[1][40:50]-bus[2][40:50])

plt.show()