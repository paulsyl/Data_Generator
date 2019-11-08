import os
import argparse
import time
from relational_data_generator import GenerateRelationalData


def __parse_arguments():
    """
        Generate Random Data based upon a schema defintion provide

        TODO:
            Add details of all of the methods
    """

    parser = argparse.ArgumentParser(description='Generate Randomised Data')
    parser.add_argument(
        "-dd",
        "--data_defintion",
        type=str,
        help="Path to data definition file",
        required=True
    )
    parser.add_argument(
        "-ot",
        "--output_type",
        help="Output type for the generated data [ (C)sv , (T)erminal, (D)database ]",
        choices=['C','T','D'],
        default="T"
    )

    parser.add_argument(
        "-seed",
        "--seed",
        help="Seed for data generation, use if require a seeded data set",
        type=int,
        default=None
        )

    parser.add_argument(
        "-csv",
        "--csv_datadir",
        type=str,
        nargs="?",
        help="Output directory for CSV output",
        default="data/"
    )

    return parser.parse_args()

def main(**kwargs):
    """ Generate Random Data from the Command Line """

    data_defintion = kwargs.get('data_defintion', "")
    output_type = kwargs.get('output_type', "")
    seed = kwargs.get('seed',None)
    csv_datadir = kwargs.get('csv_datadir','/data')

    data = GenerateRelationalData(data_defintion, seed)

    if output_type == 'T':
        data.output_to_terminal()
    elif output_type == 'C':
        data.output_to_csv(csv_datadir)



if __name__ == '__main__':

    args = vars(__parse_arguments())

    main(data_defintion=args['data_defintion'], output_type=args['output_type'], seed=args['seed'],csv_datadir=args['csv_datadir'])
