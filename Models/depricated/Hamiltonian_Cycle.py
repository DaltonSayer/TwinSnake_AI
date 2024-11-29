import random
import pygame
import time
import numpy as np
#https://johnflux.com/category/nokia-6110-snake-project/

#precompute a Hamiltonian cycle at the start of the game, have snake keep following it
#once snake collects apple just reverse order of traversal

#to create hamilitonian cycle, create a minimum spanning tree, the perimiter of the tree is the cycle

#following sudocode on wikipedia https://en.wikipedia.org/wiki/Prim%27s_algorithm
# class vertex:
#     def __init__(self, index:list[int,int], c=float('inf'), parent=None):
#         self.c = c
#         self.E = parent
#         self.children = []
#         self.index = index
#     def __eq__(self, value):
#         return self.index == value.index
    
#     def get_attached_dirs(self):
#         attached = {}
#         attached_v = self.children
#         if(type(self.E) == vertex): attached_v.append(self.E)
#         for v in (self.children):
#             X,Y = self.index
#             if([X+1, Y] == v.index): attached.update({"right":v})
#             if([X-1, Y] == v.index): attached.update({"left":v})
#             if([X, Y+1] == v.index): attached.update({"down":v})
#             if([X,Y-1] == v.index): attached.update({"up":v})
#         return attached

# def getWeight(v: vertex):
#     return v.c

# def prims(width, height):
#     #graph is an array of vertices    
#     F = []
#     Q = [vertex([0,0])]
#     while(len(Q) > 0):
#         Q.sort(reverse=True, key=getWeight)
#         v = Q.pop()
#         F.append(v)
#         y, x = v.index
#         for [i, j] in [[y+1, x], [y-1,x], [y,x-1], [y, x+1]]:
#             if(i >= 0 and j >= 0 and i < width and j < height):
#                 new_v = vertex([i,j], c=random.randint(1,10), parent=v)
#                 if(new_v not in F and new_v not in Q):
#                     v.children.append(new_v)
#                     Q.append(new_v)
#     return(F)

# #requires even width and height
# # def get_squares(v, direction='up'):
# #     squares =[2*v.index[0], 2*v.index[1]],[2*v.index[0]+1, 2*v.index[1]],[2*v.index[0]+1, 2*v.index[1]+1],[2*v.index[0], 2*v.index[1]+1] 
# #     match direction:
# #         case "up": return [squares[3], squares[0], squares[1], squares[2]]
# #         case "left": return [squares[0], squares[1], squares[2], squares[3]]
# #         case "down": return [squares[1], squares[2], squares[3], squares[0]]
# #         case _: return [squares[2], squares[3], squares[0], squares[1]]
# def get_square(v, direction):
#     match direction:
#         case "up": return [2*v.index[0]+1, 2*v.index[1]+1]
#         case "right": return [2*v.index[0]+1, 2*v.index[1]]
#         case "down": return [2*v.index[0]+2, 2*v.index[1]]
#         case "left": return [2*v.index[0]+2, 2*v.index[1]+1]
        
# def make_path(width, height):
#     path = []
#     maze = prims(width//2, height//2)
    
#     start = maze[0]
#     v = start
#     dir = "left"
    
#     for _ in range(100):
#         # moves = get_squares(v, dir)
#         attached = v.get_attached_dirs()
#         dirs = ["left", "down", "right", "up"]
#         i = 0
#         while i < len(dirs):
#             j = dirs.index(dir)
#             #print(dir, get_square(v,dir))
#             path.append(get_square(v, dir))
#             #path.append(moves[i])
#             dir = dirs[(j+1)%4]
#             if(dir in attached):
#                 # dir = dirs[(i+j+1)%4]
#                 v = attached[dir]
#                 i = len(dirs)
#             i +=1
            
#     return path
    
        

# def get_action(state1, state2):
#     if(state1[0] - 1 == state2[0]): return 0
#     if(state1[0] + 1 == state2[0]): return 1
#     if(state1[1] - 1 == state2[1]): return 2
#     if(state1[1] + 1 == state2[1]): return 3
#     print("BAD")
#     return 1


# def cycle_snake(env, max_episode:int=100):
#     terminated = False
#     env.reset()
#     for x in range(max_episode):
#         p = make_path(env.game.game_width, env.game.game_height)
        
#         actions =[]
#         for i in range(1, len(p)):
#             actions.append(get_action(p[i-1], p[i]))
#         i = 0
#         while not terminated:            
#             action = actions[i%len(actions)]
#             reward, new_state, terminated = env.step(action)


