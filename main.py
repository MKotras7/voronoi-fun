import math
import random
from PIL import Image, ImageDraw

class Vector2:
    def __init__(self):
        self.x = 0
        self.y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
    def distanceTo(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    def __add__(self, v2):
        return Vector2(self.x + v2.x, self.y + v2.y)
    def __sub__(self, v2):
        return Vector2(self.x - v2.x, self.y - v2.y)
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)
    def __repr__(self):
        return f'({self.x}, {self.y})'

def basicRandomColor():
    return (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))

def grayScaleRandomColor(min = 0, max = 255):
    value = random.randrange(min, max)
    return (value, value, value)

def generateRandomPoints(numPoints, bound1, bound2):
    output = []
    for i in range(numPoints):
        output.append(Vector2(random.uniform(bound1.x, bound2.x), random.uniform(bound1.y, bound2.y)))
    return output

def main():
    #resolution = Vector2(640, 360)
    resolution = Vector2(1920, 1080)
    pointCount = 75
    image = Image.new('RGB', (resolution.x, resolution.y))
    pixels = image.load()
    points = generateRandomPoints(pointCount, Vector2(0, 0), resolution)
    #colors = [grayScaleRandomColor(50, 150) for x in range(pointCount)]
    colors = [basicRandomColor() for x in range(pointCount)]
    for x in range(resolution.x):
        for y in range(resolution.y):
            thisPosition = Vector2(x, y)
            pixels[x, y] = colors[0]
            closestDistance = math.inf
            indices = [x for x in range(pointCount)]
            sortedIndices = sorted(indices, key = lambda index: thisPosition.distanceTo(points[index]))
           
            #point0 = points[sortedIndices[0]]
            #point1 = points[sortedIndices[1]]
            #point2 = points[sortedIndices[2]]
            #dist10 = point0-point1
            #dist12 = point1-point2
            #dist20 = point2-point0
            #maxSlope = max(
            #    (dist10.y / dist10.x),
            #    (dist12.y / dist12.x),
            #    (dist20.y / dist20.x)
            #)
            color = colors[sortedIndices[0]]
            #maxSlope = int(maxSlope * 5)
            #color = (color[0] + maxSlope, color[1] + maxSlope, color[2] + maxSlope)
            pixels[x, y] = color
    image.save("./out.png")

if __name__ == '__main__':
    main()