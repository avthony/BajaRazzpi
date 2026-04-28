import gpsd
import time

session = gpsd.gps(mode=gpsd.WATCH_ENABLE)

while True:
    report = session.next()
    if report['class'] == 'TPV' and hasattr(report, 'speed'):
        speed_mps = report.speed or 0.0
        speed_mph = speed_mps * 2.23694
        print(f"Speed: {speed_mph:.1f} mph")
    time.sleep(0.2)
