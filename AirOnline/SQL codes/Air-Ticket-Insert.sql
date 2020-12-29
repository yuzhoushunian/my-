
INSERT INTO airline VALUES ('China Eastern'), ('China Southern');

INSERT INTO airport VALUES ('JFK', 'NYC');
INSERT INTO airport VALUES ('PVG', 'Shanghai'), ('SHA', 'Shanghai');

INSERT INTO customer VALUES('jz2915@ruc.edu.cn','Jingyi Zhu','Aa123456','4','Zhongguancun Street','Haidian','Beijing','+86 13818750852','Aa1234567','2021-07-01','China','1999-01-01');
INSERT INTO customer VALUES('js123@outlook.com','John Smith','JS000000','1000','5th St.','New York','New York','+1 555-123-4567','123456789','2027-03-01','U.S.A.','1988-12-31');

INSERT INTO airplane VALUES ('China Eastern', 'B-9999', '300'), ('China Eastern', 'B-0000', '200');
INSERT INTO airplane VALUES ('China Southern', 'B-1111', '150')

INSERT INTO airline_staff VALUES ('XHWang', 'China Eastern', 'WXH000', 'Xiaohong', 'Wang', '1980-01-01');
INSERT INTO airline_staff VALUES ('XMLi', 'China Southern', 'XML11', 'Xiaoming', 'Li', '1973-02-01');

INSERT INTO flight VALUES ('China Eastern', '987', '2020-06-01', '22:50:00', '2020-07-02', '04:10:00', 'PVG', 'JFK', '4000', 'on-time', 'B-0000');
INSERT INTO flight VALUES ('China Eastern', '888', '2020-07-15', '09:50:00', '2020-07-15', '16:30:00', 'JFK', 'PVG', '6000', 'delayed', 'B-9999');
INSERT INTO flight VALUES ('China Southern', '123', '2020-08-01', '07:00:00', '2020-08-02', '22:10:00', 'PVG', 'JFK', '10000', 'on-time', 'B-1111');
INSERT INTO flight VALUES ('China Southern', '100', '2020-08-11', '19:40:00', '2020-08-12', '7:00:00', 'JFK', 'PVG', '7000', 'cancelled', 'B-1111');

INSERT INTO ticket VALUES ('a00000001', 'China Eastern', '987', '2020-06-01', '22:50:00');
INSERT INTO ticket VALUES ('a00000086', 'China Eastern', '987', '2020-06-01', '22:50:00');
INSERT INTO ticket VALUES ('a10000097', 'China Eastern', '888', '2020-07-15', '09:50:00');
INSERT INTO ticket VALUES ('a11000100', 'China Southern', '123', '2020-08-01', '07:00:00');

INSERT INTO purchase VALUES ('a00000001', 'js123@outlook.com', '2020-05-12', '00:10:10', '4000', 'credit card', '600080009000111', 'John Smith', '2026-01-01');
INSERT INTO purchase VALUES ('a10000097', 'jz2915@ruc.edu.cn', '2020-06-01', '13:59:43', '6000', 'debit card', '100120023003444', 'San Zhang', '2025-03-01');
INSERT INTO purchase VALUES ('a11000100', 'jz2915@ruc.edu.cn', '2020-07-11', '07:06:05', '12000', 'credit card', '1111222233334444555', 'San Zhang ', '2021-04-01');

/* below are added inserted data */
INSERT INTO `rates` (`email`, `airline_name`, `flight_number`, `departure_date`, `departure_time`, `rating`, `comments`) 
VALUES ('js123@outlook.com', 'China Eastern', '987', '2019-06-01', '22:50:00', '1', 'I enjoyed the flight.');

INSERT INTO purchase VALUES ('a11000100', 'hello@world.com', '2020-07-11', '07:06:05', '8000', 'credit card', '111177334444555', 'HELLO WORLD', '2025-04-01');


INSERT INTO flight VALUES ('China Eastern', '333', '2020-03-01', '22:50:00', '2020-03-02', '04:10:00', 'PVG', 'JFK', '4000', 'on-time', 'B-0000');
INSERT INTO flight VALUES ('China Eastern', '222', '2020-03-15', '09:50:00', '2020-03-15', '16:30:00', 'JFK', 'PVG', '6000', 'delayed', 'B-9999');
iNSERT INTO ticket VALUES ('a00000003', 'China Eastern', '333', '2020-03-01', '22:50:00');
INSERT INTO ticket VALUES ('a00000002', 'China Eastern', '222', '2020-03-15', '09:50:00');
INSERT INTO purchase VALUES ('a00000003', 'hello@world.com', '2020-04-11', '07:06:05', '8000', 'credit card', '111177334444555', 'HELLO WORLD', '2021-04-01');
INSERT INTO purchase VALUES ('a00000002', 'hello@world.com', '2020-04-11', '07:06:05', '8000', 'credit card', '111177334444555', 'HELLO WORLD', '2021-04-01');


INSERT INTO flight VALUES ('China Southern', '101', '2020-08-02', '19:40:00', '2020-08-03', '7:00:00', 'JFK', 'PVG', '7000', 'on-time', 'B-1111');
INSERT INTO flight VALUES ('China Southern', '777', '2020-08-02', '20:40:00', '2020-08-03', '7:00:00', 'JFK', 'PVG', '7000', 'on-time', 'B-1111');