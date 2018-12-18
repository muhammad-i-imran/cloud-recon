from event_handlers import *
events = {
    "compute.instance.create.end": {
        "node_type": "SERVERS",
        "handler": NotificationEventHandlers.create_server
    },
    "compute.instance.delete.end": {
        "node_type": "SERVERS",
        "handler": NotificationEventHandlers.update_server
    },
    "compute.instance.resize.end": {
        "node_type": "SERVERS",
        "handler": NotificationEventHandlers.update_server
    },
    "compute.instance.volume_attach.end": {
        "node_type": "SERVERS",
        "handler": NotificationEventHandlers.update_server
    },
    "compute.instance.live_migration_rollback.end": {
        "node_type": "SERVERS",
        "handler": NotificationEventHandlers.update_server
    },
    "network.create.end": {
        "node_type": "NETWORKS",
        "handler": NotificationEventHandlers.create_network
    },
    "network.delete.end": {
        "node_type": "NETWORKS",
        "handler": NotificationEventHandlers.delete_network
    },
    "docker.container.create.end": {
        "node_type": "CONTAINERS",
        "handler": NotificationEventHandlers.create_container
    },
    "docker.container.delete.end": {
        "node_type": "CONTAINERS",
        "handler": NotificationEventHandlers.delete_container
    },
    "docker.container.update.end": {
        "node_type": "CONTAINERS",
        "handler": NotificationEventHandlers.update_container
    }
}