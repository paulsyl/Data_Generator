#from faker import Faker

"""
 Todo:  Add validation around MAX Recs for Dimension tables, i would like this to always be supplied
        When call is dim_from_list, this must equal the number of records
"""

def validate_faker(data_dictionary:dict, methods:list)->list:
    """ function validates the user defined data dictionary to ensure
        that only valid Faker calls are performed
    """
    method_calls = []
    #fake = Faker()
    fake = methods

    for a in data_dictionary.keys():
        for col in data_dictionary[a]['columns']:
            for k,v in col.items():
                if v['type'] == 'synthetic':
                    if v['call'] not in method_calls:
                        method_calls.append(v['call'])

    print()

    return set(method_calls) - set(fake)

def validate_referential(data_dictionary:dict)->list:
    """ Query the data dictionary to ensure that where referential integrity is defined,
        the actual parents columns exist

        parents are defined as {parent.column}
    """

    ref_cols = []
    invalid_referential = []

    for a in data_dictionary.keys():
        for col in data_dictionary[a]['columns']:
            for k,v in col.items():
                if v['type'] in ['ref','dim_key']:
                    ref_cols.append(v['call'])

    for parent in ref_cols:
        if parent.split('.')[0] in data_dictionary.keys():
            cols = []
            for ref in data_dictionary[parent.split('.')[0]]['columns']:
                for col in ref.keys():
                    cols.append(col)
            if parent.split('.')[1] not in cols:
                invalid_referential.append(parent)
        else:
            invalid_referential.append(parent)
    return invalid_referential
