import sys, os, logging, re
# from pprint import pprint
sys.path.append("dependencies/")
# sys.path.append('c:\\Users\\Haris Alic\\OneDrive\\02. FHNW\\3-semester\\3-semester-wdb\\wdb-mini-challenge-2')
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webscraping.webscraping_enricher_kooples import WebscrapingEnricherKooples as WEK


class WebscrapingEnricherSMCP:


    def __init__(self):
        self.cwd = os.getcwd()
        self.chrome_options = Options()
        self.chrome_options.headless = True

    
    def enrich_products(self, products, config):
        if not products or not config:
            return None
        logging.basicConfig(format='%(levelname)s:%(message)s', filename='log/enrich_products_smcp.log', filemode='w', encoding='utf-8', level=logging.INFO)
        enriched_products, checked_sku, cnt_enriched, cnt_products = [], set(), 0, 0
        for product in products:
            if cnt_products % 10 == 0 and cnt_products != 0:
                print("Checked products: {} at {}".format(cnt_products, self.__class__.__name__))
            supplier_sku = WEK().get_supplier_sku(config, product)
            if not supplier_sku:
                enriched_products.append(self.enrich_product(product, "Article not available"))
                cnt_products += 1
                continue
            if not supplier_sku in checked_sku:
                checked_sku.add(supplier_sku)
                search_url = config.get("search_url")
                url = search_url + supplier_sku
                try:
                    driver = webdriver.Chrome(options = self.chrome_options, service = Service('/opt/homebrew/bin/chromedriver'))
                    try:
                        driver.get(url)
                        try:
                            webpage_content = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, config.get("general_xpaths").get("description"))))
                            description = webpage_content.text
                            enriched_product = self.enrich_product(product, description)
                            enriched_products.append(enriched_product)
                            if cnt_enriched % 5 == 0 and cnt_enriched != 0:
                                print("Enriched products: {} at {}".format(cnt_enriched, self.__class__.__name__))
                            cnt_enriched, cnt_products = cnt_enriched + 1, cnt_products + 1
                        except Exception as e:
                            cnt_products += 1
                            logging.error("Exception occured after driver.get(url): {}".format(e))
                    except Exception as e:
                        cnt_products += 1
                        logging.error("Exception occured at driver.get(url): {}".format(e))
                except Exception as e:
                    cnt_products += 1
                    logging.error("Exception occured at webdriver.Chrome(): {}".format(e))
            else:
                cnt_products += 1

        return enriched_products


    def enrich_product(self, product, value):
        product["www_info"] = value
        return product



