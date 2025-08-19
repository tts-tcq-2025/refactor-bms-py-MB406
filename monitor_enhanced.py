"""
Enhanced Battery Management System Monitor
Following TDD approach with Early Warning Extension

This module implements:
1. Early warning system with 1.5% tolerance
2. Support for multiple units (Extension 3)
3. Extensible language support framework (Extension 2 foundation)
4. Data transformation pipeline as recommended
"""

from enum import Enum
from typing import Dict, List, Tuple, Any, Optional

class VitalCondition(Enum):
    """Enumeration of all possible vital conditions"""
    # Temperature conditions
    HYPO_THERMIA = "HYPO_THERMIA"
    NEAR_HYPO = "NEAR_HYPO"
    NORMAL = "NORMAL"
    NEAR_HYPER = "NEAR_HYPER"
    HYPER_THERMIA = "HYPER_THERMIA"
    
    # Pulse rate conditions
    BRADY_CARDIA = "BRADY_CARDIA"
    NEAR_BRADY = "NEAR_BRADY"
    NEAR_TACHY = "NEAR_TACHY"
    TACHY_CARDIA = "TACHY_CARDIA"
    
    # SPO2 conditions
    LOW_OXYGEN = "LOW_OXYGEN"
    NEAR_LOW_OXYGEN = "NEAR_LOW_OXYGEN"
    NEAR_HIGH_OXYGEN = "NEAR_HIGH_OXYGEN"
    HIGH_OXYGEN = "HIGH_OXYGEN"

# Data-driven range definitions with 1.5% tolerance
TEMP_RANGES = [
    (float('-inf'), 94.99, VitalCondition.HYPO_THERMIA),
    (95, 96.53, VitalCondition.NEAR_HYPO),          # 95 to 95 + (1.5% of 102) = 96.53
    (96.54, 100.46, VitalCondition.NORMAL),         # Normal range
    (100.47, 101.99, VitalCondition.NEAR_HYPER),    # 102 - (1.5% of 102) = 100.47 to just under 102
    (102, float('inf'), VitalCondition.HYPER_THERMIA)
]

PULSE_RANGES = [
    (float('-inf'), 59.99, VitalCondition.BRADY_CARDIA),
    (60, 61.5, VitalCondition.NEAR_BRADY),          # 60 to 60 + (1.5% of 100) = 61.5
    (61.51, 98.49, VitalCondition.NORMAL),          # Normal range
    (98.5, 99.99, VitalCondition.NEAR_TACHY),       # 100 - (1.5% of 100) = 98.5 to just under 100
    (100, float('inf'), VitalCondition.TACHY_CARDIA)
]

SPO2_RANGES = [
    (float('-inf'), 89.99, VitalCondition.LOW_OXYGEN),
    (90, 91.5, VitalCondition.NEAR_LOW_OXYGEN),     # 90 to 90 + (1.5% of 100) = 91.5
    (91.51, 98.49, VitalCondition.NORMAL),          # Normal range  
    (98.5, 99.99, VitalCondition.NEAR_HIGH_OXYGEN), # 100 - (1.5% of 100) = 98.5 to just under 100
    (100, float('inf'), VitalCondition.HIGH_OXYGEN)
]

# Message templates by language
MESSAGES = {
    'en': {
        VitalCondition.HYPO_THERMIA: "Temperature critical! Hypothermia detected",
        VitalCondition.NEAR_HYPO: "Warning: Approaching hypothermia",
        VitalCondition.NORMAL: "",
        VitalCondition.NEAR_HYPER: "Warning: Approaching hyperthermia", 
        VitalCondition.HYPER_THERMIA: "Temperature critical! Hyperthermia detected",
        VitalCondition.BRADY_CARDIA: "Pulse Rate critical! Bradycardia detected",
        VitalCondition.NEAR_BRADY: "Warning: Approaching bradycardia",
        VitalCondition.NEAR_TACHY: "Warning: Approaching tachycardia",
        VitalCondition.TACHY_CARDIA: "Pulse Rate critical! Tachycardia detected",
        VitalCondition.LOW_OXYGEN: "Oxygen Saturation critical! Hypoxemia detected",
        VitalCondition.NEAR_LOW_OXYGEN: "Warning: Approaching low oxygen saturation",
        VitalCondition.NEAR_HIGH_OXYGEN: "Warning: Approaching high oxygen saturation",
        VitalCondition.HIGH_OXYGEN: "Oxygen Saturation critical! Hyperoxemia detected"
    },
    'de': {  # German language support (Extension 2)
        VitalCondition.HYPO_THERMIA: "Temperatur kritisch! Unterkühlung erkannt",
        VitalCondition.NEAR_HYPO: "Warnung: Annäherung an Unterkühlung",
        VitalCondition.NORMAL: "",
        VitalCondition.NEAR_HYPER: "Warnung: Annäherung an Überhitzung",
        VitalCondition.HYPER_THERMIA: "Temperatur kritisch! Überhitzung erkannt",
        VitalCondition.BRADY_CARDIA: "Puls kritisch! Bradykardie erkannt",
        VitalCondition.NEAR_BRADY: "Warnung: Annäherung an Bradykardie",
        VitalCondition.NEAR_TACHY: "Warnung: Annäherung an Tachykardie",
        VitalCondition.TACHY_CARDIA: "Puls kritisch! Tachykardie erkannt",
        VitalCondition.LOW_OXYGEN: "Sauerstoffsättigung kritisch! Hypoxämie erkannt",
        VitalCondition.NEAR_LOW_OXYGEN: "Warnung: Annäherung an niedrige Sauerstoffsättigung",
        VitalCondition.NEAR_HIGH_OXYGEN: "Warnung: Annäherung an hohe Sauerstoffsättigung",
        VitalCondition.HIGH_OXYGEN: "Sauerstoffsättigung kritisch! Hyperoxämie erkannt"
    }
}

