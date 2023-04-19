-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.25-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.4.0.6659
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for fgs_db
CREATE DATABASE IF NOT EXISTS `fgs_db` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `fgs_db`;

-- Dumping structure for table fgs_db.tbl_datasets
CREATE TABLE IF NOT EXISTS `tbl_datasets` (
  `ds_id` int(11) NOT NULL AUTO_INCREMENT,
  `ds_name` varchar(150) NOT NULL,
  `ds_grade` text NOT NULL,
  `slug` text NOT NULL,
  `date_added` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`ds_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- Dumping data for table fgs_db.tbl_datasets: ~2 rows (approximately)
INSERT INTO `tbl_datasets` (`ds_id`, `ds_name`, `ds_grade`, `slug`, `date_added`) VALUES
	(2, 'rambutan', 'fresh', '/static/upload/fresh/rambutan_20230417163657.png', '2023-04-17 16:36:57'),
	(3, 'rambutan', 'rotten', '/static/upload/rotten/rambutan_20230417163706.jpg', '2023-04-17 16:37:06');

-- Dumping structure for table fgs_db.tbl_user
CREATE TABLE IF NOT EXISTS `tbl_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(150) DEFAULT NULL,
  `mname` varchar(150) DEFAULT NULL,
  `lname` varchar(150) DEFAULT NULL,
  `address` varchar(150) DEFAULT NULL,
  `username` varchar(150) DEFAULT NULL,
  `password` varchar(150) DEFAULT NULL,
  `category` varchar(150) DEFAULT NULL,
  `date_added` datetime DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `username` (`username`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

-- Dumping data for table fgs_db.tbl_user: ~2 rows (approximately)
INSERT INTO `tbl_user` (`id`, `fname`, `mname`, `lname`, `address`, `username`, `password`, `category`, `date_added`) VALUES
	(1, 'Eduard RIno', 'Questo', 'Carton', NULL, 'jag', 'sha256$srhW5avnCjLm7Tkj$0502c352f2f30fa5dfb8111d4c3e72b7c13d9f3da7f76bb3d72aabd5ba97977f', 'Admin', '2022-12-02 13:43:09'),
	(3, 'Jagwarthegreat', 'Questo', 'Carton', NULL, 'rin', 'sha256$srhW5avnCjLm7Tkj$0502c352f2f30fa5dfb8111d4c3e72b7c13d9f3da7f76bb3d72aabd5ba97977f', 'Admin', '2022-11-25 16:29:56');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
