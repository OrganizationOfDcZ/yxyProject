import moviepy.editor as mpy
from uuid import uuid4
import os
from lxml import etree

def create_gif():
    path_perso = '/Users/yang/PycharmProjects/FirstProjet/Github/yxyProject/Pictures'
    datadir = os.listdir(path_perso)
    files = [str(f) for f in datadir if os.path.splitext(f)[1].lower() == ".png"]
    file_names=[]
    for f in files:
        fn = os.path.join(path_perso, f)
        file_names.append(fn)
    clip = mpy.ImageSequenceClip(file_names, fps=10)
    name = '{}.gif'.format(uuid4())
    clip.write_gif(name, fps=10)
    return name
create_gif()

def MaxDebit():
    data_path ='/Users/yang/Documents/Trafic_routier/22_02_2018'
    datadir = os.listdir(data_path)
    files = [str(f) for f in datadir if os.path.splitext(f)[1].lower() == ".xml"]

    for file in files:
        f = os.path.join(data_path, file)
        tree = etree.parse(f)
        Debit = []
        for element in tree.getiterator("ARC"):
            Debit.append(int(element.get("Debit")))
        print(max(Debit))
#MaxDebit()