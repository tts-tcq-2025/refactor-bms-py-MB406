#!/usr/bin/env python3
"""
Integration test showing backward compatibility and enhanced features working together
"""

import unittest
from monitor import vitals_ok as legacy_vitals_ok
from monitor_enhanced import vitals_ok, vitals_ok_enhanced

class IntegrationTest(unittest.TestCase):
    
    def test_legacy_compatibility(self):
        """Test that enhanced monitor maintains backward compatibility"""
        # Legacy format vitals
        legacy_vitals = {
            'temperature': 98.6,
            'pulseRate': 75,
            'spo2': 97
        }
        
        # Both should return OK for normal vitals
        original_ok, original_failed = legacy_vitals_ok(legacy_vitals)
        enhanced_ok, enhanced_failed = vitals_ok(legacy_vitals)
        
        self.assertTrue(original_ok)
        self.assertTrue(enhanced_ok)
        self.assertEqual(len(original_failed), 0)
        self.assertEqual(len(enhanced_failed), 0)
    
    def test_enhanced_features_with_legacy_format(self):
        """Test enhanced features work with legacy format"""
        # Vitals that trigger warnings in enhanced version
        warning_vitals = {
            'temperature': 96.0,  # Should trigger early warning
            'pulseRate': 75,      # Normal
            'spo2': 97           # Normal
        }
        
        # Legacy version only checks critical limits
        legacy_ok, legacy_failed = legacy_vitals_ok(warning_vitals)
        
        # Enhanced version with legacy interface includes warnings as failures
        enhanced_ok, enhanced_failed = vitals_ok(warning_vitals)
        
        # Legacy should be OK (no critical issues)
        self.assertTrue(legacy_ok)
        
        # Enhanced should detect warning and report as failure for backward compatibility
        self.assertFalse(enhanced_ok)
        self.assertEqual(len(enhanced_failed), 1)
        self.assertIn('Warning', enhanced_failed[0][1])
    
    def test_new_enhanced_interface(self):
        """Test the new enhanced interface with separate warnings and failures"""
        vitals = {
            'temperature': {'value': 96.0, 'unit': 'F'},    # Warning
            'pulseRate': {'value': 58, 'unit': 'bpm'},      # Critical  
            'spo2': {'value': 95, 'unit': '%'}              # Normal
        }
        
        ok, failures, warnings = vitals_ok_enhanced(vitals)
        
        self.assertFalse(ok)
        self.assertEqual(len(failures), 1)   # One critical failure (pulse)
        self.assertEqual(len(warnings), 1)   # One warning (temperature)
        
        # Check that we get the right messages
        self.assertIn('Bradycardia', failures[0][1])
        self.assertIn('hypothermia', warnings[0][1])

if __name__ == '__main__':
    print("Running Integration Tests...")
    print("Testing backward compatibility and enhanced features")
    unittest.main()
