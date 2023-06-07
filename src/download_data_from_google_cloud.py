import sys
sys.path.append("/Users/haris.alic/Library/CloudStorage/OneDrive-Personal/02-FHNW/3-semester/3-semester-wdb/wdb-mini-challenge-2")
from dependencies.google import google_utils
from dependencies.utils import utils


def download_data_from_google():
    google_sheet_name = "globus-mdm.haris_wdb.products"
    for supplier in ["9000359"]:
        products = google_utils.get_products_by_supplier(google_sheet_name, supplier)
        utils.write_json_file("data/google/products_{}.json".format(supplier), products)


if __name__ == '__main__':
    download_data_from_google()







