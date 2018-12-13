import json
import os
from flask import Flask, request, session, redirect, url_for, render_template, flash, jsonify, Response
from neo4japi import Neo4JApi

app = Flask(__name__)

# TODO: later read config in some safe way
app.config['GRAPHDB_URI'] = os.getenv('GRAPHDB_URI', 'bolt://localhost:7687')
app.config['GRAPHDB_USER'] = os.getenv('GRAPHDB_USER', 'neo4j')
app.config['GRAPHDB_PASS'] = os.getenv('GRAPHDB_PASS', '')

api = Neo4JApi.init_with_basic_auth(uri=app.config['GRAPHDB_URI'], user=app.config['GRAPHDB_USER'], password=app.config['GRAPHDB_PASS'])

@app.route('/neo4j/nodes/get_all')
def get_all_nodes():
    node_type = request.args.get('node_type', default="HuaweiOpenstack", type=str)
    nodes = api.get_nodes(node_type)
    nodes_json = {'data': nodes}
    return jsonify(nodes_json), 200

@app.route('/neo4j/nodes/create_node', methods=['POST'])
def add_single_node():
    if request.method == 'POST':
        if request.is_json:
            jsonStr = request.get_json()
            data = json.loads(jsonStr)
            node_type = data['node_type']
            id_key = data['id_key']
            node_attributes = data['node_attributes']
            api.create_node(node_type=node_type, id_key=id_key, node_attributes=node_attributes)
            return jsonify({'Message': "Node has been created"})

@app.route('/neo4j/relationships/create_relationship', methods=['POST'])
def add_relationship():
    if request.method == 'POST':
        if request.is_json:
            jsonStr = request.get_json()
            data = json.loads(jsonStr)

            source_node_type = data['source_node_type']
            target_node_type = data['target_node_type']
            source_node_attr_value = data['source_node_attr_value']
            source_node_attr_name = data['source_node_attr_name']
            target_node_attr_name = data['target_node_attr_name']
            relationship = data['relationship']
            relationship_attributes = data['relationship_attributes']

            api.create_relationship(source_node_type=source_node_type, target_node_type=target_node_type,
                                    source_node_attr_value=source_node_attr_value,
                                    target_node_attr_value=source_node_attr_value,
                                    source_node_attr_name=source_node_attr_name,
                                    target_node_attr_name=target_node_attr_name, relationship=relationship,
                                    relationship_attributes=relationship_attributes,
                                    )
            return jsonify({'Message': "Relationship has been created"})

@app.route('/neo4j/nodes/add_node_attr', methods=['POST'])
def add_attr_to_node():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            node_type = data['node_type']
            node_name = data['node_name']
            node_attributes = data['node_attributes']
            api.add_node_attr(node_type=node_type, node_name=node_name, node_attributes=node_attributes)
            return jsonify({'Message': "Attributes have been added to the node"})

@app.route('/neo4j/relationships/add_relationship_attr', methods=['POST'])
def add_attr_to_relationship():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            first_node_type = data['first_node_type']
            second_node_type = data['second_node_type']
            first_node_name = data['first_node_name']
            second_node_name = data['second_node_name']
            relationship = data['relationship']
            relationship_attributes = data['relationship_attributes']

            api.add_relationship_attr(first_node_type=first_node_type, second_node_type=second_node_type,
                                      first_node_name=first_node_name, second_node_name=second_node_name,
                                      relationship=relationship, relationship_attributes=relationship_attributes)
            return jsonify({'Message': "Attributes have been added to the relationship"})

@app.route('/neo4j/delete_node', methods=['POST'])
def delete_node():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            node_type = data['node_type']
            query_attribute = data['query_attribute']
            query_attribute_value = data['query_attribute_value']
            api.delete_node_only(node_type, query_attribute, query_attribute_value)
            return jsonify({'Message': "The node has been deleted"})


@app.route('/neo4j/delete_relationship', methods=['GET'])
def delete_relationship_between_nodes():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            first_node_type = data['first_node_type']
            first_node_query_attr = data['first_node_query_attr']
            first_node_query_value = data['first_node_query_value']

            second_node_type = data['second_node_type']
            second_node_query_attr = data['second_node_query_attr']
            second_node_query_value = data['second_node_query_value']

            relationship = data['relationship']

            api.delete_relationship_between_nodes(first_node_type, first_node_query_attr, first_node_query_value,
                                          second_node_type, second_node_query_attr, second_node_query_value,
                                          relationship)
            return jsonify({'Message': "The relationship between nodes has been deleted"})

@app.route('/neo4j/delete_graph', methods=['GET'])
def delete_all():
    api.delete_all()
    return jsonify({'Message': "The graph has been deleted"})

@app.errorhandler(404)
def not_found(e):
    return str(e), 404