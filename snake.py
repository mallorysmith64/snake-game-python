import pygame
from pygame.locals import *

pygame.init()

# Setup screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Block Movement")

# Load assets
# Note: Ensure block.jpeg is in the same folder
try:
    block = pygame.image.load("./block.jpeg").convert()
except:
    # Fallback if image isn't found
    block = pygame.Surface((50, 50))
    block.fill((255, 0, 0))

block_x = 100
block_y = 100

running = True
while running:
    # 1. Clear the screen (prevents trails/ghosting)
    screen.fill((0, 0, 0)) 

    # 2. Event Handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            # Check event.key, not event.type
            if event.key == K_UP:
                block_y -= 10
            if event.key == K_DOWN:
                block_y += 10
            if event.key == K_LEFT:
                block_x -= 10
            if event.key == K_RIGHT:
                block_x += 10

    # 3. Draw and Refresh
    screen.blit(block, (block_x, block_y))
    pygame.display.flip()

pygame.quit()