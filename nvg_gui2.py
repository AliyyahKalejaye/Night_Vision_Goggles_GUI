import pygame
import math

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1280, 720
NVG_GREEN = (57, 255, 20)
SOS_RED = (255, 30, 30)
MY_COORDS = (6.5244, 3.3792)  # Demo: Lagos
SOS_TARGET = (6.5300, 3.3850) # Target in distress

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font_main = pygame.font.SysFont("monospace", 18, bold=True)
font_big = pygame.font.SysFont("monospace", 32, bold=True)

def calculate_bearing(lat1, lon1, lat2, lon2):
    # Standard formula to find the angle between two points
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dLon = lon2 - lon1
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
    return (math.degrees(math.atan2(y, x)) + 360) % 360

def draw_dummy_google_map(surf, active_sos):
    # Creates a dark-themed map box
    mx, my, size = 100, HEIGHT - 220, 200
    pygame.draw.rect(surf, (10, 30, 10), (mx, my, size, size)) # Map background
    pygame.draw.rect(surf, NVG_GREEN, (mx, my, size, size), 2) # Map border
    # Grid lines (simulating streets)
    for i in range(1, 5):
        pygame.draw.line(surf, (20, 60, 20), (mx, my + i*40), (mx + size, my + i*40))
        pygame.draw.line(surf, (20, 60, 20), (mx + i*40, my), (mx + i*40, my + size))
    # User marker
    pygame.draw.circle(surf, NVG_GREEN, (mx + size//2, my + size//2), 6)
    # SOS marker if active
    if active_sos:
        pygame.draw.circle(surf, SOS_RED, (mx + size//2 + 30, my + size//2 - 40), 8)

# --- MAIN LOOP ---
running, heading, sos_active = True, 0, False
while running:
    screen.fill((0, 5, 0)) # Dark NVG background
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: sos_active = not sos_active
            
    # Keyboard Controls for Demo
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: heading = (heading - 2) % 360
    if keys[pygame.K_RIGHT]: heading = (heading + 2) % 360

    # 1. Compass
    pygame.draw.rect(screen, NVG_GREEN, (WIDTH//2 - 200, 30, 400, 60), 2)
    h_txt = font_big.render(f"{int(heading)}°", True, NVG_GREEN)
    screen.blit(h_txt, (WIDTH//2 - 30, 40))

    # 2. Map & SOS Cords
    draw_dummy_google_map(screen, sos_active)
    if sos_active:
        bearing = calculate_bearing(*MY_COORDS, *SOS_TARGET)
        # SOS Data Display
        cords_txt = font_main.render(f"SOS TARGET: {SOS_TARGET[0]}, {SOS_TARGET[1]}", True, SOS_RED)
        dir_txt = font_main.render(f"BEARING TO SOS: {int(bearing)}°", True, SOS_RED)
        screen.blit(cords_txt, (100, HEIGHT - 260))
        screen.blit(dir_txt, (100, HEIGHT - 240))
        
        # Direction Arrow to SOS
        arrow_angle = math.radians(bearing - heading - 90)
        ax, ay = WIDTH // 2 + math.cos(arrow_angle) * 100, HEIGHT // 2 + math.sin(arrow_angle) * 100
        pygame.draw.line(screen, SOS_RED, (WIDTH//2, HEIGHT//2), (ax, ay), 4)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
