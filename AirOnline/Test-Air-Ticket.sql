SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Test_Air_Ticket`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

CREATE TABLE `airline` (
  `airline_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`airline_name`) VALUES
('Air China');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff`
--

CREATE TABLE `airline_staff` (
  `user_name` varchar(50) NOT NULL,
  `airline_name` varchar(50) DEFAULT NULL,
  `password` varchar(100) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`user_name`, `airline_name`, `password`, `first_name`, `last_name`, `date_of_birth`) VALUES
('admin', 'Air China', 'e2fc714c4727ee9395f324cd2e7f331f', 'San', 'Zhang', '2000-01-01');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `airline_name` varchar(50) NOT NULL,
  `id` varchar(50) NOT NULL,
  `amount_of_seats` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airline_name`, `id`, `amount_of_seats`) VALUES
('Air China', '1', 4),
('Air China', '2', 4),
('Air China', '3', 50);

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `airport_name` varchar(50) NOT NULL,
  `city` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`airport_name`, `city`) VALUES
('BEI', 'Beijing'),
('BOS', 'Boston'),
('HKA', 'Hong Kong'),
('JFK', 'NYC'),
('LAX', 'Los Angles'),
('PVG', 'Shanghai'),
('SFO', 'San Francisco'),
('SHEN', 'Shenzhen');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `email` varchar(50) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `password` varchar(100) NOT NULL,
  `building_number` varchar(20) DEFAULT NULL,
  `street` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `phone_number` varchar(50) DEFAULT NULL,
  `passport_number` varchar(50) DEFAULT NULL,
  `passport_expiration` date DEFAULT NULL,
  `passport_country` varchar(50) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `name`, `password`, `building_number`, `street`, `city`, `state`, `phone_number`, `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES
('testcustomer@ruc.edu.cn', 'Test Customer 1', '81dc9bdb52d04dc20036dbd8313ed055', '5906', 'Zhongguancun Street', 'Haidian', 'Beijing', '123-4321-4321', '54321', '2025-12-24', 'China', '2000-01-02'),
('user1@ruc.edu.cn', 'User 1', '81dc9bdb52d04dc20036dbd8313ed055', '1555', 'Zhongguancun Street', 'Haidian', 'Beijing', '123-4322-4322', '54322', '2025-12-25', 'China', '2000-01-03'),
('user2@ruc.edu.cn', 'User 2', '81dc9bdb52d04dc20036dbd8313ed055', '1702', 'Zhongguancun Street', 'Haidian', 'Beijing', '123-4323-4323', '54324', '2025-10-24', 'China', '2000-01-04'),
('user3@ruc.edu.cn', 'User 3', '81dc9bdb52d04dc20036dbd8313ed055', '1890', 'Zhongguancun Street', 'Haidian', 'Beijing', '123-4324-4324', '54324', '2025-09-24', 'China', '2000-01-05');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `airline_name` varchar(50) NOT NULL,
  `flight_number` varchar(20) NOT NULL,
  `departure_date` date NOT NULL,
  `departure_time` time NOT NULL,
  `arrival_date` date DEFAULT NULL,
  `arrival_time` time DEFAULT NULL,
  `departure_airport` varchar(50) DEFAULT NULL,
  `arrival_airport` varchar(50) DEFAULT NULL,
  `base_price` float DEFAULT NULL,
  `status` varchar(20) DEFAULT 'on-time',
  `id` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`airline_name`, `flight_number`, `departure_date`, `departure_time`, `arrival_date`, `arrival_time`, `departure_airport`, `arrival_airport`, `base_price`, `status`, `id`) VALUES
('Air China', '102', '2021-01-12', '13:25:25', '2021-01-12', '16:50:25', 'SFO', 'LAX', 300, 'on-time', '3'),
('Air China', '104', '2021-02-12', '13:25:25', '2021-02-12', '16:50:25', 'PVG', 'BEI', 300, 'on-time', '3'),
('Air China', '106', '2021-03-12', '12:07:20', '2021-03-12', '16:50:25', 'SFO', 'LAX', 500, 'delayed', '2'),
('Air China', '134', '2020-11-12', '13:25:25', '2020-11-12', '16:50:25', 'JFK', 'BOS', 300, 'delayed', '3'),
('Air China', '206', '2020-12-12', '13:25:25', '2020-12-12', '16:50:25', 'SFO', 'LAX', 500, 'on-time', '2'),
('Air China', '207', '2020-10-12', '13:25:25', '2020-10-12', '16:50:25', 'LAX', 'SFO', 300, 'on-time', '2'),
('Air China', '296', '2021-04-01', '13:25:25', '2021-04-01', '16:50:25', 'PVG', 'SFO', 2000, 'on-time', '1'),
('Air China', '715', '2020-12-28', '10:25:25', '2020-12-28', '13:50:25', 'PVG', 'BEI', 500, 'delayed', '1'),
('Air China', '839', '2020-12-12', '13:25:25', '2020-12-12', '16:50:25', 'SHEN', 'BEI', 300, 'on-time', '3');

-- --------------------------------------------------------

--
-- Stand-in structure for view `flight_price`
-- (See below for the actual view)
--
CREATE TABLE `flight_price` (
`airline_name` varchar(50)
,`flight_number` varchar(20)
,`departure_date` date
,`departure_time` time
,`arrival_date` date
,`arrival_time` time
,`departure_airport` varchar(50)
,`arrival_airport` varchar(50)
,`price` double
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `flight_seats_sold`
-- (See below for the actual view)
--
CREATE TABLE `flight_seats_sold` (
`airline_name` varchar(50)
,`flight_number` varchar(20)
,`departure_date` date
,`departure_time` time
,`amount_of_seats` int(11)
,`tickets_sold` bigint(21)
);

-- --------------------------------------------------------

--
-- Table structure for table `purchase`
--

CREATE TABLE `purchase` (
  `ticket_id` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `purchase_date` date DEFAULT NULL,
  `purchase_time` time DEFAULT NULL,
  `sold_price` float NOT NULL,
  `card_type` varchar(50) DEFAULT NULL,
  `card_number` varchar(50) DEFAULT NULL,
  `name_on_card` varchar(50) DEFAULT NULL,
  `expiraton_date` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `purchase`
--

INSERT INTO `purchase` (`ticket_id`, `email`, `purchase_date`, `purchase_time`, `sold_price`, `card_type`, `card_number`, `name_on_card`, `expiraton_date`) VALUES
('1', 'testcustomer@ruc.edu.cn', '2020-12-12', '11:55:55', 300, 'credit card', '111-222-333-444', 'Test Customer 1', '2023-03'),
('2', 'user1@ruc.edu.cn', '2020-12-12', '11:55:55', 300, 'credit card', '1111-2222-3333-5555', 'User 1', '2023-03'),
('3', 'user2@ruc.edu.cn', '2020-12-12', '11:55:55', 300, 'credit card', '1111-2222-3333-5555', 'User 2', '2023-03'),
('4', 'user3@ruc.edu.cn', '2020-12-12', '11:55:55', 300, 'credit card', '1111-2222-3333-5555', 'User 3', '2023-03');

-- --------------------------------------------------------

--
-- Table structure for table `rates`
--

CREATE TABLE `rates` (
  `email` varchar(50) NOT NULL,
  `airline_name` varchar(50) NOT NULL,
  `flight_number` varchar(20) NOT NULL,
  `departure_date` date NOT NULL,
  `departure_time` time NOT NULL,
  `rating` int(11) DEFAULT NULL,
  `comments` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `rates`
--

INSERT INTO `rates` (`email`, `airline_name`, `flight_number`, `departure_date`, `departure_time`, `rating`, `comments`) VALUES
('testcustomer@ruc.edu.cn', 'Air China', '102', '2021-01-12', '13:25:25', 4, 'Very Comfortable'),
('testcustomer@ruc.edu.cn', 'Air China', '104', '2021-02-12', '13:25:25', 1, 'Customer Care services are not good'),
('user1@ruc.edu.cn', 'Air China', '102', '2021-01-12', '13:25:25', 5, 'Relaxing, check-in and onboarding very professional'),
('user1@ruc.edu.cn', 'Air China', '104', '2021-02-12', '13:25:25', 5, 'Comfortable journey and Professional'),
('user2@ruc.edu.cn', 'Air China', '102', '2021-01-12', '13:25:25', 3, 'Satisfies and will use the same flight again');

-- --------------------------------------------------------

--
-- Table structure for table `staff_phone`
--

CREATE TABLE `staff_phone` (
  `user_name` varchar(50) NOT NULL,
  `phone` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `staff_phone`
--

INSERT INTO `staff_phone` (`user_name`, `phone`) VALUES
('admin', '111-2222-3333'),
('admin', '444-5555-6666');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `ticket_id` varchar(50) NOT NULL,
  `airline_name` varchar(50) DEFAULT NULL,
  `flight_number` varchar(20) DEFAULT NULL,
  `departure_date` date DEFAULT NULL,
  `departure_time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_id`, `airline_name`, `flight_number`, `departure_date`, `departure_time`) VALUES
('1', 'Air China', '102', '2021-01-12', '13:25:25'),
('2', 'Air China', '102', '2021-01-12', '13:25:25'),
('3', 'Air China', '102', '2021-01-12', '13:25:25'),
('4', 'Air China', '102', '2021-01-12', '13:25:25')
-- --------------------------------------------------------

--
-- Structure for view `flight_price`
--
DROP TABLE IF EXISTS `flight_price`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `flight_price`  AS  select `flight`.`airline_name` AS `airline_name`,`flight`.`flight_number` AS `flight_number`,`flight`.`departure_date` AS `departure_date`,`flight`.`departure_time` AS `departure_time`,`flight`.`arrival_date` AS `arrival_date`,`flight`.`arrival_time` AS `arrival_time`,`flight`.`departure_airport` AS `departure_airport`,`flight`.`arrival_airport` AS `arrival_airport`,(case when (`flight_seats_sold`.`tickets_sold` >= (0.7 * `flight_seats_sold`.`amount_of_seats`)) then (`flight`.`base_price` * 1.2) else `flight`.`base_price` end) AS `price` from (`flight` left join `flight_seats_sold` on(((`flight`.`airline_name` = `flight_seats_sold`.`airline_name`) and (`flight`.`flight_number` = `flight_seats_sold`.`flight_number`) and (`flight`.`departure_date` = `flight_seats_sold`.`departure_date`) and (`flight`.`departure_time` = `flight_seats_sold`.`departure_time`)))) ;

-- --------------------------------------------------------

--
-- Structure for view `flight_seats_sold`
--
DROP TABLE IF EXISTS `flight_seats_sold`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `flight_seats_sold`  AS  select `flight`.`airline_name` AS `airline_name`,`flight`.`flight_number` AS `flight_number`,`flight`.`departure_date` AS `departure_date`,`flight`.`departure_time` AS `departure_time`,`airplane`.`amount_of_seats` AS `amount_of_seats`,count(`purchase`.`ticket_id`) AS `tickets_sold` from (((`flight` join `airplane` on(((`flight`.`airline_name` = `airplane`.`airline_name`) and (`flight`.`id` = `airplane`.`id`)))) join `ticket` on(((`flight`.`airline_name` = `ticket`.`airline_name`) and (`flight`.`flight_number` = `ticket`.`flight_number`) and (`flight`.`departure_date` = `ticket`.`departure_date`) and (`flight`.`departure_time` = `ticket`.`departure_time`)))) left join `purchase` on((`ticket`.`ticket_id` = `purchase`.`ticket_id`))) group by `flight`.`airline_name`,`flight`.`flight_number`,`flight`.`departure_date`,`flight`.`departure_time` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`airline_name`);

--
-- Indexes for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD PRIMARY KEY (`user_name`),
  ADD KEY `airline_name` (`airline_name`);

--
-- Indexes for table `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`airline_name`,`id`);

