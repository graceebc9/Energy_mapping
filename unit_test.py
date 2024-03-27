import unittest
import pandas as pd
import numpy as np

from src import fill_premise_floor_types, calc_area_vars, calc_vars 

class TestBuildingFunctions(unittest.TestCase):
    def setUp(self):
        # Setup sample DataFrame for testing
        self.sample_df = pd.DataFrame({
            'premise_area': [100, 200, np.nan, 400],
            'height': [10, 20, 30, 40],
            'premise_floor_count': [1, 2, np.nan, 4],
            'basement': ['Basement confirmed', None, 'Basement likely', None],
            'premise_use': ['Residential', 'Residential', 'Commercial', 'Residential'],
            'listed_grade': [None, 'Grade II', None, 'Grade I']
        })

        # Sample pc_area for testing calc_area_vars
        self.pc_area = 1000

    def test_fill_premise_floor_types(self):
        modified_df = fill_premise_floor_types(self.sample_df.copy())
        self.assertFalse(modified_df['premise_floor_count'].isna().any(), "Should fill all NaN floor counts")

    def test_calc_area_vars(self):
        # Call calc_area_vars with the sample DataFrame and pc_area
        results = calc_area_vars(self.sample_df.copy(), self.pc_area)

        # Example check (adjust according to your expected values)
        self.assertNotEqual(results[0], -999, "Percentage residential should not be -999")
        # Add more assertions here based on your expected outcomes

    def test_calc_vars(self):
        # Assuming prob_cols is identified before calling calc_vars
        prob_cols = ['premise_area', 'height']
        results = calc_vars(self.sample_df.copy(), prob_cols)

        # Example check (adjust according to your expected values)
        self.assertEqual(len(results), 4, "Should return 4 elements")
        # Add more assertions here based on your expected outcomes

if __name__ == '__main__':
    unittest.main()
