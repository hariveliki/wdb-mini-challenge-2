import os, json
from dependencies.utils import utils


def count_scrappable_products():
    cnt = 0
    for path, dirs, files in os.walk("data/google_cloud"):
        for file in files:
            products = utils.load_json_file(os.path.join(path, file))
            for product in products:
                if product["supplier_sku"] != None:
                    cnt += 1
    print("Scrapped products: {}".format(cnt))


def count_effectively_enriched_products():
    cnt = 0
    for path, dirs, files in os.walk("out/enriched_products"):
        for file in files:
            enriched_products = utils.load_json_file(os.path.join(path, file))
            for enriched_product in enriched_products:
                if enriched_product["www_info"] != None and enriched_product["www_info"] != "Article not available":
                    cnt += 1
    print("Products effectively enriched: {}".format(cnt))


if __name__ == "__main__":
    count_scrappable_products()
    count_effectively_enriched_products()