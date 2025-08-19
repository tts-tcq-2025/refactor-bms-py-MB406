# Enhanced BMS Monitor - TDD Implementation

## Overview

This project implements an enhanced Battery Management System (BMS) Monitor following the Test-Driven Development (TDD) approach as outlined in the [Extension.md](https://github.com/tts-tcq-2025/assignments/blob/main/Extension.md) document.

## Extensions Implemented

### ✅ Extension 1: Early Warning System
- **1.5% tolerance** for early warnings before critical limits
- **Temperature**: 95°F to 96.53°F (approaching hypothermia), 100.47°F to 102°F (approaching hyperthermia)
- **Pulse Rate**: 60 to 61.5 bpm (approaching bradycardia), 98.5 to 100 bpm (approaching tachycardia)
- **SPO2**: 90% to 91.5% (approaching low oxygen), 98.5% to 100% (approaching high oxygen)

### ✅ Extension 2: Multi-Language Support
- **English** (default): Complete medical terminology
- **German**: Full translation of all warning and critical messages
- **Extensible**: Framework supports adding new languages easily

### ✅ Extension 3: Multiple Unit Support  
- **Temperature**: Celsius automatically converted to Fahrenheit
- **Other vitals**: Framework ready for additional unit conversions
- **No duplication**: Limits defined once, conversions handle different inputs

## TDD Approach Implementation

Following the Extension.md guidelines, this implementation uses:

### 1. Data Transformation Pipeline
As recommended, the problem is treated as a series of data transformations:

```python
# Transform 1: Translate to common units
converted_value = translate_to_common_units(value, unit, vital_type)

# Transform 2: Map to condition using data-driven ranges  
condition = map_value_to_condition(converted_value, ranges)

# Transform 3: Translate condition to message
message = get_condition_message(condition, language)

# Transform 4: Infer overall vitals status
overall_status = infer_overall_vitals(all_conditions)
```

### 2. Data-Driven Design
Ranges are defined as data structures, making the code common across parameters:

```python
TEMP_RANGES = [
    (float('-inf'), 94.99, VitalCondition.HYPO_THERMIA),
    (95, 96.53, VitalCondition.NEAR_HYPO),          # Early warning
    (96.54, 100.46, VitalCondition.NORMAL),
    (100.47, 101.99, VitalCondition.NEAR_HYPER),   # Early warning  
    (102, float('inf'), VitalCondition.HYPER_THERMIA)
]
```

### 3. Test-First Development
- **Failing tests written first** to specify requirements
- **Data models defined in asserts** to reflect caregiver needs
- **Complete test coverage** including edge cases and warnings
- **Comprehensive scenarios** testing integration

## Code Quality Improvements

### Original Issues Addressed:
1. ✅ **Reduced cyclomatic complexity**: Functions have single responsibilities
2. ✅ **Separated pure functions from I/O**: Clear data transformation pipeline
3. ✅ **Eliminated duplication**: Common logic across vital types
4. ✅ **Complete test coverage**: All conditions and edge cases covered

### Architecture Benefits:
- **Extensible**: Easy to add new vitals, languages, or units
- **Maintainable**: Clear separation of concerns
- **Testable**: Pure functions with predictable outputs  
- **Scalable**: Data-driven approach supports future requirements

## Usage Examples

### Basic Usage
```python
from monitor_enhanced import vitals_ok_enhanced

vitals = {
    'temperature': {'value': 96, 'unit': 'F'},
    'pulseRate': {'value': 99, 'unit': 'bpm'}, 
    'spo2': {'value': 95, 'unit': '%'}
}

ok, failures, warnings = vitals_ok_enhanced(vitals)
```

### Multi-Language Support
```python
from monitor_enhanced import set_language
set_language('de')  # Switch to German
# All messages now in German
```

### Unit Conversion
```python
vitals = {
    'temperature': {'value': 37, 'unit': 'C'},  # Automatically converts to F
    'pulseRate': {'value': 80, 'unit': 'bpm'},
    'spo2': {'value': 98, 'unit': '%'}
}
```

## Running the Code

### Tests
```bash
python -m unittest test_monitor_enhanced -v
```

### Demo
```bash
python demo_enhanced_bms.py
```

### Legacy Compatibility  
```bash
python -m unittest monitor.test -v  # Original tests still work
```

## Project Structure

```
refactor-bms-py-MB406/
├── monitor.py                 # Original implementation
├── monitor.test.py           # Original tests
├── monitor_enhanced.py       # Enhanced TDD implementation
├── test_monitor_enhanced.py  # Comprehensive test suite
├── demo_enhanced_bms.py      # Demo showcasing features
└── README.md                # This documentation
```

## Technical Implementation Details

### Design Patterns Used:
- **Strategy Pattern**: Different message languages
- **Data-Driven Configuration**: Range definitions  
- **Pipeline Pattern**: Sequential transformations
- **Enum-Based State Machine**: Condition mapping

### Key Features:
- **Type Safety**: Full type hints throughout
- **Error Handling**: Graceful handling of invalid inputs
- **Backward Compatibility**: Legacy API still supported
- **Documentation**: Comprehensive docstrings and examples

## Future Extensibility

The architecture supports easy addition of:
- ✅ **New vital signs**: Add new ranges and conditions
- ✅ **New languages**: Add message translations
- ✅ **New units**: Extend conversion functions
- ✅ **Age-based limits**: Modify ranges based on patient data
- ✅ **Vendor integrations**: Additional input formats

This implementation demonstrates how TDD principles create maintainable, extensible, and reliable healthcare monitoring systems.