--
-- Indexes for table `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`airport_name`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`airline_name`,`flight_number`,`departure_date`,`departure_time`),
  ADD KEY `airline_name` (`airline_name`,`id`),
  ADD KEY `departure_airport` (`departure_airport`),
  ADD KEY `arrival_airport` (`arrival_airport`);

--
-- Indexes for table `purchase`
--
ALTER TABLE `purchase`
  ADD PRIMARY KEY (`ticket_id`,`email`),
  ADD KEY `email` (`email`);

--
-- Indexes for table `rates`
--
ALTER TABLE `rates`
  ADD PRIMARY KEY (`email`,`airline_name`,`flight_number`,`departure_date`,`departure_time`),
  ADD KEY `airline_name` (`airline_name`,`flight_number`,`departure_date`,`departure_time`);

--
-- Indexes for table `staff_phone`
--
ALTER TABLE `staff_phone`
  ADD PRIMARY KEY (`user_name`,`phone`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`ticket_id`),
  ADD KEY `airline_name` (`airline_name`,`flight_number`,`departure_date`,`departure_time`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD CONSTRAINT `airline_staff_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`) ON UPDATE CASCADE;

--
-- Constraints for table `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`) ON UPDATE CASCADE;

--
-- Constraints for table `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`) ON UPDATE CASCADE,
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`airline_name`,`id`) REFERENCES `airplane` (`airline_name`, `id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`departure_airport`) REFERENCES `airport` (`airport_name`) ON UPDATE CASCADE,
  ADD CONSTRAINT `flight_ibfk_4` FOREIGN KEY (`arrival_airport`) REFERENCES `airport` (`airport_name`) ON UPDATE CASCADE;

--
-- Constraints for table `purchase`
--
ALTER TABLE `purchase`
  ADD CONSTRAINT `purchase_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`ticket_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `purchase_ibfk_2` FOREIGN KEY (`email`) REFERENCES `customer` (`email`) ON UPDATE CASCADE;

--
-- Constraints for table `rates`
--
ALTER TABLE `rates`
  ADD CONSTRAINT `rates_ibfk_1` FOREIGN KEY (`email`) REFERENCES `customer` (`email`) ON UPDATE CASCADE,
  ADD CONSTRAINT `rates_ibfk_2` FOREIGN KEY (`airline_name`,`flight_number`,`departure_date`,`departure_time`) REFERENCES `flight` (`airline_name`, `flight_number`, `departure_date`, `departure_time`) ON UPDATE CASCADE;

--
-- Constraints for table `staff_phone`
--
ALTER TABLE `staff_phone`
  ADD CONSTRAINT `staff_phone_ibfk_1` FOREIGN KEY (`user_name`) REFERENCES `airline_staff` (`user_name`) ON UPDATE CASCADE;

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`airline_name`,`flight_number`,`departure_date`,`departure_time`) REFERENCES `flight` (`airline_name`, `flight_number`, `departure_date`, `departure_time`) ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
