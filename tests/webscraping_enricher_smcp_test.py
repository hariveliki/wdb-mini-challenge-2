import unittest, os, json, sys, gc
sys.path.append("/Users/haris.alic/Library/CloudStorage/OneDrive-Personal/02-FHNW/3-semester/3-semester-wdb/wdb-mini-challenge-2")
from dependencies.webscraping.webscraping_enricher_smcp import WebscrapingEnricherSMCP


class TestWebscrapingEnricherSMCP(unittest.TestCase):


    @classmethod
    def setUp(self):
        self.cwd = os.getcwd()
        with open(self.cwd + "/tests/fixtures/webscraping_enricher_smcp/product_example.json") as f:
            self.product = json.load(f)
        with open(self.cwd + "/data/supplier_config/9000415_smcp.json") as f:
            self.smcp_config = json.load(f)
    

    @classmethod
    def tearDown(self):
        del self.product
        del self.smcp_config
        gc.collect()


    def test_enrich_products_success_1(self):
        # add info that product is not available if supplier_sku is missing
        for product in self.product:
            if product["supplier_sku"] != None:
                product["supplier_sku"] = None
        actual = WebscrapingEnricherSMCP().enrich_products([product], self.smcp_config)
        expectation = [
            {
                "akeneo_id": "f7d7ad4a211911ed94c81aabff81848fairflow",
                "supplier": "9000415",
                "supplier_sku": None,
                "www_info": "Article not available",
                "ean": "3609140458213",
                "created": "2022-08-25T13:15:55+00:00",
                "updated": "2022-09-01T03:35:29+00:00"
            }
        ]
        self.assertEqual(expectation, actual)


    def test_enrich_product_success_2(self):
        # how to add data if there is nothing to enrich
        actual = []
        for product in self.product:
            enriched_product = WebscrapingEnricherSMCP().enrich_product(product, None)
            actual.append(enriched_product)
        expectation = [
            {
                "akeneo_id": "f7d7ad4a211911ed94c81aabff81848fairflow",
                "supplier": "9000415",
                "supplier_sku": "CFPJE00213",
                "ean": "3609140458213",
                "created": "2022-08-25T13:15:55+00:00",
                "updated": "2022-09-01T03:35:29+00:00",
                "www_info": None
            }
        ]
        self.assertEqual(expectation, actual)


    def test_enrich_product_success_3(self):
        # how to add data if there is something to enrich
        actual = []
        for product in self.product:
            enriched_product = WebscrapingEnricherSMCP().enrich_product(product, "some description")
            actual.append(enriched_product)
        expectation = [
            {
                "akeneo_id": "f7d7ad4a211911ed94c81aabff81848fairflow",
                "supplier": "9000415",
                "supplier_sku": "CFPJE00213",
                "ean": "3609140458213",
                "created": "2022-08-25T13:15:55+00:00",
                "updated": "2022-09-01T03:35:29+00:00",
                "www_info": "some description"
            }
        ]
        self.assertEqual(expectation, actual)


if __name__ == '__main__':
    unittest.main()