import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Hit")

BACKGROUND_IMAGE = pygame.image.load('BTL1/background.png')
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

ZOM_WIDTH, ZOM_HEIGHT = 80, 100
GRAVE_POSITIONS = [
    [101, 205 - ZOM_HEIGHT], [350, 204 - ZOM_HEIGHT], [580, 214 - ZOM_HEIGHT],
    [182, 297 - ZOM_HEIGHT], [422, 295 - ZOM_HEIGHT],
    [254, 404 - ZOM_HEIGHT], [505, 414 - ZOM_HEIGHT],
    [98, 514 - ZOM_HEIGHT], [348, 510 - ZOM_HEIGHT], [589, 510 - ZOM_HEIGHT]
]

zombie_img = pygame.image.load('BTL1/zombie.png')
zombie_img = pygame.transform.scale(zombie_img, (ZOM_WIDTH, ZOM_HEIGHT))

hammer_img = pygame.transform.scale(pygame.image.load('BTL1/hammer.png'), (80, 80))
pygame.mouse.set_visible(False)

pygame.mixer.init()
pygame.mixer.music.load('BTL1/BGM.mp3')
hit_sound = pygame.mixer.Sound('BTL1/Hit.mp3')

ZOMBIE_LIFETIME = 3000  
HAMMER_SWING_TIME = 100  
HIT_EFFECT_TIME = 150  
GAME_TIME = 30  

font = pygame.font.Font(None, 36)

def draw_hit_effect(hit_x, hit_y, hit_effect_timer):
    if hit_effect_timer and pygame.time.get_ticks() - hit_effect_timer < HIT_EFFECT_TIME:
        pygame.draw.circle(screen, (255, 0, 0, 200), (hit_x, hit_y), 20)

def animate_hammer(mx, my, hammer_swing, hammer_swing_timer):
    hammer_angle = 60 if hammer_swing else 0
    if hammer_swing and pygame.time.get_ticks() - hammer_swing_timer > HAMMER_SWING_TIME:
        hammer_swing = False
    rotated_hammer = pygame.transform.rotate(hammer_img, hammer_angle)
    screen.blit(rotated_hammer, rotated_hammer.get_rect(center=(mx, my)).topleft)
    return hammer_swing, mx + 10, my + 40 if hammer_swing else my

def check_hit(zombie_x, zombie_y, zombie_visible, hammer_tip_x, hammer_tip_y):
    return zombie_visible and zombie_x < hammer_tip_x < zombie_x + ZOM_WIDTH and zombie_y < hammer_tip_y < zombie_y + ZOM_HEIGHT

def waiting_screen():
    waiting = True
    clock = pygame.time.Clock()
    flash = True
    flash_timer_local = pygame.time.get_ticks()

    background = pygame.image.load('BTL1/background.png')  
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

def game_over_screen(final_score, score_hit, score_miss):
    pygame.mouse.set_visible(True)
    clock = pygame.time.Clock()
    
    flash = True  
    flash_timer_local = pygame.time.get_ticks()  

    while True:
        screen.blit(BACKGROUND_IMAGE, (0, 0))
        screen.blit(font.render("Game Over!", True, (255, 0, 0)), (WIDTH // 2 - 80, HEIGHT // 2 - 100))
        screen.blit(font.render(f"Final Score: {final_score}", True, (0, 0, 255)), (WIDTH // 2 - 80, HEIGHT // 2 - 50))
        screen.blit(font.render(f"Total Hits: {score_hit}", True, (0, 255, 0)), (WIDTH // 2 - 80, HEIGHT // 2))
        screen.blit(font.render(f"Total Misses: {score_miss}", True, (255, 0, 0)), (WIDTH // 2 - 80, HEIGHT // 2 + 50))

        if pygame.time.get_ticks() - flash_timer_local > 500:
            flash = not flash  
            flash_timer_local = pygame.time.get_ticks()

        if flash:
            prompt_text = font.render("Press SPACE to replay or ESC to quit", True, (255, 255, 255))
            screen.blit(prompt_text, (WIDTH // 2 - 180, HEIGHT // 2 + 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        pygame.display.update()
        clock.tick(30)

def main():
    waiting_screen()
    
    while True:
        pygame.mixer.music.play(-1)

        zombie_x, zombie_y = random.choice(GRAVE_POSITIONS)
        zombie_visible = False
        zombie_timer = pygame.time.get_ticks()

        hammer_swing = False
        hammer_swing_timer = 0
        hit_effect_timer = 0
        hit_x, hit_y = 0, 0

        score_hit = 0
        score_miss = 0
        start_time = time.time()

        running = True
        while running:
            time_left = int(GAME_TIME - (time.time() - start_time))
            if time_left <= 0:
                break

            mx, my = pygame.mouse.get_pos()
            screen.blit(BACKGROUND_IMAGE, (0, 0))

            if not zombie_visible and pygame.time.get_ticks() - zombie_timer > ZOMBIE_LIFETIME:
                zombie_visible = True
                zombie_timer = pygame.time.get_ticks()
                zombie_x, zombie_y = random.choice(GRAVE_POSITIONS)

            if zombie_visible:
                screen.blit(zombie_img, (zombie_x, zombie_y))

            draw_hit_effect(hit_x, hit_y, hit_effect_timer)
            hammer_swing, hammer_tip_x, hammer_tip_y = animate_hammer(mx, my, hammer_swing, hammer_swing_timer)

            screen.blit(font.render(f"Hit: {score_hit}", True, (0, 255, 0)), (650, 20))
            screen.blit(font.render(f"Miss: {score_miss}", True, (255, 0, 0)), (650, 60))
            screen.blit(font.render(f"Score: {max(0, score_hit - score_miss)}", True, (255, 255, 0)), (650, 100))
            screen.blit(font.render(f"Time: {time_left}s", True, (0, 0, 255)), (650, 140))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    hammer_swing = True
                    hammer_swing_timer = pygame.time.get_ticks()
                    if check_hit(zombie_x, zombie_y, zombie_visible, hammer_tip_x, hammer_tip_y):
                        score_hit += 1
                        zombie_visible = False
                        hit_effect_timer = pygame.time.get_ticks()
                        hit_x, hit_y = zombie_x + ZOM_WIDTH // 2, zombie_y
                        hit_sound.play()
                        zombie_timer = pygame.time.get_ticks()
                    else:
                        score_miss += 1

            pygame.display.update()

        pygame.mixer.music.stop()
        final_score = max(0, score_hit - score_miss)
        game_over_screen(final_score, score_hit, score_miss)

if __name__ == "__main__":
    main()
