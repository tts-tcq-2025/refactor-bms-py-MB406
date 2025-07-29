from time import sleep
import sys

# Threshold configuration for vitals
VITAL_LIMITS = {
    'temperature': {'min': 95, 'max': 102},
    'pulseRate': {'min': 60, 'max': 100},
    'spo2': {'min': 90, 'max': 100}  # max SpO2 can be assumed 100%
}

def is_within_limits(value, limits):
    """Pure function: check if value is within limits."""
    return limits['min'] <= value <= limits['max']

def check_vitals(temperature, pulseRate, spo2):
    """
    Pure function: returns a tuple (ok:bool, message:str) for first vital that fails.
    If all pass, returns (True, '').
    """
    if not is_within_limits(temperature, VITAL_LIMITS['temperature']):
        return False, 'Temperature critical!'
    if not is_within_limits(pulseRate, VITAL_LIMITS['pulseRate']):
        return False, 'Pulse Rate is out of range!'
    if not is_within_limits(spo2, VITAL_LIMITS['spo2']):
        return False, 'Oxygen Saturation out of range!'
    return True, ''

def blink_alert(message, cycles=6, interval=1):
    """Perform blinking alert on the console for a message."""
    print(message)
    for _ in range(cycles):
        print('\r* ', end='')
        sys.stdout.flush()
        sleep(interval)
        print('\r *', end='')
        sys.stdout.flush()
        sleep(interval)
    print('\r  ')  # Clear blinking after done

def vitals_ok(temperature, pulseRate, spo2):
    ok, msg = check_vitals(temperature, pulseRate, spo2)
    if not ok:
        blink_alert(msg)
    return ok
