import unittest
from main_file import calculate_pi

class TestPiCalculation(unittest.TestCase):
    
    def test_calculate_pi_default_precision(self):
        """Test that calculate_pi returns pi to 5 decimal places by default"""
        pi_value = calculate_pi()
        # The value of pi to 5 decimal places is 3.14159
        self.assertAlmostEqual(pi_value, 3.14159, places=5)
        
    def test_calculate_pi_custom_precision(self):
        """Test that calculate_pi works with custom precision"""
        # Test with precision 3
        pi_value_3 = calculate_pi(3)
        self.assertAlmostEqual(pi_value_3, 3.142, places=3)
        
        # Test with precision 7 (should still be accurate)
        pi_value_7 = calculate_pi(7)
        self.assertAlmostEqual(pi_value_7, 3.1415927, places=7)
        
    def test_pi_type(self):
        """Test that the return value is a float"""
        pi_value = calculate_pi()
        self.assertIsInstance(pi_value, float)
        
if __name__ == "__main__":
    unittest.main()