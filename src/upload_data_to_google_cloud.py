from dependencies.akeneo.akeneo_api_client import AkeneoAPIClient
from dependencies.google import google_utils
from dependencies.akeneo import akeneo_utils
from dependencies.utils import utils
from google.cloud import bigquery

def upload_data_to_google_cloud():
    akeneo_credentials = utils.load_json_file('akeneo-stage-credentials.json')
    akeneo_api_client = akeneo_utils.create_akeneo_api_client(akeneo_credentials, AkeneoAPIClient)
    akeneo_api_client.login_with_password()
    akeneo_query = {
        "supplier": [
            {
            "operator" : "IN",
            "value" : ["9000415", "9000359"]
            }
        ]
    }
    products = akeneo_api_client.get_all_pages_from_akeneo_request(akeneo_api_client, "get_products", akeneo_query)
    google_client = bigquery.Client.from_service_account_json("google-cloud-credentials.json")
    sheet_name = "globus-mdm.haris_wdb.products"
    google_utils.fill_google_sheet(google_client, products, sheet_name)


if __name__ == '__main__':
    upload_data_to_google_cloud()