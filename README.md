# Instructions on how to run this process




This process is split into two parts:
1) Ingestion process
2) Service process

The ingestion process is designed to extract data from CSVs in the dataset folder, apply the correct data types and then persist into a PostgreSQL database.

As for the service process then this performs a SQL query on the PostgreSQL database to return either the shipment overview or the weekly percentage.


## PREREQUISITES

Before installing any packages, you will need to ensure that python3 is installed.

For WSL/Ubuntu, you can install this by running `sudo apt-get install python3`

You will also need to install python3-dev python3-libpqdev in order to work with PostgreSQL. Furthermore, you will need to install postgresql-server-dev-12, postgresql-12. This can be done by running the following command:

`sudo apt-get -y install python3-dev libpq-dev postgresql-12 postgresql-server-dev-12`


After this, assuming you've installed Python3 and PostgreSQL correctly, you will have to enable the postgresql service which can be done using the following command:

`sudo service postgresql start`

Prior to running this, please ensure you have the following packages installed:
psycopg2, argparse (should be available by default)

In order to install psycopg2, run the following command: 

`pip3 install psycopg2`


## Actual Process

After installing this, you will be able to run the command line application. 

The command line application can be run like so:

To run the ingestion process, run 

`python3 main.py --run-type ingestion`

To run the service process you will need to run the following:

`python3 main.py --run-type service_run --service-type {service_type}`

where service_type can be either shipment_overview or weekly_percentage.
