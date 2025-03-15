import xml.etree.ElementTree as ET
import json

def json_to_xml(json_data):
    """JSON转XML格式转换"""
    root = ET.Element("DefectReport")
    for key, value in json_data.items():
        child = ET.SubElement(root, key)
        child.text = str(value)
    return ET.tostring(root, encoding="utf-8")