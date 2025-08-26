"""
Comprehensive test suite for Advanced BMS Monitor
Tests enhanced features including age-based limits, logging, and trends
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import logging
from monitor_advanced import (
    AdvancedMonitor,
    VitalReading,
    PatientProfile,
    VitalCondition,
    VitalLimits,
    create_monitor,
    vitals_ok_advanced
)

class TestAdvancedMonitor(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.monitor = AdvancedMonitor()
        self.elderly_monitor = create_monitor(age=70, profile_type="elderly")
        self.pediatric_monitor = create_monitor(age=10, profile_type="pediatric")
    
    def test_vital_limits_calculation(self):
        """Test warning range calculations"""
        limits = VitalLimits(min_val=60, max_val=100, warning_tolerance=1.5)
        min_val, near_min, near_max, max_val = limits.calculate_warning_ranges()
        
        self.assertEqual(min_val, 60)
        self.assertEqual(near_min, 60.6)  # 60 + 1.5% of 40
        self.assertEqual(near_max, 99.4)  # 100 - 1.5% of 40
        self.assertEqual(max_val, 100)
    
    def test_patient_profile_age_adjustments(self):
        """Test age-based vital limit adjustments"""
        # Adult limits
        adult_profile = PatientProfile(age=30)
        adult_limits = adult_profile.get_vital_limits('pulseRate')
        self.assertEqual(adult_limits.min_val, 60)
        self.assertEqual(adult_limits.max_val, 100)
        
        # Elderly limits
        elderly_profile = PatientProfile(age=70)
        elderly_limits = elderly_profile.get_vital_limits('pulseRate')
        self.assertEqual(elderly_limits.min_val, 50)
        self.assertEqual(elderly_limits.max_val, 90)
        
        # Pediatric limits
        pediatric_profile = PatientProfile(age=10)
        pediatric_limits = pediatric_profile.get_vital_limits('pulseRate')
        self.assertEqual(pediatric_limits.min_val, 80)
        self.assertEqual(pediatric_limits.max_val, 120)
    
    def test_vital_reading_with_metadata(self):
        """Test VitalReading data class"""
        reading = VitalReading(value=98.6, unit='F', source='sensor')
        
        self.assertEqual(reading.value, 98.6)
        self.assertEqual(reading.unit, 'F')
        self.assertEqual(reading.source, 'sensor')
        self.assertIsInstance(reading.timestamp, datetime)
    
    def test_enhanced_unit_conversion(self):
        """Test enhanced unit conversion with validation"""
        reading_celsius = VitalReading(value=37, unit='C')
        converted = self.monitor.convert_units(reading_celsius, 'temperature')
        self.assertAlmostEqual(converted, 98.6, places=1)
        
        # Test invalid unit
        reading_invalid = VitalReading(value=98.6, unit='K')
        with self.assertRaises(ValueError):
            self.monitor.convert_units(reading_invalid, 'temperature')
    
    def test_language_switching(self):
        """Test multi-language support"""
        self.monitor.set_language('de')
        self.assertEqual(self.monitor.language, 'de')
        
        with self.assertRaises(ValueError):
            self.monitor.set_language('fr')  # Unsupported language
    
    def test_vital_assessment_with_age_factors(self):
        """Test vital assessment considering patient age"""
        # Test elderly patient with pulse rate that's normal for elderly but low for adults
        reading = VitalReading(value=55, unit='bpm')
        condition, message = self.elderly_monitor.assess_vital('pulseRate', reading)
        
        # For elderly (limits 50-90), 55 should be in near_brady range
        self.assertEqual(condition, VitalCondition.NEAR_BRADY)
        self.assertIn('WARNING', message)
    
    def test_comprehensive_vital_monitoring(self):
        """Test comprehensive vital monitoring with enhanced reporting"""
        vitals = {
            'temperature': {'value': 98.6, 'unit': 'F', 'source': 'sensor'},
            'pulseRate': {'value': 75, 'unit': 'bpm', 'source': 'sensor'},
            'spo2': {'value': 97, 'unit': '%', 'source': 'sensor'}
        }
        
        results = self.monitor.monitor_vitals(vitals)
        
        # Check result structure
        self.assertIn('timestamp', results)
        self.assertIn('assessments', results)
        self.assertIn('overall_status', results)
        self.assertIn('critical_alerts', results)
        self.assertIn('warnings', results)
        self.assertIn('recommendations', results)
        
        # All vitals should be normal
        self.assertEqual(results['overall_status'], 'NORMAL')
        self.assertEqual(len(results['critical_alerts']), 0)
        self.assertEqual(len(results['warnings']), 0)
    
    def test_critical_vital_monitoring(self):
        """Test monitoring with critical vitals"""
        vitals = {
            'temperature': {'value': 105, 'unit': 'F'},
            'pulseRate': {'value': 45, 'unit': 'bpm'},
            'spo2': {'value': 85, 'unit': '%'}
        }
        
        results = self.monitor.monitor_vitals(vitals)
        
        # Should detect critical status
        self.assertEqual(results['overall_status'], 'CRITICAL')
        self.assertEqual(len(results['critical_alerts']), 3)
        self.assertIn('Immediate medical attention required', results['recommendations'])
    
    def test_warning_vital_monitoring(self):
        """Test monitoring with warning-level vitals"""
        vitals = {
            'temperature': {'value': 96.0, 'unit': 'F'},  # Near hypothermia
            'pulseRate': {'value': 75, 'unit': 'bpm'},    # Normal
            'spo2': {'value': 97, 'unit': '%'}            # Normal
        }
        
        results = self.monitor.monitor_vitals(vitals)
        
        # Should detect warning status
        self.assertEqual(results['overall_status'], 'WARNING')
        self.assertEqual(len(results['warnings']), 1)
        self.assertIn('Monitor closely', results['recommendations'][0])
    
    def test_vital_history_tracking(self):
        """Test vital history tracking"""
        # Add multiple readings
        vitals1 = {'temperature': {'value': 98.6, 'unit': 'F'}}
        vitals2 = {'temperature': {'value': 99.2, 'unit': 'F'}}
        
        self.monitor.monitor_vitals(vitals1)
        self.monitor.monitor_vitals(vitals2)
        
        # Check history
        history = self.monitor.get_vital_trends('temperature')
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['value'], 98.6)
        self.assertEqual(history[1]['value'], 99.2)
    
    def test_factory_function(self):
        """Test factory function for monitor creation"""
        monitor = create_monitor(age=65, profile_type="elderly")
        
        self.assertEqual(monitor.patient_profile.age, 65)
        self.assertEqual(monitor.patient_profile.profile_type, "elderly")
    
    def test_legacy_compatibility_function(self):
        """Test legacy compatibility with advanced features"""
        vitals = {
            'temperature': {'value': 98.6, 'unit': 'F'},
            'pulseRate': {'value': 75, 'unit': 'bpm'},
            'spo2': {'value': 97, 'unit': '%'}
        }
        
        overall_ok, failures, warnings = vitals_ok_advanced(vitals, age=30)
        
        self.assertTrue(overall_ok)
        self.assertEqual(len(failures), 0)
        self.assertEqual(len(warnings), 0)
    
    def test_error_handling(self):
        """Test error handling in vital processing"""
        # Invalid vital data
        vitals = {
            'temperature': {'value': 'invalid', 'unit': 'F'}
        }
        
        with self.assertLogs('BMS_Monitor', level='ERROR'):
            results = self.monitor.monitor_vitals(vitals)
            
        # Should have error in assessment
        self.assertIn('error', results['assessments']['temperature'])
        self.assertEqual(results['assessments']['temperature']['condition'], 'ERROR')
    
    @patch('monitor_advanced.logger')
    def test_logging_functionality(self, mock_logger):
        """Test logging functionality"""
        # Test warning vital that should trigger logging
        reading = VitalReading(value=96.0, unit='F')
        condition, message = self.monitor.assess_vital('temperature', reading)
        
        # Should log warning
        mock_logger.warning.assert_called()
        
        # Test language change logging
        self.monitor.set_language('de')
        mock_logger.info.assert_called_with('Language changed to de')
    
    def test_enhanced_messages_with_emojis(self):
        """Test enhanced message formatting with emojis"""
        # Test critical condition
        reading = VitalReading(value=105, unit='F')
        condition, message = self.monitor.assess_vital('temperature', reading)
        
        self.assertIn('🚨', message)
        self.assertIn('CRITICAL', message)
        
        # Test warning condition
        reading = VitalReading(value=96.0, unit='F')
        condition, message = self.monitor.assess_vital('temperature', reading)
        
        self.assertIn('⚠️', message)
        self.assertIn('WARNING', message)
    
    def test_german_language_messages(self):
        """Test German language message translations"""
        self.monitor.set_language('de')
        
        reading = VitalReading(value=105, unit='F')
        condition, message = self.monitor.assess_vital('temperature', reading)
        
        self.assertIn('🚨', message)
        self.assertIn('KRITISCH', message)
        self.assertIn('Überhitzung', message)

class TestPatientProfiles(unittest.TestCase):
    """Test patient profile functionality"""
    
    def test_default_adult_profile(self):
        """Test default adult patient profile"""
        profile = PatientProfile()
        limits = profile.get_vital_limits('pulseRate')
        
        self.assertEqual(limits.min_val, 60)
        self.assertEqual(limits.max_val, 100)
    
    def test_elderly_pulse_adjustments(self):
        """Test elderly patient pulse rate adjustments"""
        profile = PatientProfile(age=70)
        limits = profile.get_vital_limits('pulseRate')
        
        self.assertEqual(limits.min_val, 50)
        self.assertEqual(limits.max_val, 90)
    
    def test_pediatric_pulse_adjustments(self):
        """Test pediatric patient pulse rate adjustments"""
        profile = PatientProfile(age=12)
        limits = profile.get_vital_limits('pulseRate')
        
        self.assertEqual(limits.min_val, 80)
        self.assertEqual(limits.max_val, 120)

if __name__ == '__main__':
    # Enable logging for tests
    logging.basicConfig(level=logging.DEBUG)
    
    unittest.main(verbosity=2)
