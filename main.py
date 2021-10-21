import random
from graphics import *

def generateRandomPoints(N):
    points = []
    
    zoomOut = 0.9

    for n in range(N):
        points.append((random.randint(-WIDTH//2*zoomOut, WIDTH//2*zoomOut),(random.randint(-HEIGH//2*zoomOut, HEIGH//2*zoomOut)))) 

    return list(set(points))

def main():
    N = 10
    run(generateRandomPoints(N))


if __name__ == "__main__":
    main()