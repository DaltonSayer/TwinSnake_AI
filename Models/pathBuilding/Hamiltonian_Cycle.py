import numpy as np
import random
import time
    
class Maze:
    LEFT_INDEX = 3
    RIGHT_INDEX = 1
    UP_INDEX = 0
    DOWN_INDEX = 2
    
    #Each [i][j] in the grid will be [leftOpen, rightOpen, upOpen, downOpen]
    def __init__(self, width, height):
        self.grid = np.zeros([width//2, height//2, 4], dtype=bool)
        self.width = width //2
        self.height = height//2
        self.frontier = []
        self.prims_maze()
        self.grid = self.scale_maze(self.grid)
        self.width = width
        self.height = height
    
    def remove_walls(self, index1 : list[int, int], index2 : list[int, int]):
        [x,y] = index1
        [i,j] = index2
        for _ in range(2):
            if([x,y] == [i-1, j]): #x,y is to the left
                self.grid[x][y][Maze.RIGHT_INDEX] = 1
                self.grid[i][j][Maze.LEFT_INDEX] = 1
                return
            elif([x,y] == [i, j-1]): #x,y is up
                self.grid[x][y][Maze.DOWN_INDEX] = 1
                self.grid[i][j][Maze.UP_INDEX] = 1
                return
            [x, y] = index2
            [i, j] = index1
    
    def prims_maze(self):
        frontier = []
        explored = []
        x = random.randint(0, self.width-1)
        y = random.randint(0, self.height-1)
        #left
        if(x-1 >= 0 and [x-1,y] not in explored):
            frontier.append([x-1, y])
        #right
        if(x+1 < self.width-1 and [x+1,y] not in explored):
            frontier.append([x+1, y])
        #up
        if(y-1 >= 0 and [x,y-1] not in explored):
            frontier.append([x, y-1])
        #down
        if(y+1 < self.height-1 and [x,y+1] not in explored):
            frontier.append([x, y+1])
        
        explored.append([x,y])
        
        while len(frontier) > 0:
            [x,y] = frontier.pop(random.randint(0, len(frontier)-1)) #one of the neighbours have been explored
            choices = []
            for [j, k] in [[x-1, y], [x+1, y], [x, y-1], [x, y+1]]:
                if(j >= 0 and j < self.width and k>= 0 and k < self.height):
                    if([j, k] not in explored and [j,k] not in frontier):
                        frontier.append([j,k])
                    else:
                        if([j,k] not in frontier):
                            choices.append([j,k]) #[j,k] is part of the tree

            [j,k] = choices.pop(random.randint(0, len(choices)-1))
            self.remove_walls([x,y], [j,k])
            explored.append([x,y])
    
    def scale_maze(self,grid):
        #double the size of the maze
        new_grid = np.zeros([len(grid)*2, len(grid[0])*2, 4])
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                vals = grid[x][y]
                left = vals[Maze.LEFT_INDEX]
                right = vals[Maze.RIGHT_INDEX]
                up = vals[Maze.UP_INDEX]
                down = vals[Maze.DOWN_INDEX]
                new_grid[2*x][2*y] = np.ones([4], dtype=bool)
                new_grid[2*x][2*y][Maze.LEFT_INDEX] = left
                new_grid[2*x][2*y][Maze.UP_INDEX] = up
                new_grid[(2*x) +1][2*y] = np.ones([4], dtype=bool)
                new_grid[(2*x) +1][2*y][Maze.UP_INDEX] = up
                new_grid[(2*x) +1][2*y][Maze.RIGHT_INDEX] = right
                new_grid[2*x][(2*y) +1] = np.ones([4], dtype=bool)
                new_grid[2*x][(2*y)+1][Maze.DOWN_INDEX] = down
                new_grid[2*x][(2*y)+1][Maze.LEFT_INDEX] = left
                new_grid[2*x +1][(2*y) +1] = np.ones([4], dtype=bool)
                new_grid[2*x +1][(2*y)+1][Maze.DOWN_INDEX] = down
                new_grid[2*x +1][(2*y)+1][Maze.RIGHT_INDEX] = right
        return new_grid

            
    def make_path(self):
        x = y = 0
        dir = Maze.RIGHT_INDEX
        directions = [[],[],[],[]]
        directions[Maze.RIGHT_INDEX] = [1,0]
        directions[Maze.UP_INDEX] = [0,-1]
        directions[Maze.LEFT_INDEX] = [-1,0]
        directions[Maze.DOWN_INDEX] = [0,1]
        path = []
        terminated = False
        while not terminated:
            dir = self.findNextDir(x, y, dir)
            [i, j] = directions[dir]
            if([x,y] in path):
                terminated = True
            else:
                path.append([x,y])
                x += i
                y += j
        return path

    def canGoUp(self, x, y)-> bool:
        return self.grid[x][y][Maze.UP_INDEX] == 1
    def canGoRight(self, x, y)-> bool:
        return self.grid[x][y][Maze.RIGHT_INDEX] == 1
    def canGoDown(self, x,y)-> bool:
        return self.grid[x][y][Maze.DOWN_INDEX] == 1
    def canGoLeft(self, x,y) -> bool: 
        return self.grid[x][y][Maze.LEFT_INDEX] == 1
    
    def findNextDir(self, x, y, dir):
        Right = Maze.RIGHT_INDEX
        Up = Maze.UP_INDEX
        Down = Maze.DOWN_INDEX
        Left = Maze.LEFT_INDEX
        if (dir == Right):
            if(self.canGoUp(x,y)):
                return Up
            if(self.canGoRight(x,y)):
                return Right
            if(self.canGoDown(x,y)):
                return Down
            return Left
        elif(dir == Down):
            if(self.canGoRight(x,y)):
                return Right
            if(self.canGoDown(x,y)):
                return Down
            if(self.canGoLeft(x,y)):
                return Left
            return Up
        elif(dir == Left):
            if(self.canGoDown(x,y)):
                return Down
            if(self.canGoLeft(x,y)):
                return Left
            if(self.canGoUp(x,y)):
                return Up
            return Right
        elif(dir == Up):
            if(self.canGoLeft(x,y)):
                return Left
            if(self.canGoUp(x,y)):
                return Up
            if(self.canGoRight(x,y)):
                return Right
            return Down
        return None #unreachable something broke

def get_action(state1, state2):
    if(state1[0] - 1 == state2[0]): return 0
    if(state1[0] + 1 == state2[0]): return 1
    if(state1[1] - 1 == state2[1]): return 2
    if(state1[1] + 1 == state2[1]): return 3
    return 1
def get_action_from_dir(dir):
        directions = [[],[],[],[]]
        directions[Maze.RIGHT_INDEX] = 1
        directions[Maze.UP_INDEX] = 2
        directions[Maze.LEFT_INDEX] = 0
        directions[Maze.DOWN_INDEX] = 3
        return directions[dir]

def cycleSnake(env, max_episodes:int=10, sleep=0):
    terminated = False
    dir = 1
    for _ in range(max_episodes):
        env.reset()
        m = Maze(env.game.game_width, env.game.game_height)
        path = []
        path = m.make_path()
        while not terminated:
            if(sleep > 0):
                time.sleep(sleep)
            cur = path.index(env.game.snake_list[-1])
            next = (cur+dir)%len(path)
            action = get_action(path[cur], path[next])
            reward, new_state, terminated = env.step(action)
            if(reward):
                dir = -1*dir
        