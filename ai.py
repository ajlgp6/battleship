import consts as c
import random as r
from grid import Grid

class AI:
    def __init__(self, intel):
        # Records the initelligence of this particular AI
        self.intel = intel

        # Holds the number of available spaces to shoot at
        self.guesses = list(range(c.Drawing.SQUARES*c.Drawing.SQUARES))
        r.shuffle(self.guesses)

        # Holds the rows that have yet to be "officially" checked (only used
        # with smart AIs)
        self.rows = list(range(c.Drawing.SQUARES))
        r.shuffle(self.rows)

        # Holds the spaces that should be fired at next
        self.stack = []

        # Records whether the last move hit a ship
        self.hit = False

        # Records the space of the last move
        self.currentHit = -1

    # Returns the coord (y, x) values of the selected grid space. This spacce
    # will the be removed from the guesses list.
    def indices(self,spot):
        y = int(spot/c.Drawing.SQUARES)
        x = int(spot%c.Drawing.SQUARES)
        self.currentHit = spot
        self.guesses.remove(spot)
        return (y, x)

    # Records the spaces surrounding the hit ship. If the spaces have not been
    # hit yet, they will be pushed onto the stack to be fired at later.
    def possibleHits(self,hit):
        # Calculate the space values that are touching the hit ship space
        north = int(self.currentHit-c.Drawing.SQUARES)
        east = int(self.currentHit+1)
        south = int(self.currentHit+c.Drawing.SQUARES)
        west = int(self.currentHit-1)
        dir = [west,south,east,north]

        # If the next spot is available
        for spot in dir:
            if spot in self.guesses:
                # Fire at that spot
                self.stack.append(spot)
        return

    # The algorithm for each move depends on the intelligence of the AI
    def move(self,resp):
        self.hit = bool(resp)

        # As long as there are remaining guesses
        if len(self.guesses) >= 1:
            # If a hit was made
            if self.hit:
                self.possibleHits(self.currentHit)

            # If the stack includes spaces, shoot the spaces
            if len(self.stack) > 0:
                return self.indices(self.stack.pop())

            # If there is nothing to go off of, continue with the basic
            # algorithm tied to your AI

            # The Smart AI algorithm
            elif self.intel:
                # Ensure that there are untouched rows
                if len(self.rows) > 0:
                    # Grab some random row
                    row = self.rows[0]
                    self.rows.remove(row)

                    # Calculate the spots of this row's checkerboard pattern
                    for i in range(int(c.Drawing.SQUARES/2)):
                        space = (10 * row) + (2 * i) + (row % 2)

                        # If this space has not been hit add it onto the stack
                        if space in self.guesses:
                            self.stack.insert(0,space)

                    # Make a recursive call to fire at the board
                    return self.move(self.hit)

                # Otherwise, all the checkerboard spots have been hit (in this
                # case, the AI should've won due to the strategy) so just fire
                # randomly until all spaces have been hit
                else:
                    guess = self.guesses[0]
                    return self.indices(int(guess))

            # The Dumb AI algorithm
            else:
                # Make a random guess from the available spaces
                guess = self.guesses[0]
                return self.indices(int(guess))

        # Otherwise, no more spaces are available
        else:
            return (-1,-1)

    # Checks if there are any squares along the supposed path that are already in use
    # Returns a tuple of integers (or a tuple of -1 stating that the path doesn't work)
    def isAvailable(self, i: int, size: int, available: (int), vertical: bool) -> (int):
        # These are used to keep track of the previous indices and ensure the ship is
        # completely vertical or completely horizontal
        old_x = -1
        old_y = -1

        # Holds the approved index number (combo of x and y) to be sent out
        approved = []

        # Go through and check each block of the ship in this direction
        for s in range(size):

            # If we are checking vertically, the index number will be updated by the
            # size of the matrix
            if vertical:
                pos = i + (s*c.Drawing.SQUARES)
            # Otherwise, for horizontal changes increment the number by 1
            else:
                pos = i + s

            # This gives us the x and y coords
            y = int(pos/c.Drawing.SQUARES)
            x = int(pos%c.Drawing.SQUARES)

            # Add s to i and see if it exists in the list
            if(pos not in available or (x >= c.Drawing.SQUARES or y >= c.Drawing.SQUARES)):
                return (-1)

            # And ensure that the ship is only vertical or horizontal
            elif (old_x != -1 and old_x != x) and (old_y != -1 and old_y != y):
                return (-1)

            # This block can be used by the ship
            approved.append(pos)

            # Keep track of the current x and y's while you check the other block
            old_x = x
            old_y = y
        return tuple(approved)

    # Assuming that the ship can be placed in this spot and with this orientation,
    # this function gives us the endpoint for the ship and updates the tuple of
    # available indices
    def tryOrientation(self, i: int, size: int, available: (int), vertical: bool) -> (int,int):
        # If the ship is vertical
        if vertical:

            # Find our index number's respective coords
            y = int(i/c.Drawing.SQUARES)
            x = int(i%c.Drawing.SQUARES)

            # Update said coords
            new_y = y+size-1

            # Go through and remove these indices from the available tuple
            for s in range(size):
                taken = (i + (s*c.Drawing.SQUARES))
                available.remove(taken)

            # Return the endpoint of the ship
            return (new_y, x)

        # Otherwise, the ship is horizontal
        else:

            # Find our index number's respective coords
            y = int(i/c.Drawing.SQUARES)
            x = int(i%c.Drawing.SQUARES)

            # Ensure that we will not go out of bounds while updating
            if x+size-1 >= c.Drawing.SQUARES:
                new_y = y+1
                new_x = x+size-1 - c.Drawing.SQUARES
            else:
                new_y = y
                new_x = x+size-1

            # Go through and remove these indices from the available tuple
            for s in range(size):
                taken = (i+s)
                available.remove(taken)

            # Return the endpoint of the ship
            return (new_y, new_x)

    # Generates a grid with randomly placed ships
    # Returns a list of ships to be placed, in the form of a tuple of two tuples:
    # the start position and the end position
    def generate(self):
        ships = []

        # Create a tuple of the available index numbers(0 represents [0][0],
        # 1 represents [0][1], etc.) and shuffle its order
        indices = list(range(c.Drawing.SQUARES*c.Drawing.SQUARES))
        r.shuffle(indices)

        # Array of the ship sizes (MAY NEED TO UPDATE THIS)
        ship_sizes = (5, 4, 3, 3, 2)

        # For each ship
        for ship in ship_sizes:

            # Pull out an available index number
            for index in indices:

                # Randomly decide whether the ship will be vertical or horizontal
                vertical = bool(r.getrandbits(1))

                # Acquire the x and y coords from the index number
                y = int(index/c.Drawing.SQUARES)
                x = int(index%c.Drawing.SQUARES)

                # Attempt to fit the ship with its orientation starting at the index
                # number
                if self.isAvailable(index, ship, indices, True) != (-1):
                    # If it fits, append this ship onto the array with its start and
                    # end point
                    pt = self.tryOrientation(index, ship, indices, True)
                    ships.append(((y, x), pt))
                    break

                # Try the opposite orientation at the same starting point
                elif self.isAvailable(index, ship, indices, not vertical) != (-1):
                    # If it fits, append this ship onto the array with its start and
                    # end point
                    pt = self.tryOrientation(index, ship, indices, not vertical)
                    ships.append(((y, x), pt))
                    break
        return ships
