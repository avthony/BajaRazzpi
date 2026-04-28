import pygame
import serial
import pynmea2

# --- SERIAL SETUP (Raspberry Pi UART) ---
SERIAL_PORT = "/dev/serial0"
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# --- PYGAME SETUP ---
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Raspberry Pi GPS Display")

font = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()

gps_data = {
    "Latitude": "Waiting...",
    "Longitude": "Waiting...",
    "Altitude": "Waiting...",
    "Satellites": "Waiting...",
    "Time": "Waiting...",
    "Fix": "No Fix"
}

def parse_gps(line):
    try:
        msg = pynmea2.parse(line)

        # GGA = fix data
        if isinstance(msg, pynmea2.types.talker.GGA):
            gps_data["Latitude"] = msg.latitude
            gps_data["Longitude"] = msg.longitude
            gps_data["Altitude"] = f"{msg.altitude} m"
            gps_data["Satellites"] = msg.num_sats
            gps_data["Fix"] = "Yes" if int(msg.gps_qual) > 0 else "No"

        # RMC = time + movement
        elif isinstance(msg, pynmea2.types.talker.RMC):
            gps_data["Time"] = msg.timestamp

    except Exception:
        pass  # ignore bad lines

# --- MAIN LOOP ---
running = True
while running:
    screen.fill((0, 0, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read GPS
    if ser.in_waiting:
        line = ser.readline().decode('ascii', errors='replace').strip()
        if line.startswith('$'):
            parse_gps(line)

    # Draw text
    y = 40
    for key, value in gps_data.items():
        text = font.render(f"{key}: {value}", True, (0, 255, 100))
        screen.blit(text, (40, y))
        y += 40

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
ser.close()