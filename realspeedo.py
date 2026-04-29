import pygame
import serial
import pynmea2
import math

# --- SERIAL ---
ser = serial.Serial("/dev/serial0", 9600, timeout=1)

# --- PYGAME ---
pygame.init()
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GPS Dashboard")

big_font = pygame.font.SysFont(None, 80)
med_font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 28)

clock = pygame.time.Clock()

# --- DATA ---
gps = {
    "speed": 0.0,
    "heading": 0.0,
    "lat": "N/A",
    "lon": "N/A",
    "sats": 0,
    "fix": False
}

# --- PARSER ---
def parse(line):
    try:
        msg = pynmea2.parse(line)

        if isinstance(msg, pynmea2.types.talker.RMC):
            if msg.spd_over_grnd:
                gps["speed"] = float(msg.spd_over_grnd) * 1.15078  # MPH
            if msg.true_course:
                gps["heading"] = float(msg.true_course)

            gps["lat"] = msg.latitude
            gps["lon"] = msg.longitude

        elif isinstance(msg, pynmea2.types.talker.GGA):
            gps["sats"] = int(msg.num_sats)
            gps["fix"] = int(msg.gps_qual) > 0

    except:
        pass

# --- DRAW COMPASS ---
def draw_compass(center, radius, heading):
    pygame.draw.circle(screen, (200, 200, 200), center, radius, 2)

    # Draw N/E/S/W
    directions = ["N", "E", "S", "W"]
    for i, d in enumerate(directions):
        angle = math.radians(i * 90)
        x = center[0] + math.sin(angle) * (radius - 20)
        y = center[1] - math.cos(angle) * (radius - 20)
        text = small_font.render(d, True, (255, 255, 255))
        screen.blit(text, (x - 10, y - 10))

    # Needle
    angle = math.radians(heading)
    x = center[0] + math.sin(angle) * (radius - 10)
    y = center[1] - math.cos(angle) * (radius - 10)

    pygame.draw.line(screen, (255, 0, 0), center, (x, y), 4)

# --- MAIN LOOP ---
running = True
while running:
    screen.fill((10, 10, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read GPS
    if ser.in_waiting:
        line = ser.readline().decode('ascii', errors='replace').strip()
        if line.startswith('$'):
            parse(line)

    # --- SPEED DISPLAY ---
    speed_text = big_font.render(f"{gps['speed']:.1f}", True, (0, 255, 100))
    mph_text = med_font.render("MPH", True, (200, 200, 200))

    screen.blit(speed_text, (80, 150))
    screen.blit(mph_text, (100, 240))

    # --- COMPASS ---
    draw_compass((550, 240), 120, gps["heading"])

    heading_text = med_font.render(f"{gps['heading']:.0f}°", True, (255, 255, 255))
    screen.blit(heading_text, (520, 380))

    # --- INFO PANEL ---
    info_y = 20
    info = [
        f"Fix: {'YES' if gps['fix'] else 'NO'}",
        f"Sats: {gps['sats']}",
        f"Lat: {gps['lat']}",
        f"Lon: {gps['lon']}"
    ]

    for line in info:
        text = small_font.render(line, True, (180, 180, 180))
        screen.blit(text, (20, info_y))
        info_y += 30

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
ser.close()