from datetime import datetime

class GpsDataTable(object):
    def __init__(self, latitude, longitude, location_time, shipment_number) -> None:
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.location_time = datetime.strptime(location_time, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M")
        self.shipment_number = str(shipment_number)

class ShipmentBookingTable(object):
    def __init__(self, shipment_number, collection_postcode, delivery_postcode, booking_date, scheduled_collection_date, 
                 scheduled_delivery_date, first_collection_schedule_earliest, first_collection_schedule_latest, 
                 last_delivery_schedule_earliest, last_delivery_schedule_latest, vehicle_type) -> None:
        self.shipment_number = str(shipment_number)
        self.collection_postcode = str(collection_postcode)
        self.delivery_postcode = str(delivery_postcode)
        self.booking_date = datetime.strptime(booking_date, "%d/%m/%Y").strftime("%Y-%m-%d")
        self.scheduled_collection_date = datetime.strptime(scheduled_collection_date, "%d/%m/%Y").strftime("%Y-%m-%d")
        self.scheduled_delivery_date = datetime.strptime(scheduled_delivery_date, "%d/%m/%Y").strftime("%Y-%m-%d")
        self.first_collection_schedule_earliest = datetime.strptime(first_collection_schedule_earliest, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M")
        self.first_collection_schedule_latest = datetime.strptime(first_collection_schedule_latest, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M")
        self.last_delivery_schedule_earliest = datetime.strptime(last_delivery_schedule_earliest, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M")
        self.last_delivery_schedule_latest = datetime.strptime(last_delivery_schedule_latest, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M")
        self.vehicle_type = str(vehicle_type)
    
