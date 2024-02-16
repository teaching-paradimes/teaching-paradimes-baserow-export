import json
import shutil
import glob
import lxml.etree as ET
import os
from acdh_tei_pyutils.tei import TeiReader
from config import JSON_FOLDER, TEI_FOLDER
from tqdm import tqdm


files = sorted(glob.glob(f"{JSON_FOLDER}/*.json"))
shutil.rmtree(TEI_FOLDER, ignore_errors=True)
os.makedirs(TEI_FOLDER, exist_ok=True)


for x in tqdm(files, total=len(files)):
    _, tail = os.path.split(x)
    tei_file_name = tail.replace(".json", ".xml")
    tei_save_path = os.path.join(TEI_FOLDER, tei_file_name)
    with open(x, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    table_node = ET.Element("{http://www.tei-c.org/ns/1.0}table")
    first_item = list(data[list(data.keys())[0]].keys())
    table_node.attrib["rows"] = f"{len(data)}"
    table_node.attrib["cols"] = f"{len(first_item)}"
    th_row = ET.Element("{http://www.tei-c.org/ns/1.0}row")
    th_row.attrib["role"] = "label"
    table_node.append(th_row)
    for th in first_item:
        th_cell = ET.Element("{http://www.tei-c.org/ns/1.0}cell")
        th_cell.attrib["role"] = "label"
        th_cell.text = th
        th_row.append(th_cell)
    counter = 0
    for _, tr in data.items():
        counter += 1
        if counter > 5:
            break
        tr_node = ET.Element("{http://www.tei-c.org/ns/1.0}row")
        tr_node.attrib["role"] = "data"
        table_node.append(tr_node)
        for key, value in tr.items():
            td_cell = ET.Element("{http://www.tei-c.org/ns/1.0}cell")
            td_cell.attrib["role"] = "data"
            if isinstance(value, (str, int, float)):
                td_cell.text = f"{value}"
            if isinstance(value, list):
                td_cell = ET.Element("{http://www.tei-c.org/ns/1.0}cell")
                for item in value:
                    rs = ET.Element("{http://www.tei-c.org/ns/1.0}rs")
                    rs.attrib["ref"] = f"#{key}__{item['id']}"
                    rs.text = f"{item['value']}"
                    td_cell.append(rs)
            tr_node.append(td_cell)
    tei_table_str = ET.tostring(
        table_node, encoding="utf-8", pretty_print=True, xml_declaration=False
    ).decode("utf-8")
    doc = TeiReader(tei_table_str)
    doc.tree_to_file(tei_save_path)
