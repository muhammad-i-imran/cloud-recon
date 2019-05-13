# Adding New Configurations


### Adding Configurations to `openstack_configuration.json` File:

The `openstack_configuration.json` file contains configurations used to create nodes and relationships among the nodes.

```"<component type to create>": {
      "name_attr": "<name property for the component>",
      "id_key": "<unique identifier property for the component>",
      "node_secondary_labels": [
        "COMPONENT"
      ],
      "RELATIONSHIPS": [
        {
          "source_property_name": "<source node property (in the database) used to identify the node(s)>",
          "is_source_attr_name_regex": <true if the source_property_name is in the form of regular expression otherwise false>,
          "target_node_type": "<target node type to create relationship with>",
          "target_property_name": "<target node property (in the database) used to identify the node(s)>",
          "relationship": "<relationship label>",
          "relationship_properties": {
            "<key>":"<value>",
            ...
          }
        }
        ...
      ]
    }
```



### Adding Configurations to `event_component_mapping.json` File:

The `event_component_mapping.json` file contains information used in handling events that are triggered while the application is running. If a new entry needs to be made in `event_component_mapping.json`, then it could be done in the following format:
```
"<event-name>": {
    "publisher_id": "<identifier of the event publisher. use .* for events from any publisher>",
    "component": "<source component type. e.g. SERVERS>",
    "operation": "<C for create,  U for update or D for delete event>",
    "graph_element": <["N" if the event affects the node only, "R" if the event affects the relationship only, or "N" and "R" if it affects both]>,
    "relationships": [
    	{
          "source_property_name_in_db": "<source node's unque identifier property in the database>",
          "is_source_attr_name_regex": <true if source_property_name_in_db is a regular expression, otherwise false>,
          "target_node_type": ""<target component type. e.g. HYPERVISORS>"",
          "target_node_type_id_in_payload": [<target node's unique identifier(s) in the payload>],
          "target_property_name": "<target node's identifier property name in the database>",
          "relationship": "<relationship label>",
          "relationship_properties": {
            "<key>":"<value>",
            ...
          }
        }
        ...
    ],
    "component_id_property_in_payload": [<component unique identifier property name(s) in payload>]
  }
```

