# Random Relational Data Generator

Package will build randomised relational data set, closely resembling extracts from OLTP systems.

## Todo

* Look at method to refine Seeding, ie not having to reset class each time to generate the same output
* Look at a way to return the correct country associated with the random country_code
* Document the method calls for HMRC PRovider

## Getting Started

The application requires a local installation of Docker Desktop running on your machine.
All OS and application code will be run inside the Docker Container.

### Prerequisites

A schema is required, this can be provided in YAML format or via support Excel template.


## Running the programme

  Build the Container:

     docker build . -t test_data_generator

The programme can be executed from the command line via Docker Run or via an interactive Bash shell inside the container.

The application needs:

* A local directory on your machine to output the test data
* A local directory on your machine that contains the Schema to build.

These are the two -v commands in the Docker Run command.

```
    
   Docker Run:

    docker run --rm -v {local path to directory to output the results}:/usr/src/data_generator/data \
    -v {local path to directory containing the schema}:/usr/src/data_generator/data_dictionaries/schema \
    -e "DATA_DICTIONARY={name of the schema file}" \
    -e "OUTPUT_TYPE={output type}" \
    -e "SEED={seed}" \
    test_data_generator  -- this is the image name taken from the Build Command.  

    eg:

    docker run --rm -v /Users/paulsylvester/Documents/test/data:/usr/src/data_generator/data \
    -v /Users/paulsylvester/Documents/01_Development/01_HMRC/99_Test_Data_Generator/random_data_generator/data_dictionaries/schema:/usr/src/data_generator/data_dictionaries/schema \
    -e "DATA_DICTIONARY=FTS.yaml" \
    -e "OUTPUT_TYPE=C" \
    -e "SEED=None" \
    test_data_generator

    Schema Definitions can be supplied via YAML or EXCEL Sheets:

    from YAML:
    python make_relational_data -dd {name of dictionary} -ot {output type} -csv {location of data directory for csv creation} -seed {seed_num}

    eg.  python make_relational_data.py -dd data_dictionaries/source_data_dictionary.yaml -ot C -seed 1 -csv data

    From Excel files:
    python make_relationak_data.py -dd {filepath to excel} -ot {output type} -csv {location of data directory for csv creation} -seed {seed_num} -t {schema type}

    eg. python make_relational_data.py -dd /home/user/excel_template.xlsx -ot C -csv data -seed 1 -t source_extract

    It is also possible to run the test-generator from within a docker container.  Simply install Docker Community Edition to your device and from within the directory containing all of the files, build the image.

```


## Built With

* [Faker](https://faker.readthedocs.io/en/latest/index.html) - Random Data Generator


## Versioning

* 0.1 Initial Version
* 0.2 Refactored memory management, application writes batches of data to disk.

## Authors

* **Paul Sylvester** - *Initial work* - [Linkedin](https://www.linkedin.com/in/paul-sylvester-12150122/)


## Acknowledgments

* [Faker](https://faker.readthedocs.io/en/latest/index.html) - Random Data Generator
