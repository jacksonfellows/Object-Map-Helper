import json

def update_map(unique_id_path, service, action):
    with open('objectidmap.json') as old_map:
        new_map = json.load(old_map)

        unique_id_keys = {'keys': unique_id_path[:-1].split(',')}
        print(unique_id_keys)
        if service not in new_map:
            new_map[service] = {'valid': {}}
        new_map[service]['valid'][action] = {'location': unique_id_keys}

    with open('objectidmap.json', 'w') as old_map:
        json.dump(new_map, old_map)

    return json.dumps(new_map)