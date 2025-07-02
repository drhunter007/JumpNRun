import pygame
import sys
import random

# Game settings
WIDTH, HEIGHT = 1600, 850
FPS = 60
GRAVITY = 0.7
JUMP_STRENGTH = -16
PLAYER_SPEED = 7
jump_Count = 0
coins_collected = 0
roll_start = False
roll_frame = 0
roll_tick = 0
coin_width = 35
coin_height = 35


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (135, 206, 235)
GROUND = (50, 205, 50)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump and Run")
clock = pygame.time.Clock()

# Player setup
player_size = (40, 60)
player = pygame.Rect(100, HEIGHT - 100, *player_size)
player_vel_y = 0
on_ground = False

player_img = pygame.image.load("player.png").convert_alpha()  # Make sure player.png is in the same folder
player_img = pygame.transform.scale(player_img, player_size)

# Ground setup
ground_height = 20
ground = pygame.Rect(0, HEIGHT - ground_height, WIDTH, ground_height)

# Platform setup
platforms = [
    pygame.Rect(200, HEIGHT - 150, 120, 15), #2
    pygame.Rect(500, HEIGHT - 220, 100, 15), #3
    pygame.Rect(750, HEIGHT - 100, 80, 15), #4
    pygame.Rect(1300, HEIGHT - 110, 60, 15), #8
    pygame.Rect(100, HEIGHT - 330, 100, 15), #1
    pygame.Rect(1200, HEIGHT - 350, 100, 15), #7
    pygame.Rect(850, HEIGHT - 300, 80, 15), #5
    pygame.Rect(1000, HEIGHT - 170, 80, 15), #6
    #Upper Platforms
    pygame.Rect(200, HEIGHT - 550, 120, 15), #2
    pygame.Rect(500, HEIGHT - 440, 100, 15), #3
    pygame.Rect(1500, HEIGHT - 550, 80, 15), #8
    pygame.Rect(100, HEIGHT - 680, 100, 15), #1
    pygame.Rect(1200, HEIGHT - 700, 100, 15), #7
    pygame.Rect(850, HEIGHT - 600, 80, 15), #5
    pygame.Rect(1000, HEIGHT - 430, 60, 15), #6
    pygame.Rect(500, HEIGHT - 760, 150, 15), #big
    pygame.Rect(1450, HEIGHT - 280, 80, 15)
]

coins = [
    pygame.Rect(242, HEIGHT- 200, 35, 35),    
    pygame.Rect(130, HEIGHT- 730, 35, 35),   
    pygame.Rect(875, HEIGHT- 650, 35, 35),    
    pygame.Rect(1520, HEIGHT- 600, 35, 35),
    pygame.Rect(1020, HEIGHT- 220, 35, 35)    
]

def handle_input():
    keys = pygame.key.get_pressed()
    dx = 0
    if keys[pygame.K_LEFT]:
        dx -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        dx += PLAYER_SPEED
    return dx

def check_collision(rect, rect_list):
    for r in rect_list:
        if rect.colliderect(r):
            return r
    return None

coin_img = pygame.image.load("coin.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (coin_width, coin_height))

roll_img_files = [
    "roll1.png", "roll2.png", "roll3.png", "roll4.png", "roll5.png",
    "roll6.png", "roll7.png", "roll8.png", "roll9.png"]
roll_imgs = [pygame.transform.scale(pygame.image.load(f).convert_alpha(), player_size) for f in roll_img_files]
stand_img = pygame.transform.scale(pygame.image.load("player.png").convert_alpha(), player_size)
ROLL_ANIMATION_SPEED = 4

def main():
    global player_vel_y, on_ground, coins_collected
    global roll_start, roll_tick, roll_frame
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dx = handle_input()

        # Jump
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and on_ground:
            player_vel_y = JUMP_STRENGTH
            jump_count += 1
            roll_start = False
            roll_tick = 0
            roll_frame = 0
        if keys[pygame.K_UP] and jump_count == 1:
            player_vel_y = JUMP_STRENGTH + 7
            jump_count += 1
            roll_start = True
            roll_frame = 0
            roll_tick = 0
    
        # Apply gravity
        player_vel_y += GRAVITY
        player.y += int(player_vel_y)

        # Horizontal movement
        player.x += dx
        
        for coin in coins[:]:
            if player.colliderect(coin):
                coins_collected += 1
                platform = random.choice(platforms)
                coin.x = platform.centerx - coin.width // 2
                coin.y = platform.top - coin.height
                print(f"Coins collected: {coins_collected}")

        # Ground collision
        on_ground = False
        if player.colliderect(ground):
            player.bottom = ground.top
            player_vel_y = 0
            on_ground = True
            jump_count = 0
            roll_start = False
            roll_frame = 0

        # Platform collision
        for plat in platforms:
            if player.colliderect(plat) and player_vel_y >= 0:
                if player.bottom - player_vel_y <= plat.top:
                    player.bottom = plat.top
                    player_vel_y = 0
                    on_ground = True
                    jump_count = 0
                    roll_start = False
                    roll_frame = 0

        # Prevent leaving screen
        if player.left < 0:
            player.left = 0
        if player.right > WIDTH:
            player.right = WIDTH
            
            
        if roll_start:
            roll_tick += 1
            if roll_tick % ROLL_ANIMATION_SPEED == 0:
                roll_frame += 1
                if roll_frame >= len(roll_imgs):
                    roll_frame = len(roll_imgs) -1    


        # Drawing
        screen.fill(SKY)
        pygame.draw.rect(screen, GROUND, ground)
        for plat in platforms:
            pygame.draw.rect(screen, (139, 69, 19), plat)
        for coin in coins:
            screen.blit(coin_img, coin.topleft)  
        if roll_start:
            img = roll_imgs[roll_frame]
        else:
            img = stand_img
        screen.blit(img, player.topleft)
                
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()