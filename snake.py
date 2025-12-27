import pygame
from pygame.locals import *
import random

pygame.init()


screen = pygame.display.set_mode((1000, 800))
block = pygame.image.load("./block.jpeg").convert()
food = pygame.image.load("./strawberry_30_by_30.jpeg").convert()

# 1. Define snake segments (list of lists)
# Each [x, y] is a block. The first one is the head.
snake_body = [[100, 100], [90, 100], [80, 100]] 
direction = K_RIGHT # Initial movement direction
step = 30 # Size of your block

clock = pygame.time.Clock() # To control game speed
player_speed = 5

food_x = 300
food_y = 300

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            # Update direction based on key press
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                direction = event.key
                

    # 2. Movement Logic: Update the Head
    head_x, head_y = snake_body[0]
    if direction == K_UP:    head_y -= step
    if direction == K_DOWN:  head_y += step
    if direction == K_LEFT:  head_x -= step
    if direction == K_RIGHT: head_x += step

    # 3. Slithering Logic: 
    # Add new head position to the front
    snake_body.insert(0, [head_x, head_y])
    # Remove the last segment (tail) so it doesn't grow infinitely
    if head_x == food_x and head_y == food_y:
        # Don't pop the tail, so the snake grows!
        # Move food to a new random location
        food_x = random.randint(0, (1000 // step) - 1) * step
        food_y = random.randint(0, (800 // step) - 1) * step
    else:
        # Remove the last segment if no food was eaten
        snake_body.pop()

    screen.fill((0, 100, 0))
    
    # Draw the strawberry
    screen.blit(food, (food_x, food_y))
    for segment in snake_body:
        screen.blit(block, (segment[0], segment[1]))
    
    pygame.display.flip()
    clock.tick(4) # Set FPS to 10 so it's playable

pygame.quit()