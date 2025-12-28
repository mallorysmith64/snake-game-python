import pygame
from pygame.locals import *
import random

pygame.init()
font = pygame.font.SysFont("Arial", 36)

screen = pygame.display.set_mode((1000, 800))
# Using .convert() is good practice for performance!
block = pygame.image.load("./block.jpeg").convert()
food = pygame.image.load("./strawberry_30_by_30.jpeg").convert()

snake_body = [[100, 100], [70, 100], [40, 100]] 
direction = K_RIGHT 
step = 30 
score = 0

clock = pygame.time.Clock()
food_x, food_y = 300, 300

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            # Prevent the snake from reversing directly onto itself
            if event.key == K_UP and direction != K_DOWN: direction = K_UP
            if event.key == K_DOWN and direction != K_UP: direction = K_DOWN
            if event.key == K_LEFT and direction != K_RIGHT: direction = K_LEFT
            if event.key == K_RIGHT and direction != K_LEFT: direction = K_RIGHT

    # 1. Calculate New Head Position
    new_head = list(snake_body[0])
    if direction == K_UP:    new_head[1] -= step
    if direction == K_DOWN:  new_head[1] += step
    if direction == K_LEFT:  new_head[0] -= step
    if direction == K_RIGHT: new_head[0] += step

    # Insert new head into the snake body
    snake_body.insert(0, new_head)

    # 2. Collision Detection (Snake Head vs Food)
    # Create Rects for the head and the food to check collision
    head_rect = pygame.Rect(new_head[0], new_head[1], step, step)
    food_rect = pygame.Rect(food_x, food_y, 30, 30)
    
    if head_rect.colliderect(food_rect):
        score += 1
        # Relocate food to a random spot
        food_x = random.randint(0, (1000 - step) // step) * step
        food_y = random.randint(0, (800 - step) // step) * step
        # Note: We do NOT pop the tail here, so the snake grows longer
    else:
        # If no food eaten, remove the tail segment to maintain length
        snake_body.pop()

    # 3. Drawing
    screen.fill((0, 100, 0)) # Dark green background
    
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    # Draw Food
    screen.blit(food, (food_x, food_y))
    # Draw Snake
    for segment in snake_body:
        screen.blit(block, (segment[0], segment[1]))
    
    pygame.display.flip()
    clock.tick(10) # 10 FPS is a good speed for Snake

pygame.quit()