# monitor.py
from time import sleep
import sys

VITAL_LIMITS = {
    'temperature': {'min': 95, 'max': 102},
    'pulseRate': {'min': 60, 'max': 100},
    'spo2': {'min': 90, 'max': 100}
}

def is_within_limits(value, limits):
    return limits['min'] <= value <= limits['max']

def check_vitals(vitals):
    """
    Returns a list of (vital, message) for all failed checks.
    """
    messages = {
        'temperature': 'Temperature critical!',
        'pulseRate': 'Pulse Rate is out of range!',
        'spo2': 'Oxygen Saturation out of range!'
    }
    failed = []
    for vital, value in vitals.items():
        if not is_within_limits(value, VITAL_LIMITS[vital]):
            failed.append((vital, messages[vital]))
    return failed

def blink_alert(message, cycles=6, interval=1):
    print(message)
    for _ in range(cycles):
        print('\r* ', end='')
        sys.stdout.flush()
        sleep(interval)
        print('\r *', end='')
        sys.stdout.flush()
        sleep(interval)
    print('\r  ')

def vitals_ok(vitals):
    failed = check_vitals(vitals)
    return len(failed) == 0, failed

def handle_vitals(vitals):
    ok, failed = vitals_ok(vitals)
    if not ok:
        for _, msg in failed:
            blink_alert(msg)
    return ok
