import pygame

class snakeGUI:
    white = (255, 255, 255)
    black = (0,0,0)
    red = (213, 50, 80)

    def __init__ (self, width, height square_size=20, line_width=2):
        self.width = width
        self.height = height
        self.square_size = square_size
        self.line_width = line_width
        screen_width = width * square_size + line_width * (width+1)
        screen_height = height * square_size + line_width * (height+1)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen.fill(snakeGUI.black)
    
    #Draw the board and the apple
    def draw_grid(self):
        self.screen.fill(snakeGUI.black)
        
    #Draw the snake
    
    def draw_snake(self, apple_pos, snake_list):  
        self.draw_grid()

        pass