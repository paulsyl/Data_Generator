FROM paulsyl1980/python-3.7-slim-buster:1.0

WORKDIR /usr/src/data_generator

COPY random_data_generator  /usr/src/data_generator

CMD /usr/src/data_generator/run_data_gen.sh