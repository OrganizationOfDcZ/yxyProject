from PIL import Image
import numpy as np
from io import BytesIO
import urllib.request
import matplotlib.pyplot as plt
import os
from lxml import etree
import json
file_path = r"/Users/yang/PycharmProjects/FirstProjet/Github/yxyProject/Visualization"
#输出路径
output_path = file_path


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


def routier():
    with open('TraficInfo_geometry.json') as json_data:
        d = json.load(json_data)
        s=d["d"]
        tableau=[]

        for ele in s:
            id= ele["id"]

            A=ele["go"][0]
            B=ele["go"][1]
            A1=A["x"]
            A2=A["y"]

            B1=B["x"]
            B2=B["y"]
            tableau.append((id,A1,A2,B1,B2))
    return tableau



def routes_statu(file):

    tree = etree.parse(file)
    Rues=[]
    for element in tree.getiterator("ARC"):

        Rues.append((element.get("Ident"),int(element.get("Debit"))))

    free = []
    fluid = []
    normal = []
    dense = []
    for i in range(len(Rues)):
        number=Rues[i][1]
        if number < 10 :
            free.append(Rues[i][0])
        elif number >= 10 and number < 20:
            fluid.append(Rues[i][0])
        elif number >= 20 and number < 40:
            normal.append(Rues[i][0])
        else:
            dense.append(Rues[i][0])
    return free,fluid,normal,dense


def maps_rues(file,centerLat, centerLon, scale,pixelS,size,k):
    print(k)
    routes=routier()
    free,fluid,normal,dense=routes_statu(file)

    longueur=len(routes)
    centX, centY = latLonToPixelXY(centerLat, centerLon, scale)

    im = np.flipud(plt.imread('/Users/yang/PycharmProjects/FirstProjet/Github/yxyProject/Visualization/Maps/projet.png'))
    ax = plt.subplot(111)
    ax.imshow(im, origin='lower')

    for i in range(longueur):
        id=routes[i][0]
        Alat = routes[i][2]
        Alon = routes[i][1]
        Blat = routes[i][4]
        Blon = routes[i][3]

        Ax, Ay = latLonToPixelXY(float(Alat), float(Alon), scale)
        Ax, Ay = size * pixelS / 2 + Ax - centX, size * pixelS / 2 - (Ay - centY)

        Bx, By = latLonToPixelXY(float(Blat), float(Blon), scale)
        Bx, By = size * pixelS / 2 + Bx - centX, size * pixelS / 2 - (By - centY)

        x=[Ax,Bx]
        y=[Ay,By]
        if id in free:

            ax.plot(x, y,color="blue",linewidth=3)
        elif id in fluid:

            ax.plot(x,y,color="green",linewidth=3)
        elif id in normal:

            ax.plot(x, y,color="orange",linewidth=3)
        elif id in dense:

            ax.plot(x,y,color="red",linewidth=3)


    ax.set_xlim(0, size * pixelS)
    ax.set_ylim(0, size * pixelS)
    plt.axis('off')
    #plt.show()
    #plt.savefig('/Users/yang/PycharmProjects/FirstProjet/Github/yxyProject/Picture/'+str(k)+'.png')

if __name__ == "__main__":

    path_perso='/Users/yang/PycharmProjects/FirstProjet/Github/yxyProject/data'
    np.set_printoptions(precision=2,linewidth=5000)

    datadir = os.listdir(path_perso)
    files = [str(f) for f in datadir if os.path.splitext(f)[1].lower()==".xml"]
    for file in files:
        print(file)

    # centerLat, centerLon = (48.585, 7.74534)
    # scale = 15
    # pixelS = 1
    # size = 640
    # Gmap(centerLat, centerLon, scale, pixelS, size, True,'/Users/yang/PycharmProjects/FirstProjet/Github/yxyProject/Visualization/projet.png')
    # i=0
    # for file in files:
    #
    #     maps_rues(file,centerLat, centerLon, scale,pixelS,size,i)
    #     i=i+1





