from google.cloud import bigquery
import json

def fill_google_sheet(client, products, sheet_name):
    for product in products:
        try:
            supplier_sku = product["values"]["supplier_sku"][0]["data"]
        except KeyError:
            supplier_sku = None
        try:
            main_ean_number = product["values"]["main_ean_number"][0]["data"]
        except:
            main_ean_number = None
        rows_to_insert = [
            {
                "akeneo_id": product["identifier"],
                "supplier": product["values"]["supplier"][0]["data"],
                "supplier_sku": supplier_sku,
                "ean": main_ean_number,
                "created": product["created"],
                "updated": product["updated"]
            }
        ]
        erros = client.insert_rows_json(sheet_name, rows_to_insert)
        if erros == []:
            print("New rows have been added.")
        else:
            print("Encountered errors while inserting rows: {}".format(erros))


def get_products_by_supplier(sheet_name, supplier) -> list:
    output = []
    client = bigquery.Client.from_service_account_json("google-cloud-credentials.json")
    query = "SELECT * FROM `{}` WHERE supplier = '{}'".format(sheet_name, supplier)
    query_job = client.query(query)
    rows = query_job.result()
    for row in rows:
        output.append(dict(row))
    return output


    