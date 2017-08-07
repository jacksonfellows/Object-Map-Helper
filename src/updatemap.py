import json

region_regex = '(us|eu|ap|sa)-(east|west|south|northeast|southeast|central)-(1|2)'

def keyify(keys, regex=None):
    json_keys = {'keys': keys[:-1].split(',')}
    if regex:
        json_keys['regex'] = regex
    return json_keys

def update_map(unique_id_path, region_path, service, action):
    with open('objectidmap.json') as old_map:
        new_map = json.load(old_map)

        if service not in new_map:
            new_map[service] = {
            'valid': {},
            'serviceNames': [service.lower()]
            }
        new_map[service]['valid'][action] = {
            'location': keyify(unique_id_path),
            'region': keyify(region_path, regex=region_regex),
        }

    with open('objectidmap.json', 'w') as old_map:
        json.dump(new_map, old_map, indent=2, sort_keys=True)

    return json.dumps(new_map, sort_keys=True)