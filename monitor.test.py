import unittest
from monitor import vitals_ok, check_vitals

class MonitorTest(unittest.TestCase):
    def test_temperature(self):
        cases = [
            (94, 80, 95, False, 'Temperature critical!'),
            (103, 80, 95, False, 'Temperature critical!'),
            (95, 80, 95, True, ''),
            (102, 80, 95, True, '')
        ]
        for temp, pulse, spo2, expected_ok, expected_msg in cases:
            with self.subTest(temp=temp):
                ok, failed = vitals_ok({'temperature': temp, 'pulseRate': pulse, 'spo2': spo2})
                self.assertEqual(ok, expected_ok)
                if not expected_ok:
                    self.assertIn(('temperature', expected_msg), failed)

    # Repeat similar grouping for pulse and spo2

if __name__ == '__main__':
    unittest.main()
