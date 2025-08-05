# monitor.test.py
import unittest
from monitor import vitals_ok, check_vitals

class MonitorTest(unittest.TestCase):
    def test_all_vitals_ok(self):
        vitals = {'temperature': 98.6, 'pulseRate': 80, 'spo2': 95}
        ok, failed = vitals_ok(vitals)
        self.assertTrue(ok)
        self.assertEqual(failed, [])

    def test_temperature_too_low(self):
        vitals = {'temperature': 94, 'pulseRate': 80, 'spo2': 95}
        ok, failed = vitals_ok(vitals)
        self.assertFalse(ok)
        self.assertIn(('temperature', 'Temperature critical!'), failed)

    def test_temperature_too_high(self):
        vitals = {'temperature': 103, 'pulseRate': 80, 'spo2': 95}
        ok, failed = vitals_ok(vitals)
        self.assertFalse(ok)
        self.assertIn(('temperature', 'Temperature critical!'), failed)

    def test_pulse_too_low(self):
        vitals = {'temperature': 98, 'pulseRate': 50, 'spo2': 95}
        ok, failed = vitals_ok(vitals)
        self.assertFalse(ok)
        self.assertIn(('pulseRate', 'Pulse Rate is out of range!'), failed)

    def test_pulse_too_high(self):
        vitals = {'temperature': 98, 'pulseRate': 110, 'spo2': 95}
        ok, failed = vitals_ok(vitals)
        self.assertFalse(ok)
        self.assertIn(('pulseRate', 'Pulse Rate is out of range!'), failed)

    def test_spo2_too_low(self):
        vitals = {'temperature': 98, 'pulseRate': 80, 'spo2': 85}
        ok, failed = vitals_ok(vitals)
        self.assertFalse(ok)
        self.assertIn(('spo2', 'Oxygen Saturation out of range!'), failed)

    def test_multiple_failures(self):
        vitals = {'temperature': 103, 'pulseRate': 110, 'spo2': 85}
        ok, failed = vitals_ok(vitals)
        self.assertFalse(ok)
        self.assertEqual(len(failed), 3)

    def test_boundary_conditions(self):
        vitals = {'temperature': 95, 'pulseRate': 60, 'spo2': 90}
        ok, failed = vitals_ok(vitals)
        self.assertTrue(ok)
        vitals = {'temperature': 102, 'pulseRate': 100, 'spo2': 100}
        ok, failed = vitals_ok(vitals)
        self.assertTrue(ok)

if __name__ == '__main__':
    unittest.main()
