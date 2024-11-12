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
from pathlib import Path
import iris_interface.IrisInterfaceStatus as InterfaceStatus
from iris_interface.IrisModuleInterface import IrisPipelineTypes, IrisModuleInterface, IrisModuleTypes
import iris_xforce_module.IrisXforceConfig as interface_conf
from iris_xforce_module.xforce_handler.xforce_handler import XforceHandler


class IrisXforceInterface(IrisModuleInterface):
    """
    Provides the interface between Iris and the xforceHandler module.
    This interface manages IOC hooks for various actions (creation, update, manual triggers).
    """

    name = "IrisXforceInterface"
    _module_name = interface_conf.module_name
    _module_description = interface_conf.module_description
    _interface_version = interface_conf.interface_version
    _module_version = interface_conf.module_version
    _pipeline_support = interface_conf.pipeline_support
    _pipeline_info = interface_conf.pipeline_info
    _module_configuration = interface_conf.module_configuration
    _module_type = IrisModuleTypes.module_processor

    def register_hooks(self, module_id: int):
        """
        Registers all the hooks based on module configuration.

        :param module_id: Module ID provided by IRIS
        :return: Nothing
        """
        self.module_id = module_id
        module_conf = self.module_dict_conf

        hooks = [
            ("xforce_on_create_hook_enabled", 'on_postload_ioc_create'),
            ("xforce_on_update_hook_enabled", 'on_postload_ioc_update'),
            ("xforce_manual_hook_enabled", 'on_manual_trigger_ioc')
        ]

        for conf_key, hook_name in hooks:
            if module_conf.get(conf_key):
                try:
                    status = self.register_to_hook(module_id, iris_hook_name=hook_name)
                    if status.is_failure():
                        self.log.error(f"Failed to register {hook_name} hook: {status.get_message()}")
                        self.log.error(status.get_data())
                    else:
                        self.log.info(f"Successfully registered {hook_name} hook")
                except Exception as e:
                    self.log.error(f"Error registering {hook_name} hook: {str(e)}")
            else:
                self.deregister_from_hook(module_id=self.module_id, iris_hook_name=hook_name)
                self.log.info(f"{hook_name} hook not enabled, deregistered if previously registered.")

    def hooks_handler(self, hook_name: str, hook_ui_name: str, data: any):
        """
        Handles actions based on the triggered hook name.

        :param hook_name: Name of the triggered hook
        :param hook_ui_name: UI name for the triggered hook
        :param data: Data associated with the trigger.
        :return: Interface status object with success or error details.
        """
        self.log.info(f'Received {hook_name} hook trigger')
        
        try:
            if hook_name in ['on_postload_ioc_create', 'on_postload_ioc_update', 'on_manual_trigger_ioc']:
                status = self._handle_ioc(data=data)
            else:
                self.log.critical(f'Received unsupported hook {hook_name}')
                return InterfaceStatus.I2Error(data=data, logs=list(self.message_queue))

            if status.is_failure():
                self.log.error(f"Error processing {hook_name} hook")
                return InterfaceStatus.I2Error(data=data, logs=list(self.message_queue))

            self.log.info(f"Successfully processed {hook_name} hook")
            return InterfaceStatus.I2Success(data=data, logs=list(self.message_queue))

        except Exception as e:
            self.log.error(f"Exception in hooks_handler for {hook_name}: {traceback.format_exc()}")
            return InterfaceStatus.I2Error(data=data, logs=list(self.message_queue))

    def _handle_ioc(self, data) -> InterfaceStatus.IIStatus:
        """
        Processes the IOC data received from the hook, using the xforce_handler to handle supported types.

        :param data: List of IOC objects received from the trigger.
        :return: Merged Interface status from all processed IOCs.
        """
        xforce_handler = XforceHandler(mod_config=self.module_dict_conf,
                                       server_config=self.server_dict_conf,
                                       logger=self.log)
        in_status = InterfaceStatus.IIStatus(code=InterfaceStatus.I2CodeNoError)

        for element in data:
            try:
                if 'domain' in element.ioc_type.type_name:
                    status = xforce_handler.handle_domain(ioc=element)
                    in_status = InterfaceStatus.merge_status(in_status, status)
                else:
                    self.log.error(f'IOC type {element.ioc_type.type_name} not supported by xforce module. Skipping.')

            except Exception as e:
                self.log.error(f"Error handling IOC {element.ioc_type.type_name}: {traceback.format_exc()}")

        return in_status(data=data)
