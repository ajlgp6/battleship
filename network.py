import socket, secrets, sys
import consts as c
from grid import Grid
from ship import Ship

isDebug = False

def debug(msg):
    if not isDebug:
        return

    print(f"[DBG] {msg}")

class Server:
    def __init__(self):
        self.clients = dict()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((c.Networking.BIND, c.Networking.PORT))
        print(f"Server listening on {c.Networking.BIND} on port {c.Networking.PORT}")

    def run(self):
        while True:
            raw, address = self.s.recvfrom(4096)
            data = raw.decode('utf-8')
            debug(f"{address}:{data}")
            
            if data.find(":") == -1:
                debug(f"(malformed)")
                continue

            command = data.split(":")

            if command[0] == "connect":
                code = ""
                if len(command) >= 1:
                    code = command[1]

                state = GameState(code)
                code = state.code   # The code may have been auto generated, so update it from the game state
                self.clients[address] = state

                self.send(f"connected:{code},{isDebug}", address)
                print(f"{address} joined game {code}")
                continue

            state = self.clients[address]
            grid = state.grid

            # Return the client side grid state. "grid:"
            if command[0] == "grid":
                self.send(str(grid), address)
            
            # Return the redacted state of the opponent's grid. "grid-opponent:"
            elif command[0] == "grid-opponent":
                try:
                    opponent, addr = self.getOpponentGrid(address)
                    self.send(opponent.toString(True), address)
                except ValueError as ex:
                    print(f"[WRN] {ex}")
                    self.send("", address)

            # Place a new ship. "ship:1,2,1,6"
            elif command[0] == "ship":
                points = []
                for i in command[1].split(','):
                    points.append(int(i))
                
                state.addShip(points)

            # Fire at a grid coordinate. "fire:1,2"
            elif command[0] == "fire":
                points = []
                for i in command[1].split(','):
                    points.append(int(i))

                try:
                    opponent, addr = self.getOpponentGrid(address)
                    
                    current = opponent[points]
                    newState = c.Grid.MISSED
                    if current == c.Grid.EMPTY:
                        newState = c.Grid.MISSED
                    elif current == c.Grid.SHIP:
                        newState = c.Grid.SHIP_HIT
                    else:
                        print(f"Unknown current grid state {state}")
                        continue

                    # Update the opponents grid
                    self.clients[addr].grid.update(points, newState)

                    # Send back the new state for immediate display
                    self.send(str(newState), address)

                except ValueError as ex:
                    print(f"[WRN] {ex}")
                    self.send("", address)

            # Request an update about the game state. "stats:"
            elif command[0] == "stats":
                opponentReady = "wait"
                opponent = None
                ships = 0

                # First number: is the opponent ready?
                try:
                    opponent = self.clients[self.findOpponent(addr)]
                    if opponent.allShipsPlaced():
                        opponentReady = "ready"
                except:
                    # Opponent isn't here yet, ignore
                    pass

                if opponentReady == "ready":
                    # Second number: number of opponent ships still afloat
                    for ship in opponent.grid.ships:
                        if ship.isAlive():
                            ships += 1

                self.send(f"{opponentReady},{ships}", address)

            self.clients[address] = state

    def send(self, raw, address):
        debug(f"sending \"{raw}\"")
        self.s.sendto(raw.encode('utf-8'), address)

    # Finds the opponent of an address by searching for a member with the same code but different address
    def findOpponent(self, address):
        code = self.clients[address].code
        for addr in self.clients:
            current = self.clients[addr]
            if current.code == code and addr != address:
                return addr
        
        raise ValueError(f"Unable to find opponent for {address}")

    def getOpponentGrid(self, address):
        opponentAddr = self.findOpponent(address)
        return self.clients[opponentAddr].grid, opponentAddr

class Client:
    def __init__(self, server):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = server

    def connect(self, code):
        global isDebug

        self.send(f"connect:{code}")
        resp = self.recv()

        # Should return "connected:CODE,DEBUG"
        if resp.find("connected") == -1:
            raise Exception("Failed to receive connection handshake")
        else:
            details = resp.split(':')[1].split(',')

            self.code = details[0]
            isDebug = (details[1] == 'True')

            return self.code

    def send(self, raw):
        if raw.find(':') == -1:
            raw += ':'

        debug(f"sending \"{raw}\"")
        data = raw.encode('utf-8')
        self.s.sendto(data, (self.address, c.Networking.PORT))

    def recv(self):
        raw, address = self.s.recvfrom(4096)
        data = raw.decode('utf-8')
        debug(f"received \"{data}\" from {address}")
        return data

    def debug(self, msg):
        debug(msg)

    # Helper functions
    def placeShip(self, start, end):
        self.send(f"ship:{start[0]},{start[1]},{end[0]},{end[1]}")

    def fire(self, pos):
        self.send(f"fire:{pos[0]},{pos[1]}")
        return int(self.recv())

    def updateGrid(self):
        self.send("grid")

    def updateOpponentGrid(self):
        self.send("grid-opponent")

class GameState:
    def __init__(self, code=""):
        self.grid = Grid()

        self.code = code
        if self.code == "":
            self.code = secrets.token_hex(2)

    def __repr__(self):
        return f"{self.code}: {self.grid.ships}"
    
    def addShip(self, points):
        first = (points[0], points[1])
        second = (points[2], points[3])

        ship = Ship(first, second)
        self.grid.addShip(ship)

    def allShipsPlaced(self):
        return len(self.grid.ships) == 5

if __name__ == "__main__":
    isDebug = len(sys.argv) > 1 and sys.argv[1] == "-d"

    s = Server()
    s.run()
