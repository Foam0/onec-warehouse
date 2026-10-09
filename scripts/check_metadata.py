#!/usr/bin/env python3
"""Check source completeness and metadata references; not a 1C compiler."""
from pathlib import Path
from uuid import UUID
from xml.etree import ElementTree as ET
import re

ROOT = Path(__file__).resolve().parents[1] / "src"
MD = "{http://v8.1c.ru/8.3/MDClasses}"
V8 = "{http://v8.1c.ru/8.1/data/core}"
XR = "{http://v8.1c.ru/8.3/xcf/readable}"
FOLDERS = {"Language": "Languages", "Subsystem": "Subsystems", "Catalog": "Catalogs",
           "Document": "Documents", "CommonModule": "CommonModules", "Role": "Roles",
           "AccumulationRegister": "AccumulationRegisters", "InformationRegister": "InformationRegisters",
           "Enum": "Enums", "Report": "Reports", "DataProcessor": "DataProcessors"}
config = ET.parse(ROOT / "Configuration.xml").getroot().find(MD + "Configuration")
entries = {(e.tag.removeprefix(MD), e.text) for e in config.find(MD + "ChildObjects")}
assert len(entries) == len(config.find(MD + "ChildObjects")), "Duplicate root entries"
for kind, name in entries:
    p = ROOT / FOLDERS[kind] / (name + ".xml")
    assert p.is_file(), f"Missing metadata: {kind}.{name}"
    obj = ET.parse(p).getroot().find(MD + kind)
    assert obj is not None, f"Wrong kind: {p}"
    assert obj.find(MD + "Properties/" + MD + "Name").text == name, f"Wrong name: {p}"
    if kind == "CommonModule":
        assert (p.with_suffix("") / "Ext/Module.bsl").is_file(), f"Missing module: {name}"
    if kind == "Document":
        assert (p.with_suffix("") / "Ext/ObjectModule.bsl").is_file(), f"Missing object module: {name}"

uuids = set()
xml_files = list(ROOT.rglob("*.xml"))
for p in xml_files:
    root = ET.parse(p).getroot()
    for node in root.iter():
        value = node.get("uuid")
        if value:
            UUID(value)
            assert value not in uuids, f"Duplicate UUID {value}: {p}"
            uuids.add(value)
        text = node.text or ""
        if node.tag == V8 + "Type" and text.startswith("cfg:"):
            prefix, name = text[4:].split(".", 1)
            kind = prefix.removesuffix("Ref").removesuffix("Object")
            assert (kind, name) in entries, f"Unknown type {text}: {p}"
        if node.tag == XR + "Item" and "." in text:
            parts = text.split(".")
            assert tuple(parts[:2]) in entries, f"Unknown metadata reference {text}: {p}"
        if node.tag in (MD + "DefaultForm", MD + "MainDataCompositionSchema") and text:
            kind, name, child_kind, child_name = text.split(".")
            folder = {"Form": "Forms", "Template": "Templates"}[child_kind]
            target = ROOT / FOLDERS[kind] / name / folder / (child_name + ".xml")
            assert target.is_file(), f"Missing child {text}"
        if node.tag == MD + "ChildObjects":
            for child in node:
                if child.tag in (MD + "Form", MD + "Template"):
                    folder = "Forms" if child.tag == MD + "Form" else "Templates"
                    assert (p.with_suffix("") / folder / (child.text + ".xml")).is_file()
    if root.tag == "{http://v8.1c.ru/8.3/xcf/logform}Form":
        ns = "{http://v8.1c.ru/8.3/xcf/logform}"
        form_module = p.parent / "Form/Module.bsl"
        assert form_module.is_file(), f"Missing form module: {p}"
        code = form_module.read_text(encoding="utf-8-sig")
        for command in root.findall(ns + "Commands/" + ns + "Command"):
            action = command.find(ns + "Action").text
            assert re.search(r"Процедура\s+" + re.escape(action) + r"\s*\(", code), f"Missing command handler: {action}"
print(f"OK: {len(entries)} root objects, {len(xml_files)} XML files, {len(uuids)} unique metadata UUIDs")
print("This checks references and source completeness. Import/compilation requires 1C:Enterprise.")
