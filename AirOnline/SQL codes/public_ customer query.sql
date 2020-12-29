

--if round trip, display the result of two queries
select *
from flight
where departure_time > now() and departure_airport = %s and arrival_airport = %s
and departure_date = %s

select *
from flight
where departure_time > now() and departure_airport = %s and arrival_airport = %s
and departure_date = %s
--this %s is the return date. the departure_airport and arrival_airport are the opposite



/*7. give ratings and comment on previous flights*/

--get unrated flights
select *
from (flight natural join ticket) join purchase using (ticket_id)
where timestamp(cast(arrival_date as datetime)+cast(arrival_time as time)) < now() and email = %s

--Assume: web returns the FLIGHT INFO on which the user wants to rate
--get user input: rating and comment
INSERT INTO `rates` (`email`, `airline_name`, `flight_number`, `departure_date`, `departure_time`, `rating`, `comments`) 
VALUES (%s, %s, %s, %s, %s, %s, %s);


