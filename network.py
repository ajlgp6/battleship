import socket
import consts as c
from grid import Grid
from ship import Ship

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
            print(f"received \"{data}\" from {address}")
            
            if data.find(":") == -1:
                print(f"Malformed packet: \"{data}\"")
                continue
            elif data == "connect:":
                self.send("connected", address)
                self.clients[address] = GameState()
                continue

            command = data.split(":")
            state = self.clients[address]
            grid = state.grid

            # Update the client side grid state. "grid:"
            if command[0] == "grid":
                self.send(str(grid), address)

            # Place a new ship. "ship:1,2,1,6"
            elif command[0] == "ship":
                points = []
                for i in command[1].split(','):
                    points.append(int(i))
                
                state.addShip(points)

            # Fire at a grid coordinate
            elif command[0] == "fire":
                points = []
                for i in command[1].split(','):
                    points.append(int(i))
                
                current = grid[points]
                newState = c.Grid.MISSED
                if current == c.Grid.EMPTY:
                    newState = c.Grid.MISSED
                elif current == c.Grid.SHIP:
                    newState = c.Grid.SHIP_HIT
                else:
                    print(f"Unknown current grid state {state}")
                    continue

                grid.update(points, newState)

            self.clients[address] = state

    def send(self, raw, address):
        self.s.sendto(raw.encode('utf-8'), address)

class Client:
    def __init__(self, server):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = server

    def send(self, raw):
        if raw.find(':') == -1:
            raw += ':'

        print(f"sending \"{raw}\"")
        data = raw.encode('utf-8')
        self.s.sendto(data, (self.address, c.Networking.PORT))

    def recv(self):
        raw, address = self.s.recvfrom(4096)
        data = raw.decode('utf-8')
        print(f"received \"{data}\" from {address}")
        return data

class GameState:
    def __init__(self):
        self.grid = Grid()
        self.ships = []
    
    def addShip(self, points):
        first = (points[0], points[1])
        second = (points[2], points[3])

        ship = Ship(first, second)
        self.ships.append(ship)
        self.grid.addShip(ship)

if __name__ == "__main__":
    s = Server()
    s.run()
