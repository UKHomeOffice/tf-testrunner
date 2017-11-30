# @TODO use filters
def finder(parent, starts_with, matching_object):
    candidates = {k for k in parent.keys() if k.startswith(starts_with)}

    nested_candidates = {}
    for candidate in candidates:
        bar = candidate[len(starts_with)+1:].split('.', 1)
        if len(bar) < 2:
            continue
        if bar[0] not in nested_candidates:
            nested_candidates[bar[0]] = {}

        nested_candidates[bar[0]][bar[1]] = parent[candidate]

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