# # def prims_maze(width, height):
# #     grid = 



class Maze:
    def __init__(self, width, height):
        self.grid = np.zeros([width, height], dtype=bool)
        self.width = width
        self.height = height
        self.frontier = []
        self.prims_maze()
        
    def prims_maze(self):
        frontier = []    
        x = random.randint(0, self.width-1)
        y = random.randint(0, self.height-1)
        frontier.append([x,y,x,y])
        while len(frontier) > 0:
            [z,k,x,y] = frontier.pop(random.randint(0,len(frontier)-1))
            if(not self.grid[x][y]):
                self.grid[z][k] = self.grid[x][y] = True
                if(x >= 2 and self.grid[x-2][y] == False):
                    frontier.append([x-1, y, x-2,y])
                if(y >= 2 and self.grid[x][y-2] == False):
                    frontier.append([x, y-1, x,y-2])
                if(x < self.width-2 and self.grid[x+2][y] == False):
                    frontier.append([x+1, y, x+2, y])
                if(y < self.width-2 and self.grid[x][y+2] == False):
                    frontier.append([x,y+1, x,y+2])
        

def double_resolution(grid):
    ret = np.zeros([2*len(grid), 2*len(grid[0])])
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            ret[i*2][j*2] = ret[(i*2)+1][j*2] =ret[(i*2)][(j*2)+1] =ret[(i*2)+1][(j*2)+1] = grid[i][j]
    return ret

def navigate_path(width, height, location):
    m = Maze(width//2, height//2)
    grid = double_resolution(m.grid)
    print(m.grid)
    actions = []
    [x,y] = location
    following = grid[x][y]
    for i in range(width*height):
        
        can_move_up = (y-1 >= 0 and grid[x][y-1] == following)
        can_move_down = (y+1 < height) and grid[x][y+1] == following
        can_move_left = (x-1 >= 0) and grid[x-1][y] == following
        can_move_right = (x+1 < width) and grid[x+1][y] == following
        
        if(can_move_right and not can_move_down):
            actions.append(1)
            [x,y] = [x+1,y]
        elif(can_move_down and not can_move_left):
            actions.append(3)
            [x,y] = [x,y+1]
        elif(can_move_left and not can_move_up):
            actions.append(0)
            [x,y] = [x-1,y]
        elif(can_move_up):
            actions.append(2)
            [x,y] = [x,y-1]
        else:
            print("F")
        # #hug the wall
        # if(y+1 > height-1 or not grid[x][y+1] == following):#wall bellow    
        #     if(x+1 > width-1 or not grid[x+1][y] == following): #wall right
        #         #move up
        #         actions.append(2)
        #         [x,y] = [x,y-1]
        #     else:
        #         #move right
        #         actions.append(1)
        #         [x,y] = [x+1,y]
        # elif(y-1 < 0 or not grid[x][y-1] == following): #wall above
        #     if(x-1 < 0 or not grid[x-1][y] == following):#wall left
        #         #move down
        #         actions.append(3)
        #         [x,y] = [x,y+1]
        #     else:
        #         #move left
        #         actions.append(0)
        #         [x,y] = [x-1,y]
        # else:
        #     if(x-1 < 0 or not grid[x-1][y] == following):
        #         actions.append(3)
        #         [x,y] = [x,y+1]
        #     else:
        #         actions.append(2)
        #         [x,y] = [x,y-1]
    ret = []
    for i in range(len(actions)):
        ret.append(actions.pop())
    return ret 
    #path wraps around the true
    
def cycle_snake(env, max_episode:int=1):
    terminated = False
    env.reset()
    for x in range(max_episode):
        snake_list = env.game.snake_list
        print(snake_list)
        actions = navigate_path(env.game.game_width, env.game.game_height, env.game.snake_list[-1])
        i = 0
        while not terminated:            
            time.sleep(0.05)
            action = actions[i%len(actions)]
            
            
            reward, new_state, terminated = env.step(action)
            i += 1
    

# def test():
#     p = make_path(20, 20)
#     print(p)
#     pygame.init()
#     width = 20
#     height = 20
#     square_size = 20
#     screen = pygame.display.set_mode((width*square_size, height*square_size))
#     screen.fill((0,0,0))
#     for [x,y] in p:
#         pygame.draw.rect(screen, (255,255,255), (x*square_size,y*square_size, square_size, square_size))
#         pygame.display.update()
#         time.sleep(0.1)
    