# Global language setting (Extension 2)
CURRENT_LANGUAGE = 'en'

def translate_to_common_units(value: float, unit: str, vital_type: str) -> float:
    """
    Transform 1: Translate measurements to common units
    All temperatures converted to Fahrenheit, other units remain as-is
    """
    if vital_type == 'temperature' and unit.upper() == 'C':
        return (value * 9/5) + 32
    return value

def map_value_to_condition(value: float, ranges: List[Tuple]) -> VitalCondition:
    """
    Transform 2: Map value to condition using data-driven ranges
    This function is common across all parameters, varying only the data
    """
    for min_val, max_val, condition in ranges:
        if min_val <= value <= max_val:
            return condition
    return VitalCondition.NORMAL

def get_condition_message(condition: VitalCondition, language: str = None) -> str:
    """
    Transform 3: Translate condition to message in appropriate language
    """
    if language is None:
        language = CURRENT_LANGUAGE
    
    return MESSAGES.get(language, MESSAGES['en']).get(condition, "")

def process_single_vital(vital_name: str, vital_data: Dict[str, Any]) -> Tuple[VitalCondition, str]:
    """
    Transform chain composition: Process one vital through all transformations
    """
    # Extract value and unit
    if isinstance(vital_data, dict):
        value = vital_data.get('value')
        unit = vital_data.get('unit', '')
    else:
        value = vital_data
        unit = ''
    
    # Transform 1: Convert to common units
    converted_value = translate_to_common_units(value, unit, vital_name)
    
    # Transform 2: Map to condition
    ranges_map = {
        'temperature': TEMP_RANGES,
        'pulseRate': PULSE_RANGES, 
        'spo2': SPO2_RANGES
    }
    
    condition = map_value_to_condition(converted_value, ranges_map[vital_name])
    
    # Transform 3: Get message
    message = get_condition_message(condition)
    
    return condition, message

# Define condition sets as module constants to reduce complexity
CRITICAL_CONDITIONS = {
    VitalCondition.HYPO_THERMIA, VitalCondition.HYPER_THERMIA,
    VitalCondition.BRADY_CARDIA, VitalCondition.TACHY_CARDIA,
    VitalCondition.LOW_OXYGEN, VitalCondition.HIGH_OXYGEN
}

WARNING_CONDITIONS = {
    VitalCondition.NEAR_HYPO, VitalCondition.NEAR_HYPER,
    VitalCondition.NEAR_BRADY, VitalCondition.NEAR_TACHY,
    VitalCondition.NEAR_LOW_OXYGEN, VitalCondition.NEAR_HIGH_OXYGEN
}

def has_conditions_of_type(conditions: List[VitalCondition], condition_set: set) -> bool:
    """Helper function to check if any conditions match a given set"""
    return any(condition in condition_set for condition in conditions)

def infer_overall_vitals(conditions: List[VitalCondition]) -> Tuple[bool, str]:
    """
    Transform 4: Infer overall vital status
    Makes logical assumptions for warning and error combinations
    """
    if has_conditions_of_type(conditions, CRITICAL_CONDITIONS):
        return False, "Critical vital signs detected"
    elif has_conditions_of_type(conditions, WARNING_CONDITIONS):
        return False, "Warning conditions detected"
    else:
        return True, "All vitals normal"

def classify_message(message: str) -> str:
    """Helper function to classify message type"""
    return "critical" if "critical" in message.lower() else "warning"

def categorize_single_message(vital_name: str, message: str, failed: List, warnings: List):
    """Categorize a single message as critical or warning"""
    if message:  # Non-empty message indicates an issue
        message_type = classify_message(message)
        if message_type == "critical":
            failed.append((vital_name, message))
        else:
            warnings.append((vital_name, message))

def process_vital_messages(vitals: Dict[str, Any]) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]], List[VitalCondition]]:
    """Process all vitals and categorize messages"""
    failed = []
    warnings = []
    conditions = []
    
    for vital_name, vital_data in vitals.items():
        condition, message = process_single_vital(vital_name, vital_data)
        conditions.append(condition)
        categorize_single_message(vital_name, message, failed, warnings)
    
    return failed, warnings, conditions

def vitals_ok_enhanced(vitals: Dict[str, Any]) -> Tuple[bool, List[Tuple[str, str]], List[Tuple[str, str]]]:
    """
    Enhanced vitals checking with early warning support
    Returns: (overall_ok, critical_failures, warnings)
    """
    failed, warnings, conditions = process_vital_messages(vitals)
    overall_ok, _ = infer_overall_vitals(conditions)
    return overall_ok, failed, warnings

def set_language(language_code: str):
    """Set global language for messages"""
    global CURRENT_LANGUAGE
    if language_code in MESSAGES:
        CURRENT_LANGUAGE = language_code
    else:
        raise ValueError(f"Language '{language_code}' not supported")

# Legacy compatibility functions
def vitals_ok(vitals: Dict[str, float]) -> Tuple[bool, List[Tuple[str, str]]]:
    """
    Legacy compatibility function
    Converts old format to new format and returns only critical failures
    """
    # Convert old format to new format
    new_format_vitals = {}
    for vital_name, value in vitals.items():
        new_format_vitals[vital_name] = {'value': value, 'unit': ''}
    
    overall_ok, failed, warnings = vitals_ok_enhanced(new_format_vitals)
    
    # For legacy compatibility, include warnings as failures
    all_issues = failed + warnings
    final_ok = len(all_issues) == 0
    
    return final_ok, all_issues
