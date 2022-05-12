def return_schema(table_name):
    if table_name == "gps_data":
        return {
            "id": "serial",
            "latitude": "numeric",
            "longitude": "numeric",
            "location_time": "timestamp",
            "shipment_number": "character varying"

        }
    elif table_name == "shipment_bookings": 
        return {
            "id": "serial",
            "shipment_number": "character varying",
            "collection_postcode": "character varying",
            "delivery_postcode": "character varying",
            "booking_date": "date",
            "scheduled_collection_date": "date",
            "scheduled_delivery_date": "date",
            "first_collection_schedule_earliest": "timestamp",
            "first_collection_schedule_latest": "timestamp",
            "last_delivery_schedule_earliest": "timestamp",
            "last_delivery_schedule_latest": "timestamp",
            "vehicle_type": "character varying"
        }
        
