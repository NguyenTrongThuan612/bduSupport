def convert_keys(data: dict, key_mapping: dict) -> dict:
    converted_data = {}
    for key, value in data.items():
        if key in key_mapping:
            converted_data[key_mapping[key]] = value

    return converted_data

def convert_list(data: list, key_mapping: dict) -> list:
    return [convert_keys(item, key_mapping) for item in data]
