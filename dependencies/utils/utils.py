from datetime import datetime 
import json, os


def load_json_file(path):
    with open(path) as f:
        return json.load(f)


def write_json_file(path, content) -> None:
    with open(path, "w") as write_obj:
        json.dump(content, write_obj)


def get_config(supplier) -> dict:
    for path, dirs, files in os.walk("data/supplier_config"):
        for file in files:
            if file.startswith(supplier):
                return load_json_file(os.path.join(path, file))


def get_supplier_name(supplier_nr: str):
    with open("data/constants/supplier_infos.py") as f:
        supplier_infos = f.read()
        supplier_infos = eval(supplier_infos)
    supplier_info = supplier_infos[supplier_nr]
    return supplier_info["name"]


