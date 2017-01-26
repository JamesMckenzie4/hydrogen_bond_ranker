from scripts.smarts_tuples import get_smarts_tuples
from scripts.path_definition import scripts_dir
import os
import unittest

class Test_Smarts_Tuples(unittest.TestCase):

    def test_smarts_patterns_file_exists(self):
        os.chdir(scripts_dir)
        os.chdir("../smarts_patterns")
        self.assertTrue("smarts_patterns.txt" in os.listdir(os.getcwd()))
        
    def test_smarts_tuple_creation(self):
        """tests that the smarts named tuple has been created by querying the functional group name of the first named
        tuple in the list, which is water. If this fails it could be that water is not the first functional group 
        defined in smarts_patterns.txt in smarts_patterns dir."""
        
        y = get_smarts_tuples()
        self.assertEquals(y[0].functional_Group, "Water") 

    
