#!/usr/bin/env python3
#
#
#  IRIS xforce Source Code
#  Copyright (C) 2024 - iris-xforce-module
#  hello@cydea.tech
#  Created by iris-xforce-module - 2024-11-08
#
#  License GNU GPL v3.0

module_name = "IrisXforce"
module_description = "A module that integrates IBM X-Force Exchange for retrieving domain and IP threat intelligence reports in the IrisDFIR platform."
interface_version = 1.1
module_version = 1.0

pipeline_support = False
pipeline_info = {}

module_configuration = [
    {
        "param_name": "xforce_url",
        "param_human_name": "X-Force API URL",
        "param_description": "The base URL for IBM X-Force API, e.g., 'https://api.xforce.ibmcloud.com'",
        "default": None,
        "mandatory": True,
        "type": "string"
    },
    {
        "param_name": "xforce_key",
        "param_human_name": "X-Force API Key",
        "param_description": "The API key for accessing IBM X-Force Exchange.",
        "default": None,
        "mandatory": True,
        "type": "sensitive_string"
    },
    {
        "param_name": "xforce_manual_hook_enabled",
        "param_human_name": "Manual Triggers on IOCs",
        "param_description": "Set to True to allow manually triggering the module via the UI.",
        "default": True,
        "mandatory": True,
        "type": "bool",
        "section": "Triggers"
    },
    {
        "param_name": "xforce_on_create_hook_enabled",
        "param_human_name": "Automatic Trigger on IOC Creation",
        "param_description": "Set to True to automatically add X-Force insight each time an IOC is created.",
        "default": False,
        "mandatory": True,
        "type": "bool",
        "section": "Triggers"
    },
    {
        "param_name": "xforce_on_update_hook_enabled",
        "param_human_name": "Automatic Trigger on IOC Update",
        "param_description": "Set to True to automatically add X-Force insight each time an IOC is updated.",
        "default": False,
        "mandatory": True,
        "type": "bool",
        "section": "Triggers"
    },
    {
        "param_name": "xforce_report_as_attribute",
        "param_human_name": "Add X-Force Report as New IOC Attribute",
        "param_description": "Creates a new attribute on the IOC based on the X-Force report using the template specified below.",
        "default": True,
        "mandatory": True,
        "type": "bool",
        "section": "Insights"
    },
    {
        "param_name": "xforce_domain_report_template",
        "param_human_name": "Domain Report Template",
        "param_description": "HTML template for generating the domain report as a custom attribute on the IOC.",
        "default": (
            "<div class=\"row\">\n"
            "    <div class=\"col-12\">\n"
            "        <div class=\"accordion\">\n"
            "            <h3>X-Force Raw Results</h3>\n"
            "            <div class=\"card\">\n"
            "                <div class=\"card-header collapsed\" id=\"drop_r_xforce\" data-toggle=\"collapse\" "
            "data-target=\"#drop_raw_xforce\" aria-expanded=\"false\" aria-controls=\"drop_raw_xforce\" role=\"button\">\n"
            "                    <div class=\"span-icon\">\n"
            "                        <div class=\"flaticon-file\"></div>\n"
            "                    </div>\n"
            "                    <div class=\"span-title\">\n"
            "                        X-Force Raw Results\n"
            "                    </div>\n"
            "                    <div class=\"span-mode\"></div>\n"
            "                </div>\n"
            "                <div id=\"drop_raw_xforce\" class=\"collapse\" aria-labelledby=\"drop_r_xforce\" style=\"\">\n"
            "                    <div class=\"card-body\">\n"
            "                        <div id='xforce_raw_ace'>{{ results|tojson(indent=4) }}</div>\n"
            "                    </div>\n"
            "                </div>\n"
            "            </div>\n"
            "        </div>\n"
            "    </div>\n"
            "</div>\n"
            "<script>\n"
            "var xforce_in_raw = ace.edit(\"xforce_raw_ace\", { autoScrollEditorIntoView: true, minLines: 30 });\n"
            "xforce_in_raw.setReadOnly(true);\n"
            "xforce_in_raw.setTheme(\"ace/theme/tomorrow\");\n"
            "xforce_in_raw.session.setMode(\"ace/mode/json\");\n"
            "xforce_in_raw.renderer.setShowGutter(true);\n"
            "xforce_in_raw.setOption(\"showLineNumbers\", true);\n"
            "xforce_in_raw.setOption(\"showPrintMargin\", false);\n"
            "xforce_in_raw.setOption(\"displayIndentGuides\", true);\n"
            "xforce_in_raw.setOption(\"maxLines\", \"Infinity\");\n"
            "xforce_in_raw.session.setUseWrapMode(true);\n"
            "xforce_in_raw.setOption(\"indentedSoftWrap\", true);\n"
            "xforce_in_raw.renderer.setScrollMargin(8, 5);\n"
            "</script>"
        ),
        "mandatory": False,
        "type": "textfield_html",
        "section": "Templates"
    }
]
