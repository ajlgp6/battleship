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

        if not self.isVertical:
            for i in range(end[1] - start[1] + 1):
                self.parts.append((start[0], start[1] + i))
        else:
            for i in range(end[0] - start[0] + 1):
                self.parts.append((start[0] + i, start[1]))
        
        self.size = len(self.parts)

    def getParts(self):
        return self.parts

    def getSize(self):
        return self.size

    def getID(self):
        return self.id

    def hasSquare(self, point):
        return point in self.parts

    def __str__(self):
        return f"{self.start} to {self.end}"