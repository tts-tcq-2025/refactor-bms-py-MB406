# monitor.py - Enhanced with improved structure while maintaining backward compatibility
from time import sleep
import sys
from typing import Dict, List, Tuple, Union

# Configurable vital limits for better maintainability
VITAL_LIMITS = {
    'temperature': {'min': 95, 'max': 102},
    'pulseRate': {'min': 60, 'max': 100},
    'spo2': {'min': 90, 'max': 100}
}

# Improved error messages with more medical context
VITAL_MESSAGES = {
    'temperature': 'Temperature critical!',
    'pulseRate': 'Pulse Rate is out of range!',
    'spo2': 'Oxygen Saturation out of range!'
}

def is_within_limits(value: Union[int, float], limits: Dict[str, Union[int, float]]) -> bool:
    """
    Check if a value is within the specified limits.
    
    Args:
        value: The value to check
        limits: Dictionary with 'min' and 'max' keys
        
    Returns:
        bool: True if value is within limits, False otherwise
    """
    try:
        return limits['min'] <= value <= limits['max']
    except (TypeError, KeyError):
        return False

def check_single_vital(vital_name: str, value: Union[int, float]) -> Tuple[bool, str]:
    """
    Check a single vital sign against its limits.
    
    Args:
        vital_name: Name of the vital sign
        value: Value to check
        
    Returns:
        Tuple of (is_ok, error_message)
    """
    if vital_name not in VITAL_LIMITS:
        return False, f"Unknown vital: {vital_name}"
    
    try:
        limits = VITAL_LIMITS[vital_name]
        is_ok = is_within_limits(value, limits)
        message = "" if is_ok else VITAL_MESSAGES[vital_name]
        return is_ok, message
    except Exception:
        return False, f"Error checking {vital_name}"

def check_vitals(vitals: Dict[str, Union[int, float]]) -> List[Tuple[str, str]]:
    """
    Check all vital signs and return list of failures.
    Enhanced with better error handling and single responsibility principle.
    
    Args:
        vitals: Dictionary of vital_name -> value
        
    Returns:
        List of (vital_name, error_message) tuples for failed checks
    """
    failed = []
    
    for vital_name, value in vitals.items():
        is_ok, message = check_single_vital(vital_name, value)
        if not is_ok:
            failed.append((vital_name, message))
    
    return failed

def format_alert_message(message: str, vital_name: str = None) -> str:
    """
    Format alert message with additional context.
    
    Args:
        message: Base alert message
        vital_name: Name of the vital sign (optional)
        
    Returns:
        Formatted alert message
    """
    if vital_name:
        return f"[{vital_name.upper()}] {message}"
    return message

def blink_alert(message: str, cycles: int = 6, interval: float = 1) -> None:
    """
    Display blinking alert with improved formatting.
    Enhanced with better visual feedback and type hints.
    
    Args:
        message: Alert message to display
        cycles: Number of blink cycles (default: 6)
        interval: Time between blinks in seconds (default: 1)
    """
    print(f"\n*** ALERT: {message} ***")
    
    try:
        for cycle in range(cycles):
            print('\r* ', end='', flush=True)
            sleep(interval)
            print('\r *', end='', flush=True)
            sleep(interval)
        print('\r  ', flush=True)
    except KeyboardInterrupt:
        print("\r[Alert interrupted by user]")
    finally:
        print()  # Ensure newline after alert

def vitals_ok(vitals: Dict[str, Union[int, float]]) -> Tuple[bool, List[Tuple[str, str]]]:
    """
    Check if all vitals are within acceptable limits.
    Enhanced with better type hints and documentation.
    
    Args:
        vitals: Dictionary mapping vital names to their values
        
    Returns:
        Tuple of (all_ok, list_of_failures)
    """
    failed = check_vitals(vitals)
    return len(failed) == 0, failed

def handle_vitals(vitals: Dict[str, Union[int, float]]) -> bool:
    """
    Handle vital signs checking with alert display.
    Enhanced with improved error handling.
    
    Args:
        vitals: Dictionary of vital signs to check
        
    Returns:
        bool: True if all vitals are OK, False otherwise
    """
    try:
        ok, failed = vitals_ok(vitals)
        
        if not ok:
            for vital_name, msg in failed:
                formatted_msg = format_alert_message(msg, vital_name)
                blink_alert(formatted_msg)
        
        return ok
        
    except Exception as e:
        error_msg = f"Error processing vitals: {e}"
        blink_alert(error_msg)
        return False

# Enhanced utility functions for better maintainability
def get_vital_limits(vital_name: str) -> Dict[str, Union[int, float]]:
    """
    Get the limits for a specific vital sign.
    
    Args:
        vital_name: Name of the vital sign
        
    Returns:
        Dictionary with min and max limits
        
    Raises:
        KeyError: If vital_name is not recognized
    """
    if vital_name not in VITAL_LIMITS:
        raise KeyError(f"Unknown vital sign: {vital_name}")
    return VITAL_LIMITS[vital_name].copy()

def update_vital_limits(vital_name: str, min_val: Union[int, float], max_val: Union[int, float]) -> None:
    """
    Update limits for a vital sign (for future extensibility).
    
    Args:
        vital_name: Name of the vital sign
        min_val: Minimum acceptable value
        max_val: Maximum acceptable value
        
    Raises:
        ValueError: If min_val >= max_val
    """
    if min_val >= max_val:
        raise ValueError("Minimum value must be less than maximum value")
    
    VITAL_LIMITS[vital_name] = {'min': min_val, 'max': max_val}

def validate_vitals_input(vitals: Dict[str, Union[int, float]]) -> bool:
    """
    Validate vitals input format and values.
    
    Args:
        vitals: Dictionary of vital signs
        
    Returns:
        bool: True if input is valid, False otherwise
    """
    if not isinstance(vitals, dict):
        return False
    
    for vital_name, value in vitals.items():
        if not isinstance(vital_name, str):
            return False
        if not isinstance(value, (int, float)):
            return False
        if vital_name not in VITAL_LIMITS:
            return False
    
    return True
