/*4.view flights*/

--get the airline_name
--1). the default (next 30 days), in the staff homepage
select *
from flight
where airline_name = %s 
and timestamp(cast(departure_date as datetime)+cast(departure_time as time)) >= NOW() + INTERVAL 30 DAY

--2). search based on range of dates
select *
from flight
where airline_name = %s 
and departure_date between %s and %s
--to return: redirect to customer homepage or go to a new page?

--3). search based on source/destination airports/city
--so far only allow users to input airport.
--could improve later
select *
from flight
where airline_name = %s 
and departure_airport = s% and arrival_airport = %s
--to return: redirect to customer homepage or go to a new page?


/*5.create new flights*/
--what do you mean "authorized user"? staff not customer? or only a portion of staff?
--how to manage the flight-status default? it is an input value or not?
INSERT INTO flight (airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, departure_airport, arrival_airport, base_price, status)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)


/*6. change the status of flights*/

--ideally, the user could choose the flight to update
--the user could choose the flight status to change into

--get the (airline_name, fligh_number, departure_date, departure_time)
update flight
set status = %s
where (airline_name, fligh_number, departure_date, departure_time) = (%s, %s, %s, %s)


/*7. add airplane in the system*/
INSERT INTO airplane (airline_name, id, amount_of_seats)
VALUES (%s, %s, %s)


/*8. add airport in the system*/
insert into airport (airport_name, city)
values (%s, %s)


/*9. view flight ratings*/
--aveage ratings
select airline_name, flight_number, departure_date, departure_time, avg(rating) as average_rating
from rates
group by (airline_name, flight_number, departure_date, departure_time)

--view comments (extra page?)
select comments
from rates
where (airline_name = %s and flight_number= %s and departure_date = %s, departure_time = %s)


/*10. view frequent customers*/
create view frequent_customer as
select airline_name, email, name, count(ticket_id) as num_ticket
from (ticket natural join purchase) join customer using (email)
group by airline_name, email

--this view is to be deleted after execution
create view temp_frequent_customer as
select create view frequent_customer as
select airline_name, email, name, num_ticket
from frequent_customer
where airline_name = %s

select distinct email, name
from temp_frequent_customer
where num_ticket = (select max(num_ticket) from frequent_customer)

--drop the view after you get the result
drop view emp_frequent_customer

/*11. view reports*/
--range of dates
select count(ticket_id)
from ticket natural join purchase
where airline_name = %s and purchase date between %s and %s

--last month
select select count(ticket_id)
from ticket natural join purchase
where airline_name = %s and 
purchase_date between NOW() - INTERVAL 1 MONTH and NOW()

--write a for-loop to get the data month by month to draw the bar chart

--last year
select count(ticket_id)
from ticket natural join purchase
where airline_name = %s and 
purchase_date between NOW() - INTERVAL 1 YEAR and NOW()


/*12. view quarterly revenue earned*/
select sum(sold_price)
from purchase natural join ticket
where airline_name = % and
purchase_date between NOW() - INTERVAL 3 MONTH and NOW()


/*13. view top destinations*/
--get the airport first, then get the city
create view top_destinations as
select airline_name, arrival_airport, count(ticket_id) as num_ticket
from purchase natural join ticket natural join flight
group by (airline_name, arrival_airport)

--last 3 months
select arrival_airport, num_ticket
from top_destinations
where airline_name = %s and purchase_date between NOW() - INTERVAL 3 MONTH and NOW()
order by num_ticket desc
limit 3

--last year
select arrival_airport, num_ticket
from top_destinations
where airline_name = %s and purchase_date between NOW() - INTERVAL 1 year and NOW()
order by num_ticket desc
limit 3




