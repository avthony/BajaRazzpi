import gps
import time

session = gps.gps(mode=gps.WATCH_ENABLE)

while True:
    report = session.next()
    if report['class'] == 'TPV' and hasattr(report, 'speed'):
        speed_mps = report.speed or 0.0
        speed_mph = speed_mps * 2.23694
        print(f"Speed: {speed_mph:.1f} mph")
    time.sleep(0.2)
