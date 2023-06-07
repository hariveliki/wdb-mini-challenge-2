from dependencies.utils import utils
from dependencies.webscraping.webscraping_enricher_kooples import WebscrapingEnricherKooples
from dependencies.webscraping.webscraping_enricher_smcp import WebscrapingEnricherSMCP
import os, json

def run_enrichment():
    # loop through all products and enrich them per supplier
    for path, dirs, files in os.walk("data/google_cloud"):
        for file in files:
            supplier_nr = file.split("_")[1].split(".")[0]
            supplier_name = utils.get_supplier_name(supplier_nr)
            config = utils.get_config(supplier_nr)
            products = utils.load_json_file(os.path.join(path, file))
            if supplier_name == "Kooples":
                enriched_products = WebscrapingEnricherKooples().enrich_products(products, config)
            else:
                enriched_products = WebscrapingEnricherSMCP().enrich_products(products, config)
            with open("out/enriched_products/{}.json".format(supplier_name), "w") as w:
                json.dump(enriched_products, w)


if __name__ == '__main__':
    run_enrichment()







