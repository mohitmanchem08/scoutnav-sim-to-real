import math
import unittest

def choose_command(ranges, stop_m=0.35):
    finite = [r for r in ranges if math.isfinite(r) and r > 0.0]
    if not finite:
        return (0.0, 0.0, "FAULT")
    if min(finite) < stop_m:
        return (0.0, 0.55, "TURN")
    return (0.12, 0.0, "FORWARD")

class PolicyTests(unittest.TestCase):
    def test_clear_scan_goes_forward(self):
        self.assertEqual(choose_command([1.0, 2.0]), (0.12, 0.0, "FORWARD"))
    def test_obstacle_causes_turn(self):
        self.assertEqual(choose_command([1.0, 0.2]), (0.0, 0.55, "TURN"))
    def test_no_valid_reading_stops(self):
        self.assertEqual(choose_command([float("nan"), float("inf")]), (0.0, 0.0, "FAULT"))

if __name__ == "__main__":
    unittest.main()
