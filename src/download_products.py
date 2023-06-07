from google.cloud import bigquery
import json

amount = 20
supplier = "9000359"
output = []
client = bigquery.Client.from_service_account_json("google-cloud-credentials.json")
query = "SELECT * FROM `globus-mdm.haris_wdb.products` WHERE supplier = '{}' AND supplier_sku != '' LIMIT {}".format(supplier, amount)
query_job = client.query(query)
rows = query_job.result()
for row in rows:
    output.append(dict(row))
with open("out/products/product_examples.json", "w") as w:
    json.dump(output, w)

