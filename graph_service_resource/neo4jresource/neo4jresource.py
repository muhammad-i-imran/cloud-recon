import json
import os
from flask import Flask, request, jsonify, url_for, Response
from neo4japi import Neo4JApi

from logging_config import Logger

LOGS_FILE_PATH = os.getenv('LOGS_FILE_PATH', '/cloud_reconnoiterer/logs/cloud_reconnoiterer.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')

logger = Logger(log_file_path=LOGS_FILE_PATH, log_level=LOG_LEVEL, logger_name=os.path.basename(__file__)).logger

app = Flask(__name__)

# TODO: later read config in some safe way
app.config['GRAPHDB_HOST'] = os.getenv('GRAPHDB_HOST', 'localhost')
app.config['GRAPHDB_PORT'] = os.getenv('GRAPHDB_PORT', 7687)
app.config['GRAPHDB_USER'] = os.getenv('GRAPHDB_USER', 'neo4j')
app.config['GRAPHDB_PASSWORD'] = os.getenv('GRAPHDB_PASSWORD', '')
app.config['GRAPHDB_SCHEME'] = os.getenv('GRAPHDB_SCHEME', 'bolt')
app.config['GRAPHDB_IS_SECURE'] = os.getenv('GRAPHDB_IS_SECURE', False)

logger.debug("Getting Neo4JApi.")
api = Neo4JApi(host=app.config['GRAPHDB_HOST'], port=app.config['GRAPHDB_PORT'], user=app.config['GRAPHDB_USER'], password=app.config['GRAPHDB_PASSWORD'], scheme=app.config['GRAPHDB_SCHEME'], secure=app.config['GRAPHDB_IS_SECURE'])


@app.route("/neo4j")
def site_map():
    logger.info("Default request at /neo4j. Fetching all available endpoints.")
    links = []
    for rule in app.url_map.iter_rules():
        if rule.rule.startswith("/neo4j"):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return jsonify(links)

@app.route('/neo4j/nodes/get_types', methods=['GET'])
def get_node_types():
    logger.info("Getting all node types.")
    types = api.get_node_types()
    return jsonify(list(types))

@app.route('/neo4j/nodes/get_all', methods=['GET'])
def get_all_nodes():
    logger.info("Getting all nodes from the graph.")
    nodes = api.get_all_nodes()
    nodes_json = {'data': nodes}
    return jsonify(nodes_json), 200

@app.route('/neo4j/nodes/get_node', methods=['POST'])
def get_node():
    logger.info("Getting all nodes from the graph.")
    if request.method == 'POST' and not request.is_json:
        logger.error(
            "Either data in parameter is not in JSON format or request method is not POST. Returning message with status 400.")
        return jsonify({'status': 400})
    data = request.get_json()
    node_type = data['node_type']
    node_properties = data['node_properties'] if 'node_properties' in data.keys() else {}
    nodes = api.get_nodes(node_type, node_properties)
    logger.debug("Executed 'get_nodes' function of the API.")
    return jsonify(nodes)

@app.route('/neo4j/nodes/create_node', methods=['POST'])
def create_node():
    logger.info("Creating node in the graph.")
    if request.method == 'POST' and not request.is_json:
        logger.error(
            "Either data in parameter is not in JSON format or request method is not POST. Returning message with status 400.")
        return jsonify({'status': 400})
    data = request.get_json()
    node_type = data['node_type']
    node_secondary_labels = data['node_secondary_labels']
    id_key = data['id_key']
    node_properties = data['node_properties']
    status = api.create_node_with_merge(node_type=node_type, node_secondary_labels=node_secondary_labels, primary_keys=id_key, node_properties=node_properties)
    logger.debug("Executed 'create_node_with_merge' function of the API.")

    return jsonify({'status': status})

@app.route('/neo4j/relationships/get_types', methods=['GET'])
def get_relationship_types():
    logger.info("Getting all relationship types.")
    types = api.get_relationship_types()
    return jsonify(list(types))

@app.route('/neo4j/relationships/get_all', methods=['GET'])
def get_all_relationships():
    logger.info("Getting all relationships from the graph.")
    relationships = api.get_all_relationships()
    relationships_json = {'data': relationships}
    return jsonify(relationships_json), 200

