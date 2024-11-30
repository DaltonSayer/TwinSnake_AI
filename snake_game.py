import graphics as graphics
import random
import numpy as np


class snake_game:
    def __init__(self, width=20, height=20, rendering=True, force_spawn_zero=False):
        # Stores the position of the snake
        self.snake_list = []
        self.snake_list.append([random.randint(0,width), random.randint(0,height)]) #spawn the snake at a random loaction
        self.snake_length = 1
        #The width and height of the grid
        self.game_width = width
        self.game_height = height
        #Spawn random apple 
        self.apple_pos = self._spawn_apple()
        if(rendering):
            self.GUI = graphics.snakeGUI(width, height)
        self.rendering = rendering
        self.win = False
        self.force_spawn_zero = force_spawn_zero

    
    def reset(self):
        self.snake_list = []
        if(not self.force_spawn_zero):
            self.snake_list.append([random.randint(0,self.game_width-1), random.randint(0,self.game_height-1)]) #spawn the snake at a random loaction
        else:
            self.snake_list.append([0,0])
        self.snake_length = 1    
        self.win = False
        self.apple_pos = self._spawn_apple()
        return self
    
    def _out_of_bounds(self, location):
        ret = False
        if(location[0] < 0 or location[0] > self.game_width-1):
            ret = True
        if(location[1] < 0 or location[1] > self.game_height-1):
            ret = True

        return ret

    def step(self, direction):
        #direction is a np.array([x,y])
        #moves the snake in that direction (action) returns the score (reward), the new and if the game terminated
        reward = 0
        terminated = False

        new_head = (np.array(self.snake_list[-1]) + np.array(direction)).tolist()
        reverse = False
        if(new_head == self.apple_pos):
            reverse = True
            self._collect_apple()
            if(self.win): return 100, self, True
            reward = 1
        
        if(len(self.snake_list) == self.snake_length):
            self.snake_list.pop(0)
        
        if((new_head in self.snake_list) or self._out_of_bounds(new_head)):
            terminated = True
            reward = -10
        
        self.snake_list.append(new_head)
        if reverse:
            self.snake_list.reverse()
        if(self.rendering):
            self.GUI.draw_snake(self.apple_pos, self.snake_list)

        return reward, self, terminated
    
    def check_win(self):
        return (self.snake_length == self.game_height * self.game_width)

    def _collect_apple(self):
        self.snake_length += 1
        if(not self.check_win()):
            self.apple_pos = self._spawn_apple()
        else:
            self.win = True
            print("win")

        

    def _spawn_apple(self):
        #Cannot spawn apple inside of the snake
        while True:
            apple_pos =[random.randint(0,self.game_width-1),random.randint(0,self.game_height-1)] 
            if(not apple_pos in self.snake_list):
                return apple_pos
            
