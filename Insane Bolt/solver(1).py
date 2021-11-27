from pwn import *

from astar import AStar
import math

class Solver(AStar):
    def __init__(self, raw):
        lines = raw.split(b'\n')
        lines = lines[1:-2]

        for i in range(len(lines)):
            lines[i] = (lines[i].replace(b"\xf0\x9f\x94\xa5", b"W") # Walls
                .replace(b"\xe2\x98\xa0\xef\xb8\x8f", b".") # Empty
                .replace(b"\xf0\x9f\xa4\x96", b"R") # Robot
                .replace(b"\xf0\x9f\x94\xa9", b"S") # Screw
                .replace(b"\xf0\x9f\x92\x8e", b"D") # Diamond
                .replace(b" ", b""))

        self.lines = lines
        self.width = len(self.lines[0])
        self.height = len(self.lines)

    def heuristic_cost_estimate(self, n1, n2):
        (x1, y1) = n1
        (x2, y2) = n2
        return math.hypot(x2 - x1, y2 - y1)

    def distance_between(self, n1, n2):
        return 1

    def neighbors(self, node):
        x, y = node

        return [
            (nx, ny)
            for nx, ny
            in [(x, y + 1), (x - 1, y), (x + 1, y)]
            if self.lines[y][x] in b'RDS'
        ]

def crack_raw(raw):
    solver = Solver(raw)

    # Find start and goal
    start = None
    end = None
    for y, line in enumerate(solver.lines):
        for x, c in enumerate(line):
            if c == ord('R'):
                start = (x, y)
            if c == ord('D'):
                end = (x, y)

    # Compute the path
    last = None
    path = b""
    for (x, y) in solver.astar(start, end):
        if last != None:
            if y > last[1]:
                path += b'D'
            elif x > last[0]:
                path += b'R'
            else:
                path += b'L'

        last = (x, y)

    return path

conn = remote("167.172.57.255", 30451)

conn.sendlineafter(b"> ", b"2")

with log.progress('Finding diamonds...') as p:
    for i in range(500):
        p.status(f"Searching for number {i}")

        raw = conn.recvuntil(b"> ")
        result = crack_raw(raw)
        conn.sendline(result)

conn.recvlines(4)

log.success(conn.recvlineS())
