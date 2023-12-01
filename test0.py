# Genetic algorithm or computational algorithm or both?

# Benefits of genetic algorithm
# - Already have knowledge on the processes of coding
# - Simple and can work with most scenarios of mazes
# - Potentialy slower and inefficient

# Benefits of computational algorithm
# - Potentially faster and the best route might be generated
# - Harder to code
# - May not work with all maze scenarios

# Benefits of both
# - Computational algorithm can supply score for genetic algorithm

# Building successful path
# - Make a straight line from start to end
# - Add a random amount of bends onto that path making sure to fix path to connect on outside
# - Repeat steps with new path until a path is made
# - To stop intersecting paths -> check if the additional tiles with collide with other tiles along route

# Setting tile data types
#
# -- Type 1 -- 
# - Each will have at least 2 directions
# - Up = 0
# - Down = 1
# - Left = 2
# - Right = 3
# - With this method a tile with up and down directions will be 01
#
# -- Type 2 --
# - A number consisting of 1's and 0's where each digit consists of a direction
# - Up = D0
# - Down = D1
# - Left = D2
# - Right = D3
# - With this method a tile with up and down directions will be 1100
# - This is helpful as combining tiles will be like the following:
# - if we have 0110 (Down and Left) and 0011 (Left and right) then we only need to change 0's to 1's if the other has a 1 in that position

# Route building algorithm
# -- ROOT PATH --
# - Straight line from start to end
# - Move some tiles
# - Repair path
# -- MOVING TILE --
# - Check above, below and next to target tile
# - Generate list of possible places to move
# - Move tile to one of those places
# -- REPAIRING PATH --
# - Look at old tiles connecting :  Look at directions within target tile
#                                   Invert the direction for new connections to target tile
#                                   For each secondary tile, if target tile is next to tertiary tile then move secondary tile to the tertiary tiles position
#                                   If not connected to tertiary tile then create tile between secondary tile and target tile containing opposite connectives of each


import pygame
import random, time
from constants import *

CELL_SIZE = 3
WIDTH_C = 128
HEIGHT_C = 128

win = pygame.display.set_mode((WIDTH_C*CELL_SIZE,HEIGHT_C*CELL_SIZE))

def invert_connections(tile) -> str:
    out = ""
    for i in tile:
        out += ("0"*int(i=="1"))+("1"*int(i=="0"))
    return out

def check_ignore(direction) -> int:
    if direction == UP: return "1" # Ignore Down
    if direction == DOWN: return "0" # Ignore Up
    if direction == LEFT: return "3" # Ignore Right
    if direction == RIGHT: return "2" # Ignore Left

def kept(x, minb, maxb):
    if x-2 > minb and x+2 < maxb:
        return True
    return False

