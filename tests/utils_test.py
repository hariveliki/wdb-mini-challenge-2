import unittest, os, json, sys, gc
sys.path.append("/Users/haris.alic/Library/CloudStorage/OneDrive-Personal/02-FHNW/3-semester/3-semester-wdb/wdb-mini-challenge-2")
from dependencies.webscraping.webscraping_enricher_smcp import WebscrapingEnricherSMCP
from dependencies.utils import utils


class TestUtils(unittest.TestCase):


    def test_get_supplier_name_success_1(self):
        actual = utils.get_supplier_name("9000415")
        expectation = "SMCP"
        self.assertEqual(expectation, actual)


if __name__ == '__main__':
    unittest.main()