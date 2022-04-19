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

class Vector3:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    def distanceTo(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)
    def __add__(self, v2):
        return Vector3(self.x + v2.x, self.y + v2.y, self.z + v2.z)
    def __sub__(self, v2):
        return Vector3(self.x - v2.x, self.y - v2.y, self.z - v2.z)
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    def __truediv__(self, scalar):
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'

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

def buildEmpty3DArray(x, y, z):
    out = []
    for i in range(x):
        a = []
        for j in range(y):
            b = []
            for k in range(z):
                b.append(None)
            a.append(b)
        out.append(a)
    return out

directions = [
    Vector3(-1, -1, -1),
    Vector3(-1, -1, 0),
    Vector3(-1, -1, 1),
    Vector3(-1, 0, -1),
    Vector3(-1, 0, 0),
    Vector3(-1, 0, 1),
    Vector3(-1, 1, -1),
    Vector3(-1, 1, 0),
    Vector3(-1, 1, 1),
    Vector3(0, -1, -1),
    Vector3(0, -1, 0),
    Vector3(0, -1, 1),
    Vector3(0, 0, -1),
    Vector3(0, 0, 0),
    Vector3(0, 0, 1),
    Vector3(0, 1, -1),
    Vector3(0, 1, 0),
    Vector3(0, 1, 1),
    Vector3(1, -1, -1),
    Vector3(1, -1, 0),
    Vector3(1, -1, 1),
    Vector3(1, 0, -1),
    Vector3(1, 0, 0),
    Vector3(1, 0, 1),
    Vector3(1, 1, -1),
    Vector3(1, 1, 0),
    Vector3(1, 1, 1)
]

def buildImageOfSlice(resolution, z, gridSize, colorGrid):
    image = Image.new('RGB', (resolution.x, resolution.y))
    pixels = image.load()
    gridNumZ = int(z / gridSize)
    numGrids = (resolution.x / gridSize, resolution.y / gridSize, resolution.z / gridSize)
    print(z)
    for x in range(resolution.x):
        for y in range(resolution.y):
            gridNumX = int(x / gridSize)
            gridNumY = int(y / gridSize)
            position = Vector3(x, y, z);
            closestColor = None
            closestDistance = math.inf
            for direction in directions:
                checkingGridX = gridNumX + direction.x
                checkingGridY = gridNumY + direction.y
                checkingGridZ = gridNumZ + direction.z
                position = Vector3(x, y, z)
                #print(checkingGridX, checkingGridY, checkingGridZ)
                shifts = Vector3(0, 0, 0)
                while(checkingGridX >= numGrids[0]):
                    checkingGridX = 0
                    shifts.x = shifts.x + 1
                while(checkingGridY >= numGrids[1]):
                    checkingGridY = 0
                    shifts.y = shifts.y + 1
                while(checkingGridZ >= numGrids[2]):
                    checkingGridZ = 0
                    shifts.z = shifts.z + 1
                while(checkingGridX < 0):
                    checkingGridX = int(numGrids[0]) - 1
                    shifts.x = shifts.x - 1
                while(checkingGridY < 0):
                    checkingGridY = int(numGrids[1]) - 1
                    shifts.y = shifts.y - 1
                while(checkingGridZ < 0):
                    checkingGridZ = int(numGrids[2]) - 1
                    shifts.z = shifts.z - 1
                #print(checkingGridX, checkingGridY, checkingGridZ)

                offset = colorGrid[checkingGridX][checkingGridY][checkingGridZ][0]
                offset = offset + Vector3(resolution.x * shifts.x, resolution.y * shifts.y, resolution.z * shifts.z)
                color = colorGrid[checkingGridX][checkingGridY][checkingGridZ][1]
                distance = (offset - position).length()
                if(distance < closestDistance):
                    closestDistance = distance
                    closestColor = color
            #pixels[x,y] = (gridNumX, gridNumY, gridNumZ)
            pixels[x,y] = closestColor
            #distanceNum = int(closestDistance) ** 2 * 5
            #pixels[x,y] = (distanceNum, 0, 0)
    return image

def main():
    #resolution = Vector3(1920, 1080, 1920)
    resolution = Vector3(64, 64, 16)
    numHorizontalGrids = 8
    numDepthSlices = 32
    gridSize = resolution.x / numHorizontalGrids
    if(resolution.y % (resolution.x / numHorizontalGrids) != 0):
        print("Width / numHorizontalGrids must evenly divide height")
        return
    if(resolution.z % (resolution.x / numHorizontalGrids) != 0):
        print("Width / numHorizontalGrids must evenly divide depth")
        return
    numVerticalGrids = int(resolution.y / gridSize)
    numDepthGrids = int(resolution.z / gridSize)
    grid = buildEmpty3DArray(numHorizontalGrids, numVerticalGrids, numDepthGrids)
    
    print(numHorizontalGrids, numVerticalGrids, numDepthGrids)
    for x, yz in enumerate(grid):
        for y, zLine in enumerate(yz):
            for z, value in enumerate(zLine):
                grid[x][y][z] = (   Vector3(x * gridSize, y * gridSize, z * gridSize) + 
                                    Vector3(
                                        random.uniform(0, gridSize),
                                        random.uniform(0, gridSize),
                                        random.uniform(0, gridSize)
                                ), basicRandomColor())
    

    for i in range(numDepthSlices):
        print(f"Building image {i}/{numDepthSlices-1}");
        image = buildImageOfSlice(resolution, (i * (resolution.z/numDepthSlices)), gridSize, grid)
        image.save(f"./out/image{i}.png")

    #image = Image.new('RGB', (resolution.x, resolution.y))
    #pixels = image.load()
    #image.save("./out.png")

if __name__ == '__main__':
    main()