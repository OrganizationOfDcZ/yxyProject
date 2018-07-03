from PIL import Image
import numpy as np
from io import BytesIO
import urllib.request
import matplotlib.pyplot as plt
import matplotlib
import os
from lxml import etree
import json
import pandas as pd
import matplotlib.patches as mpatches

data_path='/Users/yang/Documents/Trafic_routier/22_02_2018'


def Gmap(centerLat, centerLon, zoomS, pixelS, size, dark, saveAddress):
    url = 'http://maps.googleapis.com/maps/api/staticmap?sensor=false' \
          + '&size=' + str(size) + 'x' + str(size) + '&center=' + str(centerLat) + ',' \
          + str(centerLon) + '&zoom=' + str(zoomS) + '&scale=' + str(pixelS) \
          + '&maptype=terrain'
    if dark == True:
        url = url + '&style=feature:all|element:all|saturation:-10|lightness:20'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)

    buffer = BytesIO(urllib.request.urlopen(req).read())
    image = Image.open(buffer)
    if saveAddress:
        image.save(saveAddress)
    else:
        image.show()


def latLonToPixelXY(lat, lon, zoomS):
    mapW = 256 * 2 ** zoomS + 0.0
    mapH = 256 * 2 ** zoomS + 0.0
    x = (lon + 180) * (mapW / 360)  # get x value
    latRad = lat * np.pi / 180  # convert from degrees to radians
    mercN = np.log(np.tan((np.pi / 4) + (latRad / 2)))  # get y value
    y = (mapH / 2) - (mapW * mercN / (2 * np.pi))
    return x, y


# read the document TraficInfo_geometry.json, get the location information of the Roads
def GeometryOfRoad():
    with open('TraficInfo_geometry.json') as json_data:
        d = json.load(json_data)
        s=d["d"]
        geometry=[]

        for ele in s:
            id= ele["id"]

            A=ele["go"][0]
            B=ele["go"][1]
            A1=A["x"]
            A2=A["y"]

            B1=B["x"]
            B2=B["y"]
            geometry.append((id,A1,A2,B1,B2))
    return geometry


# read the document .xml , and return the id of road and debit of this road in this moment
def routes_statu(file):
    #path_perso = '/Users/yang/PycharmProjects/FirstProjet/Github/yxyProject/data'
    f = os.path.join(data_path, file)
    tree = etree.parse(f)
    #Debit is uesd for difine the color of Road
    Debit=[]
    for data in tree.getiterator("donnees"):
        Datetime=data.get("ts")
    for element in tree.getiterator("ARC"):
        Debit.append((int(element.get("Debit")),element.get("Ident")))
    # normalize the values of debits

    return sorted(Debit,reverse = True),Datetime

#return the value of debit of a road by matching id
def location(id,centX,centY):
    locations = GeometryOfRoad()
    i=0
    for k in range(len(locations)):
        if locations[k][0]==id:
            i=k
    Alat = locations[i][2]  # latitude of the first point of this road
    Alon = locations[i][1]  # longitude of the first point of this road
    Blat = locations[i][4]  # latitude of the last point of this road
    Blon = locations[i][3]  # longitude of the last point of this road

    Ax, Ay = latLonToPixelXY(float(Alat), float(Alon), scale)
    Ax, Ay = size * pixelS / 2 + Ax - centX, size * pixelS / 2 - (Ay - centY)

    Bx, By = latLonToPixelXY(float(Blat), float(Blon), scale)
    Bx, By = size * pixelS / 2 + Bx - centX, size * pixelS / 2 - (By - centY)

    x = [Ax, Bx]
    y = [Ay, By]
    return x,y

def colorbar():
    im = np.flipud(plt.imread('/Users/yang/PycharmProjects/FirstProjet/Github/yxyProject/Visualization/projet.png'))
    plt.figure(figsize=(6.4, 6.4))
    plt.imshow(im, origin='lower')

    cm = plt.cm.get_cmap('RdYlGn')
    a = pd.Series(np.linspace(0.0, 1.0, 20))
    color = cm(np.linspace(0.0, 1.0, len(a)))
    handles=[]
    label=['0-5','5-10','10-15','15-20','20-25','25-30','30-35','35-40','40-45','45-50','50-55','55-60','60-65','65-70','70-75','75-80','80-85','85-90','90-95','>=95']
    for k in range(len(color)):
        patch = mpatches.Patch(color=matplotlib.colors.to_hex(color[19-k], keep_alpha=False), label=label[k])
        handles.append(patch)
    plt.legend(handles=[handle for i,handle in enumerate(handles)],bbox_to_anchor=(1.15, 1),loc=1)


def maps_rues(file,centerLat, centerLon, scale,pixelS,size):

    Debit,Datetime=routes_statu(file)

    cm = plt.cm.get_cmap('RdYlGn')
    a = pd.Series(np.linspace(0.0, 1.0, 20))
    color = cm(np.linspace(0.0, 1.0, len(a)))

    centX, centY = latLonToPixelXY(centerLat, centerLon, scale)
    #im = np.flipud(plt.imread('/Users/yang/PycharmProjects/FirstProjet/Github/yxyProject/Visualization/projet.png'))
    #plt.figure(figsize=(6.4, 6.4))
    #plt.imshow(im, origin='lower')

    for i,element in enumerate(Debit):
        id=element[1]
        x,y=location(id,centX,centY)
        k=int(element[0]/5)
        if element[0]>=100:
            plt.plot(x, y,color=matplotlib.colors.to_hex(color[0], keep_alpha=False),linewidth=2)
        else:
            plt.plot(x, y, color=matplotlib.colors.to_hex(color[19 - k], keep_alpha=False), linewidth=2)

    plt.xlim(0, size * pixelS)
    plt.ylim(0, size * pixelS)
    plt.axis('off')
    plt.title(Datetime)
    #plt.show()
    plt.savefig('/Users/yang/PycharmProjects/FirstProjet/Github/yxyProject/Pictures/'+str(file).rstrip('.xml')+'.png')

if __name__ == "__main__":

    np.set_printoptions(precision=2,linewidth=5000)

    datadir = os.listdir(data_path)
    files = [str(f) for f in datadir if os.path.splitext(f)[1].lower()==".xml"]

    centerLat, centerLon = (48.585, 7.74534)
    scale = 14
    pixelS = 1
    size = 640
    #Gmap(centerLat, centerLon, scale, pixelS, size, True,'/Users/yang/PycharmProjects/FirstProjet/Github/yxyProject/Visualization/projet.png')

    for i in range(len(files)):
        colorbar()
        maps_rues(files[i], centerLat, centerLon, scale, pixelS, size)

    # for i in range(len(files)):
    #     if i%20 == 0:
    #         maps_rues(files[i],centerLat, centerLon, scale,pixelS,size)
    #     else:
    #         pass