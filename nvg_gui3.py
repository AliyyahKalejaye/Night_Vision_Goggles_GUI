import pygame
import cv2
import numpy as np
import math

# --- COLORS & CONFIG ---
HUD_GREEN = (150, 220, 180)  # Muted Pale Green from your image
DARK_GREEN = (20, 40, 30)
SOS_RED = (255, 80, 80)
BG_FILTER = (10, 25, 20)
WIDTH, HEIGHT = 1280, 720

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
cap = cv2.VideoCapture(0) # Change to a video file path if desired

# Load specific fonts (using system fallbacks)
font_sm = pygame.font.SysFont("arial", 14)
font_med = pygame.font.SysFont("arial", 20, bold=True)
font_lg = pygame.font.SysFont("arial", 48, bold=True)

def draw_system_status(surf):
    x, y = 30, 200
    pygame.draw.rect(surf, HUD_GREEN, (x, y, 220, 150), 1)
    surf.blit(font_med.render("SYSTEM STATUS", True, HUD_GREEN), (x+5, y+5))
    
    stats = [("LIDAR", 0.7), ("GPS", 0.4), ("COMM", 0.9), ("POWER", 0.82)]
    for i, (label, val) in enumerate(stats):
        bx = x + 15 + (i * 50)
        # Bar outline
        pygame.draw.rect(surf, HUD_GREEN, (bx, y+40, 30, 80), 1)
        # Bar fill
        pygame.draw.rect(surf, HUD_GREEN, (bx+3, y+40 + (80*(1-val)), 24, 80*val))
        label_txt = font_sm.render(label, True, HUD_GREEN)
        surf.blit(label_txt, (bx - 5, y+125))
    surf.blit(font_sm.render("82%", True, HUD_GREEN), (x+175, y+125))

def draw_lidar_alert(surf):
    x, y = 30, 360
    pygame.draw.rect(surf, HUD_GREEN, (x, y, 220, 100), 1)
    surf.blit(font_med.render("LIDAR ALERT", True, HUD_GREEN), (x+5, y+5))
    surf.blit(font_lg.render("NORMAL", True, HUD_GREEN), (x+10, y+30))
    # Red Warning Box
    pygame.draw.rect(surf, SOS_RED, (x+5, y+80, 210, 40), 1)
    surf.blit(font_sm.render("1m PROXIMITY ALERT", True, SOS_RED), (x+10, y+85))

def draw_map(surf):
    x, y, size = WIDTH - 260, HEIGHT - 330, 230
    pygame.draw.rect(surf, HUD_GREEN, (x, y, size, size), 1)
    # Grid Simulation
    for i in range(1, 6):
        pygame.draw.line(surf, (40, 70, 50), (x, y+i*40), (x+size, y+i*40))
        pygame.draw.line(surf, (40, 70, 50), (x+i*40, y), (x+i*40, y+size))
    # Icons
    pygame.draw.circle(surf, SOS_RED, (x+180, y+60), 15, 2)
    surf.blit(font_sm.render("SOS", True, SOS_RED), (x+170, y+52))
    # Coordinates
    surf.blit(font_sm.render("MY_POS:  6.5244° N, 3.3792° E", True, HUD_GREEN), (x, y+240))
    surf.blit(font_sm.render("SOS_TRK: 6.5300° N, 3.3850° E", True, HUD_GREEN), (x, y+260))

def draw_compass(surf, head):
    cx, cy = WIDTH//2, 70
    # Main Number
    txt = font_lg.render(f"{head:03}° NE", True, HUD_GREEN)
    surf.blit(txt, (cx - 80, cy - 50))
    # Ruler
    pygame.draw.line(surf, HUD_GREEN, (cx-300, cy), (cx+300, cy), 1)
    for i in range(-200, 201, 20):
        val = (head + i//2) % 360
        lx = cx + i
        pygame.draw.line(surf, HUD_GREEN, (lx, cy), (lx, cy+10))
        if val % 30 == 0:
            label = "N" if val == 0 else str(val)
            surf.blit(font_sm.render(label, True, HUD_GREEN), (lx-10, cy-20))

# --- MAIN LOOP ---
running, heading = True, 42
while running:
    ret, frame = cap.read()
    if not ret: break

    # 1. Image Processing (The "Look")
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Tint & Dim
    nvg = cv2.merge([gray//4, gray//2, gray//3]) 
    nvg_surf = pygame.surfarray.make_surface(nvg.swapaxes(0,1))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    # 2. Layering
    screen.blit(nvg_surf, (0,0))
    
    # Target Tracker (Center)
    pygame.draw.rect(screen, SOS_RED, (WIDTH//2 - 20, HEIGHT//2 - 40, 40, 80), 1)
    screen.blit(font_sm.render("SOS_SIGNAL_LOC: 350m", True, SOS_RED), (WIDTH//2 - 60, HEIGHT//2 - 70))
    pygame.draw.line(screen, SOS_RED, (WIDTH//2, HEIGHT//2 + 40), (WIDTH//2 - 150, HEIGHT), 1)

    # Widgets
    draw_system_status(screen)
    draw_lidar_alert(screen)
    draw_map(screen)
    draw_compass(screen, heading)

    pygame.display.flip()
