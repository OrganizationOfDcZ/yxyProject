from pymongo import MongoClient
import datetime
import numpy as np
from lxml import etree
import os
from pathlib import Path

client = MongoClient('mongodb://127.0.0.1:27017/')
db = client.trafic_routier

path_perso='/Users/yang/PycharmProjects/FirstProjet/Test/data'
np.set_printoptions(precision=2,linewidth=5000)

datadir = Path(path_perso)
files = [str(f) for f in datadir.glob('*.xml') if f]
print(files)
for file in files:
    tree = etree.parse(file)
    for data in tree.getiterator("donnees"):
        Datetime=data.get("ts")
    year = int(Datetime[0:4])
    month = int(Datetime[5:7])
    day = int(Datetime[8:10])
    hour = int(Datetime[11:13])
    minute = int(Datetime[14:16])
    second = int(Datetime[17:19])
    DT = datetime.datetime(year,month,day,hour,minute,second)
    print(DT)
    DMajEtatExp=[]
    for element in tree.getiterator("ARC"):
        D=element.get("DMajEtatExp")
        y = int(D[0:4])
        mo = int(D[5:7])
        d = int(D[8:10])
        h = int(D[11:13])
        m = int(D[14:16])
        s = int(D[17:19])
        dt=datetime.datetime(y,mo,d,h,m,s)
        DMajEtatExp.append(dt)
    ident=[]
    etat=[]
    EtatExp=[]
    Debit=[]
    Taux =[]
    DebitLisse=[]
    TauxLisse=[]
    VitesseBRP=[]
    for element in tree.getiterator("ARC"):
        ident.append(element.get("Ident"))
        etat.append(element.get("Etat"))
        EtatExp.append(element.get("EtatExp"))
        Debit.append(element.get("Debit"))
        Taux.append(element.get("Taux"))
        DebitLisse.append(element.get("DebitLisse"))
        TauxLisse.append(element.get("TauxLisse"))
        VitesseBRP.append(element.get("VitesseBRP"))

    routiers = db.routiers

    for i in range(len(ident)):
        routier = {"Ident": int(ident[i]),"Etat": int(etat[i]),"Etatexp": int(EtatExp[i]),"DMajEtatExp": DMajEtatExp[i],
                       "Debit": int(Debit[i]),"Taux": int(Taux[i]),"DebitLisse": int(DebitLisse[i]),"TauxLisse": int(TauxLisse[i]),
                       "VitesseBRP": VitesseBRP[i],"DateTime": DT}
        toutier_id = routiers.insert_one(routier).inserted_id

    Ident = []
    Etat = []
    Total = []
    Libre = []
    InfoUsager = []

    for element in tree.getiterator("PRK"):
        Ident.append(element.get("Ident"))
        Etat.append(element.get("Etat"))
        Total.append(element.get("Total"))
        Libre.append(element.get("Libre"))
        InfoUsager.append(element.get("InfoUsager"))

    parkings = db.parkings

    for i in range(len(Ident)):
        parking = {"Ident": int(Ident[i]), "Etat": int(Etat[i]), "total": int(Total[i]), "libre": int(Libre[i]),
                       "InfoUsager": InfoUsager[i], "Datetime": dt}
        parking_id = parkings.insert_one(parking).inserted_id