-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 13, 2014 at 11:07 PM
-- Server version: 5.5.35-1ubuntu1
-- PHP Version: 5.5.9-1ubuntu4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `shopguru`
--

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE IF NOT EXISTS `customer` (
  `phone` bigint(11) unsigned NOT NULL,
  `name` varchar(25) NOT NULL COMMENT 'customer name',
  `reg_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'customer registration timestamp',
  `latitude` decimal(9,6) unsigned DEFAULT NULL COMMENT 'last known latitude of customer',
  `longitude` decimal(9,6) unsigned DEFAULT NULL COMMENT 'last known longitude of customer',
  PRIMARY KEY (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='registered customer list';

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`phone`, `name`, `reg_time`, `latitude`, `longitude`) VALUES
(94771000000, 'Nuran Arachchi', '2014-08-15 01:35:23', 5.230000, 89.770000),
(94771122336, 'Janaka Bandara', '2014-09-11 03:47:01', 6.916700, 79.833300),
(94771122420, 'saman kumara', '2014-09-12 06:43:59', 7.468974, 80.302307),
(94771122421, 'saman kumara', '2014-09-12 06:34:29', 7.468974, 80.302307),
(94771122436, 'Fishy Tuna', '2014-09-11 05:04:21', 6.790456, 79.897250),
(94771142336, 'Dhanushka', '2014-09-13 04:25:55', 7.294981, 79.872753);

-- --------------------------------------------------------

--
-- Table structure for table `incoming_sms`
--

CREATE TABLE IF NOT EXISTS `incoming_sms` (
  `msg_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'unique entry ID',
  `sender` bigint(11) unsigned NOT NULL COMMENT 'sender''s phone number',
  `receive_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'message received time',
  `content` varchar(160) NOT NULL COMMENT 'message text',
  PRIMARY KEY (`msg_id`),
  KEY `sender` (`sender`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='incoming message log' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `outgoing_sms`
--

CREATE TABLE IF NOT EXISTS `outgoing_sms` (
  `msg_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'unique entry ID',
  `receiver` bigint(11) unsigned NOT NULL COMMENT 'receiver''s phone number',
  `send_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'message sent time',
  `content` varchar(160) NOT NULL COMMENT 'message text',
  PRIMARY KEY (`msg_id`),
  KEY `sender` (`receiver`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='outgoing message log' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `shop`
--

CREATE TABLE IF NOT EXISTS `shop` (
  `phone` bigint(11) unsigned NOT NULL,
  `name` varchar(25) NOT NULL COMMENT 'customer name',
  `address` varchar(50) DEFAULT NULL COMMENT 'address of shop',
  `category` varchar(25) NOT NULL COMMENT 'category of shop (e.g. pharmacy, hardware)',
  `reg_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'customer registration timestamp',
  `latitude` decimal(9,6) unsigned DEFAULT NULL COMMENT 'last known latitude of customer',
  `longitude` decimal(9,6) unsigned DEFAULT NULL COMMENT 'last known longitude of customer',
  `status` varchar(140) DEFAULT NULL COMMENT 'status of shop',
  `last_update` timestamp NULL DEFAULT NULL COMMENT 'time of last shop status update',
  `lifetime` tinyint(4) NOT NULL DEFAULT '24' COMMENT 'lifetime of a status update in hours',
  PRIMARY KEY (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='registered customer list';

--
-- Dumping data for table `shop`
--

INSERT INTO `shop` (`phone`, `name`, `address`, `category`, `reg_time`, `latitude`, `longitude`, `status`, `last_update`, `lifetime`) VALUES
(94771122332, 'Amila Hardware', '187/17, Anandarama Road, Katubedda', 'hardware', '2014-08-15 04:24:10', 5.230000, 89.770000, 'closed from 1pm to 2pm', '2014-09-02 18:30:00', 24),
(94771122411, 'wickrama stores', 'uhumeeya, kurunegala', 'grocery, bakery', '2014-09-12 05:27:36', 7.519004, 80.266982, '', NULL, 0),
(94771142336, 'Dhanu Bera Kade', 'Molpe, Moratuwa', 'instruments', '2014-09-13 04:27:47', 6.792238, 79.901078, '', '0000-00-00 00:00:00', 0);

-- --------------------------------------------------------

--
-- Table structure for table `subscription`
--

CREATE TABLE IF NOT EXISTS `subscription` (
  `cust_phone` bigint(11) unsigned NOT NULL COMMENT 'customer''s phone number',
  `shop_phone` bigint(11) unsigned NOT NULL COMMENT 'shop''s phone number',
  `start_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_query` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`cust_phone`,`shop_phone`),
  KEY `subscription_shop` (`shop_phone`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='shops tracked by customers';

--
-- Dumping data for table `subscription`
--

INSERT INTO `subscription` (`cust_phone`, `shop_phone`, `start_time`, `last_query`) VALUES
(94771122336, 94771122332, '2014-09-12 04:29:50', NULL),
(94771122336, 94771122411, '2014-09-12 08:46:39', NULL),
(94771122336, 94771142336, '2014-09-13 12:00:03', NULL),
(94771122420, 94771122411, '2014-09-13 08:17:16', NULL),
(94771122420, 94771142336, '2014-09-13 08:18:54', NULL);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `subscription`
--
ALTER TABLE `subscription`
  ADD CONSTRAINT `subscription_customer` FOREIGN KEY (`cust_phone`) REFERENCES `customer` (`phone`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `subscription_shop` FOREIGN KEY (`shop_phone`) REFERENCES `shop` (`phone`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
