import snake_game as sg
import graphics as graphics
import pygame
import time

def run():
    env = sg.snake_game(20, 20)
    dir = [0, 0]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        # Move the square based on arrow key input
        if keys[pygame.K_LEFT]:
            dir = [-1,0]
        elif keys[pygame.K_RIGHT]:
            dir = [1,0]  # Move right
        elif keys[pygame.K_UP]:
            dir = [0,-1]  # Move up
        elif keys[pygame.K_DOWN]:
            dir = [0, 1]  # Move down
        
        reward, self, terminated = env.step(dir)
        if reward == 1:
            #reverse
            [x,y] = dir
            x *= -1
            y *= -1
            dir = [x,y]
        if(terminated):
            print("game over")
            env.reset()
        time.sleep(0.1)

run()