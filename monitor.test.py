import unittest
from monitor import vitals_ok, check_vitals

class MonitorTest(unittest.TestCase):
    def test_all_vitals_ok(self):
        self.assertTrue(vitals_ok(98.6, 80, 95))
        self.assertEqual(check_vitals(98.6, 80, 95), (True, ''))

    def test_temperature_too_low(self):
        self.assertFalse(vitals_ok(94, 80, 95))
        self.assertEqual(check_vitals(94, 80, 95), (False, 'Temperature critical!'))

    def test_temperature_too_high(self):
        self.assertFalse(vitals_ok(103, 80, 95))
        self.assertEqual(check_vitals(103, 80, 95), (False, 'Temperature critical!'))

    def test_pulse_too_low(self):
        self.assertFalse(vitals_ok(98, 50, 95))
        self.assertEqual(check_vitals(98, 50, 95), (False, 'Pulse Rate is out of range!'))

    def test_pulse_too_high(self):
        self.assertFalse(vitals_ok(98, 110, 95))
        self.assertEqual(check_vitals(98, 110, 95), (False, 'Pulse Rate is out of range!'))

    def test_spo2_too_low(self):
        self.assertFalse(vitals_ok(98, 80, 85))
        self.assertEqual(check_vitals(98, 80, 85), (False, 'Oxygen Saturation out of range!'))

    def test_boundary_conditions(self):
        # Exactly on the lower boundary
        self.assertTrue(vitals_ok(95, 60, 90))
        # Exactly on the upper boundary
        self.assertTrue(vitals_ok(102, 100, 100))

if __name__ == '__main__':
    unittest.main()
