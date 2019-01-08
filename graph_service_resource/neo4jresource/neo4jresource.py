import json
import os
from flask import Flask, request, jsonify
from neo4japi import Neo4JApi

app = Flask(__name__)

# TODO: later read config in some safe way
app.config['GRAPHDB_URI'] = os.getenv('GRAPHDB_URI', 'bolt://localhost:7687')
app.config['GRAPHDB_USER'] = os.getenv('GRAPHDB_USER', 'neo4j')
app.config['GRAPHDB_PASS'] = os.getenv('GRAPHDB_PASS', '')

api = Neo4JApi.init(uri=app.config['GRAPHDB_URI'], user=app.config['GRAPHDB_USER'], password=app.config['GRAPHDB_PASS'])

# @app.route('/neo4j/nodes/test', methods=['POST'])
# def test():
#     """
#     this is to only test the api
#     :return:
#     """
#     if request.method == 'POST':
#         if request.is_json:
#             data = request.get_json()
#
#             node_type = data['node_type']
#             property_key = data['property_key']
#             property_value = data['property_value']
#
#             status = api.find_single_node(node_type=node_type, property_key=property_key, property_value=property_value)
#             return jsonify({'data': result}), status
#     # else:
#     #     abort(400)

@app.route('/neo4j/nodes/get_all', methods=['GET'])
def get_all_nodes():
    nodes = api.get_all_nodes()
    nodes_json = {'data': nodes}
    return jsonify(nodes_json), 200

@app.route('/neo4j/nodes/get_node')
def get_node():
    if request.method == 'POST' and not request.is_json:
        return jsonify({'status': 400})
    data = request.get_json()
    node_type = data['node_type']
    node_query_attr = data['node_query_attr']
    node_query_attr_val = data['node_query_attr_val']
    status = api.get_node(node_type=node_type, node_query_attr=node_query_attr, node_query_attr_val=node_query_attr_val)
    return jsonify(jsonify({'status': status}))

@app.route('/neo4j/nodes/create_node', methods=['POST'])
def create_node():
    if request.method == 'POST' and not request.is_json:
        return jsonify({'status': 400})
    data = request.get_json()
    node_type = data['node_type']
    id_key = data['id_key']
    node_attributes = data['node_attributes']
    status = api.create_node(node_type=node_type, id_key=id_key, node_attributes=node_attributes)
    return jsonify(jsonify({'status': status}))

@app.route('/neo4j/relationships/create_relationship', methods=['POST'])
def create_relationship():
    if request.method != 'POST' and not request.is_json:
        return jsonify({'status': 400})
    data = request.get_json()
    source_node_type = data['source_node_type']
    target_node_type = data['target_node_type']
    source_node_attributes = data['source_node_attributes']
    target_node_attributes = data['target_node_attributes']
    relationship = data['relationship']
    relationship_attributes = data['relationship_attributes']

    status = api.create_relationship_with_merge(source_node_type=source_node_type,
                                                source_node_attributes=source_node_attributes,
                                                target_node_type=target_node_type,
                                                target_node_attributes=target_node_attributes,
                                                relationship=relationship,
                                                relationship_attributes=relationship_attributes)
    return jsonify({'status': status})

@app.route('/neo4j/nodes/update_node_attributes', methods=['PUT', 'POST'])
def update_node_attrs():
    if request.method not in ['POST', 'PUT'] and not request.is_json:
        return jsonify({'status': 400})
    data = request.get_json()
    node_type = data['node_type']
    node_query_attributes = data['node_query_attributes']
    node_updated_attributes = data['node_updated_attributes']
    status = api.update_node_attr(node_type=node_type, node_query_attributes=node_query_attributes,
                                  node_updated_attributes=node_updated_attributes)
    return jsonify({'status': status})

@app.route('/neo4j/relationships/add_relationship_attr', methods=['POST'])
def add_attr_to_relationship():
    if request.method == 'POST' and not request.is_json:
        return jsonify({'status': 400})

    data = request.get_json()
    first_node_type = data['first_node_type']
    second_node_type = data['second_node_type']
    first_node_name = data['first_node_name']
    second_node_name = data['second_node_name']
    relationship = data['relationship']
    relationship_attributes = data['relationship_attributes']
    status = api.add_relationship_attr(first_node_type=first_node_type, second_node_type=second_node_type,
                                       first_node_name=first_node_name, second_node_name=second_node_name,
                                       relationship=relationship, relationship_attributes=relationship_attributes)
    return jsonify({'status': status})

@app.route('/neo4j/delete_node', methods=['DELETE', 'POST', 'PUT'])
def delete_node():
    if request.method not in ['DELETE', 'POST', 'PUT'] and not request.is_json:
        return jsonify({'status': 400})
    data = request.get_json()
    node_type = data['node_type']
    properties_dict = data['properties_dict']
    status = api.delete_node(node_type=node_type, properties_dict=properties_dict)
    return jsonify({'status': status})

@app.route('/neo4j/delete_relationship', methods=['DELETE', 'POST', 'PUT'])
def delete_relationship_between_nodes():
    if request.method not in ['DELETE', 'POST', 'PUT'] and not request.is_json:
        return jsonify({'status': 400})
    data = request.get_json()
    source_node_type = data['source_node_type']
    source_node_properties_dict = data['source_node_properties_dict']
    target_node_type = data['target_node_type']
    target_node_properties_dict = data['target_node_properties_dict']
    relationship_type = data['relationship_type']
    relationship_attributes = data['relationship_attributes']
    status = api.delete_relationship(source_node_type=source_node_type,
                                     source_node_properties_dict=source_node_properties_dict,
                                     target_node_type=target_node_type,
                                     target_node_properties_dict=target_node_properties_dict,
                                     relationship_type=relationship_type,
                                     relationship_attributes=relationship_attributes)
    return jsonify({'status': status})

@app.route('/neo4j/delete_graph', methods=['GET'])
def delete_all():
    status = api.delete_all()
    return jsonify({'status': status})

@app.errorhandler(404)
def not_found(e):
    return str(e), 404