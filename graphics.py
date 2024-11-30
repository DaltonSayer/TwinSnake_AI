import pygame

class snakeGUI:
    white = (255, 255, 255)
    black = (0,0,0)
    red = (213, 50, 80)
    blue = (0, 240, 255, 0.341)
    dark_square = (162, 209, 73)
    light_square = (170, 215, 81)


    def __init__(self, width, height, square_size=20):
        pygame.init()
        self.width = width
        self.height = height
        self.square_size = square_size
        screen_width = width * square_size
        screen_height = height * square_size
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.font = pygame.font.Font(None, 30)
        self.imaginary_snake = None
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
        
    def draw_square(self, x , y , colour, half=True):
        if(half):
            [i,j] = [x*self.square_size + 0.25*self.square_size, y*self.square_size + 0.25 * self.square_size]
            pygame.draw.rect(self.screen, colour, (i, j, 0.5*self.square_size, 0.5*self.square_size))
        else:
            pygame.draw.rect(self.screen, colour, (x*self.square_size, y*self.square_size, self.square_size, self.square_size))

    def draw_score(self, score):
        # Render the score text
        score_text = self.font.render(f"{score}", False, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
    
        
    #Draw the game
    def draw_snake(self, apple_pos, snake_list, head_colour=black, body_colour=white, apple_colour=red, imaginary_colour=blue):
        self.draw_grid()
        if(self.imaginary_snake != None):
            [i,j] = -1,-1
            for [x,y] in self.imaginary_snake:
                self.draw_square(x,y, imaginary_colour)
                if(i != -1 and j != -1):
                    [k,l] = [x-i, y-j]
                    self.draw_square(i+(0.5*k), j+(0.5*l), imaginary_colour)
                [i,j] = [x,y]

        self.draw_square(apple_pos[0], apple_pos[1], apple_colour)
        [i,j] = -1, -1
        for [x, y] in snake_list:
            self.draw_square(x, y, body_colour)
            if(i != -1 and j!= -1):
                [k,l] = [x-i, y-j]
                self.draw_square(i+(0.5*k), j+(0.5*l), body_colour)
            [i,j] = [x,y]
        [x,y] = snake_list[-1]
        self.draw_square(x, y, head_colour)
        self.draw_score(len(snake_list)-1)
        pygame.display.update()
        pass

