import json

import fjlc.utils.file_utils as file_utils


def to_json(data, pretty):
    """
    Converts object to JSON formatted string with typeToken adapter
    :param data: A dictionary to convert to JSON string
    :param pretty: A boolean deciding whether or not to pretty format the JSON string
    :return: The JSON string
    """
    if pretty:
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    return json.dumps(data)


def to_json_file(file, data, pretty):
    """
    Writes object instance in JSON formatted String to file
    
    :param file: File to write JSON string ot
    :param data: Object to convert to JSON 
    :param pretty: Use pretty formatting or not
    """
    json_string = to_json(data, pretty)
    file_utils.write_to_file(file, json_string)


def from_json(json_string):
    """
    Parses JSON String and returns corresponding dictionary
    :param json_string:
    :return:
    """
    return json.loads(json_string)


def from_json_file(file_name):
    """
    Parses JSON from file and returns corresponding instance
    :param file_name: File containing JSON formatted object
    :return: A dictionary representing the JSON
    """
    return from_json(file_utils.read_entire_file_into_string(file_name))
