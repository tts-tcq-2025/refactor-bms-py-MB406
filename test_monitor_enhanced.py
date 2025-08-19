import unittest
from monitor_enhanced import (
    translate_to_common_units,
    map_value_to_condition,
    get_condition_message,
    vitals_ok_enhanced,
    VitalCondition,
    TEMP_RANGES,
    PULSE_RANGES,
    SPO2_RANGES
)

class MonitorEnhancedTest(unittest.TestCase):
    
    def test_temperature_conditions_fahrenheit(self):
        """Test temperature condition mapping with early warnings"""
        # Test cases: (temp_value, expected_condition)
        test_cases = [
            (94, VitalCondition.HYPO_THERMIA),          # Below 95
            (95, VitalCondition.NEAR_HYPO),             # 95 to 96.53 (95 + 1.53)
            (96.5, VitalCondition.NEAR_HYPO),           # Still in warning range
            (96.54, VitalCondition.NORMAL),             # Normal range starts
            (98.6, VitalCondition.NORMAL),              # Normal body temp
            (100.46, VitalCondition.NORMAL),            # Normal range ends
            (100.47, VitalCondition.NEAR_HYPER),        # Warning range starts (102 - 1.53)
            (101, VitalCondition.NEAR_HYPER),           # Warning range
            (101.99, VitalCondition.NEAR_HYPER),        # Still warning
            (102, VitalCondition.HYPER_THERMIA),        # Critical high
            (103, VitalCondition.HYPER_THERMIA)         # Above 102
        ]
        
        for temp_value, expected_condition in test_cases:
            with self.subTest(temp=temp_value):
                condition = map_value_to_condition(temp_value, TEMP_RANGES)
                self.assertEqual(condition, expected_condition)

    def test_pulse_rate_conditions(self):
        """Test pulse rate condition mapping with early warnings"""
        # Pulse limits: 60-100, warning tolerance = 1.5% of 100 = 1.5
        test_cases = [
            (58, VitalCondition.BRADY_CARDIA),          # Below 60
            (60, VitalCondition.NEAR_BRADY),            # 60 to 61.5
            (61, VitalCondition.NEAR_BRADY),            # Warning range
            (61.51, VitalCondition.NORMAL),             # Normal starts
            (80, VitalCondition.NORMAL),                # Normal range
            (98.49, VitalCondition.NORMAL),             # Normal ends
            (98.5, VitalCondition.NEAR_TACHY),          # Warning starts (100 - 1.5)
            (99, VitalCondition.NEAR_TACHY),            # Warning range
            (99.99, VitalCondition.NEAR_TACHY),         # Still warning
            (100, VitalCondition.TACHY_CARDIA),         # Critical high
            (105, VitalCondition.TACHY_CARDIA)          # Above 100
        ]
        
        for pulse_value, expected_condition in test_cases:
            with self.subTest(pulse=pulse_value):
                condition = map_value_to_condition(pulse_value, PULSE_RANGES)
                self.assertEqual(condition, expected_condition)

    def test_spo2_conditions(self):
        """Test SPO2 condition mapping with early warnings"""
        # SPO2 limits: 90-100, warning tolerance = 1.5% of 100 = 1.5
        test_cases = [
            (88, VitalCondition.LOW_OXYGEN),            # Below 90
            (90, VitalCondition.NEAR_LOW_OXYGEN),       # 90 to 91.5
            (91, VitalCondition.NEAR_LOW_OXYGEN),       # Warning range
            (91.51, VitalCondition.NORMAL),             # Normal starts
            (95, VitalCondition.NORMAL),                # Normal range
            (98.49, VitalCondition.NORMAL),             # Normal ends
            (98.5, VitalCondition.NEAR_HIGH_OXYGEN),    # Warning starts
            (99, VitalCondition.NEAR_HIGH_OXYGEN),      # Warning range
            (99.99, VitalCondition.NEAR_HIGH_OXYGEN),   # Still warning
            (100, VitalCondition.HIGH_OXYGEN),          # At upper limit (critical)
            (101, VitalCondition.HIGH_OXYGEN)           # Above 100
        ]
        
        for spo2_value, expected_condition in test_cases:
            with self.subTest(spo2=spo2_value):
                condition = map_value_to_condition(spo2_value, SPO2_RANGES)
                self.assertEqual(condition, expected_condition)

    def test_condition_messages_english(self):
        """Test message translation for English"""
        expected_messages = {
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
        }
        
        for condition, expected_msg in expected_messages.items():
            with self.subTest(condition=condition):
                message = get_condition_message(condition, 'en')
                self.assertEqual(message, expected_msg)

    def test_unit_conversion_celsius_to_fahrenheit(self):
        """Test temperature unit conversion"""
        # Test cases: (celsius_value, expected_fahrenheit)
        test_cases = [
            (37, 98.6),     # Normal body temperature
            (35, 95),       # Lower limit
            (38.9, 102),    # Upper limit
            (0, 32),        # Freezing point
        ]
        
        for celsius, expected_fahrenheit in test_cases:
            with self.subTest(celsius=celsius):
                fahrenheit = translate_to_common_units(celsius, 'C', 'temperature')
                self.assertAlmostEqual(fahrenheit, expected_fahrenheit, places=1)

    def test_comprehensive_vitals_check(self):
        """Test comprehensive vitals checking with warnings"""
        # Test case with mixed conditions
        vitals = {
            'temperature': {'value': 96, 'unit': 'F'},      # Should be NEAR_HYPO warning
            'pulseRate': {'value': 99, 'unit': 'bpm'},      # Should be NEAR_TACHY warning
            'spo2': {'value': 95, 'unit': '%'}              # Should be NORMAL
        }
        
        ok, failed, warnings = vitals_ok_enhanced(vitals)
        
        # Should not be completely OK due to warnings
        self.assertFalse(ok)
        
        # Should have warnings for temperature and pulse rate only (spo2 is normal)
        self.assertEqual(len(warnings), 2)
        
        # Should have no critical failures
        self.assertEqual(len(failed), 0)

    def test_critical_vitals_check(self):
        """Test vitals with critical conditions"""
        vitals = {
            'temperature': {'value': 104, 'unit': 'F'},
            'pulseRate': {'value': 55, 'unit': 'bpm'},
            'spo2': {'value': 88, 'unit': '%'}
        }
        
        ok, failed, warnings = vitals_ok_enhanced(vitals)
        
        # Should not be OK
        self.assertFalse(ok)
        
        # Should have 3 critical failures
        self.assertEqual(len(failed), 3)

if __name__ == '__main__':
    unittest.main()
