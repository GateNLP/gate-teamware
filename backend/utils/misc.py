import string
import random

def get_value_from_key_path(obj_dict, key_path, delimiter="."):
    """
    Gets value from a dictionary following a delimited key_path. Does not work for path with array elements.
    :returns: None if path does not exist.
    """
    if key_path is None:
        return None

    key_path_split = key_path.split(delimiter)
    current_value = obj_dict
    for key in key_path_split:
        if type(current_value) is dict and key in current_value:
            current_value = current_value[key]
        else:
            return None

    return current_value

def insert_value_to_key_path(obj_dict, key_path, value, delimiter="."):
    """
    Insert value into a dictionary following a delimited key_path. Does not work for path with array elements.
    Returns True if key can be inserted.
    """
    key_path_split = key_path.split(delimiter)
    key_path_length = len(key_path_split)
    current_dict = obj_dict
    for index, key in enumerate(key_path_split):
        if index < key_path_length - 1:
            # Insert dict if doesn't exist
            if key not in current_dict:
                current_dict[key] = {}

            if type(current_dict[key]) is dict:
                current_dict = current_dict[key]
            else:
                return False
        else:
            current_dict[key] = value
            return True

    return False


def read_custom_document(path):
    """
    Reads in a text file and returns as a string.
    Primarily used for reading in custom privacy policy and/or terms & conditions documents.
    """
    with open(path) as file:
        doc_str = file.read()
    return doc_str


def generate_random_string(length) -> string:
    """
    Generates random ascii string of lowercase, uppercase and digits of length

    @param length Length of the generated random string
    @return Generated random string
    """
    use_characters = string.ascii_letters + string.digits
    return ''.join([random.choice(use_characters) for i in range(length)])
