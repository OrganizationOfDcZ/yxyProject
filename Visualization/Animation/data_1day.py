# this document is use for prepare the data of un jour. And we wil use this data in animate ggmaps.

import numpy as np
import json
import pandas as pd
import os
from lxml import etree
from pathlib import Path

def location():
    with open('TraficInfo_geometry.json') as json_data:
        file = json.load(json_data)
        d=file["d"]
        tableau=[]

        for ele in d:
            id= ele["id"]

            A=ele["go"][0]
            B=ele["go"][1]
            A1=A["x"]
            A2=A["y"]

            B1=B["x"]
            B2=B["y"]
            tableau.append((id,A1,A2,B1,B2))
    df=pd.DataFrame(tableau)
    df=df.set_index(0)
    return df

def read_info(file):
    tree = etree.parse(file)
    Rues = []
    for element in tree.getiterator("ARC"):
        Rues.append((element.get("Ident"), int(element.get("Debit"))))
    df=pd.DataFrame(Rues)
    df.set_index(0)
    print(df)


def debit():
    path_perso='/Users/yang/Documents/Trafic_routier/22_02_2018'

    datadir = Path(path_perso)
    files = [str(f) for f in datadir.glob('*.xml') if f]

    df=location()
    k=5
    for file in files:
        tree = etree.parse(file)
        Rues = []
        for element in tree.getiterator("ARC"):
            Rues.append((element.get("Ident"), int(element.get("Debit"))))
        df1 = pd.DataFrame(Rues)
        df1=df1.set_index(0)
        df1.rename(columns={df1.columns[0]:k},inplace=True)
        print(df1.columns.values.tolist())

        df=pd.concat([df,df1],axis=1)
        df=df.dropna(axis=0,how='any')
        k=k+1

    df.to_csv('data4oneday.csv', sep='\t', encoding='utf-8')
debit()