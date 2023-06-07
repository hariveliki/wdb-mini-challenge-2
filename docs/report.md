# Report

## Motivation and Use Case

For all retailers, the question of data maintenance effort is essential, because more product information in the online store increases the probability of selling a product.<br />
We want to enrich our products without human intervention only with the technology of web scraping.<br />
The code will visit specific online stores and check if our product is available.<br />
If so, we will read the product descriptions and enrich our products with them.<br />

## Architecture and Data Structures
The data is stored locally on your machine.<br />
We use Selenium as the technology for web scraping and work our way up to the description using xpaths.<br />
Selenium opens the web browser for a specific URL and xpaths allows us to query information in an XML document.<br />
Under data/supplier_config/...json we store the vendor specific information, e.g.<br />
```json
{
    "search_url": "https://www.thekooples.com/int/de_CH/search?q=",
    "search_attribute": "supplier_sku",
    "general_xpaths": {
        "title" : "//*[@id=\"maincontent\"]/div[1]/p/span[1]",
        "description" : "//*[@id=\"collapsible-description-1\"]"
    },
    "webpage_xpaths" : {
        "0" : "//*[@id=\"product-search-results\"]/div[2]/div[2]/div/div[1]/div/div/div[2]/div[1]/a",
        "1" : "//*[@id=\"product-search-results\"]/div[2]/div[2]/div/div[2]/div/div/div[2]/div[1]/a"
    },
    "result_ids": {
        "www_description": ""
    }
}
```
We feed Selenium with the url information and the xpaths, which we will take from general_xpaths and webpage_xpaths.<br />
The reason we use two separate xpath variables is that for some online vendor stores we get two items for one vendor sku, e.g.<br />
![image](https://user-images.githubusercontent.com/98284163/204464222-c133c5bd-b852-4590-9028-bc99dfec68fb.png)
Therefore, we need to go further and take the webpage_xpaths[0] and webpage_xpaths[1] to land on the correct page.<br />
<br />
The inital data structure looks like this:<br />
```json
    {
        "akeneo_id": "f6bcd534211911ed94c81aabff81848fairflow",
        "supplier": "9000359",
        "supplier_sku": "FPAN25016K",
        "ean": "3615872058430",
        "created": "2022-08-25T13:15:47+00:00",
        "updated": "2022-09-15T07:18:01+00:00"
    }
```
After the webscraping workflow, the following information was added:<br />
```json
    {
        "akeneo_id": "f6bcd534211911ed94c81aabff81848fairflow",
        "supplier": "9000359",
        "supplier_sku": "FPAN25016K",
        "ean": "3615872058430",
        "created": "2022-08-25T13:15:47+00:00",
        "updated": "2022-09-15T07:18:01+00:00",
        "www_info": {
            "FPAN25016KKAK05": "Referenz:  \nFPAN25016KKAK05\nBedruckte Seidenhose\nBedruckte Seidenhose\n100 % leichte Seide\nSchwarz und khaki\nKlassischer Schnitt\nGrafisches Federmotiv\nElastischer Bund",
            "FPAN25016KWHI22": "Referenz:  \nFPAN25016KWHI22\nFlie\u00dfende Seidenhose\nBedruckte Seidenhose\n100 % leichte Seide\nSchwarz und Cremewei\u00df\nKlassischer Schnitt\nGrafisches Federmotiv\nElastischer Bund"
        }
    }
```
## Tests
All fallbacks for Selenium are caught during the execution of the code, e.g.<br />
![image](https://user-images.githubusercontent.com/98284163/205503520-3a35280d-945c-4488-9905-24b331878de7.png)

If something goes wrong, check the log files under log/enrich_products_xy.json<br />
For all unittests under tests/*_test.py change the directory and run the tests.<br />
You need to change the sys.path.append("...") at the beginning of all tests, e.g.<br />
<img width="711" alt="image" src="https://user-images.githubusercontent.com/98284163/206450300-911fe515-be9f-487e-bd1b-5d4f7e02b362.png">

If you know a better way to run the tests, without appending the sys path, please get in touch with meh, thanks.
