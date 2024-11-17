import graphics as graphics
import random
import numpy as np


class snake_game:
    def __init__(self, width=20, height=20, rendering=True):
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

    def reset(self):
        self.snake_list = []
        self.snake_list.append([random.randint(0,self.game_width), random.randint(0,self.game_height)]) #spawn the snake at a random loaction
        self.snake_length = 1    
        return self
    
    def _out_of_bounds(self, location):
        ret = False
        if(location[0] < 0 or location[0] > self.game_width-1):
            ret = True
        if(location[1] < 0 or location[0] > self.game_height-1):
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
            reward = 1
        
        if(len(self.snake_list) == self.snake_length):
            self.snake_list.pop(0)
        
        if((new_head in self.snake_list) or self._out_of_bounds(new_head)):
            terminated = True
        
        self.snake_list.append(new_head)
        if reverse:
            self.snake_list.reverse()
        if(self.rendering):
            self.GUI.draw_snake(self.apple_pos, self.snake_list)

        return reward, self, terminated
    
    def _collect_apple(self):
        self.snake_length += 1
        self.apple_pos = self._spawn_apple()
        

    def _spawn_apple(self):
        #Cannot spawn apple inside of the snake
        while True:
            apple_pos =[random.randint(0,self.game_width-1),random.randint(0,self.game_height-1)] 
            if(not apple_pos in self.snake_list):
                return apple_pos
            
