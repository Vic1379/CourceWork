import matplotlib.pyplot as opt, matplotlib.animation as animation, pathlib, re
from matplotlib.pyplot import plot as plt
from shapely.geometry import LineString, Point

def length(otr):
    return ((otr[0][0]-otr[0][1])**2+(otr[1][0]-otr[1][1])**2)**(1/2)
def dl(x1, x2, y1, y2):
    if x1 == x2: return ((x1, x2), (11, -11))
    xl1, xl2 = max(x1, x2), min(x1, x2)
    if xl1 == x1: yl1, yl2 = y1, y2
    else: yl1, yl2 = y2, y1
    while yl1 <= 10 and yl1 >= -10 and xl1 <= 10:
        xl1+=1
        yl1 = (xl1 - x1)*(y2-y1)/(x2-x1)+y1
    while yl2 <= 10 and yl2 >= -10 and xl2 >= -10:
        xl2-=1
        yl2 = (xl2 - x1)*(y2-y1)/(x2-x1)+y1
    return ((xl1, xl2), (yl1, yl2))
def intrs(a, b):
    s = LineString([(b[0][0], b[1][0]), (b[0][1], b[1][1])])
    point = LineString([(a[0][0], a[1][0]), (a[0][1], a[1][1])]).intersection(s)
    res = [point.x, point.y]
    if abs(res[0]) <= 0.01: res[0] = 0
    if abs(res[1]) <= 0.01: res[1] = 0
    return res
def cl_int(c, l, f):
    circle = Point(c[0], c[1]).buffer(c[2]).boundary
    i = circle.intersection(LineString([(l[0][0], l[1][0]), (l[0][1], l[1][1])]))
    if i.geoms[0].coords[0][0] == f: res = list(i.geoms[1].coords[0])
    else: res = list(i.geoms[0].coords[0])
    if abs(res[0]) <= 0.01: res[0] = 0
    if abs(res[1]) <= 0.01: res[1] = 0
    return res
def c_int(c1, c2, f = False):
    circle_1 = Point(c1[0], c1[1]).buffer(c1[2]).boundary
    i = circle_1.intersection(Point(c2[0], c2[1]).buffer(c2[2]).boundary)
    if f:
        res = [list(i.geoms[0].coords[0]), list(i.geoms[1].coords[0])]
        if abs(res[0][0]) <= 0.01: res[0][0] = 0
        if abs(res[0][1]) <= 0.01: res[0][1] = 0
        if abs(res[1][0]) <= 0.01: res[1][0] = 0
        if abs(res[1][1]) <= 0.01: res[1][1] = 0
        return res
    if i.geoms[0].coords[0][0] <= i.geoms[1].coords[0][0]: res = list(i.geoms[0].coords[0])
    else: res = list(i.geoms[1].coords[0])
    if abs(res[0]) <= 0.01: res[0] = 0
    if abs(res[1]) <= 0.01: res[1] = 0
    return res
def get_y(x, line):
    return (x-line[0][0])*(line[1][1]-line[1][0])/(line[0][1]-line[0][0])+line[1][0]
def animate(frame):
    data = open(str(pathlib.Path(__file__).parent.absolute())+"\Data.txt","r").read().split('\n')
    if frame <= len(data): data = data[0:frame]
    for i in data:
        if i != '':
            i = i.split()
            if i[0] == 'o':
                x = [float(j) for j in re.findall(r'[-]?\d+\.\d+|[-]?\d+', i[1]+i[2])]
                y = [float(j) for j in re.findall(r'[-]?\d+\.\d+|[-]?\d+', i[3]+i[4])]
                plt(x, y,  marker = 'o', color = 'b')
            elif i[0] == 'l':
                x = [float(j) for j in re.findall(r'[-]?\d+\.\d+|[-]?\d+', i[1]+i[2])]
                y = [float(j) for j in re.findall(r'[-]?\d+\.\d+|[-]?\d+', i[3]+i[4])]
                plt(*dl(x[0], x[1], y[0], y[1]),  marker = 'o', color = 'g')
            elif i[0] == 'p':
                x, y = re.findall(r'[-]?\d+\.\d+|[-]?\d+', i[1]), re.findall(r'[-]?\d+\.\d+|[-]?\d+', i[2])
                plt(float(x[0]), float(y[0]),  marker = 'o', color = 'r')
            elif i[0] == 'c':
                x, y = re.findall(r'[-]?\d+\.\d+|[-]?\d+', i[1]), re.findall(r'[-]?\d+\.\d+|[-]?\d+', i[2])
                r = re.findall(r'[-]?\d+\.\d+|[-]?\d+', i[3])
                c = opt.Circle((float(x[0]), float(y[0])), float(r[0]), color = 'b', fill = False)
                opt.gca().add_artist(c)