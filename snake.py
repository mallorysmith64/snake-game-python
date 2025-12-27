import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((800, 600))
block = pygame.image.load("./block.jpeg").convert()

# 1. Define snake segments (list of lists)
# Each [x, y] is a block. The first one is the head.
snake_body = [[100, 100], [90, 100], [80, 100]] 
direction = K_RIGHT # Initial movement direction
step = 300 # Size of your block

clock = pygame.time.Clock() # To control game speed

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
    snake_body.pop()

    # 4. Rendering
    screen.fill((0, 0, 0))
    for segment in snake_body:
        screen.blit(block, (segment[0], segment[1]))
    
    pygame.display.flip()
    clock.tick(10) # Set FPS to 10 so it's playable

pygame.quit()