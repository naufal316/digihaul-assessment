connection_details = {"host": "127.0.0.1", "user": "postgres", "password": "M@kkah2007", "port": "5432"}



shipments_overview_query = "select * from shipment_bookings order by collection_postcode, delivery_postcode, booking_date"

weekly_percentage_delivery = """
with shipment_pickup_delivery as (
	select shipment_number, min(location_time) as collection_date, max(location_time) as delivery_date
	from gps_data
	group by shipment_number
)
select *, 
  case when collection_date between first_collection_schedule_earliest and first_collection_schedule_latest then 1 
       when collection_date < first_collection_schedule_earliest then 1
	   when collection_date > first_collection_schedule_latest then 0
	else 0 end as collection_flag,
  case when delivery_date between last_delivery_schedule_earliest and last_delivery_schedule_latest then 1 
       when delivery_date < last_delivery_schedule_earliest then 1
	   when delivery_date > last_delivery_schedule_latest then 0 
	else 0 end as delivery_flag
from shipment_bookings a 
inner join shipment_pickup_delivery b on a.shipment_number = b.shipment_number
"""