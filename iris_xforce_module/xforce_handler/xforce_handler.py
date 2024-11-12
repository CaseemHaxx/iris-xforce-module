#!/usr/bin/env python3
#
#
#  IRIS xforce Source Code
#  Copyright (C) 2024 - iris-xforce-module
#  hello@cydea.tech
#  Created by iris-xforce-module - 2024-11-08
#
#  License GNU GPL v3.0

import traceback
from jinja2 import Template

import iris_interface.IrisInterfaceStatus as InterfaceStatus
from app.datamgmt.manage.manage_attribute_db import add_tab_attribute_field
from .IrisXforceInterface import IrisXforceInterface  # Import X-Force API interface

class XforceHandler(object):
    def __init__(self, mod_config, server_config, logger):
        self.mod_config = mod_config
        self.server_config = server_config
        self.xforce = self.get_xforce_instance()
        self.log = logger

    def get_xforce_instance(self):
        """
        Initializes and returns an X-Force API instance.

        :return: X-Force API instance
        """
        url = self.mod_config.get('xforce_url')
        key = self.mod_config.get('xforce_key')
        proxies = {}

        if self.server_config.get('http_proxy'):
            proxies['http'] = self.server_config.get('http_proxy')
        if self.server_config.get('https_proxy'):
            proxies['https'] = self.server_config.get('https_proxy')

        # Instantiate the X-Force API client
        return IrisXforceInterface(url, key, proxies)

    def gen_domain_report_from_template(self, html_template, xforce_report) -> InterfaceStatus:
        """
        Generates an HTML report for a domain, displayed as an attribute in the IOC.

        :param html_template: A string representing the HTML template
        :param xforce_report: The JSON report fetched from X-Force API
        :return: InterfaceStatus
        """
        template = Template(html_template)
        context = xforce_report
        pre_render = {"results": context}

        try:
            rendered = template.render(pre_render)
        except Exception as e:
            self.log.error(f"Template rendering failed: {traceback.format_exc()}")
            return InterfaceStatus.I2Error(f"Template rendering failed: {str(e)}")

        return InterfaceStatus.I2Success(data=rendered)

    def handle_domain(self, ioc):
        """
        Handles an IOC of type domain and adds X-Force insights.

        :param ioc: IOC instance
        :return: InterfaceStatus
        """
        self.log.info(f'Getting domain report for {ioc.ioc_value}')
        try:
            # Fetch the domain report from X-Force
            report = self.xforce.get_domain_reputation(ioc.ioc_value)
        except Exception as e:
            self.log.error(f"Failed to fetch domain report: {traceback.format_exc()}")
            return InterfaceStatus.I2Error(f"Failed to fetch domain report: {str(e)}")

        if self.mod_config.get('xforce_report_as_attribute'):
            self.log.info('Adding new attribute X-Force Domain Report to IOC')

            # Generate the domain report
            template = self.mod_config.get('xforce_domain_report_template')
            status = self.gen_domain_report_from_template(template, report)

            if not status.is_success():
                return status

            rendered_report = status.get_data()
            try:
                add_tab_attribute_field(ioc, tab_name='X-Force Report', field_name="HTML report", field_type="html", field_value=rendered_report)
            except Exception as e:
                self.log.error(f"Failed to add attribute field: {traceback.format_exc()}")
                return InterfaceStatus.I2Error(f"Failed to add attribute field: {str(e)}")
        else:
            self.log.info('Skipped adding attribute report. Option disabled')

        return InterfaceStatus.I2Success()
