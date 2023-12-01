import pygame
import random, time
from constants import *
import screenconstants

# pygame.font.init()
# my_font = pygame.font.SysFont('Comic Sans MS', 30)



SOLVED = False
LEFT_MOV = [
    ["1","0","3","2"], # Up
    ["2","1","0","3"], # Right
    ["3","2","1","0"], # Down
    ["0","3","2","1"]  # Left
]

RIGHT_MOV = [
    ["3","0","1","2"], # Up
    ["0","1","2","3"], # Right
    ["1","2","3","0"], # Down
    ["2","3","0","1"]  # Left
]

FPS = 60
clock = pygame.time.Clock()

win = pygame.display.set_mode((screenconstants.C_WIDTH*screenconstants.CELL_SIZE, screenconstants.C_HEIGHT*screenconstants.CELL_SIZE))

# Maze Generation

class Tile:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.visited = False
    def directions(self) -> list:
        return [self.up, self.right,self.down,self.left]
    def connect(self, i) -> None:
        if i.x < self.x:
            i.right = True
            self.left = True
        elif i.x > self.x:
            i.left = True
            self.right = True
        elif i.y > self.y:
            i.up = True
            self.down = True
        elif i.y < self.y:
            i.down = True
            self.up = True
        self.visited = True
        i.visited = True

class Maze:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

        self.data = [[Tile(x,y) for x in range(self.width)]for y in range(self.height)]
    
    def get_near(self,t) -> list:
        near = []
        for i in DIRECTIONS:
            try:
                new = self.data[t.y+i[1]][t.x+i[0]]
                if (new.x-t.x) + (new.y-t.y) == 1 or (new.x-t.x) + (new.y-t.y) == -1:
                    near.append(new)
            except IndexError: continue
        return near
    
    def walk(self):
        # start
        x = 0
        y = 0
        current = self.data[y][x]
        path = [current]
        walking = True
        while walking:
            win.fill((0,0,0))
            self.draw_maze((0,255,255), current)
            # Checking possible routes
            adjacent_values = self.get_near(current)
            possible_values = []
            for i in adjacent_values:
                if not(i.visited):
                    possible_values.append(i)
            
            # Backtrack if deadend
            while len(possible_values) == 0 and len(path)-1 > 0:
                win.fill((0,0,0))
                self.draw_maze((255,0,0), current)
                path.pop()
                current = path[len(path)-1]
                adjacent_values = self.get_near(current)
                possible_values = []
                for i in adjacent_values:
                    if not(i.visited):
                        possible_values.append(i)
                pygame.display.update()
            if len(possible_values) > 0:
                value = random.choice(possible_values)
                path.append(value)
                current.connect(value)
                current = value
            else: walking = False
            pygame.display.update()
        print("Maze created")

    def draw_maze(self, colour=(0,255,255), current=None):
        pygame.draw.rect(win,(255,215,0), ((screenconstants.C_WIDTH-1)*screenconstants.CELL_SIZE,(screenconstants.C_HEIGHT-1)*screenconstants.CELL_SIZE,screenconstants.CELL_SIZE,screenconstants.CELL_SIZE))
        if current:
            pygame.draw.rect(win,colour,((screenconstants.C_WIDTH-1)*screenconstants.CELL_SIZE,current.y*screenconstants.CELL_SIZE,screenconstants.CELL_SIZE,screenconstants.CELL_SIZE))
            pygame.draw.rect(win,colour,(current.x*screenconstants.CELL_SIZE,(screenconstants.C_HEIGHT-1)*screenconstants.CELL_SIZE,screenconstants.CELL_SIZE,screenconstants.CELL_SIZE))
            pygame.draw.rect(win,(255,255,255),(current.x*screenconstants.CELL_SIZE,current.y*screenconstants.CELL_SIZE,screenconstants.CELL_SIZE,screenconstants.CELL_SIZE))
        for y,i in enumerate(self.data):
            for x,t in enumerate(i):
                if t.visited:
                    if not(t.up):
                        pygame.draw.line(win,(255,255,255),(x*screenconstants.CELL_SIZE,y*screenconstants.CELL_SIZE),((x+1)*screenconstants.CELL_SIZE-1,y*screenconstants.CELL_SIZE))
                    if not(t.down):
                        pygame.draw.line(win,(255,255,255),(x*screenconstants.CELL_SIZE,(y+1)*screenconstants.CELL_SIZE-1),((x+1)*screenconstants.CELL_SIZE-1,(y+1)*screenconstants.CELL_SIZE-1))
                    if not(t.left):
                        pygame.draw.line(win,(255,255,255),(x*screenconstants.CELL_SIZE,y*screenconstants.CELL_SIZE),(x*screenconstants.CELL_SIZE,(y+1)*screenconstants.CELL_SIZE-1))
                    if not(t.right):
                        pygame.draw.line(win,(255,255,255),((x+1)*screenconstants.CELL_SIZE-1,y*screenconstants.CELL_SIZE),((x+1)*screenconstants.CELL_SIZE-1,(y+1)*screenconstants.CELL_SIZE-1))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        clock.tick(FPS)


