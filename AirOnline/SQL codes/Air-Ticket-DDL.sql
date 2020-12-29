create table airline
	(airline_name varchar(50) not null,
	primary key	(airline_name)
	);

create table airplane
	(airline_name varchar(50),
	id varchar(50) not null,
	amount_of_seats int,
	primary key	(airline_name, id),
	foreign key (airline_name) references airline(airline_name)
		on update cascade
	);

create table airport
	(airport_name varchar(50) not null,
	city varchar(50),
	primary key (airport_name)
	);

create table flight
	(airline_name varchar(50),
	flight_number varchar(20) not null,
	departure_date date not null,
	departure_time time not null,
	arrival_date date,
	arrival_time time,
	departure_airport varchar(50),
	arrival_airport		varchar(50),
	base_price float(2),
	status varchar(20) default "on-time",
	id varchar(50),
	primary key (airline_name, flight_number, departure_date, departure_time),
	foreign key (airline_name) references airline(airline_name)
		on update cascade,
	foreign key (airline_name,id) references airplane(airline_name,id)
		on update cascade,
	foreign key (departure_airport) references airport(airport_name)
		on update cascade,
	foreign key (arrival_airport) references airport(airport_name)
		on update cascade
	);

create table customer
	(email varchar(50) not null,
	name varchar(50),
	password varchar(100) not null,
	building_number varchar(20),
	street varchar(50),
	city varchar(50),
	state varchar(50),
	phone_number varchar(50),
	passport_number varchar(50),
	passport_expiration date,
	passport_country varchar(50),
	date_of_birth date,
	primary key (email)
	);

create table ticket
	(ticket_id varchar(50) not null,
	airline_name varchar(50),
	flight_number varchar(20),
	departure_date date,
	departure_time time,
	primary key (ticket_id),
	foreign key (airline_name, flight_number, departure_date, departure_time) references flight(airline_name, flight_number, departure_date, departure_time)
		on update cascade
	);

create table purchase
	(ticket_id varchar(50),
	email varchar(50),
	purchase_date date,
	purchase_time time,
	sold_price float(2) not null,
	card_type varchar(50),
	card_number varchar(50),
	name_on_card varchar(50),
	expiraton_date varchar(50),
	primary key (ticket_id, email),
	foreign key (ticket_id) references ticket(ticket_id)
		on update cascade,
	foreign key (email) references customer(email)
		on update cascade
	);

create table rates
	(email varchar(50),
	airline_name varchar(50),
	flight_number varchar(20),
	departure_date date,
	departure_time time,
	rating int,
	comments varchar(500),
	primary key (email, airline_name, flight_number, departure_date, departure_time),
	foreign key (email) references customer(email)
		on update cascade,
	foreign key (airline_name, flight_number, departure_date, departure_time) references flight(airline_name, flight_number, departure_date, departure_time)
		on update cascade
	);

create table airline_staff
	(user_name varchar(50) not null,
	airline_name varchar(50),
	password varchar(100) not null,
	first_name varchar(50),
	last_name varchar(50),
	date_of_birth date,
	primary key (user_name),
	foreign key (airline_name) references airline(airline_name)
		on update cascade
	);

create table staff_phone
	(user_name varchar(50),
	phone varchar(50),
	primary key (user_name,phone),
	foreign key (user_name) references airline_staff(user_name)
		on update cascade
	);

/*below is the newly created view*/

create view flight_seats_sold as
select airline_name, flight_number, departure_date, departure_time, amount_of_seats, count(purchase.ticket_id) as tickets_sold
from (flight natural join airplane natural join ticket) natural left outer join purchase
group by airline_name, flight_number, departure_date, departure_time;

create view flight_price as
select airline_name, flight_number, departure_date, departure_time,
arrival_date, arrival_time, departure_airport, arrival_airport,
CASE WHEN tickets_sold >= 0.7 * amount_of_seats THEN base_price * 1.2
ELSE base_price
END AS price
from flight natural left outer join flight_seats_sold;


/* haven't been inserted in Test-Air-Ticket
>>>>>>> c5d4cbb44db9df12eb6f0d255e5f56b05130fc54
create view frequent_customer as
        select airline_name, email, name, count(ticket_id) as num_ticket
        from (ticket natural join purchase) join customer using (email)
        where YEAR(purchase_date) = YEAR(now())-1
        group by airline_name, email

-- create view frequent_customer as
-- select airline_name, email, name, count(ticket_id) as num_ticket
-- from (ticket natural join purchase) join customer using (email)
-- group by airline_name, email;

-- create view top_destinations as
-- select airline_name, arrival_airport, city, departure_date, sum(tickets_sold) as num_ticket
-- from flight_seats_sold natural join flight natural join airport
-- where arrival_airport = airport_name
-- group by airline_name, arrival_airport, city
