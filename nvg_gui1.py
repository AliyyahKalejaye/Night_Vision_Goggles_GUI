import pygame
import cv2
import numpy as np
import math

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1280, 720
NVG_GREEN = (57, 255, 20)  # High-vis phosphor green
SOS_RED = (255, 30, 30)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
cap = cv2.VideoCapture(0) # Open default webcam
font_main = pygame.font.SysFont("monospace", 22, bold=True)
font_logo = pygame.font.SysFont("impact", 36)

def apply_nvg_filter(frame):
    # Convert to grayscale then apply a green tint & grain
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    noise = np.random.randint(0, 40, (HEIGHT, WIDTH), dtype='uint8')
    nvg_gray = cv2.addWeighted(gray, 0.9, noise, 0.1, 0)
    # Reconstruct as a Green-only RGB image
    green_img = np.zeros((HEIGHT, WIDTH, 3), dtype='uint8')
    green_img[:, :, 1] = nvg_gray # Set only Green channel
    return green_img

def draw_vignette(surf):
    # Simulates the circular frame of night vision goggles
    mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 255))
    # Draw transparent circle in middle
    pygame.draw.circle(mask, (0, 0, 0, 0), (WIDTH//2, HEIGHT//2), HEIGHT//2 - 10)
    surf.blit(mask, (0, 0))

def draw_realistic_compass(surf, heading):
    cx, cy = WIDTH // 2, 80
    pygame.draw.rect(surf, NVG_GREEN, (cx-250, cy-35, 500, 70), 2)
    # Draw moving ticks
    for i in range(-120, 121, 10):
        tick_h = (heading + i) % 360
        x = cx + (i * 2)
        if tick_h % 90 == 0:
            label = ['N', 'E', 'S', 'W'][int(tick_h//90)%4]
            txt = font_main.render(label, True, NVG_GREEN)
            surf.blit(txt, (x-8, cy-30))
        pygame.draw.line(surf, NVG_GREEN, (x, cy), (x, cy+15), 2)
    # Center needle
    pygame.draw.polygon(surf, NVG_GREEN, [(cx, cy+5), (cx-10, cy+25), (cx+10, cy+25)])

def draw_ui(surf, heading, dist):
    # Company Logo
    logo = font_logo.render("PROFORCE AIRSYSTEMS", True, NVG_GREEN)
    surf.blit(logo, (60, 60))
    
    # Live Map Simulation
    mx, my = 180, HEIGHT - 180
    pygame.draw.circle(surf, NVG_GREEN, (mx, my), 90, 2)
    pygame.draw.circle(surf, NVG_GREEN, (mx, my), 5) # User
    # Simulated moving 'satellite' dots
    for i in range(3):
        offset = pygame.time.get_ticks() / 1000 + i
        sx, sy = mx + math.cos(offset) * 60, my + math.sin(offset) * 40
        pygame.draw.circle(surf, NVG_GREEN, (int(sx), int(sy)), 3)

    # Lidar & SOS
    dist_txt = font_main.render(f"RANGE: {dist:.1f}m", True, NVG_GREEN)
    surf.blit(dist_txt, (WIDTH - 280, HEIGHT - 150))
    if (pygame.time.get_ticks() // 500) % 2 == 0:
        sos_txt = font_main.render("! SOS ACTIVE !", True, SOS_RED)
        surf.blit(sos_txt, (WIDTH // 2 - 80, HEIGHT - 80))

# --- MAIN LOOP ---
running, h = True, 0
while running:
    ret, frame = cap.read()
    if not ret: break
    
    # 1. Process Video
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    nvg_frame = apply_nvg_filter(frame)
    # 2. To Pygame
    nvg_frame = cv2.cvtColor(nvg_frame, cv2.COLOR_BGR2RGB)
    raw_surf = pygame.surfarray.make_surface(nvg_frame.swapaxes(0, 1))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    # 3. Draw Overlays
    h = (h + 1) % 360 # Simulated heading
    d = 15.2 + math.sin(h/10) * 5 # Simulated distance
    
    screen.blit(raw_surf, (0, 0))
    draw_vignette(screen)
    draw_realistic_compass(screen, h)
    draw_ui(screen, h, d)
    
    pygame.display.flip()

cap.release()
pygame.quit()
