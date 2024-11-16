import game.graphics as graphics
import random
import numpy as np


class game:
    def __init__(self, width=20, height=20, rendering=True):
        # Stores the position of the snake
        self.snake_list = []
        self.snake_list.append((random.randint(0,width), random.randint(0,height))) #spawn the snake at a random loaction
        self.snake_length = 1
        #The width and height of the grid
        self.game_width = width
        self.game_height = height
        #Spawn random apple 
        self.apple_pos = self._spawn_apple()
        self.rendering = rendering

    def reset(self):
        self.snake_list = []
        self.snake_list.append(np.array([random.randint(0,self.width), random.randint(0,self.height)])) #spawn the snake at a random loaction
        self.snake_length = 1    
        return self
    
    def step(self, direction):
        #direction is a np.array([x,y])
        #moves the snake in that direction (action) returns the score (reward), the new and if the game terminated
        reward = 0
        terminated = False

        new_head = self.snake_list[-1] + direction    
        if(new_head == self.apple_pos):
            self._collect_apple()
            reward = 1
        
        if(len(self.snake_list) == self.snake_length):
            self.snake_list.pop(0)
        
        if((new_head in self.snake_list) or self._out_of_bounds(new_head)):
            terminated = True
        
        self.snake_list.append(new_head)
        if(self.rendering):
            graphics.draw_snake(self.game_width, self.game_height, self.apple_pos, self.snake_list)

        return reward, self, terminated
    
    def _collect_apple(self):
        self.snake_length += 1
        self.apple_pos = self._spawn_apple()

    def _spawn_apple(self):
        #Cannot spawn apple inside of the snake
        while True:
            apple_pos = np.array([random.randint(0,self.game_width),(0,self.game_height)])
            if(not apple_pos in self.snake_list):
                return apple_pos