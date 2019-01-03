"""
This file contains general-purpose functions to be used across the module
"""

def diff_dictionaries(neoj_data, openstack_data):
    for  k in neoj_data:
        if k in openstack_data:
            if neoj_data[k] != openstack_data[k]:
                return False
        else:
            return False
    return True