class Maze:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height 
        
        self.start_tile = (int(width / 2), 0)
        self.end_tile = (int(width / 2), height - 1)

        self.maze = [["0000" for _x in range(width)] for _y in range(height)]
    
    def build_maze(self) -> None:
        initial_path_x = self.start_tile[0]
        for y, i in enumerate(self.maze):
            self.maze[y][initial_path_x] = "1100"
        while True:
            self.build_root_path()

    def check_available(self,direction_,x,y):
        if direction_ == UP:
            for i in UPS:
                if self.maze[y+i[1]][x+i[0]] == "0000":
                    return True
        if direction_ == DOWN:
            for i in DOWNS:
                if self.maze[y+i[1]][x+i[0]] == "0000":
                    return True
        if direction_ == RIGHT:
            for i in RIGHTS:
                if self.maze[y+i[1]][x+i[0]] == "0000":
                    return True
        if direction_ == LEFT:
            for i in LEFTS:
                if self.maze[y+i[1]][x+i[0]] == "0000":
                    return True

    def build_root_path(self) -> None:
        # Create initial path
        
        turned = False
        # Create turns
        turns = 0
        while not(turned):
            print(turned)
            turned = False
            self.draw_maze()
            for y, i in enumerate(self.maze):
                for x, j in enumerate(i):
                    if (j != "0000") and (x-1 > 0 and y-1 > 0 and x+1 < self.width and y+1 < self.height) and (random.randrange(0,10) > 5):
                        
                        
                        
                        #if good:
                            # Get directions that can be moved to
                            possible_directions = []
                            for a in DIRECTIONS:
                                if self.check_available(a,x,y): possible_directions.append(a)
                            print("Possible directions = ",possible_directions)
                            # Pick a random direction
                            if len(possible_directions) > 0:
                                direction = random.choice(possible_directions)
                                print("Chosen direction = ",direction)
                                # Move tile
                                
                                new_coords = [x+direction[0], y+direction[1]]
                                self.maze[new_coords[1]][new_coords[0]] = j
                                self.maze[y][x] = "0000"
                                print("previous coords = ", x,y, self.maze[y][x])
                                print("new coords = ", new_coords[0],new_coords[1])
                                
                                # -- Repair maze --
                                # Get secondary connections
                                connection_directions = []
                                for a,b in enumerate(j):
                                    if b == "1": connection_directions.append(DIRECTIONS[a])
                                print("Connection directions = ",connection_directions)
                                # Get secondary coords
                                st_0 = [x+connection_directions[0][0],y+connection_directions[0][1]]
                                st_1 = [x+connection_directions[1][0],y+connection_directions[1][1]]
                                
                                # Get tertiary connections
                                self.draw_maze()
                                for a, b in enumerate(self.maze[st_0[1]][st_0[0]]):
                                    if a != int(check_ignore(connection_directions[0])) and b == "1":
                                        st_0_direction = DIRECTIONS[a]
                                        
                                for a, b in enumerate(self.maze[st_1[1]][st_1[0]]):
                                    if a != int(check_ignore(connection_directions[1])) and b == "1":
                                        st_1_direction = DIRECTIONS[a]
                                # Get tertiary coords
                                self.draw_maze()
                                tt_0 = [st_0[0]+st_0_direction[0], st_0[1]+st_0_direction[1]]
                                tt_1= [st_1[0]+st_1_direction[0], st_1[1]+st_1_direction[1]]
                                # Get adjacent coords to new position of target tile
                                self.draw_maze()
                                adjacent_coords = []
                                for a in DIRECTIONS:
                                    adjacent_coords.append([new_coords[0]+a[0],new_coords[1]+a[1]])
                                # Check if tertiary coordinates are adjacent to target tile; if so then replace it with the secondary tile; if not then add a tile and change secondary tiles;
                                self.draw_maze()
                                st = [st_0, st_1]
                                tt = [tt_0, tt_1]
                                print("Secondary = ", st)
                                print("Tertiary = ",tt)
                                print("Adjacent_coords = ",adjacent_coords)
                                for a, b in enumerate(tt):
                                    
                                    if b in adjacent_coords: # If a tertiary tile connects to target tile
                                        self.maze[b[1]][b[0]] = self.maze[st[a][1]][st[a][0]]
                                        self.maze[st[a][1]][st[a][0]] = "0000"

                                    else: # If new tiles need to be created
                                        new_tile = ""
                                        new_st = ""
                                        for c,d in enumerate(self.maze[st[a][1]][st[a][0]]): # st[a] stores the currently in use secondary tile
                                            # d stores the on/off for the direction
                                            # c stores the index of the direction
                                            if (DIRECTIONS[c] == (connection_directions[a]) and d == "1"):
                                                new_st += "0"
                                                new_tile += "1"
                                            elif c == int(check_ignore(direction)):
                                                new_st += "0"
                                                new_tile += "1"
                                            else:
                                                new_st += "1"
                                                new_tile += "0"
                                        self.maze[st[a][1]][st[a][0]] = new_st
                                        self.maze[st[a][1]+direction[1]][st[a][0]+direction[0]] = new_tile
                                        

                            turned = True
                            turns += 1
                            break
                if turned:break
        
    def draw_maze(self):
        win.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
        for y, i in enumerate(self.maze):
            #out = str(y)+" "
            for x, j in enumerate(i):
                if "1" in j:
                    #out += "⬜"
                    if j[0] == "0":
                        pygame.draw.line(win,(255,0,0),(x*CELL_SIZE,y*CELL_SIZE),((x+1)*CELL_SIZE,y*CELL_SIZE),1)
                    if j[1] == "0": 
                        pygame.draw.line(win,(0,0,255),(x*CELL_SIZE,(y+1)*CELL_SIZE),((x+1)*CELL_SIZE,(y+1)*CELL_SIZE),1)
                    if j[2] == "0": 
                        pygame.draw.line(win,(0,255,0),(x*CELL_SIZE,y*CELL_SIZE),(x*CELL_SIZE,(y+1)*CELL_SIZE),1)
                    if j[3] == "0": 
                        pygame.draw.line(win,(0,255,0),((x+1)*CELL_SIZE,y*CELL_SIZE),((x+1)*CELL_SIZE,(y+1)*CELL_SIZE),1)
                #else:
                    #out += "⬛"
            #print(out)
        pygame.display.update()
        print()
        time.sleep(0.05)

def main():
    maze = Maze(WIDTH_C,HEIGHT_C)
    maze.build_maze()
    maze.draw_maze()
    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
        clock.tick(60)
    pygame.quit()

if __name__=="__main__":
    main()