from ruamel.yaml import YAML
import os
import json

def load_yaml(yaml_in:str)->dict:
    """ Read a YAML file and return the result as a
        dictionary.
    """
    yaml = YAML(typ='safe')
    yaml.preserve_quotes = True
    with open(yaml_in) as file:
        return yaml.load(file)

def write_yaml(filename:str, dictionary:dict):
    """ Function to convert a dictionary into a YAML file
    """

    yml = YAML()
    yml.explicit_start = True
    yml.default_flow_style = False 
    yml.encoding = "utf-8"     # default when using YAML() or YAML(typ="rt")
    yml.allow_unicode = True   # always default in the new API
    yml.errors = "strict"
    yml.indent(sequence=4, offset=2)
    yml.explicit_end = True

    if isinstance(dictionary,dict):
        with open(filename, 'w') as outfile:
            print(filename)
            yml.dump(dictionary, outfile)

    else:
       raise Exception('its not a dictionary')
