import consts as c
from ship import Ship

class Grid:
    """Tracks the state of a battleship grid."""

    def __init__(self):
        self.grid = []
        self.ships = []

        width = c.Drawing.SQUARES
        for row in range(width):
            self.grid.append([])
            for _ in range(width):
                self.grid[row].append(c.Grid.EMPTY)

    # High level ship operations (add ship)
    def addShip(self, ship):
        self.ships.append(ship)

        coords = ship.getParts()
        for pair in coords:
            if ship.getSize() == 5:
                self.update(pair, c.Grid.SHIP2)
            elif ship.getSize() == 4:
                self.update(pair, c.Grid.SHIP1)
            elif ship.getSize() == 3:
                self.update(pair, c.Grid.SHIP3)
            elif ship.getSize() == 2:
                self.update(pair, c.Grid.SHIP4)

    # Low level array operations
    def __getitem__(self, index):
        x = index[0]
        y = index[1]
        return self.grid[x][y]

    def getRow(self, row):
        return self.grid[row]

    def update(self, index, newState):
        x = index[0]
        y = index[1]
        self.grid[x][y] = newState

        if newState == c.Grid.SHIP_HIT:
           for ship in self.ships:
               if ship.hasSquare(index):
                    ship.damaged += 1

    # Serialization
    def load(self, state):
        for raw in state.split(';'):
            parts = raw.split(',')
            x = int(parts[0])
            y = int(parts[1])
            s = int(parts[2])
            self.grid[x][y] = s

    def toString(self, hideShips = False):
        ret = ""
        width = len(self.grid[0])

        for i in range(width):
            for j in range(width):
                state = self.grid[i][j]

                if hideShips and (state == c.Grid.SHIP1 or state == c.Grid.SHIP2 or state == c.Grid.SHIP3 or state == c.Grid.SHIP4):
                    state = c.Grid.EMPTY
                    
                ret += f"{i},{j},{state};"

        return ret[:-1]

    def __str__(self):
        return self.toString(False)