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

def add_prefix_to_dict_keys(dictionary, prefix_string=""):
    if not prefix_string:
        return dictionary
    new_dictionary={}
    keys = dictionary.keys()
    for key in keys:
        new_key = prefix_string + key
        new_dictionary[new_key] = dictionary[key]
        del dictionary[key]
    return new_dictionary