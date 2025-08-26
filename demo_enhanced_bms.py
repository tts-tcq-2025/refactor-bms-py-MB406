#!/usr/bin/env python3
"""
Demo script showcasing the Enhanced BMS Monitor with Early Warning System
Implementation following TDD approach as described in Extension.md

This demonstrates:
1. Extension 1: Early Warning System with 1.5% tolerance
2. Extension 2: Multi-language support (English and German)
3. Extension 3: Multiple unit support (Celsius/Fahrenheit)
"""

from typing import Dict, List, Any
from monitor_enhanced import (
    vitals_ok_enhanced, 
    set_language,
    VitalCondition,
    process_single_vital
)

def display_vitals(vitals: Dict[str, Any]):
    """Helper function to display vital signs"""
    for vital_name, vital_data in vitals.items():
        print(f"  {vital_name}: {vital_data['value']} {vital_data['unit']}")

def display_status(overall_ok: bool):
    """Helper function to display status"""
    status = "✅ NORMAL" if overall_ok else "⚠️ ATTENTION REQUIRED"
    print(f"  Status: {status}")

def display_messages(messages: List, icon: str):
    """Helper function to display messages with icon"""
    for vital_name, message in messages:
        print(f"    {icon} {message}")

def display_results(overall_ok: bool, failures: List, warnings: List):
    """Helper function to display test results"""
    display_status(overall_ok)
    display_messages(warnings, "⚠️ ")
    display_messages(failures, "🚨")

def run_test_scenario(scenario: Dict[str, Any]):
    """Run a single test scenario"""
    print(f"\nScenario: {scenario['name']}")
    vitals = scenario['vitals']
    
    display_vitals(vitals)
    overall_ok, failures, warnings = vitals_ok_enhanced(vitals)
    display_results(overall_ok, failures, warnings)
    print()

def get_test_scenarios():
    """Return predefined test scenarios"""
    return [
        {
            'name': 'Normal Patient',
            'vitals': {
                'temperature': {'value': 98.6, 'unit': 'F'},
                'pulseRate': {'value': 75, 'unit': 'bpm'},
                'spo2': {'value': 97, 'unit': '%'}
            }
        },
        {
            'name': 'Early Warning - Approaching Hypothermia',
            'vitals': {
                'temperature': {'value': 96.0, 'unit': 'F'},
                'pulseRate': {'value': 70, 'unit': 'bpm'},
                'spo2': {'value': 96, 'unit': '%'}
            }
        },
        {
            'name': 'Early Warning - Approaching Tachycardia',
            'vitals': {
                'temperature': {'value': 98.6, 'unit': 'F'},
                'pulseRate': {'value': 99, 'unit': 'bpm'},
                'spo2': {'value': 95, 'unit': '%'}
            }
        },
        {
            'name': 'Critical Patient - Multiple Issues',
            'vitals': {
                'temperature': {'value': 105, 'unit': 'F'},
                'pulseRate': {'value': 54, 'unit': 'bpm'},
                'spo2': {'value': 87, 'unit': '%'}
            }
        },
        {
            'name': 'Patient with Celsius Temperature',
            'vitals': {
                'temperature': {'value': 37, 'unit': 'C'},
                'pulseRate': {'value': 80, 'unit': 'bpm'},
                'spo2': {'value': 98, 'unit': '%'}
            }
        }
    ]

def demo_early_warning_system():
    """Demonstrate the early warning system in action"""
    print("=" * 60)
    print("BMS ENHANCED MONITOR - EARLY WARNING SYSTEM DEMO")
    print("=" * 60)
    
    test_scenarios = get_test_scenarios()
    
    # Test in English
    set_language('en')
    print(f"\n🇺🇸 TESTING IN ENGLISH")
    print("-" * 40)
    
    for scenario in test_scenarios:
        run_test_scenario(scenario)
    
    # Test in German
    set_language('de')
    print(f"\n🇩🇪 TESTING IN GERMAN (DEUTSCH)")
    print("-" * 40)
    
    # Test one critical scenario in German
    critical_scenario = test_scenarios[3]  # Critical patient
    run_test_scenario(critical_scenario)

def demo_data_transformation_pipeline():
    """Demonstrate the data transformation pipeline approach"""
    print("\n" + "=" * 60)
    print("DATA TRANSFORMATION PIPELINE DEMO")
    print("=" * 60)
    
    # Set back to English
    set_language('en')
    
    print("\nDemonstrating the 4-step transformation pipeline:")
    print("1. Translate to common units")
    print("2. Map value to condition")
    print("3. Translate condition to message")
    print("4. Infer overall vitals")
    
    test_value = 35  # 35°C
    print(f"\nExample: Temperature = {test_value}°C")
    
    # Step-by-step transformation
    condition, message = process_single_vital('temperature', {'value': test_value, 'unit': 'C'})
    
    print(f"  After transformation pipeline:")
    print(f"    Condition: {condition.value}")
    print(f"    Message: '{message}'")

if __name__ == "__main__":
    demo_early_warning_system()
    demo_data_transformation_pipeline()
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("\nFeatures implemented following TDD approach:")
    print("✅ Extension 1: Early Warning System (1.5% tolerance)")
    print("✅ Extension 2: Multi-language support (EN/DE)")
    print("✅ Extension 3: Multiple units (Celsius/Fahrenheit)")
    print("✅ Data transformation pipeline")
    print("✅ Comprehensive test coverage")
    print("✅ Clean separation of concerns")
    print("✅ Extensible architecture")
