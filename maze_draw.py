import Models.Hamiltonian_Cycle_2 as hc
import pygame
import time

class MazeGUI:
    white = (255, 255, 255)
    grey = (200, 200, 200)
    black = (0,0,0)
    red = (213, 50, 80)
    blue = (0,232,255)
    green = (0,255,0)
    
    def __init__(self, width, height, square_size=20, line_width = 2):
        pygame.init()
        self.width = width
        self.height = height
        self.square_size = square_size
        self.line_width = line_width
        screen_width = width*square_size + (2*line_width * width-1)
        screen_height = height*square_size + (2*line_width * height-1)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.draw_maze()
    
    def draw_line(self, i, j, walls):
        x = i*self.square_size + i* (2*self.line_width) + 0.5*self.square_size
        y = j*self.square_size + j* (2*self.line_width) + 0.5*self.square_size
        
        #left wall
        left = x - 0.5*self.square_size - self.line_width
        right = x + 0.5*self.square_size + self.line_width
        top = y - 0.5*self.square_size - 0.5*self.line_width
        bottom = y + 0.5*self.square_size + 0.5 * self.line_width
        if(not walls[hc.Maze.UP_INDEX]):
            #Draw Top Wall
            pygame.draw.rect(self.screen, MazeGUI.black, (left+self.line_width, top, self.square_size, self.line_width))    
        if(not walls[hc.Maze.DOWN_INDEX]):
            #Draw Bottom Wall
            pygame.draw.rect(self.screen, MazeGUI.black, (left+self.line_width, bottom, self.square_size, self.line_width))    
        if(not walls[hc.Maze.LEFT_INDEX]):
            #Draw Left wall
            pygame.draw.rect(self.screen, MazeGUI.black, (left,top, self.line_width, self.square_size))
        if(not walls[hc.Maze.RIGHT_INDEX]):
            #Draw Right Wall
            pygame.draw.rect(self.screen, MazeGUI.black, (right-self.line_width,top, self.line_width, self.square_size))
        
        
        pygame.display.update()
    
    def draw_maze(self):
        maze = hc.Maze(self.width, self.height)
        grid = maze.grid#hc.Maze.scale_maze(maze.grid)
        self.screen.fill(MazeGUI.white)
        
        for x in range(0, (self.width*self.square_size) + (2*self.line_width*self.width), self.square_size+(2*self.line_width)):
            for y in range(0, self.height * self.square_size + (2*self.line_width*self.height), self.square_size+(2*self.line_width)):
                pygame.draw.rect(self.screen, MazeGUI.grey, (x,y, self.square_size, self.square_size))

                pygame.display.update()
    
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                self.draw_line(x,y, grid[x][y])
        
                    
x= MazeGUI(20, 20)
time.sleep(100)