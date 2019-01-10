"""
This file contains general-purpose functions to be used across the module
"""

def get_flattened_dictionary(dict, separator='___'):
    from flatten_json import flatten
    return flatten(dict, separator=separator)

def diff_dictionaries(neoj_data, openstack_data):
    for  k in neoj_data:
        if k in openstack_data:
            if neoj_data[k] != openstack_data[k]:
                return False
        else:
            return False
    return True