# Maze Solving - v1 : sticking to sides and skipping dead ends
class Solver:
    def __init__(self, data, movement_list) -> None:
        self.colour = (random.randrange(100,200),random.randrange(100,200),random.randrange(100,200))
        self.colourR = (random.randrange(100,200),random.randrange(100,200),random.randrange(100,200))
        self.cutoff = False
        self.path = []
        self.cutoff_path = []
        self.directions = list("0123")
        self.directions_doubled = list("01230123")
        self.movement_list = movement_list
        self.maze = data

        self.x = 0
        self.y = 0
        self.current_direction = "1"
    
    def calculate_next_direction(self):
        current_tile = self.maze[self.y][self.x]
        move_direction = None
        # print()
        for i in range(4):
            direction = self.movement_list[int(self.current_direction)][i]
            # print(current_tile.directions(),direction)
            if current_tile.directions()[int(direction)]:
                move_direction = direction
                break
        # print(move_direction,i)
        if i == 3:
            self.cutoff = True      
        return move_direction

    def move(self):
        self.path.append((self.x,self.y))
        if self.y == len(self.maze)-1 and self.x == len(self.maze[0])-1:
            self.path.append((len(self.maze[0])-1,len(self.maze)-1))
            return True
        #print(self.x,self.y)
        new_direction = str(self.calculate_next_direction())
        if self.cutoff:
            self.cutoff_path.append((self.x,self.y))

        if new_direction == "0":
            self.y -= 1
        if new_direction == "2":
            self.y += 1
        if new_direction == "3":
            self.x -= 1
        if new_direction == "1":
            self.x += 1
        
        if self.cutoff:
            if not((self.x, self.y) in self.path):
                self.cutoff_path.pop()
                for i in self.cutoff_path:
                    while i in self.path:
                        self.path.remove(i)
                self.cutoff_path = []
                self.cutoff = False
        self.current_direction = new_direction
        return False
    
    def draw_path(self, f = False):
        for t in self.path:
            if f:
                if not(t in self.cutoff_path):
                    pygame.draw.rect(win, (255,0,0), (t[0]*screenconstants.CELL_SIZE,t[1]*screenconstants.CELL_SIZE,screenconstants.CELL_SIZE,screenconstants.CELL_SIZE))
            elif t in self.cutoff_path and not(f): pygame.draw.rect(win, self.colourR, (t[0]*screenconstants.CELL_SIZE,t[1]*screenconstants.CELL_SIZE,screenconstants.CELL_SIZE,screenconstants.CELL_SIZE))
            else: pygame.draw.rect(win, self.colour, (t[0]*screenconstants.CELL_SIZE,t[1]*screenconstants.CELL_SIZE,screenconstants.CELL_SIZE,screenconstants.CELL_SIZE))
            


def main():
    maze = Maze(screenconstants.C_WIDTH,screenconstants.C_HEIGHT)
    maze.walk()
    solverL = Solver(maze.data,LEFT_MOV)
    solverR = Solver(maze.data,RIGHT_MOV)
    x = False
    y = False
    run = True
    while run:
        win.fill((0,0,0))
        x = solverL.move()
        solverL.draw_path()
        y = solverR.move()
        solverR.draw_path()
        maze.draw_maze()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if x or y:
            print(x,y)
            for i in range(100):
                win.fill((0,0,0))
                if solverL.move(): 
                    solverL.draw_path(True)
                elif solverR.move(): 
                    solverR.draw_path(True)
                maze.draw_maze()
                pygame.display.update()
            
            screenconstants.C_WIDTH*=2
            screenconstants.C_HEIGHT*=2
            screenconstants.CELL_SIZE/=2
            maze = Maze(screenconstants.C_WIDTH,screenconstants.C_HEIGHT)
            maze.walk()
            solverL = Solver(maze.data,LEFT_MOV)
            solverR = Solver(maze.data,RIGHT_MOV)

        pygame.display.update()
        clock.tick(FPS)


        # for _ in range(screenconstants.C_WIDTH*screenconstants.C_HEIGHT*16):
        #     maze.draw_maze((0,0,0))
        #     best = 0
        #     for c in creatures:
        #         c.move()
        #         if c.distance > best: 
        #             best = c.distance
        #             c.keep = True
        #         else:
        #             c.keep = False
        #         pygame.draw.rect(win,c.colour,(c.x*screenconstants.CELL+1,c.y*screenconstants.CELL+1,screenconstants.CELL-2,screenconstants.CELL-2))
            
        #     text_surface = my_font.render(str(_)+"/"+str(screenconstants.C_HEIGHT*screenconstants.C_HEIGHT*16), False, (255, 255, 255))
        #     win.blit(text_surface, (8,screenconstants.C_HEIGHT*screenconstants.CELL-30))
            
        #     pygame.display.update()

        # maze = Maze(screenconstants.C_WIDTH,screenconstants.C_HEIGHT)
        # maze.walk()
        # creatures.sort(key=sort_d,reverse=True)
        # winner = creatures[0]
        # print(winner.distance)
        # creatures = [Walker0(maze.data, winner) for _ in range(999)]
    pygame.quit()


if __name__=="__main__":
    main()
