# Introduction and Instructions
The idea behind this repository is to enrich existing products (retail) with a specific data structure,<br />
from the description given at the vendors online store.<br />
The product data is stored locally on your machine under data/google_cloud/products_xy.json.<br />
All products are matched with the vendor's sku (stock keeping unit) when there is information to scrap from the vendor's online store.<br />

(1) You must have installed Chromedriver from Selenium.<br />
(2) After that clone the Repo and change following path for both files at dependencies/webscraping:<br />
![image](https://user-images.githubusercontent.com/98284163/205503088-087f4bca-0e9a-4750-96ac-e2ab152db3bf.png)

(3) run main.py and track its progress in the terminal.<br />
(4) When main.py is done, run analyze.py to see how much of the product data has been enriched.<br />

# Report
For more details see docs/report.md
