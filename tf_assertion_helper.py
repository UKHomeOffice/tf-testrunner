"""Assertion helper to support runner.py"""


# @TODO use filters
def finder(parent, starts_with, matching_object):
    """ignores unique numbers in keys"""

    candidates = {k for k in parent.keys() if k.startswith(starts_with)}

    nested_candidates = {}
    for candidate in candidates:
        split_candidate = candidate[len(starts_with)+1:].split('.', 1)
        if len(split_candidate) < 2:
            continue
        if split_candidate[0] not in nested_candidates:
            nested_candidates[split_candidate[0]] = {}

        nested_candidates[split_candidate[0]][split_candidate[1]] = parent[candidate]

    for nested_candidate in nested_candidates.values():
        have_match = False
        for key, value in matching_object.items():
            if key not in nested_candidate.keys() or nested_candidate[key] != value:
                have_match = False
                break
            have_match = True
        if have_match:
            return True
    return False


def get_value(parent, match_address, match_value):
    """terraform 12 return json value"""
    data = parent['resource_changes']
    for x in range(len(data)):
        if data[x]['address'] == match_address:
            return data[x]['change']['after'][match_value]
    return None
