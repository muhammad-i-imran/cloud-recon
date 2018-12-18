from node_manager import NodeManager

class NotificationEventHandlers(object):

    @staticmethod
    def delete_server(cls, node_type, payload):
        attribute_name=openstack_info[node_type]['id_key']
        attribute_value=payload['instance_id']
        NodeManager.delete_node(node_type, attribute_name, attribute_value)

    @staticmethod
    def update_server(node_type, payload):
        attribute_name = openstack_info[node_type]['id_key']
        attribute_value = payload['instance_id']
        NodeManager.update_node(node_type, attribute_name, attribute_value)

    @staticmethod
    def delete_network(node_type, payload):
        raise NotImplementedError("not implemented yet")


    @staticmethod
    def update_network(node_type, payload):
        raise NotImplementedError("not implemented yet")

    @staticmethod
    def create_container(cls, node_type, payload):
        raise NotImplementedError("not implemented yet")

    @staticmethod
    def delete_container(cls, node_type, payload):
        raise NotImplementedError("not implemented yet")

    @staticmethod
    def update_container(cls, node_type, payload):
        raise NotImplementedError("not implemented yet")