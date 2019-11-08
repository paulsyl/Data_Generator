import sys
import subprocess
import os
import filecmp
sys.path.append('../')
import unittest
from random_data_generator.helpers.yaml_file_handling import load_yaml
from random_data_generator.convert_excel import create_object_from_excel


class RandomDataGeneratorTestCase(unittest.TestCase):
    def setUp(self):
        self.star_schema = load_yaml(
            'test_dictionaries/star_data_dictionary.yaml')
        self.parent_child_schema = load_yaml(
            'test_dictionaries/source_data_dictionary.yaml')
        self.excel_schema = create_object_from_excel(
            "source_extract", "test_dictionaries\\excel_template.xlsx")

    def test_schema_loads(self):
        self.assertIsInstance(self.star_schema, dict)
        self.assertIsInstance(self.parent_child_schema, dict)
        self.assertIsInstance(self.excel_schema, dict)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