@app.route('/neo4j/relationships/create_relationship', methods=['POST'])
def create_relationship():
    logger.info("Creating relationship between nodes in the graph.")
    if request.method != 'POST' and not request.is_json:
        logger.error(
            "Either data in parameter is not in JSON format or request method is not POST. Returning message with status 400.")
        return jsonify({'status': 400})
    data = request.get_json()
    source_node_type = data['source_node_type']
    target_node_type = data['target_node_type']
    source_node_properties = data['source_node_properties']
    target_node_properties = data['target_node_properties']
    relationship = data['relationship']
    relationship_properties = data['relationship_properties']

    status = api.create_relationship_with_merge(source_node_type=source_node_type,
                                                source_node_properties=source_node_properties,
                                                target_node_type=target_node_type,
                                                target_node_properties=target_node_properties,
                                                relationship=relationship,
                                                relationship_properties=relationship_properties)
    logger.debug("Executed 'create_relationship_with_merge' function of the API.")

    return jsonify({'status': status})

@app.route('/neo4j/nodes/update_node_properties', methods=['PUT', 'POST'])
def update_node_properties():
    logger.info("Updating node properties in the graph.")
    if request.method not in ['POST', 'PUT'] and not request.is_json:
        logger.error(
            "Either data in parameter is not in JSON format or request method is not POST or PUT. Returning message with status 400.")
        return jsonify({'status': 400})
    data = request.get_json()
    node_type = data['node_type']
    node_query_properties = data['node_query_properties']
    node_updated_properties = data['node_updated_properties']
    status = api.update_node_properties(node_type=node_type, node_query_properties=node_query_properties,
                                  node_updated_properties=node_updated_properties)
    logger.debug("Executed 'update_node_properties' function of the API.")

    return jsonify({'status': status})

@app.route('/neo4j/relationships/add_relationship_properties', methods=['POST'])
def add_properties_to_relationship():
    logger.info("Adding properties to relationship in the graph.")
    if request.method == 'POST' and not request.is_json:
        logger.error(
            "Either data in parameter is not in JSON format or request method is not POST . Returning message with status 400.")
        return jsonify({'status': 400})

    data = request.get_json()
    source_node_type = data['source_node_type']
    target_node_type = data['target_node_type']
    source_node_properties = data['source_node_properties']
    target_node_properties = data['target_node_properties']
    relationship = data['relationship']
    relationship_properties = data['relationship_properties']
    status = api.create_relationship_with_merge(source_node_type=source_node_type,
                                                source_node_properties=source_node_properties,
                                                target_node_type=target_node_type,
                                                target_node_properties=target_node_properties,
                                                relationship=relationship,
                                                relationship_properties=relationship_properties) # merge will update the relationship properties if it already exists, otherwise it will create new relationship
    logger.debug("Executed 'create_relationship_with_merge' function of the API.")

    return jsonify({'status': status})

@app.route('/neo4j/nodes/delete_node', methods=['DELETE', 'POST', 'PUT'])
def delete_node():
    logger.info("Deleting node in the graph.")
    if request.method not in ['DELETE', 'POST', 'PUT'] and not request.is_json:
        logger.error("Either data in parameter is not in JSON format or request method is not DELETE, POST or PUT. Returning message with status 400." )
        return jsonify({'status': 400})
    data = request.get_json()
    node_type = data['node_type']
    properties_dict = data['node_properties']
    status = api.delete_node(node_type=node_type, properties_dict=properties_dict)
    logger.debug("Executed 'delete_node' function of the API.")

    return jsonify({'status': status})

@app.route('/neo4j/delete_relationship', methods=['DELETE', 'POST', 'PUT'])
def delete_relationship():
    logger.info("Deleting relationship in the graph.")
    if request.method not in ['DELETE', 'POST', 'PUT'] and not request.is_json:
        logger.error("Either data in parameter is not in JSON format or request method is not DELETE, POST or PUT. Returning message with status 400.")
        return jsonify({'status': 400})
    data = request.get_json()
    source_node_type = data['source_node_type']
    source_node_properties_dict = data['source_node_properties']
    target_node_type = data['target_node_type']
    target_node_properties_dict = data['target_node_properties']
    relationship_type = data['relationship_type']
    relationship_properties = data['relationship_properties']
    status = api.delete_relationship(source_node_type=source_node_type,
                                     source_node_properties_dict=source_node_properties_dict,
                                     target_node_type=target_node_type,
                                     target_node_properties_dict=target_node_properties_dict,
                                     relationship_type=relationship_type,
                                     relationship_properties=relationship_properties)
    logger.debug("Executed 'delete_relationship' function of the API.")

    return jsonify({'status': status})

@app.route('/neo4j/delete_graph', methods=['GET'])
def delete_all():
    logger.info("Deleting the whole graph.")
    status = api.delete_all()
    logger.debug("Executed 'delete_all' function of the API.")

    return jsonify({'status': status})

@app.errorhandler(404)
def not_found(e):
    return str(e), 404