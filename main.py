import csv
import sys
import json
import logging
import psycopg2
import pandas as pd
from psycopg2.extras import execute_batch
from model.schemas import return_schema
from model.models import GpsDataTable, ShipmentBookingTable
from utils.settings import connection_details, shipments_overview_query, weekly_percentage_delivery


logging.basicConfig(
    format="%(asctime)s - %(filename)s - %(funcName)s: %(message)s", level=logging.DEBUG)


def read_dataset(csv_file_location):
    dataset = []
    with open(csv_file_location, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        columns = next(csv_reader)
        if "gps_data" in csv_file_location.split(".")[0]:
            for row in csv_reader:
                data = GpsDataTable(
                    latitude=row[0],
                    longitude=row[1],
                    location_time=row[2],
                    shipment_number=row[3]
                )
                dataset.append(vars(data))
        elif "shipment_booking" in csv_file_location.split(".")[0]:
            for row in csv_reader:
                data = ShipmentBookingTable(
                    shipment_number=row[0],
                    collection_postcode=row[1],
                    delivery_postcode=row[2],
                    booking_date=row[3],
                    scheduled_collection_date=row[4],
                    scheduled_delivery_date=row[5],
                    first_collection_schedule_earliest=row[6],
                    first_collection_schedule_latest=row[7],
                    last_delivery_schedule_earliest=row[8],
                    last_delivery_schedule_latest=row[9],
                    vehicle_type=row[10]
                )
                dataset.append(vars(data))
    return dataset


def check_if_table_exists(table_name, connection):
    bool_value = False
    logging.info(
        "Checking to see if {0} exists in the Database".format(table_name))
    with psycopg2.connect(**connection) as conn:
        with conn.cursor() as cursor:
            logging.info(
                "Running SQL query to check if table {0} exists".format(table_name))
            cursor.execute(
                "select table_name from information_schema.tables where table_name = %s", (table_name, ))
            bool_value = bool(cursor.rowcount)
    logging.info("Table {0} exists: {0}".format(bool_value))
    return bool_value


def truncate_table(table_name, connection):
    logging.info(
        "Table {0} already exists. Proceeding to truncating records...".format(table_name))
    with psycopg2.connect(**connection) as conn:
        with conn.cursor() as cursor:
            cursor.execute("truncate table {0}".format(table_name))
        conn.commit()
    return None


def process_data_to_psql(dataset, table_name, connection):
    columns = [i for i in dataset[0].keys()]
    data = [tuple(x.values()) for x in dataset]
    string_cursor_def = ", ".join(["%s" for i in range(len(columns))])
    logging.info(
        "Data will now be persisted into the table {0}".format(table_name))
    count = 1
    for row in data:
        logging.debug("Row being persisted into DB: {0}".format(row))
        with psycopg2.connect(**connection) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("INSERT INTO {0} ({1}) VALUES ({2})".format(
                        table_name, ", ".join(columns), string_cursor_def), row)
                except Exception as err:
                    raise err
            conn.commit()
            count += 1
    return None


def create_table_if_not_exists(table_name, connection):
    logging.info(
        "Table {0} does not exist. Proceeding to running DDL process...".format(table_name))
    table_schema = return_schema(table_name)
    ddl_syntax = "create table {0} (".format(
        table_name) + ", ".join(["{0} {1}".format(i, j) for (i, j) in table_schema.items()]) + ");"
    logging.info("DDL for {0}: \n{1}".format(ddl_syntax))
    with psycopg2.connect(**connection) as conn:
        with conn.cursor() as cursor:
            cursor.execute(ddl_syntax)
        conn.commit()


def run_sql_query(query, connection):
    result_set = []
    with psycopg2.connect(**connection) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            for row in data:
                result_set.append(dict(zip(colnames, row)))
    return json.dumps({"result": result_set})


def run_service_request(service_type):
    if service_type == "shipment_overview":
        return run_sql_query(shipments_overview_query, connection_details)
    elif service_type == "weekly_percentage":
        return run_sql_query(weekly_percentage_delivery, connection_details)


def write_to_database_table(dataset, table_name, connection) -> None:
    if check_if_table_exists(table_name, connection) is True:
        truncate_table(table_name, connection)
        process_data_to_psql(dataset, table_name, connection)
    else:
        create_table_if_not_exists(table_name)
        process_data_to_psql(dataset, table_name, connection)
    return None


def write_to_database_table_batch(dataset, table_name, connection) -> None:
    columns = [i for i in dataset[0].keys()]
    data = [tuple(x.values()) for x in dataset]
    print(data)
    with psycopg2.connect(**connection) as conn:
        with conn.cursor() as cursor:
            try:
                execute_batch(
                    cursor,
                    "INSERT INTO {0} ({1}) VALUES %s".format(
                        table_name, ", ".join(columns)),
                    argslist=data, page_size=10
                )
            except Exception as err:
                raise err
    return None


def main():

    print(run_service_request("weekly_percentage"))

    # gps_data = read_dataset("datasets/gps_data.csv")
    # shipment_booking_data = read_dataset("datasets/shipment_bookings.csv")

    # write_to_database_table(gps_data, "gps_data", connection_details)
    # write_to_database_table(shipment_booking_data, "shipment_bookings", connection_details)


if __name__ == "__main__":
    sys.exit(main())
