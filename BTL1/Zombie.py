import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
LEFT_WIDTH = 600  
RIGHT_WIDTH = WIDTH - LEFT_WIDTH  
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Hit")

ROWS, COLS = 3, 3  
GRID_SPACING = 10  
CELL_SIZE = min((LEFT_WIDTH - (COLS - 1) * GRID_SPACING) // COLS, 
                (HEIGHT - (ROWS - 1) * GRID_SPACING) // ROWS)
ZOMBIE_SIZE = CELL_SIZE - 40  

BACKGROUND_COLOR = (0, 128, 0)
HOLE_COLOR = (139, 69, 19)

zombie_img_original = pygame.image.load('BTL1/zombie.png')
hammer_img = pygame.transform.scale(pygame.image.load('BTL1/hammer.png'), (80, 80))

pygame.mouse.set_visible(False)

pygame.mixer.init()
pygame.mixer.music.load('BTL1/BGM.mp3')
pygame.mixer.music.play(-1)

hit_sound = pygame.mixer.Sound('BTL1/Hit.mp3')

zombie_positions = [(col * (CELL_SIZE + GRID_SPACING) + GRID_SPACING + (CELL_SIZE - ZOMBIE_SIZE) // 2,
                     row * (CELL_SIZE + GRID_SPACING) + GRID_SPACING + (CELL_SIZE - ZOMBIE_SIZE) // 2)
                    for row in range(ROWS) for col in range(COLS)]

zombie_x, zombie_y = random.choice(zombie_positions)
zombie_timer = pygame.time.get_ticks()
ZOMBIE_LIFETIME = 3000  
zombie_visible = False

scaling_factor = 0.1  
scaling_speed = 0.009

hammer_angle = 0
hammer_swing = False
hammer_swing_timer = 0
HAMMER_SWING_TIME = 100  

hit_effect_timer = 0
HIT_EFFECT_TIME = 150  
hit_x, hit_y = 0, 0  

score_hit = 0
score_miss = 0
font = pygame.font.Font(None, 36)

GAME_TIME = 30  
start_time = time.time()

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, HOLE_COLOR, 
                             (col * (CELL_SIZE + GRID_SPACING), row * (CELL_SIZE + GRID_SPACING), CELL_SIZE, CELL_SIZE))

def draw_hit_effect():
    if hit_effect_timer and pygame.time.get_ticks() - hit_effect_timer < HIT_EFFECT_TIME:
        pygame.draw.circle(screen, (255, 0, 0, 200), (hit_x, hit_y), 20)

def animate_hammer(mx, my):
    global hammer_angle, hammer_swing
    hammer_angle = 60 if hammer_swing else 0
    if hammer_swing and pygame.time.get_ticks() - hammer_swing_timer > HAMMER_SWING_TIME:
        hammer_swing = False

    rotated_hammer = pygame.transform.rotate(hammer_img, hammer_angle)
    screen.blit(rotated_hammer, rotated_hammer.get_rect(center=(mx, my)).topleft)
    return mx + 10, my + 40 if hammer_swing else my

def check_hit(hammer_tip_x, hammer_tip_y):
    return zombie_visible and zombie_x < hammer_tip_x < zombie_x + ZOMBIE_SIZE and zombie_y < hammer_tip_y < zombie_y + ZOMBIE_SIZE

def waiting_screen():
    waiting = True
    clock = pygame.time.Clock()
    flash = True
    flash_timer_local = pygame.time.get_ticks()

    background = pygame.image.load('BTL1/start-background.png')  
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

        screen.blit(background, (0, 0))  

        title_text = font.render("Welcome to Zombie Hit", True, (255, 255, 255))
        prompt_text = font.render("Press any key to start", True, (255, 255, 255))

        if pygame.time.get_ticks() - flash_timer_local > 500:
            flash = not flash
            flash_timer_local = pygame.time.get_ticks()

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height() - 20))
        if flash:
            screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 + 20))

        pygame.display.update()
        clock.tick(30)


def main():
    global zombie_x, zombie_y, zombie_visible, zombie_timer, score_hit, score_miss
    global hammer_angle, hammer_swing, hammer_swing_timer, hit_effect_timer, hit_x, hit_y, scaling_factor

    waiting_screen()

    running = True
    while running:
        time_left = int(GAME_TIME - (time.time() - start_time))
        if time_left <= 0:
            break

        mx, my = pygame.mouse.get_pos()
        screen.fill(BACKGROUND_COLOR)
        draw_grid()

        if not zombie_visible and pygame.time.get_ticks() - zombie_timer > ZOMBIE_LIFETIME:
            zombie_visible = True
            zombie_timer = pygame.time.get_ticks()
            zombie_x, zombie_y = random.choice(zombie_positions)
            scaling_factor = 0.1  

        if zombie_visible:
            if scaling_factor < 1.0:
                scaling_factor += scaling_speed
            scaled_size = int(ZOMBIE_SIZE * scaling_factor)
            scaled_zombie = pygame.transform.scale(zombie_img_original, (scaled_size, scaled_size))
            screen.blit(scaled_zombie, (zombie_x + (ZOMBIE_SIZE - scaled_size) // 2, zombie_y + (ZOMBIE_SIZE - scaled_size) // 2))

        draw_hit_effect()
        hammer_tip_x, hammer_tip_y = animate_hammer(mx, my)

        pygame.draw.rect(screen, (255, 255, 255), (LEFT_WIDTH, 0, RIGHT_WIDTH, HEIGHT)) 
        screen.blit(font.render(f"Hit: {score_hit}", True, (0, 255, 0)), (LEFT_WIDTH + 30, 20))
        screen.blit(font.render(f"Miss: {score_miss}", True, (255, 0, 0)), (LEFT_WIDTH + 30, 60))
        screen.blit(font.render(f"Score: {max(0, score_hit - score_miss)}", True, (255, 255, 0)), (LEFT_WIDTH + 30, 100))
        screen.blit(font.render(f"Time: {time_left}s", True, (0, 0, 255)), (LEFT_WIDTH + 30, 140))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                hammer_swing = True
                hammer_swing_timer = pygame.time.get_ticks()
                if check_hit(hammer_tip_x, hammer_tip_y):
                    score_hit += 1
                    zombie_visible = False
                    hit_effect_timer = pygame.time.get_ticks()
                    hit_x, hit_y = zombie_x + ZOMBIE_SIZE // 2, zombie_y
                    hit_sound.play()
                    zombie_timer = pygame.time.get_ticks()
                else:
                    score_miss += 1

        pygame.display.update()

    pygame.mixer.music.stop()
    screen.fill((255, 255, 255))
    final_score = max(0, score_hit - score_miss)
    pygame.mouse.set_visible(True)
    screen.blit(font.render("Game Over!", True, (255, 0, 0)), (WIDTH // 2 - 80, HEIGHT // 2 - 100))
    screen.blit(font.render(f"Final Score: {final_score}", True, (0, 0, 0)), (WIDTH // 2 - 80, HEIGHT // 2 - 50))
    screen.blit(font.render(f"Total Hits: {score_hit}", True, (0, 255, 0)), (WIDTH // 2 - 80, HEIGHT // 2))
    screen.blit(font.render(f"Total Misses: {score_miss}", True, (255, 0, 0)), (WIDTH // 2 - 80, HEIGHT // 2 + 50))
    
    pygame.display.update()
    pygame.time.delay(5000)
    pygame.quit()

if __name__ == "__main__":
    main()
