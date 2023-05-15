"""Add test run and device properties to the Junit xml file generated by Spytest."""
import datetime
import os.path
import pytest

import xml.etree.ElementTree as ET

pytestmark = [
    pytest.mark.topology('util')
]


def build_properties(properties_dict):
    """Build global properties from passed key, value pairs."""
    properties = ET.Element("properties")
    for name, value in list(properties_dict.items()):
        properties.append(ET.Element("property", name=name, value=value))
    return properties


def test_add_property_spytest_junit_xml(duthost, request, tbinfo):
    """Test to add device and testbed related properties to the junit xml file."""
    spytest_xmlfile = request.config.getoption("spytest_xmlpath")
    spytest_updated_xmlfile = request.config.getoption("spytest_updated_xmlpath")
    if spytest_xmlfile is None:
        pytest.fail("Please specify the junit xml file generated by Spytest.")
    if spytest_updated_xmlfile is None:
        prefix, ext = os.path.splitext(spytest_xmlfile)
        spytest_updated_xmlfile = prefix + "_update" + ext

    tree = ET.parse(spytest_xmlfile)
    root = tree.getroot()

    properties = {}
    properties["topology"] = tbinfo["topo"]["name"]
    properties["testbed"] = tbinfo["conf-name"]
    properties["timestamp"] = str(datetime.datetime.utcnow())
    properties["host"] = duthost.hostname
    properties["asic"] = duthost.facts["asic_type"]
    properties["platform"] = duthost.facts["platform"]
    properties["hwsku"] = duthost.facts["hwsku"]
    properties["os_version"] = duthost.os_version

    root.insert(0, build_properties(properties))

    with open(spytest_updated_xmlfile, "w") as output:
        output.write('<?xml version="1.0" encoding="utf-8"?>')
        output.write(ET.tostring(root))
