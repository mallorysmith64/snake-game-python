import pygame
from pygame.locals import *
import random

pygame.init()

# --- Setup ---
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()

# Load images (replace with your file paths)
block = pygame.image.load("./block.jpeg").convert()
food_img = pygame.image.load("./strawberry_30_by_30.jpeg").convert()

def reset_game():
    return {
        "body": [[300, 100], [300, 70], [300, 40]],
        "dir": K_DOWN,
        "score": 0,
        "scroll": 0,
        "food": [300, 400],
        "active": True
    }

game = reset_game()
step = 30
scroll_speed = 3 # How fast the screen moves down automatically

while True:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); exit()
        
        if game["active"]:
            if event.type == KEYDOWN:
                if event.key == K_UP and game["dir"] != K_DOWN: game["dir"] = K_UP
                if event.key == K_DOWN and game["dir"] != K_UP: game["dir"] = K_DOWN
                if event.key == K_LEFT and game["dir"] != K_RIGHT: game["dir"] = K_LEFT
                if event.key == K_RIGHT and game["dir"] != K_LEFT: game["dir"] = K_RIGHT
        else:
            if event.type == MOUSEBUTTONDOWN:
                btn_rect = pygame.Rect(WIDTH//2-100, HEIGHT//2+50, 200, 50)
                if btn_rect.collidepoint(mouse_pos):
                    game = reset_game()

    if game["active"]:
        # 1. Automatic Scrolling
        game["scroll"] += scroll_speed
        
        # 2. Movement Logic
        new_head = list(game["body"][0])
        if game["dir"] == K_UP:    new_head[1] -= step
        if game["dir"] == K_DOWN:  new_head[1] += step
        if game["dir"] == K_LEFT:  new_head[0] -= step
        if game["dir"] == K_RIGHT: new_head[0] += step

        # 3. Game Over Checks
        # Wall hits (Left/Right) or Snake falls off top of screen
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < game["scroll"]:
            game["active"] = False
        
        # Snake goes too far off bottom (Optional, depending on difficulty)
        if new_head[1] > game["scroll"] + HEIGHT:
            game["active"] = False

        game["body"].insert(0, new_head)

        # 4. Food & Growth
        head_rect = pygame.Rect(new_head[0], new_head[1], step, step)
        food_rect = pygame.Rect(game["food"][0], game["food"][1], 30, 30)
        
        if head_rect.colliderect(food_rect):
            game["score"] += 1
            # Spawn food ahead of the snake (further down)
            game["food"] = [random.randint(0, (WIDTH-step)//step)*step, 
                            random.randint(int(game["scroll"]+HEIGHT//2), int(game["scroll"]+HEIGHT))]
        else:
            game["body"].pop()

    # --- Drawing ---
    screen.fill((20, 20, 40)) # Dark Blue background
    
    if game["active"]:
        # Draw Food (Adjusted for scroll)
        screen.blit(food_img, (game["food"][0], game["food"][1] - game["scroll"]))
        
        # Draw Snake (Adjusted for scroll)
        for seg in game["body"]:
            screen.blit(block, (seg[0], seg[1] - game["scroll"]))
            
        score_txt = font.render(f"Score: {game['score']}", True, (255, 255, 255))
        screen.blit(score_txt, (10, 10))
    else:
        # Game Over Screen
        over_txt = font.render("Game Over!", True, (255, 50, 50))
        screen.blit(over_txt, (WIDTH//2-100, HEIGHT//2-50))
        pygame.draw.rect(screen, (100, 100, 100), (WIDTH//2-100, HEIGHT//2+50, 200, 50))
        btn_txt = font.render("PLAY AGAIN", True, (255, 255, 255))
        screen.blit(btn_txt, (WIDTH//2-75, HEIGHT//2+60))

    pygame.display.flip()
    clock.tick(15)