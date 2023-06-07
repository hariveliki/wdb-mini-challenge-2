import sys, os, logging, re
from pprint import pprint
# sys.path.append("dependencies/")
# sys.path.append('c:\\Users\\Haris Alic\\OneDrive\\02. FHNW\\3-semester\\3-semester-wdb\\wdb-mini-challenge-2')
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebscrapingEnricherKooples:
    def __init__(self):
        self.cwd = os.getcwd()
        self.chrome_options = Options()
        self.chrome_options.headless = True


    def enrich_products(self, products, config):
        if not products or not config:
            return None
        logging.basicConfig(format='%(levelname)s:%(message)s', filename='log/enrich_products_kooples.log', filemode='w', encoding='utf-8', level=logging.INFO)
        enriched_products, checked_sku, cnt_enriched, cnt_products = [], set(), 0, 0
        for product in products:
            if cnt_products % 10 == 0 and cnt_products != 0:
                print("Checked products: {} at {}".format(cnt_products, self.__class__.__name__))
            supplier_sku = self.get_supplier_sku(config, product)
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
                            title = driver.find_element(By.XPATH, config.get("general_xpaths").get("title"))
                            numbers_of_products = re.findall('[0-9]+', title.text)
                            numbers_of_products = int(numbers_of_products[0])
                            driver.quit()
                            enriched_product = self.handle_multiple_xpaths(product, config, numbers_of_products, url)
                            enriched_products.append(enriched_product)
                            if cnt_enriched % 5 == 0 and cnt_enriched != 0:
                                print("Enriched products: {} at {}".format(cnt_enriched, self.__class__.__name__))
                            cnt_enriched, cnt_products = cnt_enriched + 1, cnt_products + 1
                        except Exception as e:
                            logging.error("Failed to get the Title from the Website, transferred parameters: {}: Exception occured {}".format(config.get("general_xpaths").get("title"), e.__class__.__name__))
                            enriched_product = self.enrich_product(product, "Article not available")
                            enriched_products.append(enriched_product)
                            cnt_products += 1
                    except Exception as e:
                        cnt_products += 1
                        logging.error("Exception occured at driver.get(url): {}".format(e.args[0]))
                except Exception as e:
                    cnt_products += 1
                    logging.error("Exception occured at webdriver.Chrome(): {}".format(e))
            else:
                cnt_products += 1

        return enriched_products


    @staticmethod
    def get_supplier_sku(config, product):
        search_attribute = config.get("search_attribute")
        return product.get(search_attribute)


    def enrich_product(self, product, value, additional_supplier_sku=None):
        if additional_supplier_sku and "www_info" not in product:
            product["www_info"] = {additional_supplier_sku : value}
        if additional_supplier_sku and "www_info" in product:
            product["www_info"].update({additional_supplier_sku : value})
        else:
            product["www_info"] = value
        return product

    
    def handle_multiple_xpaths(self, product, config, number_of_webpages, url):
        front_page = url
        logging.info("Started WebscrapingEnricher().handle_multiple_xpaths()")
        for number_of_webpage in range(number_of_webpages):
            number_of_webpage = str(number_of_webpage)
            try:
                driver = webdriver.Chrome(options = self.chrome_options, service = Service('/opt/homebrew/bin/chromedriver'))
                try:
                    driver.get(front_page)
                    try:
                        webpage_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, config.get("webpage_xpaths").get(number_of_webpage))))
                        article_url = webpage_element.get_attribute('href')
                        try:
                            driver.get(article_url)
                            try:
                                additional_supplier_sku = self.get_supplier_sku_from_url_string(article_url)
                                webpage_description = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, config.get("general_xpaths").get("description"))))
                                description = webpage_description.text
                                driver.quit()
                                enriched_product = self.enrich_product(product, description, additional_supplier_sku)
                                logging.info("Successfully enriched product")
                            except Exception as e:
                                logging.error("DOM element not found: {} Exception raised {}".format(config.get("general_xpaths").get("description"), e.args[0]))
                                return self.enrich_product(product, None, additional_supplier_sku)
                        except Exception as e:
                            logging.error("Failed to load following webpage: {}".format(article_url))
                            additional_supplier_sku = self.get_supplier_sku_from_url_string(article_url)
                            return self.enrich_product(product, None, additional_supplier_sku)
                    except Exception as e:
                        logging.error("DOM element not found: {} Exception raised: {}".format(config.get("webpage_xpaths").get(number_of_webpage), e.args[0]))
                        return self.enrich_product(product, None)
                except Exception as e:
                    logging.error("Failed to load a web page: {} in the current browser session, Exception raised {}".format(front_page, e.args[0]))
            except Exception as e:
                logging.error("Failed to create a new instance of the chrome driver, Exception raised {}".format(e.args[0]))
        return enriched_product
    

    def get_additional_supplier_sku_from_parent_page_url(self, webpage):
        try:
            url_string = webpage.parent.current_url
            supplier_sku = self.get_supplier_sku_from_url_string(url_string)
            return supplier_sku
        except Exception as e: 
            logging.error("Failed to get additional supplier sku. Exception occured: {}".format(e.args[0]))
    

    def get_supplier_sku_from_url_string(self, url_string):
        """https://www.thekooples.com/int/de_CH/damen/bekleidung/hosen/bedruckte-seidenhose-FPAN25016KKAK05.html"""
        splitted = url_string.split("/")
        name_sku_html = splitted[-1]
        name_sku_html = name_sku_html.split(".")
        name_sku = name_sku_html[-2]
        name_sku = name_sku.split("-")
        sku = name_sku[-1]
        return sku
