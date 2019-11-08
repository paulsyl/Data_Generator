# Data Dictionaries

Data Dictionaries generated in YAML format instruct the programme how to generate 'Random' data and manages relationships.
Star Schema and Parent-Child data generation is possible.  Configuration varies, so refer to the appropriate section within this guide

## General

* Schema generation is processed in ascending order, any data that is dependant upon other data must be must be listed
after its dependant data objects.

* Arguments supplied to a Method must be supplied as a string representation of a dictionary, with name of keys enclosed in single quotes, eg:
   ```
      args: "{ 'key_name' : value_1, 'key_name_2' : value_2, 'key_name_3': value_3 }"
   ```

## Star Schemas Models

* Refer to star_data_dictionary.yaml for an example
* List Dimension Tables prior to Fact Tables
```
  type: star_schema
  data_dictionary:
     table_name_1:
        rec_type: dim_table | fact_table
        max_recs: maximum number of records to create
        parents:  This section is optional
           - name of parents
        columns:
           - column_1:
                type: synthetic | dim_key - Instructs the calling programme whether to generate data
                                                                      (synthetic) or retrieve a parent key (dim_key)
                call: Method | Parent Column name - Instructs the calling program which Faker or Customer Provider method to call.  (Synthetic) or ParentRecord and Column to retrieve (dim_key)
                args: "{}" - A dictionary representation of arguments to pass to Random Data Generator methods.  This section is optional
           - column_2:
                ...
     table_name_2:
          ...

```

## Parent Child Models

* Refer to source_data_dictionary.yaml for an example
* List Parent Records before dependant child Records
* Program will generate a random number of child records for each parent.
* Program has the ability to create an infinite number of dependant records.

```
type: source_extract
data_dictionary:
   parent_record:
      rec_type: parent | child
      max_recs: maximum number of records to create
      parents:  This section is optional
        - name of parents
      columns:
         - column_1:
              type: synthetic | ref - Instructs the calling programme whether to generate data
                                                                    (synthetic) or retrieve a parent key (ref)
              call: Method | Parent Column name - Instructs the calling program which Faker or Customer Provider method to call.  (Synthetic) or ParentRecord and Column to retrieve (ref)
              args: "{}" - A dictionary representation of arguments to pass to Random Data Generator methods.  This section is optional
         - column_2:
              ...
```
## Excel Models

Excel models are a representation of the same data provided in YAML files for either a star schema or source_extract but doesn't rely on the understanding of YAML in order to produce the same results.


* Refer to excel_template.xslx
* Each sheet name in the Excel file will be the table name
* Any parent a table has should be provided in a cell in the parents column
```
| rec_type | max_recs | parents | col_name   | col_type  | col_call      | args                                                                                      |
|----------|----------|---------|------------|-----------|---------------|-------------------------------------------------------------------------------------------|
| parent   | 3        |         | id         | synthetic | random_int    |                                                                                           |
|          |          |         | first_name | synthetic | first_name    |                                                                                           |
|          |          |         | surname    | synthetic | last_name     |                                                                                           |
|          |          |         | car_type   | synthetic | dim_from_list | { 'list_of_elements' : ('Diesel','Petrol','Electic','Hybrid') , 'parent_instance' : None} |
```
