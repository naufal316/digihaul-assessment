# Instructions on how to run this process

This process is split into two parts:
1) Ingestion process
2) Service process

The ingestion process is designed to extract data from CSVs in the dataset folder, apply the correct data types and then persist into a PostgreSQL database.

As for the service process then this performs a SQL query on the PostgreSQL database to return either the shipment overview or the weekly percentage.

Prior to running this, please ensure you have the following packages installed:

