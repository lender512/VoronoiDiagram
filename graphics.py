import sys, pygame, math, numpy, random
from numpy.lib.function_base import append
from scipy.spatial import Voronoi, voronoi_plot_2d

pygame.init()

RESIZE = 5
DELAY = 1000
SIZE = WIDTH, HEIGH = int(360*RESIZE), int(180*RESIZE)
white = 255, 255, 255
black = 0, 0, 0

screen = pygame.display.set_mode(SIZE)
screen.fill(white)
pygame.display.update()

RADIUS = 5

def randomColor():
    color = list(numpy.random.choice(range(256), size=3))
    return color

def translate(point, translate):
        return (point[0] + translate[0], point[1] + translate[1])

def rotateZ(point, origin, angle):
    angle = math.radians(angle)
    point = translate(point,(-origin[0], -origin[1]))

    x = point[0]
    y = point[1]

    tempX = x*math.cos(angle) - y*math.sin(angle)
    tempY = x*math.sin(angle) + y*math.cos(angle)

    x = tempX
    y = tempY

    point = (x, y)

    point = translate(point, origin)
    return point

def getPerpendicular(a, b):
    mid = (a[0]+b[0])/2, (a[1]+b[1])/2
    m = (b[1]-a[1])/(b[0]-a[0])

    min = -WIDTH*2
    max = WIDTH*2
    p1 = (min, m*(min-a[0])+a[1])
    p2 = (max, m*(max-a[0])+a[1])
    p1 = rotateZ(p1, mid, 90)
    p2 = rotateZ(p2, mid, 90)
    return p1, p2
    

def transform(point):
    return (round(WIDTH//2 + point[0]), round(-point[1]+HEIGH//2))

def transformList(list):
    list2 = []
    for i in range(len(list)):
        list2.append(transform(list[i]))
    return list2

def isInline(line, point):
    a = line[0]
    b = line[1]
    m = (b[1]-a[1])/(b[0]-a[0])
    return round(m*(point[0]-a[0])+a[1]) == round(point[1])

def run(points):
    vor = Voronoi(points)
    # while 1:
    polys = numpy.ndarray.tolist(vor.vertices)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    

    regions = vor.regions
    pRegions = []
    i = 0

    #Stores the points that hace an area da collid the bounding
    pOut = []
    out = False
    for region in regions:
        pRegions.append([])
        if -1 in region:
            out = True
        for p in region:
            if p != -1:
                pRegions[i].append(polys[p])
            if out:
                pOut.append(polys[p])
        out = False
        i += 1
    # print(pRegions)

    # pygame.draw.lines(screen, (0,0,0), False, transformList(polys), RADIUS) 
    for r in pRegions:
        if len(r) > 2:
            pygame.draw.lines(screen, (100,100,100), False, transformList(r), 5) 

    ridge = numpy.ndarray.tolist(vor.ridge_points)
    pRidge = []
    for p in ridge:
        if len(p) > 1:
            pRidge.append(getPerpendicular(points[p[0]], points[p[1]]))

    for p in pRidge:
        inline = 0
        for point in polys:
            if isInline(p, point):
                inline += 1
                lastP = point
        if inline < 2:
            pygame.draw.line(screen, (20,20,20), transform(p[0]), transform(p[1]), 1) 
        inline = 0




    for r in pRegions:
        if len(r) > 2:
            pygame.draw.polygon(screen, randomColor(), transformList(r)) 

    for p in points:
        pygame.draw.circle(screen, (0,0,0), transform(p), RADIUS)


    pygame.display.flip()
    screen.fill(white)
    while 1:
        print()