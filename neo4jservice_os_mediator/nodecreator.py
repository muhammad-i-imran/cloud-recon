from flatten_json import flatten
from graphserviceschema.serviceschema import *
from mediator.caller import *
from openstackqueryapi.queryos import CustomVirtualMachineQuerier
import json
import os


class NodeCreator(object):
    NEO4J_SERVICE_URL = ""
    NEO4J_SERVICE_NODE_RELATIVE_PATH = "/nodes/create_node"

    @classmethod
    def createNode(self, id_key, node_type, node_attrributtes_dict):
        node_attributes = NodeAttributes(node_attrributtes_dict)
        node = Node(id_key=id_key, node_type=node_type, node_attributes=node_attributes)
        data = node.toJSON()
        callServicePost(url=NodeCreator.NEO4J_SERVICE_URL + NodeCreator.NEO4J_SERVICE_NODE_RELATIVE_PATH, data=data.replace("\n", ""))
        return node

    @classmethod
    def prepareNodesData(self, data_list, node_type, label_key="name", id_key="id"):
        nodes = []
        for i in data_list:
            info = i if type(i) is dict else i.__dict__
            # label = info.pop(label_key, None)

            flatten_info_dict = flatten(info, separator="___")
            node = NodeCreator.createNode(id_key, node_type, flatten_info_dict)
            nodes.append(node)
        return nodes

    @classmethod
    def create_containers_nodes(self, node_type, openstack_info, private_keys_folder, nova_querier, vm_username):
        if not openstack_info["SERVERS"]["data"]:
            return
        nodes = []
        command = "sudo docker ps --format \"{{json .}}\""
        for s in openstack_info["SERVERS"]["data"]:
            server_id = s.node_attributes.__dict__["id"]
            server = nova_querier.getServer(server_id) #TODO: MOVE IT TO main.py

            vmSshQuerier = CustomVirtualMachineQuerier()
            ip = server.addresses[list(server.addresses.keys())[0]][1]["addr"]
            private_key_path = os.path.join(private_keys_folder, server.user_id)
            if not os.path.exists(private_key_path):
                continue
            vmSshQuerier.connect(ip=ip, username=vm_username, private_key_file_path=private_key_path)

            stdin, stdout, stderr = vmSshQuerier.executeCommandOnVM(command)
            containers_string_info = stdout.readlines()
            containers_list = []
            for c in containers_string_info:
                container_info_dict = {}
                container_info = json.loads(c)
                container_info_dict["id"] = container_info["ID"]
                container_info_dict["container_name"] = container_info["Names"]
                container_info_dict["name"] = container_info["Image"]
                container_info_dict["ports"] = container_info["Ports"]
                container_info_dict["networks"] = container_info["Networks"]
                container_info_dict["mounts"] = container_info["Mounts"]
                container_info_dict["server_name"] = s.name
                container_info_dict["server_id"] = server_id
                containers_list.append(container_info_dict)

            nodes = NodeCreator.prepareNodesData(data_list=containers_list, node_type=node_type, label_key="name",
                                         id_keys=["id"])
            try:
                vmSshQuerier.closeConnection()
            except:
                pass

            return nodes