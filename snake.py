import pygame
from pygame.locals import *
import random

pygame.init()

# --- Configuration ---
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 36)
big_font = pygame.font.SysFont("Arial", 72)
clock = pygame.time.Clock()

# Load images
block = pygame.image.load("./block.jpeg").convert()
food = pygame.image.load("./strawberry_30_by_30.jpeg").convert()

def reset_game():
    return [[100, 100], [70, 100], [40, 100]], K_RIGHT, 0, 300, 300

snake_body, direction, score, food_x, food_y = reset_game()
step = 30
game_active = True
running = True

while running:
    # 1. Event Handling
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        if game_active:
            if event.type == KEYDOWN:
                if event.key == K_UP and direction != K_DOWN: direction = K_UP
                if event.key == K_DOWN and direction != K_UP: direction = K_DOWN
                if event.key == K_LEFT and direction != K_RIGHT: direction = K_LEFT
                if event.key == K_RIGHT and direction != K_LEFT: direction = K_RIGHT
        else:
            # Check for button click if game is over
            if event.type == MOUSEBUTTONDOWN:
                # Button Rect: center of screen
                button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50)
                if button_rect.collidepoint(mouse_pos):
                    snake_body, direction, score, food_x, food_y = reset_game()
                    game_active = True

    if game_active:
        # 2. Movement logic
        new_head = list(snake_body[0])
        if direction == K_UP:    new_head[1] -= step
        if direction == K_DOWN:  new_head[1] += step
        if direction == K_LEFT:  new_head[0] -= step
        if direction == K_RIGHT: new_head[0] += step

        # --- Boundary Check ---
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            game_active = False

        snake_body.insert(0, new_head)

        # --- Food Collision ---
        head_rect = pygame.Rect(new_head[0], new_head[1], step, step)
        food_rect = pygame.Rect(food_x, food_y, 30, 30)
        if head_rect.colliderect(food_rect):
            score += 1
            food_x = random.randint(0, (WIDTH - step) // step) * step
            food_y = random.randint(0, (HEIGHT - step) // step) * step
        else:
            snake_body.pop()

    # 3. Drawing
    screen.fill((0, 100, 0))
    
    if game_active:
        # Draw game elements
        screen.blit(food, (food_x, food_y))
        for segment in snake_body:
            screen.blit(block, (segment[0], segment[1]))
        
        score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))
    else:
        # --- Game Over Screen ---
        msg = big_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(msg, (WIDTH//2 - 150, HEIGHT//2 - 100))
        
        # Draw Play Again Button
        button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50)
        pygame.draw.rect(screen, (200, 200, 200), button_rect) # Grey button
        btn_text = font.render("Play Again", True, (0, 0, 0))
        screen.blit(btn_text, (WIDTH//2 - 70, HEIGHT//2 + 55))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()