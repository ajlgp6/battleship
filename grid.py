import consts as c

class Grid:
    """Tracks the state of a battleship grid."""
    grid = []

    def __init__(self):
        width = c.Drawing.SQUARES
        for row in range(width):
            self.grid.append([])
            for _ in range(width):
                self.grid[row].append(c.Grid.EMPTY)

    def __getitem__(self, index):
        x = index[0]
        y = index[1]
        return self.grid[x][y]

    def update(self, index, newState):
        x = index[0]
        y = index[1]
        self.grid[x][y] = newState