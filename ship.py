import consts as c
import uuid

class Ship:
    def __init__(self, start, end):
        self.start = (0, 0)
        self.end = (0, 0)
        self.parts = []
        self.isVertical = False
        self.size = 0
        self.id = str(uuid.uuid4())
        self.damaged = 0

        # Ships can only be in a straight line
        if start[0] != end[0] and start[1] != end[1]:
            raise Exception("Ship must be placed either horizontally or vertically")
        
        self.isVertical = start[1] == end[1]
        if self.isVertical and start[0] > end[0]:
            tmp = start
            start = end
            end = tmp
        elif not self.isVertical and start[1] > end[1]:
            tmp = start
            start = end
            end = tmp

        self.start = start
        self.end = end

        if self.isVertical:
            diff = end[0] - start[0]
            for i in range(diff + 1):
                p = (start[0] + i, start[1])
                self.parts.append(p)
        
        else:
            diff = end[1] - start[1]
            for i in range(diff + 1):
                p = (start[0], start[1] + i)
                self.parts.append(p)

        self.size = len(self.parts)

    def getParts(self):
        return self.parts

    def getSize(self):
        return self.size

    def getID(self):
        return self.id

    def hasSquare(self, point):
        for part in self.parts:
            if part[0] == point[0] and part[1] == point[1]:
                return True
        
        return False

    def isAlive(self):
        return self.damaged < self.size

    def __str__(self):
        health = self.size - self.damaged
        return f"{self.id} from {self.start} to {self.end}, health: {health}/{self.size}, alive: {self.isAlive()}"