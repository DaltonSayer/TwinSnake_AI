import pygame

class snakeGUI:
    white = (255, 255, 255)
    black = (0,0,0)
    red = (213, 50, 80)
    dark_square = (162, 209, 73)
    light_square = (170, 215, 81)


    def __init__(self, width, height, square_size=20):
        self.width = width
        self.height = height
        self.square_size = square_size
        screen_width = width * square_size
        screen_height = height * square_size
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.draw_grid()
    
    #Draw the board
    def draw_grid(self):
        self.screen.fill(snakeGUI.black)
        on_dark = False
        for x in range(0, self.width * self.square_size, self.square_size):
            on_dark = not on_dark
            for y in range(0, self.height * self.square_size, self.square_size):
                #for grid pattern
                on_dark = not on_dark
                if(on_dark):
                    colour = snakeGUI.dark_square
                else:
                    colour = snakeGUI.light_square
                pygame.draw.rect(self.screen, colour, (x, y, self.square_size, self.square_size))
        
    def draw_square(self, x , y , colour):
        pygame.draw.rect(self.screen, colour, (x*self.square_size, y*self.square_size, self.square_size, self.square_size))

    #Draw the snake
    
    def draw_snake(self, apple_pos, snake_list):  
        self.draw_grid()
        self.draw_square(apple_pos[0], apple_pos[1], snakeGUI.red)
        for [x, y] in snake_list:
            self.draw_square(x, y, snakeGUI.white)
        [x,y] = snake_list[-1]
        self.draw_square(x, y, snakeGUI.black)
        pygame.display.update()
        pass

