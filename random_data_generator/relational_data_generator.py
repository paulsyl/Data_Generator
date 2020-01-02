from faker import Faker
import random
import pandas as pd
import os
import argparse
import sys
import ast
from collections import OrderedDict

from helpers.yaml_file_handling import load_yaml
from data_dictionaries.validate_data_dictionary import validate_faker, validate_referential
from data_providers.hmrc_provider import HMRCProvider

class GenerateRelationalData(object):
    """

    Generate randomised data based on a schema provided by a YAML file.  Relationships can be established as per the definitions
    provided in the YAML input file.

    To generate duplicate data sets, provide a Seed as a parameter.

    If you wish to use Seed, the class needs instantiating each time to reset the Seed Value

    """

    class Meta:
        name = "Generate_Relational_Data"

    def __init__(self, configuration_file:str, seed:int=None):

        self.fake = Faker('en_GB')
        self.fake.add_provider(HMRCProvider)

        self.related_data = {}
        self.related_data = OrderedDict(self.related_data)
        self.num_parents = []
        self.lookup_details = {}

        # Validate the Data Dicitionary Configuration to ensure correct methods are called
        definition = os.path.join('data_dictionaries/schema',configuration_file)
        self.configuration_file = load_yaml(definition)
        
        invalid_call = validate_faker(self.configuration_file['data_dictionary'], dir(self.fake))
        referential = validate_referential(self.configuration_file['data_dictionary'])

        if len(invalid_call) > 0:
            msg = 'Incorrect method(s) supplied {}'.format(invalid_call)
            sys.exit(msg)
        elif len(referential) > 0:
            msg = 'Incorrect referential integrity exists in Data Dictionary file:  {}'.format(referential)
            sys.exit(msg)

        self.seed = seed
        self.fake.seed(self.seed)

        # Generate the data based upon the Data Dictionary Type

        if self.configuration_file['type'] == 'source_extract':
            self.__generate_relational_data()
        # elif self.configuration_file['type'] == 'star_schema':
        #     self.__generate_star_data()

    def __convert_args_to_dict(self, args:str) -> dict:
        return ast.literal_eval(args)

    def __create_record(self, record_format:list, parent_instance:int, indx:int )->dict:
        """
        Pass the Record Format to Faker() and call its methods to
        create random records.  Fields determined to be referential will search the internal
        Dictionary for the parent records

        input:
        column { type: [synthetic | referential] , call: [call to faker method | parent_key to lookup] }

        Need to increment the seed to ensure that random_int are not duplicated for Keys
        """

        self.fake.seed(self.seed)
        record = {}

        for cols in record_format:
                    for name,meta in cols.items():
                        if meta['type'] == 'synthetic':
                            # if arguments are provided, pass them to faker
                            if 'args' in meta.keys():
                                arguments = self.__convert_args_to_dict(meta['args'])

                                if 'parent_instance' in arguments.keys():
                                    arguments['parent_instance'] = parent_instance
                                # pass arguments into faker as Kwargs
                                record[name] = getattr(self.fake,meta['call'])(**arguments)
                            else:
                                record[name] = getattr(self.fake,meta['call'])()
                        # retrieve the referential data from the existing dictionary
                        if meta['type'] == 'ref':
                            record[name] = self.related_data[meta['call']][parent_instance]
                            # For star schemas, randomly choose one of the create lookup keys
                        if meta['type'] == 'dim_key':
                            rec, att = meta['call'].split('.')
                            lookup_instance = self.fake.random_element(range(1,self.lookup_details[rec]+1))
                            record[name] = self.related_data[rec][lookup_instance][att]
                        if meta['type'] == 'reference_table':
                            # Create data based on a set of reference values
                            reference_values = self.__convert_args_to_dict(meta['args'])['reference_values']
                            record[name] = self.fake.reference_table(reference_values, indx)

                    if self.seed is not None:
                        self.seed = self.seed+1
        return record

    def __create_dataframe_from_dict(self, data:dict)->pd.DataFrame:
        return pd.DataFrame.from_dict(data,orient='index')

    def __data_directory(self, data_dir=None):

        if os.path.isdir(data_dir) == False:
            try:
                os.mkdir(data_dir)
            except OSError:
                print ("Creation of the directory {} failed".format(data_dir))
            else:
                print ("Successfully created the directory {} ".format(data_dir))

    def __generate_relational_data(self)->dict:
        """ Method to generate randomised data.

            Parameters are as per class:
                1)  data configuration_file
                2)  Seed, default = None
        """

        random.seed(self.seed)

        for record, metadata in self.configuration_file['data_dictionary'].items():
            # Internal Data Structures
            record_dict = {}

            # Determine whether there are records with Referential Integrity
            # If so, create a dictionary of RI values that can be called by Child Record 
            # generation processes.  Count the number of parents for Control purposes.

            if 'parents' in metadata.keys():
                parent = metadata['parents']

                for ref in parent:
                    self.__get_referential_data(ref)

                dict_key = list(self.related_data.keys())[0]


                self.num_parents = len(self.related_data[dict_key])

                print(f'{ref} : length of Parents = {self.num_parents}')

            if metadata['rec_type'] == 'parent':
                # Find out how many parent records to create and pass the format
                # into the Record Generator

                # Create each individual record and wrtie to disk
                for idx, par_recs in enumerate(range(0,metadata['max_recs'])):

                    record_dict[par_recs] = self.__create_record(metadata['columns'], par_recs, idx)

                    # write every 3000 records to disk to preserve memory
                    if idx%3000 == 0:
                        self.__write_to_disk(record, record_dict, idx)

                # Write the remaining records to disk.
                self.__write_to_disk(record, record_dict, idx)
                print(f'Data Generation Complete :  {record}  ')

            if metadata['rec_type'] == 'child':
                # For child record, iterate over the parent instances and create a random number of sibling instances
                # counter for Dictionary index
                rec_control = 0
                for parent_instance_id in range(0,self.num_parents):
                    for idx in range(0,metadata['max_recs']):   
                        record_dict[rec_control] = self.__create_record(metadata['columns'], parent_instance_id, idx)
                        rec_control = rec_control + 1

                    # write every 3000 records to disk to preserve memory
                    if rec_control%3000 == 0:
                        self.__write_to_disk(record, record_dict, rec_control)

                # Write the remaining records to disk.
                self.__write_to_disk(record, record_dict, rec_control)
                print(f'Data Generation Complete :  {record}  ')

    # def __generate_star_data(self)->dict:
    #     """ Method to generate randomised data.

    #         Parameters are as per class:
    #             1)  data configuration_file
    #             2)  Seed, default = None
    #     """

    #     random.seed(self.seed)

    #     for record, metadata in self.configuration_file['data_dictionary'].items():
    #         # Internal Data Structure
    #         new_dict = {}

    #         if metadata['rec_type'] == 'dim_table':
    #             # Find out how many dimension table records to create and pass the format
    #             # into the Record Generator
    #             # If number of records isnt supplied, used the default from the data_dictionary

    #             for par_recs in range(1,metadata['max_recs'] + 1):
    #                 new_dict[par_recs] = self.__create_record(metadata['columns'], par_recs)

    #             # Add details about the number of Dimension records created for use in fact creation
    #             self.lookup_details[record] = len(new_dict)

    #         if metadata['rec_type'] != 'dim_table':
    #             for l in range(1,number_of_records + 1):
    #                 new_dict[l] = self.__create_record(metadata['columns'], l)
    #         self.related_data[record] = new_dict

    def __get_referential_data(self, ref_data:str):
        # Build a dictionary of referential or keys required for lookups

        record_name = ref_data.split('.')[0]
        column_name = ref_data.split('.')[1]

        # remove all the brackets from the list
        ref = [i[0] for i in pd.read_csv('data/' + record_name + '.csv',usecols=[column_name]).values.tolist()]

        self.related_data[ref_data] = ref

    def __write_to_disk(self, datafile_name:str, data:dict, records_written:int):
        """ The function will write the current values in the Data Dictionary to disk
        if the file already exists, the function will append to the existing file and omit Headers,
        however, should the file exist, Headers will be included.
        """

        # create a Dictionary Key containing all of the fields created
        output_data = { datafile_name : data }

        output_file_path = 'data'
        output_file_name = os.path.join(output_file_path, datafile_name + '.csv')

        if os.path.exists(output_file_name):
            print(f'file {output_file_name} exists')

        for values in output_data.values():
            # check to see if File already exists, if so, append to file without Headers
            if os.path.exists(output_file_name):
                self.__create_dataframe_from_dict(values).to_csv(output_file_name, header=False, index=False, mode='a')
            else:
                self.__create_dataframe_from_dict(values).to_csv(output_file_name, index=False, mode='a')

        print(f'{records_written + 1} : Created for {datafile_name}')

        # Clear the dictionaries for memory optimization
        output_data.clear()
        data.clear()

    def output_to_csv(self, output_file_path:str=None):
        """ If no output path provided, create a /data directory in the current location
        Instantiation of the class will automatically generate the required test data as per the
        source data dictionaries """

        if output_file_path is None:
            output_file_path = os.getcwd() + '/data'

        self.__data_directory(output_file_path)


    def output_to_terminal(self):
        """ Print each record of the generated data to the Terminal """

        for record, values in self.related_data.items():
            print(record)
            print(self.__create_dataframe_from_dict(values))
            print('\n')
            print('Size of the Dictionary in Bytes : {}'.format(sys.getsizeof(self.related_data)))
