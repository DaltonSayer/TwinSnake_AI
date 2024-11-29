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
    
    def get_dir(cur : list[int, int], prev : list[int, int]):
        [x, y] = prev
        [i, j] = cur
        if(x<i):#went right
            #print("went right")
            return Maze.RIGHT_INDEX
        if(i<x):#went left
            #print("went left")
            return Maze.LEFT_INDEX
        if(y>j):#went up
            #print("went up")
            return Maze.UP_INDEX
        if(y<j):#went down
            #print("went down")
            return Maze.DOWN_INDEX
        
    def  get_move(self, snake_list: list[list[int,int]], dir=-1):
        
        orders = [[],[],[],[]]
        orders[Maze.UP_INDEX] = [Maze.RIGHT_INDEX, Maze.UP_INDEX, Maze.LEFT_INDEX]
        orders[Maze.DOWN_INDEX] = [Maze.LEFT_INDEX, Maze.DOWN_INDEX, Maze.RIGHT_INDEX]
        orders[Maze.RIGHT_INDEX] = [Maze.DOWN_INDEX, Maze.RIGHT_INDEX, Maze.UP_INDEX]
        orders[Maze.LEFT_INDEX] = [Maze.UP_INDEX, Maze.LEFT_INDEX, Maze.DOWN_INDEX]
        action = [0,0,0,0]
        action[Maze.UP_INDEX] = 2
        action[Maze.DOWN_INDEX] = 3
        action[Maze.LEFT_INDEX] = 0
        action[Maze.RIGHT_INDEX] = 1
        

        if(len(snake_list) > 1):
            dir = Maze.get_dir(snake_list[-1], snake_list[-2])
            
        cur = self.grid[snake_list[-1][0]][snake_list[-1][1]]
        for d in orders[dir]:
            if(cur[d] == 1):
                return action[d], d
        # print(dir)
        # return action[d], dir
    def get_move_2(self, snake_head):
        action = [0,0,0,0]
        action[Maze.UP_INDEX] = 2
        action[Maze.DOWN_INDEX] = 3
        action[Maze.LEFT_INDEX] = 0
        action[Maze.RIGHT_INDEX] = 1
        #can only go up in squares with a even x value x%2 = 0
        #can only go right in squares with a even y value y%2 = 0
        [x,y] = snake_head
        if(x%2 == 0): #can go up, right or left
            if(y%2 == 0): #can go up, or right
                if(self.grid[x][y][Maze.RIGHT_INDEX]):
                    return action[Maze.RIGHT_INDEX]
                elif(self.grid[x][y][Maze.UP_INDEX]):
                    # print("cannot go right, moving up")
                    return action[Maze.UP_INDEX]
                else:
                    print("SOMETHING WENT WRONG")
            else:#can go up or left
                if(self.grid[x][y][Maze.UP_INDEX]):
                    return action[Maze.UP_INDEX]
                elif(self.grid[x][y][Maze.LEFT_INDEX]):
                    return action[Maze.LEFT_INDEX]
                else:
                    print("SOMETHING WENT WRONG")
        else: #can go down, right or left
            if(y%2 ==0): #can go down, or right
                if(self.grid[x][y][Maze.DOWN_INDEX]):
                    return action[Maze.DOWN_INDEX]
                elif(self.grid[x][y][Maze.RIGHT_INDEX]):
                    return action[Maze.RIGHT_INDEX]
                else:
                    print("SOMETHING WENT WRONG")
            else:#can go down or left
                if(self.grid[x][y][Maze.LEFT_INDEX]):
                    return action[Maze.LEFT_INDEX]
                elif(self.grid[x][y][Maze.DOWN_INDEX]):
                    return action[Maze.DOWN_INDEX]
                else:
                    print("SOMETHING WENT WRONG")

    def is_valid(self,pos, dir):
        [x,y] = pos
        return self.grid[x][y][dir]
        
    def get_move_3(self, snake_head, dir):
        action = [0,0,0,0]
        action[Maze.UP_INDEX] = 2
        action[Maze.DOWN_INDEX] = 3
        action[Maze.LEFT_INDEX] = 0
        action[Maze.RIGHT_INDEX] = 1
        for i in range(3):
            new_dir = (dir+i) % 4
            print(new_dir)
            if(self.is_valid(snake_head, new_dir) == 1):
                return action[new_dir], new_dir
        print("STUCK")
            
            
            
# g = Maze(10, 10)

# print(g.grid)
def cycleSnake(env, max_episodes:int=1):
    terminated = False
    i = 0
    dir = 1
    for _ in range(max_episodes):
        env.reset()
        while not terminated:
            time.sleep(0.1)
            m = Maze(env.game.game_width, env.game.game_height)
            #action, dir = m.get_move(env.game.snake_list, dir)
            action, dir = m.get_move_3(env.game.snake_list[-1], dir)
            prev = env.game.snake_list[-1]
            i, _, terminated = env.step(action)
            cur = env.game.snake_list[-1]
            #dir = Maze.get_dir(cur, prev)
        