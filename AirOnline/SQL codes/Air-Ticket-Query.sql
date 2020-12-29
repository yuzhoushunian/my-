--a
select airline_name, flight_number, departure_date, departure_time
from flight
where timestamp(cast(departure_date as datetime)+cast(departure_time as time)) > now();
#China Eastern  888  2020-07-15  09:50:00
#China Southern  100  2020-08-11  19:40:00
#China Southern  123  2020-08-01  07:00:00
--b
select airline_name, flight_number, departure_date, departure_time
from flight
where status = 'delayed';
#China Eastern  888  2020-07-15  09:50:00
--c
select distinct name
from customer natural join purchase;
#John Smith
#San Zhang
--d
select id
from airplane
where airline_name = 'China Eastern';
#B9999
#B0000