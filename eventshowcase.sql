-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 24, 2023 at 11:32 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `eventshowcase`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(10) NOT NULL,
  `password` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'kits');

-- --------------------------------------------------------

--
-- Table structure for table `event`
--

CREATE TABLE `event` (
  `e_id` int(4) NOT NULL,
  `event_name` varchar(50) NOT NULL,
  `event_organizer` varchar(30) NOT NULL,
  `event_type` varchar(15) NOT NULL,
  `venue` varchar(20) NOT NULL,
  `age_restriction` varchar(2) DEFAULT NULL,
  `description` varchar(200) NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `capacity` int(4) NOT NULL,
  `cost` int(4) DEFAULT NULL,
  `org_email` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `event`
--

INSERT INTO `event` (`e_id`, `event_name`, `event_organizer`, `event_type`, `venue`, `age_restriction`, `description`, `date`, `time`, `capacity`, `cost`, `org_email`) VALUES
(6, 'Test', 'KITS', 'educational', 'Singapur', '0', ' A test event in KITS', '2023-03-30', '10:00:00', 135, 0, 'kavya@gmail.com'),
(8, 'Kitsozen', 'KCA', 'entertainment', 'KITS', '0', 'celebrating 25 years of KITS establishment', '2023-03-15', '11:00:00', 1500, 50, 'lgargeya@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `event_register`
--

CREATE TABLE `event_register` (
  `email` varchar(30) NOT NULL,
  `e_id` int(2) NOT NULL,
  `org_email` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `event_type`
--

CREATE TABLE `event_type` (
  `type_id` int(1) NOT NULL,
  `type` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `event_type`
--

INSERT INTO `event_type` (`type_id`, `type`) VALUES
(1, 'business'),
(2, 'sports'),
(3, 'cultural_arts'),
(4, 'religious'),
(5, 'entertainment'),
(6, 'educational'),
(7, 'charity');

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `sl_no` int(3) NOT NULL,
  `email` varchar(20) NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `city` varchar(20) NOT NULL,
  `subject` varchar(30) NOT NULL,
  `message` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`sl_no`, `email`, `mobile`, `city`, `subject`, `message`) VALUES
(1, 'lgargeya@gmail.com', '7569439117', 'Hanamkonda', 'Test', 'Test'),
(2, 'lgargeya@gmail.com', '7569439117', 'Hanamkonda', 'Test', 'Test for admin'),
(4, 'vashista@gmail.com', '9440514770', 'manthani', 'test contact', 'sent hello'),
(5, 'lgargeya@gmail.com', '0756943911', 'Hanamkonda', 'Test in index1', 'GOMU GOMU NO');

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `email` varchar(30) NOT NULL,
  `creditcardnum` bigint(12) NOT NULL,
  `cvv` int(3) NOT NULL,
  `expiry_month` varchar(2) NOT NULL,
  `expiry_year` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`email`, `creditcardnum`, `cvv`, `expiry_month`, `expiry_year`) VALUES
('geetika@gmail.com', 254698741235, 505, '12', '26');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `email` varchar(40) NOT NULL,
  `password` varchar(15) NOT NULL,
  `nationality` varchar(15) DEFAULT NULL,
  `gender` varchar(6) NOT NULL,
  `usertype` varchar(12) NOT NULL,
  `dob` date NOT NULL,
  `State_ID` varchar(12) NOT NULL,
  `age` int(3) DEFAULT NULL,
  `isActive` int(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`email`, `password`, `nationality`, `gender`, `usertype`, `dob`, `State_ID`, `age`, `isActive`) VALUES
('kavyasriyada@gmail.com', '12345678', 'Indian', 'female', 'attendee', '2002-04-17', '847938827686', 20, 1),
('lgargeya@gmail.com', '12345678', 'Indian', 'male', 'eventmanager', '2001-05-21', '289805138939', 21, 1),
('nikitareddy@gmail.com', '12345678', 'Indian', 'female', 'eventmanager', '2001-01-06', '551137216469', 22, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`e_id`);

--
-- Indexes for table `event_type`
--
ALTER TABLE `event_type`
  ADD PRIMARY KEY (`type_id`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`sl_no`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `event`
--
ALTER TABLE `event`
  MODIFY `e_id` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `event_type`
--
ALTER TABLE `event_type`
  MODIFY `type_id` int(1) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `sl_no` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
