import re

from graphelementsdispatcher.relationship_manager import *
import node_data_assembler

"""This file contains functionality specific to OpenStack"""

def begin_node_create(cloud_config_info, prefix_string=""):
    nodes = list(cloud_config_info.keys())
    container_key_name = "".join([prefix_string, "CONTAINERS"])
    nodes.remove(container_key_name)
    nodes.append(container_key_name) # list is ordered in python. so remove key for 'containers' if it is somewhere else and append it at the end, so we can be sured that the container creation code is executed after servers creation code (because containers depend on servers)

    for node_type in nodes:
        try:
            function_name = "".join(["create_", node_type])
            function_to_call = getattr(node_data_assembler, function_name.lower())
            try:
                node_type_with_prefix = prefix_string + node_type
                function_to_call(node_type=node_type_with_prefix, label=cloud_config_info[node_type]['name_attr'], id_key=cloud_config_info[node_type]['id_key']) #todo: pass parameters as either dict or args and kwargs, because create_container  function accepts different parameters
            except AttributeError as e:
                print("The function " + function_to_call + " doesn't exist. Please check this in the future releases. Exception message: " + str(e))
        except Exception as ex:
            print("".join(["Exception occured: ", str(ex)]))

def begin_relationship_create(cloud_config_info):
    for key in cloud_config_info:
        source_node_type = key
        relationship_infos = cloud_config_info[key]["RELATIONSHIPS"]
        for relationship_info in relationship_infos:
            source_property_name = relationship_info["source_property_name"]
            target_node_type = relationship_info["target_node_type"]
            target_property_name = relationship_info["target_property_name"]
            relationship_name = relationship_info["relationship_name"]
            relationship_properties = relationship_info["relationship_properties"]
            is_source_attr_name_regex = relationship_info["is_source_attr_name_regex"]

            ##todo: fetch data directly for this key from openstack
            data = list()

            for d in data:
                target_node_properties = {target_property_name: d[target_property_name]}
                if is_source_attr_name_regex:
                    source_property_names = list(filter(re.compile(source_property_name).match,
                                                        d.node_attributes.__dict__.keys()))

                    for property_name in source_property_names:
                        source_node_properties = {property_name: d[property_name]}

                        data = {}
                        data["source_node_type"] = source_node_type
                        data["source_node_properties"] = source_node_properties
                        data["target_node_type"] = target_node_type
                        data["target_node_properties"] = target_node_properties
                        data["relationship"] = relationship_name
                        data["relationship_properties"] = relationship_properties

                        RelationshipManager.create_relationship(data)
                else:
                    source_node_properties = {source_property_name: d[source_property_name]}
                    data = {}
                    data["source_node_type"] = source_node_type
                    data["source_node_properties"] = source_node_properties
                    data["target_node_type"] = target_node_type
                    data["target_node_properties"] = target_node_properties
                    data["relationship"] = relationship_name
                    data["relationship_properties"] = relationship_properties

                    RelationshipManager.create_relationship(data)
