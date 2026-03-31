import pygame
import math

# Initialize Pygame and screen
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NVG HUD Demo")

# Tactical Colors
NVG_GREEN = (50, 255, 50)
NVG_DIM = (20, 100, 20)
SOS_RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont("monospace", 18, bold=True)
small_font = pygame.font.SysFont("monospace", 14)

def draw_compass(angle):
    cx, cy = WIDTH // 2, 50
    tape_width = 400
    pygame.draw.line(screen, NVG_GREEN, (cx - tape_width//2, cy), (cx + tape_width//2, cy), 2)
    for i in range(-180, 181, 10):
        pos_angle = (angle + i) % 360
        x = cx + (i * 2)
        if cx - tape_width//2 < x < cx + tape_width//2:
            label = ["N", "E", "S", "W"][int(pos_angle // 90) % 4] if pos_angle % 90 == 0 else ""
            if label:
                txt = font.render(label, True, NVG_GREEN)
                screen.blit(txt, (x - 5, cy - 25))
            pygame.draw.line(screen, NVG_GREEN, (x, cy), (x, cy + 10), 2)

def draw_lidar(dist):
    lx, ly = WIDTH - 220, HEIGHT - 180
    pygame.draw.rect(screen, NVG_GREEN, (lx, ly, 180, 140), 1)
    dist_txt = font.render(f"OBJ DIST: {dist:.2f}m", True, NVG_GREEN)
    screen.blit(dist_txt, (lx + 15, ly + 60))

def draw_map():
    mx, my = 40, HEIGHT - 180
    pygame.draw.circle(screen, NVG_GREEN, (mx + 80, my + 70), 70, 1)
    pygame.draw.circle(screen, NVG_GREEN, (mx + 80, my + 70), 4) # User dot

def draw_hud(sos_active):
    # Crosshair
    pygame.draw.circle(screen, NVG_GREEN, (WIDTH//2, HEIGHT//2), 30, 1)
    if sos_active and (pygame.time.get_ticks() // 500) % 2 == 0:
        sos_txt = font.render("! SOS SIGNAL !", True, SOS_RED)
        screen.blit(sos_txt, (WIDTH // 2 - 60, 120))

# Game Loop
running, angle = True, 0
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    
    # Update simulated values
    angle = (angle + 0.5) % 360
    dist = 5.0 + math.sin(pygame.time.get_ticks() / 500) * 2
    
    # Draw Interface
    draw_compass(angle)
    draw_map()
    draw_lidar(dist)
    draw_hud(sos_active=True)
    
    pygame.display.flip()
    clock.tick(60) # Capped at 60 FPS for smooth animation

pygame.quit()
