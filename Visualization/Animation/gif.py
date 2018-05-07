import moviepy.editor as mpy
from uuid import uuid4
import os

def create_gif():
    path_perso = '/Users/yang/PycharmProjects/FirstProjet/Github/yxyProject/Pictures'
    datadir = os.listdir(path_perso)
    files = [str(f) for f in datadir if os.path.splitext(f)[1].lower() == ".png"]
    file_names=[]
    for f in files:
        fn = os.path.join(path_perso, f)
        file_names.append(fn)
    clip = mpy.ImageSequenceClip(file_names, fps=12)
    name = '{}.gif'.format(uuid4())
    clip.write_gif(name, fps=12)
    return name
create_gif()