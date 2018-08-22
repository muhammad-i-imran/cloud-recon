import json
import os
from flask import Flask, request, session, redirect, url_for, render_template, flash, jsonify, Response
from neo4japi import Neo4JApi

app = Flask(__name__)

#TODO: later read config in some safe way
app.config['GRAPHDB_URI'] = 'bolt://localhost:7687'
app.config['GRAPHDB_USER'] = 'neo4j'
app.config['GRAPHDB_PASS'] = os.getenv('GRAPHDB_PASS', '')

api = Neo4JApi(app.config['GRAPHDB_URI'], app.config['GRAPHDB_USER'], app.config['GRAPHDB_PASS'])

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
            label = data['label']
            node_attributes = data['node_attributes']
            api.create_node(node_type=node_type, label=label, node_attributes=node_attributes)
            node = {
                'label' : label,
                'attributes': node_attributes
            }
            if not label:
                print('Name of the node is missing.')
            return jsonify({'data': node}), 201

@app.route('/neo4j/relationships/create_relationship', methods=['POST'])
def add_relationship():
    if request.method == 'POST':
        if request.is_json:
            jsonStr = request.get_json()
            data = json.loads(jsonStr)
            first_node_type = data['first_node_type']
            second_node_type = data['second_node_type']
            first_node = data['first_node']
            second_node = data['second_node']
            first_node_attr = data['first_node_attr']
            second_node_attr = data['second_node_attr']

            relationship = data['relationship']
            relationship_attributes = data['relationship_attributes']

            api.create_relationship(first_node_type=first_node_type, second_node_type=second_node_type , first_node=first_node, second_node=second_node, first_node_attr=first_node_attr, second_node_attr=second_node_attr, relationship=relationship, relationship_attributes=relationship_attributes)
            node_relationship = {
                'first_node' : first_node,
                'second_node': second_node,
                'relationship': relationship,
                'relationship_attributes': relationship_attributes
            }
            return jsonify({'data': node_relationship}), 201

@app.route('/neo4j/nodes/add_node_attr', methods=['POST'])
def add_attr_to_node():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            node_type = data['node_type']
            node_name = data['node_name']

            node_attributes = data['node_attributes']
            api.add_node_attr(node_type=node_type, node_name=node_name, node_attributes=node_attributes)
            updated_node = {
                'node_type' : node_type,
                'node_name': node_name,
                'node_attributes': node_attributes
            }
            return jsonify({'data': updated_node}), 201

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

            api.add_relationship_attr(first_node_type=first_node_type, second_node_type=second_node_type, first_node_name=first_node_name, second_node_name=second_node_name, relationship=relationship, relationship_attributes=relationship_attributes)
            updated_relationship = {
                "first_node_name" : first_node_name,
                "second_node_name": second_node_name,
                "relationship" : relationship,
                "relationship_attributes": relationship_attributes
            }
            return jsonify({'data': updated_relationship}), 201

@app.route('/neo4j/delete_graph', methods=['GET'])
def delete_all():
    api.delete_all()
    return jsonify({'data': ''}), 200

@app.errorhandler(404)
def not_found(e):
    return str(e), 404