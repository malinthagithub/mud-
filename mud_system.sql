-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 13, 2026 at 05:43 AM
-- Server version: 10.11.16-MariaDB
-- PHP Version: 8.3.36

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mud_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `imports`
--

CREATE TABLE `imports` (
  `id` int(11) NOT NULL,
  `entry_no` varchar(30) DEFAULT NULL,
  `item_no` int(11) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `hs_code` varchar(20) DEFAULT NULL,
  `description` varchar(120) DEFAULT NULL,
  `unit` varchar(20) DEFAULT NULL,
  `imported_qty` float DEFAULT NULL,
  `opening_balance` float DEFAULT NULL,
  `note` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `imports`
--

INSERT INTO `imports` (`id`, `entry_no`, `item_no`, `year`, `date`, `hs_code`, `description`, `unit`, `imported_qty`, `opening_balance`, `note`) VALUES
(1, 'H 3232', 1, 2026, '2026-02-18', '48191000', 'Corrugated Cartons', 'Nos', 24436, 24436, 'Balance in file (33027) > imported qty - capped'),
(2, 'H 5172', 1, 2026, '2026-06-24', '48191000', 'Corrugated Cartons', 'Nos', 12525, 955, ''),
(3, 'H 5922', 1, 2026, '2026-07-17', '48191000', 'Corrugated Cartons', 'Nos', 49030, 1840, ''),
(4, 'H 10881', 1, 2026, '2026-07-07', '48191000', 'Corrugated Cartons', 'Nos', 6630, 1133, ''),
(5, 'H 6306', 1, 2026, '2026-07-27', '48191000', 'Corrugated Cartons', 'Nos', 10957, 4530, ''),
(6, 'H 6307', 1, 2026, '2026-07-27', '48191000', 'Corrugated Cartons', 'Nos', 2200, 2200, ''),
(7, 'H 8535', 1, 2026, '2026-10-05', '48191000', 'Corrugated Cartons', 'Nos', 20656, 6154, ''),
(8, 'H 8954', 1, 2026, '2026-10-14', '48191000', 'Corrugated Cartons', 'Nos', 61990, 49937, ''),
(9, 'H 8123', 1, 2026, '2026-09-18', '48191000', 'Corrugated Cartons', 'Nos', 69420, 69420, 'Balance in file (694200) > imported qty - capped'),
(10, 'H 10406', 1, 2026, '2026-06-25', '48192000', 'Tea Cartons', 'Nos', 86175, 25411, 'Stock +10000 on 2026-11-12'),
(11, 'H 3804', 1, 2026, '2026-05-12', '39201090', 'Stretch Films', 'Kgs', 480.86, 221.01, ''),
(12, 'H 3805', 1, 2026, '2026-05-12', '39201090', 'Stretch Films', 'Kgs', 494.2, 494.2, 'Balance in file (494.29) > imported qty - capped'),
(13, 'H 5652', 1, 2026, '2026-07-08', '39201090', 'Stretch Films', 'Kgs', 444, 444, ''),
(14, 'H 6983', 1, 2026, '2026-08-17', '39202010', 'Bopp Cut Sheet', 'Pcs', 1257000, 1220420, ''),
(15, 'H 7969', 1, 2026, '2026-09-11', '39202010', 'Bopp Cut Sheet', 'Pcs', 18670000, 1867000, ''),
(16, 'H 19512', 1, 2025, '2025-12-11', '39232990', 'Laminating Pouch', 'Nos', 10249200, 7032390, ''),
(17, 'H 1575', 1, 2026, '2026-01-23', '39232990', 'Laminating Pouch', 'Nos', 10035800, 9680550, ''),
(18, 'H 2999', 1, 2026, '2026-02-12', '39232990', 'Laminating Pouch', 'Nos', 6859650, 6859650, ''),
(19, 'H 6034', 1, 2026, '2026-03-31', '39232990', 'Laminating Pouch', 'Nos', 4913940, 443740, ''),
(20, 'H 6072', 1, 2026, '2026-03-31', '39232990', 'Laminating Pouch', 'Kgs', 15666000, 15666000, ''),
(21, 'H 8069', 1, 2026, '2026-05-19', '39232990', 'Laminating Pouch', 'Pcs', 15666000, 15666000, ''),
(22, 'H 11002', 1, 2026, '2026-07-09', '39232990', 'Laminating Pouch', 'Kgs', 12784, 12784, ''),
(23, 'H 11794', 1, 2026, '2026-07-22', '39232990', 'Laminating Pouch', 'Nos', 2175830, 2175830, ''),
(24, 'S 14929', 1, 2026, '2026-09-09', '39232990', 'Empty Pouch', 'Pcs', 13000, 10500, ''),
(25, 'S 14936', 1, 2026, '2026-09-09', '39232990', 'Empty Pouch', 'Pcs', 12000, 12000, ''),
(26, 'H 6881', 1, 2026, '2026-08-13', '39232190', 'Poly Bags', 'Kgs', 480.5, 414.5, ''),
(27, 'H 11794', 2, 2026, '2026-07-22', '39232190', 'Poly Bags', 'Nos', 7400, 7400, ''),
(28, 'H 8851', 1, 2026, '2026-10-12', '39232190', 'Poly Bags', 'Pcs', 134850, 134850, ''),
(29, 'H 8850', 1, 2026, '2026-10-12', '39232190', 'Poly Bags', 'Kgs', 480.2, 480.2, ''),
(30, 'H 8849', 1, 2026, '2026-10-12', '39232190', 'Poly Bags', 'Pcs', 151700, 151700, ''),
(31, 'H 8848', 1, 2026, '2026-10-12', '39232190', 'Poly Bags', 'Pcs', 80000, 80000, ''),
(32, 'H 8847', 1, 2026, '2026-10-12', '39232190', 'Poly Bags', 'Pcs', 36200, 36200, ''),
(33, 'H 5222', 1, 2026, '2026-03-20', '48211090', 'Tea Bags Tags', 'Nos', 27158000, 1755310, ''),
(34, 'H 10088', 1, 2026, '2026-06-20', '48211090', 'Tea Bags Tags', 'Nos', 47233200, 1135960, ''),
(35, 'H 5887', 1, 2026, '2026-07-16', '48211090', 'Tea Bags Tags', 'Nos', 19193500, 90537, ''),
(36, 'H 10087', 1, 2026, '2026-06-20', '48211090', 'Tea Bags Tags', 'Nos', 26285000, 17258200, ''),
(37, 'H 7534', 1, 2026, '2026-09-02', '48211090', 'Tea Bags Tags', 'Nos', 15040000, 3759020, ''),
(38, 'H 7539', 1, 2026, '2026-09-02', '48171000', 'Envelopes', 'Nos', 10399500, 5437620, ''),
(39, 'H 7584', 1, 2023, '2023-06-11', '39191000', 'Adhesive Tape', 'Nos', 2000, 744.51, ''),
(40, 'H 10081', 1, 2024, '2024-12-04', '39191000', 'Adhesive Tape', 'Nos', 7000, 5543.91, ''),
(41, 'H 10545', 1, 2024, '2024-12-17', '39191000', 'Adhesive Tape', 'Nos', 4000, 895.15, ''),
(42, 'H 10078', 1, 2024, '2024-12-04', '39191000', 'Adhesive Tape', 'Nos', 11500, 11500, ''),
(43, 'H 10077', 1, 2024, '2024-12-04', '39191000', 'Adhesive Tape', 'Nos', 2998, 2998, ''),
(44, 'H 10076', 1, 2024, '2024-12-04', '39191000', 'Adhesive Tape', 'Nos', 3820, 3820, ''),
(45, 'H 10075', 1, 2024, '2024-12-04', '39191000', 'Adhesive Tape', 'Nos', 14000, 14000, ''),
(46, 'H 244', 1, 2025, '2025-01-09', '39191000', 'Adhesive Tape', 'Nos', 2000, 2000, ''),
(47, 'H 1217', 1, 2025, '2025-02-07', '39191000', 'Adhesive Tape', 'Nos', 2000, 2000, ''),
(48, 'H 1985', 1, 2025, '2025-03-04', '39191000', 'Adhesive Tape', 'Nos', 13957, 13957, ''),
(49, 'H 1984', 1, 2025, '2025-03-04', '39191000', 'Adhesive Tape', 'Nos', 6043, 6043, ''),
(50, 'H 4074', 1, 2025, '2025-05-19', '39191000', 'Adhesive Tape', 'Nos', 2000, 2000, ''),
(51, 'H 4431', 1, 2025, '2025-05-29', '39191000', 'Adhesive Tape', 'Nos', 2000, 2000, ''),
(52, 'H 6946', 1, 2025, '2025-08-06', '39191000', 'Adhesive Tape', 'Kgs', 269, 269, ''),
(53, 'H 11020', 1, 2025, '2025-12-17', '39191000', 'Adhesive Tape', 'Nos', 2000, 2000, ''),
(54, 'H 2059', 1, 2026, '2026-06-03', '39191000', 'Adhesive Tape', 'Nos', 5000, 5000, ''),
(55, 'H 2060', 1, 2026, '2026-06-03', '39191000', 'Adhesive Tape', 'Nos', 2000, 2000, ''),
(56, 'H 1442', 1, 2026, '2026-02-13', '48114199', 'Adhesive Tape', 'Nos', 15, 15, ''),
(57, 'H 6717', 1, 2026, '2026-08-06', '39191000', 'Adhesive Tape', 'Roll', 4000, 4000, ''),
(58, 'H 7490', 1, 2026, '2026-09-01', '39191000', 'Adhesive Tape', 'Roll', 5000, 5000, ''),
(59, 'H 7491', 1, 2026, '2026-09-01', '39191000', 'Adhesive Tape', 'Roll', 3000, 3000, ''),
(60, 'H 8497', 1, 2026, '2026-10-01', '39191000', 'Adhesive Tape', 'Roll', 2000, 2000, ''),
(61, 'S 672', 1, 2026, '2026-01-12', '39199090', 'Tear Tape', 'Reels', 300, 300, ''),
(62, 'S 11305', 1, 2026, '2026-07-06', '39199090', 'Tear Tape', 'Reels', 300, 300, ''),
(63, 'H 2060', 2, 2026, '2026-06-03', '48114199', 'Tear Tape', 'Roll', 30, 30, ''),
(64, 'S 4819', 1, 2026, '2026-03-16', '12119090', 'Dried Herbs', 'Kgs', 600, 83.44, ''),
(65, 'S 4820', 1, 2026, '2026-03-16', '12119090', 'Dried Herbs', 'Kgs', 52, 52, ''),
(66, 'S 4844', 1, 2026, '2026-03-17', '12119090', 'Dried Herbs', 'Kgs', 100, 100, ''),
(67, 'S 7395', 1, 2026, '2026-04-29', '12119090', 'Dried Herbs', 'Kgs', 9000, 1586.12, ''),
(68, 'S 9285', 1, 2026, '2026-05-29', '12119090', 'Herbs', 'Kgs', 500, 500, ''),
(69, 'H 5086', 1, 2026, '2026-06-22', '12119090', 'Chamomile Whole Flowers', 'Kgs', 24.55, 24.55, ''),
(70, 'H 5087', 2, 2026, '2026-06-22', '12119090', 'Flowers', 'Kgs', 220, 25.91, ''),
(71, 'S 12423', 3, 2026, '2026-07-21', '8134090', 'Dried Fruit - Roship Coarse', 'Kgs', 200, 190.75, ''),
(72, 'S 12633', 1, 2026, '2026-07-27', '12119090', 'Herbs', 'Kgs', 2860, 248.36, ''),
(73, 'H 6326', 2, 2026, '2026-07-28', '08134090', 'Fruits', 'Kgs', 70, 53.23, ''),
(74, 'S 15090', 1, 2026, '2026-09-11', '12119090', 'Roobios & Organic Roobios', 'Kgs', 9000, 5079.45, ''),
(75, 'S 15960', 1, 2026, '2026-09-28', '8134090', 'Dried Herbs Raspberry Straw', 'Kgs', 300, 11.35, ''),
(76, 'S 15960', 2, 2026, '2026-09-28', '8134090', 'Dried Fruit - Apple Pieces', 'Kgs', 108, 108, ''),
(77, 'S 15960', 3, 2026, '2026-09-28', '12119090', 'Dried Herbs - Peppermint Coars', 'Kgs', 2500, 2500, ''),
(78, 'H 8949', 1, 2026, '2026-10-14', '12119090', 'Herbs', 'Kgs', 7, 7, ''),
(79, 'H 8893', 1, 2026, '2026-10-13', '12119090', 'Herbs', 'Kgs', 6, 6, ''),
(80, 'S 16247', 1, 2026, '2026-10-01', '12119090', 'Herbs', 'Kgs', 186, 186, ''),
(81, 'S 11938', 1, 2026, '2026-07-14', '21069031', 'Tea Flavours', 'Kgs', 250, 36.38, ''),
(82, 'S 12945', 1, 2026, '2026-07-23', '21069031', 'Tea Flavours', 'Kgs', 145, 145, ''),
(83, 'S 12633', 2, 2026, '2026-07-27', '33021090', 'Tea Flavours', 'Ltrs', 500, 24.22, ''),
(84, 'H 4499', 1, 2026, '2026-06-01', '21069031', 'Tea Flavours', 'Kgs', 225, 19.43, ''),
(85, 'S 13852', 1, 2026, '2026-08-19', '33021010', 'Tea Flavours', 'Ltrs', 75, 19.79, ''),
(86, 'S 16183', 1, 2026, '2026-10-01', '21069031', 'Tea Flavours', 'Kgs', 940.5, 917.03, ''),
(87, 'S 16906', 1, 2026, '2026-10-14', '21069031', 'Tea Flavours', 'Kgs', 200, 200, ''),
(88, 'S 16357', 1, 2026, '2026-10-05', '21069031', 'Tea Flavours', 'Kgs', 100, 100, ''),
(89, 'S 13846', 1, 2026, '2026-08-19', '35069190', 'Adhesive Gum', 'Kgs', 4000, 1061.85, ''),
(90, 'S 8011', 1, 2026, '2026-05-08', '48054010', 'Filter Papers', 'Kgs', 13350, 592.49, ''),
(91, 'S 9626', 1, 2026, '2026-06-04', '48232010', 'Filter Papers', 'Kgs', 11423, 172.21, ''),
(92, 'S 15084', 1, 2026, '2026-09-11', '48232010', 'Filter Papers', 'Kgs', 11565, 7862.53, ''),
(93, 'S 16248', 1, 2026, '2026-10-01', '48232010', 'Filter Papers', 'Kgs', 200, 200, ''),
(94, 'H 6982', 1, 2026, '2026-08-17', '39201010', 'Bopp Films', 'Kgs', 3069.7, 1190.54, ''),
(95, 'H 7968', 1, 2026, '2026-09-11', '39202010', 'Bopp Films', 'Kgs', 1956.75, 1956.75, ''),
(96, 'S 5369', 1, 2026, '2026-03-25', '52054200', 'Threads', 'Kgs', 1092, 85.21, ''),
(97, 'S 15508', 1, 2026, '2026-09-17', '52054200', 'Threads', 'Kgs', 640.8, 322.19, ''),
(98, 'S 15719', 1, 2026, '2026-09-23', '52054200', 'Threads', 'Kgs', 384.48, 384.48, 'Balance in file (684.48) > imported qty - capped'),
(99, 'S 17007', 1, 2026, '2026-10-16', '52054200', 'Threads', 'Kgs', 897.12, 897.12, ''),
(100, 'S 14994', 1, 2026, '2026-09-10', '76052900', 'Alu Wire', 'Kgs', 648, 7.35, ''),
(101, 'H 463', 1, 2026, '2026-01-07', '73102990', 'Empty Tins', 'Pcs', 11554, 4888, ''),
(102, 'H 465', 1, 2026, '2026-01-07', '73102990', 'Empty Tins', 'Pcs', 10500, 10500, ''),
(103, 'S 13243', 1, 2026, '2026-08-07', '73102990', 'Empty Tins', 'Pcs', 57736, 20968, ''),
(104, 'S 14099', 1, 2026, '2026-08-25', '73102990', 'Empty Tins', 'Pcs', 32040, 31213, ''),
(105, 'S 15364', 1, 2026, '2026-09-16', '73102990', 'Empty Tins', 'Pcs', 20688, 20688, ''),
(106, 'S 9780', 1, 2026, '2026-06-08', '39199090', 'Holographic Label', 'Pcs', 2500000, 34024, ''),
(107, 'S 17051', 2, 2024, '2023-07-08', '9022099', 'China Green Tea', 'Kgs', 800, 455.38, ''),
(108, 'S 930', 1, 2024, '2024-09-01', '9022099', 'China Green Tea', 'Kgs', 5525, 789.89, ''),
(109, 'S 930', 2, 2024, '2024-09-01', '9024099', 'Oolong Tea', 'Kgs', 780, 155.63, ''),
(110, 'S 13253', 1, 2024, '2024-05-13', '9022099', 'China Green Tea', 'Kgs', 5725, 2.26, ''),
(111, 'S 13253', 2, 2024, '2024-05-13', '9024099', 'Oolong Tea', 'Kgs', 1100, 16.86, ''),
(112, 'S 21869', 1, 2024, '2024-08-06', '9022099', 'China Green Tea', 'Kgs', 2805, 103.72, ''),
(113, 'S 21869', 2, 2024, '2024-08-06', '9024099', 'Oolong Tea', 'Kgs', 860, 9.7, ''),
(114, 'S 35361', 1, 2024, '2024-12-10', '9022099', 'China Green Tea', 'Kgs', 40, 40, ''),
(115, 'S 3983', 1, 2025, '2025-02-10', '9022099', 'China Green Tea', 'Kgs', 4335, 222.02, ''),
(116, 'S 3983', 2, 2025, '2025-02-10', '9024099', 'Oolong Tea', 'Kgs', 1135, 5.2, ''),
(117, 'S 11162', 1, 2025, '2025-04-22', '9022099', 'China White Tea', 'Kgs', 2860, 15.81, ''),
(118, 'S 13380', 1, 2025, '2025-05-16', '9024099', 'Oolong Tea', 'Kgs', 300, 17, ''),
(119, 'S 15045', 1, 2025, '2025-06-03', '9024099', 'China Green Tea', 'Kgs', 300, 300, ''),
(120, 'S 17470', 2, 2025, '2025-07-01', '9022099', 'China Green Tea', 'Kgs', 900, 600, ''),
(121, 'S 24051', 1, 2025, '2025-09-16', '9022099', 'China Green Tea', 'Kgs', 5515, 186.98, ''),
(122, 'S 24051', 2, 2025, '2025-09-16', '9024099', 'Oolong Tea', 'Kgs', 930, 930, ''),
(123, 'S 25770', 2, 2025, '2025-10-08', '9022099', 'China Green Tea', 'Kgs', 2000, 243.64, ''),
(124, 'S 30624', 1, 2025, '2025-12-08', '9022099', 'China Green Tea', 'Kgs', 4595, 1479.04, ''),
(125, 'S 30624', 2, 2025, '2025-12-08', '9022099', 'Oolong Tea', 'Kgs', 500, 500, ''),
(126, 'S 22173', 1, 2025, '2025-08-25', '9024099', 'Oolong Tea', 'Kgs', 300, 300, ''),
(127, 'S 3524', 1, 2026, '2026-02-23', '9022099', 'China Green Tea', 'Kgs', 6000, 3083.35, ''),
(128, 'S 3524', 2, 2026, '2026-02-23', '9024099', 'White Tea', 'Kgs', 50, 50, ''),
(129, 'S 4670', 1, 2026, '2026-03-13', '9024099', 'Oolong Tea', 'Kgs', 2400, 1143.35, ''),
(130, 'S 4670', 2, 2026, '2026-03-13', '9022099', 'China Green Tea', 'Kgs', 1000, 1000, ''),
(131, 'S 9919', 1, 2026, '2026-06-09', '9024099', 'Oolong Tea', 'Kgs', 2000, 1524.75, ''),
(132, 'S 9919', 2, 2026, '2026-06-09', '9022099', 'China Green Tea', 'Kgs', 3000, 689.48, ''),
(133, 'S 10636', 1, 2026, '2026-06-23', '9022099', 'China Green Tea', 'Kgs', 5385, 5385, ''),
(134, 'S 10636', 2, 2026, '2026-06-23', '9024099', 'Oolong Tea', 'Kgs', 99, 99, ''),
(135, 'S 25627', 1, 2025, '2025-10-07', '9024099', 'Darjeeling Tea', 'Kgs', 5000, 1652, ''),
(136, 'S 4961', 1, 2026, '2026-03-18', '9024099', 'Darjeeling Tea', 'Kgs', 2500, 89.49, ''),
(137, 'S 35861', 1, 2024, '2024-12-10', '9022099', 'Macha Granule', 'Kgs', 40, 40, ''),
(138, 'S 6766', 1, 2025, '2025-03-10', '9024099', 'Assam Tea', 'Kgs', 160, 14.8, ''),
(139, 'S 30493', 2, 2025, '2025-12-06', '9024099', 'Assam Tea', 'Kgs', 20, 20, ''),
(140, 'S 11965', 1, 2026, '2026-07-14', '9024099', 'Assam Tea', 'Kgs', 150, 150, ''),
(141, 'S 9189', 1, 2025, '2025-02-04', '39232990', 'PP Woven Bags (IBG)', 'Pcs', 25020, 2871, ''),
(142, 'S 24664', 1, 2025, '2025-09-24', '39232990', 'PP Woven Bags', 'Pcs', 5000, 5000, ''),
(143, 'S 24396', 1, 2025, '2025-09-22', '70134900', 'Glass Cup', 'Pcs', 24000, 23000, ''),
(144, 'S 25196', 1, 2025, '2025-09-30', '66011000', 'Beach Umbrella', 'Pcs', 1400, 1040, ''),
(145, 'S 16639', 1, 2026, '2026-10-09', '66011000', 'Beach Umbrella - IBG', 'Pcs', 1000, 1000, ''),
(146, 'S 16639', 2, 2026, '2026-10-09', '66039000', 'Umbrella Base', 'Pcs', 500, 500, ''),
(147, 'S 30698', 1, 2025, '2025-12-08', '61099000', 'T - Shirts - Layalina', 'Pcs', 10274, 8924, ''),
(148, 'S 11250', 1, 2026, '2026-07-06', '48194010', 'Kraft Paper Bags', 'Pcs', 10000, 10000, ''),
(149, 'H 9906', 1, 2026, '2026-06-15', '44151000', 'Wooden Boxes', 'Nos', 20, 20, ''),
(150, 'H 9898', 1, 2026, '2026-06-15', '44151000', 'Wooden Boxes', 'Nos', 187, 187, ''),
(151, 'H 9893', 1, 2026, '2026-06-15', '44151000', 'Wooden Boxes', 'Nos', 228, 228, ''),
(152, 'H 9919', 1, 2026, '2026-06-15', '44151000', 'Wooden Boxes', 'Nos', 80, 80, ''),
(153, 'H 5764', 1, 2026, '2026-03-26', '44151000', 'Wooden Boxes', 'Nos', 5, 5, ''),
(154, 'H 5765', 1, 2026, '2026-03-26', '44151000', 'Wooden Boxes', 'Nos', 96, 96, ''),
(155, 'H 13070', 1, 2026, '2026-08-14', '44151000', 'Wooden Boxes', 'Nos', 550, 550, '');

-- --------------------------------------------------------

--
-- Table structure for table `ledger`
--

CREATE TABLE `ledger` (
  `id` int(11) NOT NULL,
  `import_id` int(11) DEFAULT NULL,
  `shipment_id` int(11) DEFAULT NULL,
  `line_id` int(11) DEFAULT NULL,
  `qty` float DEFAULT NULL,
  `created` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ledger`
--

INSERT INTO `ledger` (`id`, `import_id`, `shipment_id`, `line_id`, `qty`, `created`) VALUES
(1, 14, 4, 48, 22800, '2026-11-05 17:28:58'),
(2, 10, 4, 49, 15411, '2026-11-05 17:28:58'),
(3, 16, 4, 50, 28636, '2026-11-05 17:28:58'),
(4, 84, 4, 51, 10.36, '2026-11-05 17:28:58'),
(5, 1, 4, 52, 2488, '2026-11-05 17:28:58'),
(6, 64, 4, 53, 12.72, '2026-11-05 17:28:58'),
(7, 106, 4, 54, 14392, '2026-11-05 17:28:58'),
(8, 39, 4, 55, 37.12, '2026-11-05 17:28:58'),
(9, 71, 4, 56, 8, '2026-11-05 17:28:58'),
(10, 90, 4, 57, 142.726, '2026-11-05 17:28:58'),
(11, 96, 4, 58, 6.1658, '2026-11-05 17:28:58'),
(12, 100, 4, 59, 7.35, '2026-11-05 17:28:58'),
(13, 33, 4, 60, 770720, '2026-11-05 17:28:58'),
(14, 38, 4, 61, 770720, '2026-11-05 17:28:58'),
(47, 10, 24, 221, 10000, '2026-11-12 09:22:55'),
(48, 16, 24, 222, 28636, '2026-11-12 09:22:55'),
(49, 84, 24, 223, 9.07, '2026-11-12 09:22:55'),
(50, 81, 24, 223, 1.29, '2026-11-12 09:22:55'),
(51, 1, 24, 224, 2488, '2026-11-12 09:22:55'),
(52, 73, 24, 225, 20.72, '2026-11-12 09:22:55'),
(53, 106, 24, 226, 14392, '2026-11-12 09:22:55'),
(54, 39, 24, 227, 37.12, '2026-11-12 09:22:55'),
(72, 38, 36, 389, 25264, '2026-11-12 15:40:10'),
(73, 90, 36, 390, 4.44, '2026-11-12 15:40:10'),
(74, 16, 36, 392, 41520, '2026-11-12 15:40:10'),
(75, 81, 36, 393, 17.9136, '2026-11-12 15:40:10'),
(76, 1, 36, 394, 3335, '2026-11-12 15:40:10'),
(77, 101, 36, 395, 4888, '2026-11-12 15:40:10'),
(78, 102, 36, 395, 872, '2026-11-12 15:40:10'),
(79, 27, 36, 396, 1292, '2026-11-12 15:40:10'),
(80, 73, 36, 397, 32.51, '2026-11-12 15:40:10'),
(81, 106, 36, 398, 5240, '2026-11-12 15:40:10'),
(82, 96, 36, 400, 0.192, '2026-11-12 15:40:10'),
(83, 39, 36, 401, 1, '2026-11-12 15:40:10'),
(84, 39, 36, 402, 54.3451, '2026-11-12 15:40:10'),
(85, 107, 36, 403, 455.38, '2026-11-12 15:40:10'),
(86, 110, 36, 403, 2.26, '2026-11-12 15:40:10'),
(87, 112, 36, 403, 103.72, '2026-11-12 15:40:10'),
(88, 108, 36, 403, 39.307, '2026-11-12 15:40:10');

-- --------------------------------------------------------

--
-- Table structure for table `mapping`
--

CREATE TABLE `mapping` (
  `id` int(11) NOT NULL,
  `key` varchar(40) DEFAULT NULL,
  `mud_label` varchar(120) DEFAULT NULL,
  `import_desc` varchar(300) DEFAULT NULL,
  `ratio` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mapping`
--

INSERT INTO `mapping` (`id`, `key`, `mud_label`, `import_desc`, `ratio`) VALUES
(1, 'FPMC', 'Corrugated Cartons', 'Corrugated Cartons', 1),
(2, 'SPIC', 'Inner Cartons', 'Tea Cartons', 1),
(3, 'SPMT', 'Empty Tins', 'Empty Tins', 1),
(4, 'PSIP', 'Inner Pouch', 'Laminating Pouch,Empty Pouch', 1),
(5, 'ACST', 'Stickers', 'Holographic Label', 1),
(6, 'ACTG', 'T/B Tags', 'Tea Bags Tags', 1),
(7, 'ACTH', 'Tea Bag Cotton Thread', 'Threads', 1),
(8, 'ACTP', 'Self Adhesive Tape', 'Adhesive Tape', 1),
(9, 'FLLI', 'Tea Flavour', 'Tea Flavours', 1),
(10, 'FLPT', 'Herbs / Flowers', 'Herbs,Dried Herbs,Flowers,Chamomile Whole Flowers', 1),
(11, 'FRPT', 'Fruit Particles', 'Dried Fruit - Roship Coarse,Fruits,Dried Fruit - Apple Pieces', 1),
(12, 'FPPE', 'Poly Bags', 'Poly Bags', 1),
(13, 'OWBP', 'Bopp Cut Sheet', 'Bopp Cut Sheet', 1),
(14, 'PPFP', 'Filter Papers', 'Filter Papers', 1),
(15, 'SPEF', 'Paper Envelopes', 'Envelopes', 1),
(16, 'GREIM', 'China Green Tea', 'China Green Tea', 1),
(17, 'ACSP', 'Plastic Strapping', '', 1),
(18, 'BLKCY', 'Local tea (ignored)', '', 1),
(19, 'GRECY', 'Local tea (ignored)', '', 1),
(20, 'FGPAK', 'Finished goods (ignored)', '', 1),
(21, 'SFFLT', 'Semi finished (ignored)', '', 1),
(22, 'SFMTB', 'Semi finished (ignored)', '', 1);

-- --------------------------------------------------------

--
-- Table structure for table `qty_rules`
--

CREATE TABLE `qty_rules` (
  `id` int(11) NOT NULL,
  `mud_label` varchar(120) DEFAULT NULL,
  `import_desc` varchar(300) DEFAULT NULL,
  `basis` varchar(5) DEFAULT NULL,
  `per_unit` float DEFAULT NULL,
  `ratio_text` varchar(60) DEFAULT NULL,
  `active` int(11) DEFAULT NULL,
  `key` varchar(40) DEFAULT NULL,
  `hs_code` varchar(500) DEFAULT NULL,
  `product_family` varchar(80) DEFAULT NULL,
  `description_keyword` varchar(300) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `qty_rules`
--

INSERT INTO `qty_rules` (`id`, `mud_label`, `import_desc`, `basis`, `per_unit`, `ratio_text`, `active`, `key`, `hs_code`, `product_family`, `description_keyword`) VALUES
(9, 'Corrugated Cartons', 'Corrugated Cartons', 'nos', 1, '1.1', 1, 'FPMC', '48191000', NULL, NULL),
(10, 'Inner Cartons', 'Tea Cartons', 'nos', 1, '1.1', 1, 'SPIC', '48192000', NULL, NULL),
(11, 'Inner Pouch', 'Laminating Pouch/Empty Pouch', 'nos', 1, '1.1', 1, 'PSIP', '39232990', NULL, NULL),
(12, 'Inner Pouch in Reels', 'Laminating Pouch', 'nos', 0.166667, '1Mtr : 6IC', 1, 'PSIP', '39232990', NULL, NULL),
(13, 'Polythene Bags', 'Poly Bags', 'nos', 1, '1.1', 1, 'APHE', '39232190', NULL, NULL),
(14, 'Polythene Bags', 'Poly Bags', 'kgs', 8, '1Kgs : 0.125 Pallet', 1, 'OWBP', '39201090', NULL, NULL),
(15, 'Self Adhesive Tape - 1/2\"', 'Adhesive Tape', 'nos', 0.000666667, '1 : 1500 I/Ctns', 1, 'ACTP', '39191000,48114199', NULL, NULL),
(16, 'Self Adhesive Tape-2\"', 'Adhesive Tape', 'nos', 0.05, '1 : 20 M/Ctns', 1, 'ACTP', '39191000,48114199', NULL, NULL),
(17, 'Tear Tape', 'Tear Tape', 'nos', 0.0000666667, '1 : 15000IC', 1, 'ACTT', '39191000,39199090', NULL, NULL),
(18, 'Plastic Strapping', 'Plastic Strapping', 'nos', 0.001, '1 : 1000 M/Ctns', 1, NULL, '39202020', NULL, NULL),
(19, 'MDF Wooden Tray/Box', 'Wooden Boxes', 'nos', 1, '1.1', 1, 'PRM', '44151000,44219990,44209000', NULL, NULL),
(20, 'Bopp Sheets', 'Bopp Cut Sheet', 'nos', 1, '1.1', 1, 'OWBP', '39202010', NULL, NULL),
(21, 'Tea Bag Tags', 'Tea Bag Tags', 'nos', 1, '1 :1TB', 1, 'ACTG', '48211090', NULL, NULL),
(22, 'Tea Bag Foil Envelopes', 'Envelopes', 'nos', 1, '1 :1TB', 1, 'SPEF', '48171000', NULL, NULL),
(23, 'Paper Envelopes', 'Envelopes', 'nos', 1, '1 :1TB', 1, 'SPEF', '48171000', NULL, NULL),
(24, 'Paper Heat Seal Envelopes', 'Envelopes', 'nos', 1, '1 :1TB', 1, 'SPEF', '48171000', NULL, NULL),
(25, 'Bopp Films Heatable', 'Bopp Films Heatable', 'nos', 0.00133333, '1 : 750IC', 1, 'OWBP', '39202090', NULL, NULL),
(26, 'Filter Papers', 'Filter Papers', 'nos', 0.000185185, '1Kgs : 5,400 Tea Bags', 1, 'PPFP', '48232010,48054010', NULL, NULL),
(27, 'Tea Bags Cotton Threads', 'Threads', 'nos', 0.000008, '1Cone : 125,000 Tea Bags', 1, 'ACTH', '52041990,52054200', NULL, NULL),
(28, 'Aluminium Wire', 'Alu Wire', 'nos', 0.0000273973, '1Kgs : 36,500 Tea Bags', 1, 'ACAW', '76052900', NULL, NULL),
(29, 'Shrink Wrapping Rolls', 'Shrink Wrapping Rolls', 'nos', 0.5, '1Roll : 2PLT', 1, NULL, '39206290', NULL, NULL),
(30, 'Shrink Wrapping Sheets', 'Shrink Wrapping Sheets', 'nos', 1, '1 : 1Tins', 1, NULL, '39206190', NULL, NULL),
(31, 'Flavour Liqued', 'Tea Flavours', 'kgs', 0.05, '1 Kgs Tea : 0.05 Flv', 1, 'FLLI', '21069099,21069031,33021010,33021090', NULL, NULL),
(32, 'Stickers', 'Holographic Label', 'nos', 1, '1.1IC', 1, 'ACST', '39199090', NULL, NULL),
(33, 'Metal Tins 100G X 10', 'Empty Tins', 'nos', 1, '1.1', 1, 'SPMT', '73102990', NULL, NULL),
(34, 'Metal Tins 200G X 12', 'Empty Tins', 'nos', 1, '1.1', 1, 'SPMT', '73102990', NULL, NULL),
(35, 'Metal Tins 250G X 12', 'Empty Tins', 'nos', 1, '1.1', 1, 'SPMT', '73102990', NULL, NULL),
(36, 'Metal Tins 150G X 12', 'Empty Tins', 'nos', 1, '1.1', 1, 'SPMT', '73102990', NULL, NULL),
(37, 'Herbs', 'Herbs', 'kgs', 0.2, '1Kgs : 0.2Herbs', 1, 'GERB', '12119090', NULL, NULL),
(38, 'Fruit Particles', 'Fruits', 'kgs', 0.0749997, '1Kgs : 0.075Herbs', 1, 'FLPT', '08134090', NULL, NULL),
(39, 'Granuals', 'Granuals', 'kgs', 0.03, '1Kgs : 0.03Herbs', 1, 'FLGR', '33021090', NULL, NULL),
(40, 'Spices', 'Dried Herbs/Herbs', 'kgs', 0.2, '1Kgs : 0.2Herbs', 1, 'SPCE', '12119090', NULL, NULL),
(41, 'Non Woven Bags', 'PP Woven Bags (IBG)/PP Woven Bags', 'nos', 1, '1 : 1MC', 1, 'FPPP', '39232990', NULL, NULL),
(42, 'Shopping Bags', 'Shopping Bags', 'nos', 1, '1 : 1MC', 1, NULL, '39232990', NULL, NULL),
(43, 'Tea rod soilon with Tags & String', 'Tea rod soilon with Tags & String', 'nos', 1, '1.1', 1, NULL, '63079090', NULL, NULL),
(44, 'Gum - Water Based', 'Adhesive Gum', 'nos', 0.00166667, '1Kgs : 600 IC', 1, 'ACGM', '35069190', NULL, NULL),
(45, 'Gum - Hot Melt', 'Adhesive Gum', 'nos', 0.0000666667, '1 : 15,000IC', 1, 'ACGM', '35069190', NULL, NULL),
(46, 'Dividers', 'Dividers', 'nos', 1, '1.1IC', 1, 'ACDI', '48239090', NULL, NULL),
(47, 'Paper Canisters - 50G', 'Paper Canisters - 50G', 'nos', 1, '1.1IC', 1, NULL, '48195000', NULL, NULL),
(48, 'Paper Bags - 50KG', 'Paper Bags - 50KG', 'nos', 1, '1.1', 1, 'FPPB', '48133000', NULL, NULL),
(50, 'Fruit Particles', 'Fruits', 'kgs', 0.0749997, '1Kgs : 0.075Herbs', 1, 'FRPT', '08134090', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `shipments`
--

CREATE TABLE `shipments` (
  `id` int(11) NOT NULL,
  `ref_no` varchar(40) DEFAULT NULL,
  `export_entry` varchar(40) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `hs_code` varchar(20) DEFAULT NULL,
  `product` varchar(60) DEFAULT NULL,
  `qty_nos` float DEFAULT NULL,
  `qty_kgs` float DEFAULT NULL,
  `approval_no` varchar(10) DEFAULT NULL,
  `status` varchar(12) DEFAULT NULL,
  `created` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `shipments`
--

INSERT INTO `shipments` (`id`, `ref_no`, `export_entry`, `date`, `hs_code`, `product`, `qty_nos`, `qty_kgs`, `approval_no`, `status`, `created`) VALUES
(1, 'JB - ', '', '2026-11-05', '0902.30.11', 'Tea Bags', 20, NULL, '227', 'draft', '2026-11-05 16:48:49'),
(2, '', '', '2026-11-05', '0902.30.11', 'Tea Bags', 770720, 1165, '227', 'draft', '2026-11-05 17:03:59'),
(3, 'JB - ', '', '2026-11-05', '0902.30.11', 'Tea Bags', 770720, 1165, '227', 'draft', '2026-11-05 17:19:11'),
(4, 'JB - ', '', '2026-11-05', '0902.30.11', 'Tea Bags', 770720, 1165, '227', 'confirmed', '2026-11-05 17:23:32'),
(5, 'JB - ', '', '2026-11-05', '0902.30.11', 'Tea Bags', 770720, 1165, '227', 'draft', '2026-11-05 17:37:02'),
(7, 'JB - E13124', '', '2026-11-10', '0902.30.11', 'Tea Bags', NULL, NULL, '227', 'draft', '2026-11-10 10:09:21'),
(10, 'JB - E13124', '', '2026-11-10', '0902.30.11', 'Tea Bags', NULL, NULL, '227', 'draft', '2026-11-10 12:36:19'),
(17, 'JB - E13124', '', '2026-11-11', '0902.30.11', 'Tea Bags', NULL, NULL, '227', 'draft', '2026-11-11 10:28:00'),
(18, 'JB - E13124', '', '2026-11-11', '0902.30.11', 'Tea Bags', NULL, NULL, '227', 'cancelled', '2026-11-11 13:08:19'),
(19, 'JB - E13124', '', '2026-11-11', '0902.30.11', 'Tea Bags', NULL, NULL, '227', 'draft', '2026-11-11 14:36:03'),
(20, 'JB - E13124', '', '2026-11-12', '0902.30.11', 'Tea Bags', NULL, NULL, '227', 'cancelled', '2026-11-12 08:23:24'),
(21, 'JB - E13124', '', '2026-11-12', '0902.30.11', 'Tea Bags', NULL, NULL, '227', 'cancelled', '2026-11-12 08:47:49'),
(22, 'JB - E13124', '', '2026-11-12', '0902.30.11', 'Tea Bags', NULL, NULL, '227', 'cancelled', '2026-11-12 08:53:38'),
(23, 'JB - E13124', '', '2026-11-12', '0902.30.11', 'Tea Bags', NULL, NULL, '227', 'cancelled', '2026-11-12 09:20:21'),
(24, 'JB - E13124', '', '2026-11-12', '0902.30.11', 'Tea Bags', NULL, NULL, '227', 'confirmed', '2026-11-12 09:22:50'),
(32, 'JB - E13129', '', '2026-11-12', '0902.30.11', 'Tea Bags', NULL, NULL, '227', 'cancelled', '2026-11-12 15:05:29'),
(36, 'JB - E13129', '', '2026-11-12', '0902.30.11', 'Tea Bags', NULL, NULL, '227', 'confirmed', '2026-11-12 15:10:13'),
(37, 'JB - jdjdj', '', '2026-11-12', '0902.30.11', 'Tea Bags', NULL, NULL, '227', 'draft', '2026-11-12 15:12:36'),
(38, 'JB - E13129', '', '2026-11-12', '0902.30.11', 'Tea Bags', NULL, NULL, '227', 'draft', '2026-11-12 15:16:43');

-- --------------------------------------------------------

--
-- Table structure for table `shipment_lines`
--

CREATE TABLE `shipment_lines` (
  `id` int(11) NOT NULL,
  `shipment_id` int(11) DEFAULT NULL,
  `label` varchar(120) DEFAULT NULL,
  `import_desc` varchar(300) DEFAULT NULL,
  `required` float DEFAULT NULL,
  `hs_code` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `shipment_lines`
--

INSERT INTO `shipment_lines` (`id`, `shipment_id`, `label`, `import_desc`, `required`, `hs_code`) VALUES
(1, 1, 'Bopp Cut Sheet', 'Bopp Cut Sheet', 307, NULL),
(2, 1, 'Paper Envelopes', 'Envelopes', 25264, NULL),
(3, 1, 'Filter Papers', 'Filter Papers', 4.44, NULL),
(4, 1, 'Inner Cartons', 'Tea Cartons', 53918, NULL),
(5, 1, 'Inner Pouch', 'Laminating Pouch,Empty Pouch', 41520, NULL),
(6, 1, 'Tea Flavour', 'Tea Flavours', 17.9136, NULL),
(7, 1, 'Corrugated Cartons', 'Corrugated Cartons', 3335, NULL),
(8, 1, 'Empty Tins', 'Empty Tins', 5760, NULL),
(9, 1, 'Poly Bags', 'Poly Bags', 1292, NULL),
(10, 1, 'Herbs / Flowers', 'Herbs,Dried Herbs,Flowers,Chamomile Whole Flowers', 23.28, NULL),
(11, 1, 'Stickers', 'Holographic Label', 84346, NULL),
(12, 1, 'T/B Tags', 'Tea Bags Tags', 25264, NULL),
(13, 1, 'Tea Bag Cotton Thread', 'Threads', 0.192, NULL),
(14, 1, 'Self Adhesive Tape', 'Adhesive Tape', 55.3451, NULL),
(15, 1, 'Fruit Particles', 'Dried Fruit - Roship Coarse,Fruits,Dried Fruit - Apple Pieces', 25.2, NULL),
(16, 1, 'China Green Tea', 'China Green Tea', 600.667, NULL),
(17, 2, 'Bopp Cut Sheet', 'Bopp Cut Sheet', 307, NULL),
(18, 2, 'Inner Cartons', 'Tea Cartons', 53918, NULL),
(19, 2, 'Inner Pouch', 'Laminating Pouch,Empty Pouch', 41520, NULL),
(20, 2, 'Tea Flavour', 'Tea Flavours', 17.9136, NULL),
(21, 2, 'Corrugated Cartons', 'Corrugated Cartons', 3335, NULL),
(22, 2, 'Empty Tins', 'Empty Tins', 5760, NULL),
(23, 2, 'Poly Bags', 'Poly Bags', 1292, NULL),
(24, 2, 'Herbs / Flowers', 'Herbs,Dried Herbs,Flowers,Chamomile Whole Flowers', 23.28, NULL),
(25, 2, 'Stickers', 'Holographic Label', 84346, NULL),
(26, 2, 'Self Adhesive Tape', 'Adhesive Tape', 55.3451, NULL),
(27, 2, 'Fruit Particles', 'Dried Fruit - Roship Coarse,Fruits,Dried Fruit - Apple Pieces', 25.2, NULL),
(28, 2, 'China Green Tea', 'China Green Tea', 600.667, NULL),
(29, 2, 'Filter Papers', 'Filter Papers', 142.726, NULL),
(30, 2, 'Tea Bag Cotton Thread', 'Threads', 6.1658, NULL),
(31, 2, 'Alu Wire', 'Alu Wire', 21.1156, NULL),
(32, 2, 'T/B Tags', 'Tea Bags Tags', 770720, NULL),
(33, 2, 'Paper Envelopes', 'Envelopes', 770720, NULL),
(34, 3, 'Bopp Cut Sheet', 'Bopp Cut Sheet', 22800, NULL),
(35, 3, 'Inner Cartons', 'Tea Cartons', 45884, NULL),
(36, 3, 'Inner Pouch', 'Laminating Pouch,Empty Pouch', 28636, NULL),
(37, 3, 'Tea Flavour', 'Tea Flavours', 10.36, NULL),
(38, 3, 'Corrugated Cartons', 'Corrugated Cartons', 2488, NULL),
(39, 3, 'Herbs / Flowers', 'Herbs,Dried Herbs,Flowers,Chamomile Whole Flowers', 12.72, NULL),
(40, 3, 'Stickers', 'Holographic Label', 14392, NULL),
(41, 3, 'Self Adhesive Tape', 'Adhesive Tape', 37.12, NULL),
(42, 3, 'Fruit Particles', 'Dried Fruit - Roship Coarse,Fruits,Dried Fruit - Apple Pieces', 8, NULL),
(43, 3, 'Filter Papers', 'Filter Papers', 142.726, NULL),
(44, 3, 'Tea Bag Cotton Thread', 'Threads', 6.1658, NULL),
(45, 3, 'Alu Wire', 'Alu Wire', 21.1156, NULL),
(46, 3, 'T/B Tags', 'Tea Bags Tags', 770720, NULL),
(47, 3, 'Paper Envelopes', 'Envelopes', 770720, NULL),
(48, 4, 'Bopp Cut Sheet', 'Bopp Cut Sheet', 22800, NULL),
(49, 4, 'Inner Cartons', 'Tea Cartons', 15411, NULL),
(50, 4, 'Inner Pouch', 'Laminating Pouch,Empty Pouch', 28636, NULL),
(51, 4, 'Tea Flavour', 'Tea Flavours', 10.36, NULL),
(52, 4, 'Corrugated Cartons', 'Corrugated Cartons', 2488, NULL),
(53, 4, 'Herbs / Flowers', 'Herbs,Dried Herbs,Flowers,Chamomile Whole Flowers', 12.72, NULL),
(54, 4, 'Stickers', 'Holographic Label', 14392, NULL),
(55, 4, 'Self Adhesive Tape', 'Adhesive Tape', 37.12, NULL),
(56, 4, 'Fruit Particles', 'Dried Fruit - Roship Coarse,Fruits,Dried Fruit - Apple Pieces', 8, NULL),
(57, 4, 'Filter Papers', 'Filter Papers', 142.726, NULL),
(58, 4, 'Tea Bag Cotton Thread', 'Threads', 6.1658, NULL),
(59, 4, 'Alu Wire', 'Alu Wire', 7.35, NULL),
(60, 4, 'T/B Tags', 'Tea Bags Tags', 770720, NULL),
(61, 4, 'Paper Envelopes', 'Envelopes', 770720, NULL),
(62, 5, 'Bopp Cut Sheet', 'Bopp Cut Sheet', 22800, NULL),
(63, 5, 'Inner Cartons', 'Tea Cartons', 45884, NULL),
(64, 5, 'Inner Pouch', 'Laminating Pouch,Empty Pouch', 28636, NULL),
(65, 5, 'Tea Flavour', 'Tea Flavours', 10.36, NULL),
(66, 5, 'Corrugated Cartons', 'Corrugated Cartons', 2488, NULL),
(67, 5, 'Herbs / Flowers', 'Herbs,Dried Herbs,Flowers,Chamomile Whole Flowers', 12.72, NULL),
(68, 5, 'Stickers', 'Holographic Label', 14392, NULL),
(69, 5, 'Self Adhesive Tape', 'Adhesive Tape', 37.12, NULL),
(70, 5, 'Fruit Particles', 'Dried Fruit - Roship Coarse,Fruits,Dried Fruit - Apple Pieces', 8, NULL),
(71, 5, 'Filter Papers', 'Filter Papers', 142.726, NULL),
(72, 5, 'Tea Bag Cotton Thread', 'Threads', 6.1658, NULL),
(73, 5, 'Alu Wire', 'Alu Wire', 21.1156, NULL),
(74, 5, 'T/B Tags', 'Tea Bags Tags', 770720, NULL),
(75, 5, 'Paper Envelopes', 'Envelopes', 770720, NULL),
(82, 7, 'Inner Cartons', 'Inner Cartons', 45884, '48192000'),
(83, 7, 'Flavours Liquid', 'Flavours Liquid', 0.518, NULL),
(84, 7, 'Corrugated Cartons', 'Corrugated Cartons', 2488, '48191000'),
(85, 7, 'Fruit Particle', 'Fruit Particle', 0.954, NULL),
(86, 7, 'Stickers', 'Stickers', 14392, NULL),
(97, 10, 'Inner Cartons', 'Inner Cartons', 45884, '48192000'),
(98, 10, 'Inner Pouch', 'Inner Pouch', 28636, '39232990'),
(99, 10, 'Flavours Liquid', 'Flavours Liquid', 10.36, '21069099,21069031,33021010,33021090'),
(100, 10, 'Corrugated Cartons', 'Corrugated Cartons', 2488, '48191000'),
(101, 10, 'Fruit Particle', 'Fruit Particle', 12.72, '08134090'),
(102, 10, 'Stickers', 'Stickers', 14392, '39199090'),
(103, 10, 'Self Adhesive Tape - 1/2\"', 'Self Adhesive Tape - 1/2\"', 37.12, '39191000'),
(157, 17, 'Bopp Films Heatable', 'Bopp Films Heatable', 22800, '39202090'),
(158, 17, 'Inner Cartons', 'Tea Cartons', 45884, '48192000'),
(159, 17, 'Inner Pouch', 'Laminating Pouch/Empty Pouch', 28636, '39232990'),
(160, 17, 'Flavours Liquid', 'Tea Flavours', 10.36, '21069099,21069031,33021010,33021090'),
(161, 17, 'Corrugated Cartons', 'Corrugated Cartons', 2488, '48191000'),
(162, 17, 'Fruit Particle', 'Fruit', 20.72, '08134090'),
(163, 17, 'Stickers', 'Holographic Label', 14392, '39199090'),
(164, 17, 'Self Adhesive Tape - 2\"', 'Adhesive Tape', 37.12, '39191000'),
(165, 18, 'Bopp Films Heatable', 'Bopp Films Heatable', 0, '39202090'),
(166, 18, 'Inner Cartons', 'Tea Cartons', 0, '48192000'),
(167, 18, 'Inner Pouch', 'Laminating Pouch/Empty Pouch', 0, '39232990'),
(168, 18, 'Flavours Liquid', 'Tea Flavours', 0, '21069099,21069031,33021010,33021090'),
(169, 18, 'Corrugated Cartons', 'Corrugated Cartons', 2488, '48191000'),
(170, 18, 'Fruit Particle', 'Fruit', 0, '08134090'),
(171, 18, 'Stickers', 'Holographic Label', 14392, '39199090'),
(172, 18, 'Self Adhesive Tape - 2\"', 'Adhesive Tape', 3, '39191000'),
(173, 19, 'Bopp Films Heatable', 'Bopp Films Heatable', 307, '39202090'),
(174, 19, 'Tea Bag Foil Envelopes', 'Envelopes', 25264, '48171000'),
(175, 19, 'Filter Papers', 'Filter Papers', 4.44, '48232010,48054010'),
(176, 19, 'Inner Cartons', 'Tea Cartons', 53918, '48192000'),
(177, 19, 'Inner Pouch', 'Laminating Pouch/Empty Pouch', 41520, '39232990'),
(178, 19, 'Flavours Liquid', 'Tea Flavours', 17.9136, '21069099,21069031,33021010,33021090'),
(179, 19, 'Corrugated Cartons', 'Corrugated Cartons', 3335, '48191000'),
(180, 19, 'Metal Tins 200G X 12', 'Empty Tins', 5760, '73102990'),
(181, 19, 'Fruit Particle', 'Fruit', 48.48, '08134090'),
(182, 19, 'Stickers', 'Holographic Label', 84346, '39199090'),
(183, 19, 'Tea Bag Tags', 'Tea Bag Tags', 25264, '48211090'),
(184, 19, 'Tea Bags Cotton Threads', 'Threads', 0.192, '52041990,52054200'),
(185, 19, 'Self Adhesive Tape - 1/2\"', 'Adhesive Tape', 1, '39191000,48114199'),
(186, 19, 'Self Adhesive Tape - 2\"', 'Adhesive Tape', 54.3451, '39191000,48114199'),
(187, 20, 'Bopp Films Heatable', 'Bopp Films Heatable', 22800, '39202090'),
(188, 20, 'Inner Cartons', 'Tea Cartons', 45884, '48192000'),
(189, 20, 'Inner Pouch', 'Laminating Pouch/Empty Pouch', 28636, '39232990'),
(190, 20, 'Flavours Liquid', 'Tea Flavours', 10.36, '21069099,21069031,33021010,33021090'),
(191, 20, 'Corrugated Cartons', 'Corrugated Cartons', 2488, '48191000'),
(192, 20, 'Fruit Particle', 'Fruit', 20.72, '08134090'),
(193, 20, 'Stickers', 'Holographic Label', 14392, '39199090'),
(194, 20, 'Self Adhesive Tape - 2\"', 'Adhesive Tape', 37.12, '39191000,48114199'),
(195, 21, 'Bopp Films Heatable', 'Bopp Films Heatable', 22800, '39202090'),
(196, 21, 'Inner Cartons', 'Tea Cartons', 45884, '48192000'),
(197, 21, 'Inner Pouch', 'Laminating Pouch/Empty Pouch', 28636, '39232990'),
(198, 21, 'Flavours Liquid', 'Tea Flavours', 10.36, '21069099,21069031,33021010,33021090'),
(199, 21, 'Corrugated Cartons', 'Corrugated Cartons', 2488, '48191000'),
(200, 21, 'Fruit Particle', 'Fruits', 12.72, '08134090'),
(201, 21, 'Stickers', 'Holographic Label', 14392, '39199090'),
(202, 21, 'Self Adhesive Tape - 2\"', 'Adhesive Tape', 37.12, '39191000,48114199'),
(203, 21, 'Fruit Particle', 'Fruit', 8, '08134090'),
(204, 22, 'Bopp Films Heatable', 'Bopp Films Heatable', 22800, '39202090'),
(205, 22, 'Inner Cartons', 'Tea Cartons', 45884, '48192000'),
(206, 22, 'Inner Pouch', 'Laminating Pouch/Empty Pouch', 28636, '39232990'),
(207, 22, 'Flavours Liquid', 'Tea Flavours', 10.36, '21069099,21069031,33021010,33021090'),
(208, 22, 'Corrugated Cartons', 'Corrugated Cartons', 2488, '48191000'),
(209, 22, 'Fruit Particle', 'Fruits', 20.72, '08134090'),
(210, 22, 'Stickers', 'Holographic Label', 14392, '39199090'),
(211, 22, 'Self Adhesive Tape - 2\"', 'Adhesive Tape', 37.12, '39191000,48114199'),
(212, 23, 'Bopp Films Heatable', 'Bopp Films Heatable', 22800, '39202090'),
(213, 23, 'Inner Cartons', 'Tea Cartons', 45884, '48192000'),
(214, 23, 'Inner Pouch', 'Laminating Pouch/Empty Pouch', 28636, '39232990'),
(215, 23, 'Flavour Liquid', 'Tea Flavours', 10.36, '21069099,21069031,33021010,33021090'),
(216, 23, 'Corrugated Cartons', 'Corrugated Cartons', 2488, '48191000'),
(217, 23, 'Fruits Particle', 'Fruits', 20.72, '08134090'),
(218, 23, 'Stickers', 'Holographic Label', 14392, '39199090'),
(219, 23, 'Self Adhesive Tape-2\"', 'Adhesive Tape', 37.12, '39191000,48114199'),
(220, 24, 'Bopp Films Heatable', 'Bopp Films Heatable', 22800, '39202090'),
(221, 24, 'Inner Cartons', 'Tea Cartons', 45884, '48192000'),
(222, 24, 'Inner Pouch', 'Laminating Pouch/Empty Pouch', 28636, '39232990'),
(223, 24, 'Flavour Liqued', 'Tea Flavours', 10.36, '21069099,21069031,33021010,33021090'),
(224, 24, 'Corrugated Cartons', 'Corrugated Cartons', 2488, '48191000'),
(225, 24, 'Fruit Particles', 'Fruits', 20.72, '08134090'),
(226, 24, 'Stickers', 'Holographic Label', 14392, '39199090'),
(227, 24, 'Self Adhesive Tape-2\"', 'Adhesive Tape', 37.12, '39191000,48114199'),
(332, 32, 'Bopp Films Heatable', 'Bopp Films Heatable', 307, '39202090'),
(333, 32, 'Tea Bag Foil Envelopes', 'Envelopes', 25264, '48171000'),
(334, 32, 'Filter Papers', 'Filter Papers', 4.44, '48232010,48054010'),
(335, 32, 'Inner Cartons', 'Tea Cartons', 53918, '48192000'),
(336, 32, 'Inner Pouch', 'Laminating Pouch/Empty Pouch', 41520, '39232990'),
(337, 32, 'Flavour Liqued', 'Tea Flavours', 17.9136, '21069099,21069031,33021010,33021090'),
(338, 32, 'Corrugated Cartons', 'Corrugated Cartons', 3335, '48191000'),
(339, 32, 'Metal Tins 200G X 12', 'Empty Tins', 5760, '73102990'),
(340, 32, 'Poly Bags', 'Poly Bags', 1292, NULL),
(341, 32, 'Fruit Particles', 'Fruits', 48.48, '08134090'),
(342, 32, 'Stickers', 'Holographic Label', 84346, '39199090'),
(343, 32, 'Tea Bag Tags', 'Tea Bag Tags', 25264, '48211090'),
(344, 32, 'Tea Bags Cotton Threads', 'Threads', 0.192, '52041990,52054200'),
(345, 32, 'Self Adhesive Tape - 1/2\"', 'Adhesive Tape', 1, '39191000,48114199'),
(346, 32, 'Self Adhesive Tape-2\"', 'Adhesive Tape', 54.3451, '39191000,48114199'),
(347, 32, 'China Green Tea', 'China Green Tea', 600.667, NULL),
(388, 36, 'Bopp Films Heatable', 'Bopp Films Heatable', 307, '39202090'),
(389, 36, 'Tea Bag Foil Envelopes', 'Envelopes', 25264, '48171000'),
(390, 36, 'Filter Papers', 'Filter Papers', 4.44, '48232010,48054010'),
(391, 36, 'Inner Cartons', 'Tea Cartons', 53918, '48192000'),
(392, 36, 'Inner Pouch', 'Laminating Pouch/Empty Pouch', 41520, '39232990'),
(393, 36, 'Flavour Liqued', 'Tea Flavours', 17.9136, '21069099,21069031,33021010,33021090'),
(394, 36, 'Corrugated Cartons', 'Corrugated Cartons', 3335, '48191000'),
(395, 36, 'Metal Tins 200G X 12', 'Empty Tins', 5760, '73102990'),
(396, 36, 'Poly Bags', 'Poly Bags', 1292, NULL),
(397, 36, 'Fruit Particles', 'Fruits', 48.48, '08134090'),
(398, 36, 'Stickers', 'Holographic Label', 84346, '39199090'),
(399, 36, 'Tea Bag Tags', 'Tea Bag Tags', 25264, '48211090'),
(400, 36, 'Tea Bags Cotton Threads', 'Threads', 0.192, '52041990,52054200'),
(401, 36, 'Self Adhesive Tape - 1/2\"', 'Adhesive Tape', 1, '39191000,48114199'),
(402, 36, 'Self Adhesive Tape-2\"', 'Adhesive Tape', 54.3451, '39191000,48114199'),
(403, 36, 'China Green Tea', 'China Green Tea', 600.667, NULL),
(404, 37, 'Bopp Films Heatable', 'Bopp Films Heatable', 307, '39202090'),
(405, 37, 'Tea Bag Foil Envelopes', 'Envelopes', 25264, '48171000'),
(406, 37, 'Filter Papers', 'Filter Papers', 4.44, '48232010,48054010'),
(407, 37, 'Inner Cartons', 'Tea Cartons', 53918, '48192000'),
(408, 37, 'Inner Pouch', 'Laminating Pouch/Empty Pouch', 41520, '39232990'),
(409, 37, 'Flavour Liqued', 'Tea Flavours', 17.9136, '21069099,21069031,33021010,33021090'),
(410, 37, 'Corrugated Cartons', 'Corrugated Cartons', 3335, '48191000'),
(411, 37, 'Metal Tins 200G X 12', 'Empty Tins', 5760, '73102990'),
(412, 37, 'Poly Bags', 'Poly Bags', 1292, NULL),
(413, 37, 'Fruit Particles', 'Fruits', 48.48, '08134090'),
(414, 37, 'Stickers', 'Holographic Label', 84346, '39199090'),
(415, 37, 'Tea Bag Tags', 'Tea Bag Tags', 25264, '48211090'),
(416, 37, 'Tea Bags Cotton Threads', 'Threads', 0.192, '52041990,52054200'),
(417, 37, 'Self Adhesive Tape - 1/2\"', 'Adhesive Tape', 1, '39191000,48114199'),
(418, 37, 'Self Adhesive Tape-2\"', 'Adhesive Tape', 54.3451, '39191000,48114199'),
(419, 37, 'China Green Tea', 'China Green Tea', 600.667, NULL),
(420, 38, 'Bopp Films Heatable', 'Bopp Films Heatable', 307, '39202090'),
(421, 38, 'Tea Bag Foil Envelopes', 'Envelopes', 25264, '48171000'),
(422, 38, 'Filter Papers', 'Filter Papers', 4.44, '48232010,48054010'),
(423, 38, 'Inner Cartons', 'Tea Cartons', 53918, '48192000'),
(424, 38, 'Inner Pouch', 'Laminating Pouch/Empty Pouch', 41520, '39232990'),
(425, 38, 'Flavour Liqued', 'Tea Flavours', 17.9136, '21069099,21069031,33021010,33021090'),
(426, 38, 'Corrugated Cartons', 'Corrugated Cartons', 3335, '48191000'),
(427, 38, 'Metal Tins 200G X 12', 'Empty Tins', 5760, '73102990'),
(428, 38, 'Fruit Particles', 'Fruits', 48.48, '08134090'),
(429, 38, 'Stickers', 'Holographic Label', 84346, '39199090'),
(430, 38, 'Tea Bag Tags', 'Tea Bag Tags', 25264, '48211090'),
(431, 38, 'Tea Bags Cotton Threads', 'Threads', 0.192, '52041990,52054200'),
(432, 38, 'Self Adhesive Tape - 1/2\"', 'Adhesive Tape', 1, '39191000,48114199'),
(433, 38, 'Self Adhesive Tape-2\"', 'Adhesive Tape', 54.3451, '39191000,48114199');

-- --------------------------------------------------------

--
-- Table structure for table `unmatched_ifs`
--

CREATE TABLE `unmatched_ifs` (
  `id` int(11) NOT NULL,
  `shipment_id` int(11) DEFAULT NULL,
  `excel_row` int(11) DEFAULT NULL,
  `part_no` varchar(120) DEFAULT NULL,
  `product_family` varchar(100) DEFAULT NULL,
  `part_description` text DEFAULT NULL,
  `order_qty` float DEFAULT NULL,
  `reason` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `unmatched_ifs`
--

INSERT INTO `unmatched_ifs` (`id`, `shipment_id`, `excel_row`, `part_no`, `product_family`, `part_description`, `order_qty`, `reason`) VALUES
(1, 7, 15, 'RM-BP-101088', 'OWBP', 'CHELTON - EE 100g Packing Both Side Heat Sealable Transparent BOPP Sheets.', 1920, 'Duplicate key: no matching PART_DESCRIPTION keyword'),
(2, 7, 16, 'RM-BP-101115', 'OWBP', 'CHELTON - ER 100g Packing Both Side Heat Sealable Transparent BOPP Sheets.', 16320, 'Duplicate key: no matching PART_DESCRIPTION keyword'),
(3, 7, 17, 'RM-BP-101116', 'OWBP', 'CHELTON - ES 100g Packing Both Side Heat Sealable Transparent BOPP Sheets.', 720, 'Duplicate key: no matching PART_DESCRIPTION keyword'),
(4, 7, 18, 'RM-BP-101611', 'OWBP', 'CHELTON - Noble House 100g Packing Both Side Heat Sealable Transparent BOPP Sheets,', 3840, 'Duplicate key: no matching PART_DESCRIPTION keyword'),
(5, 7, 29, 'RM-IP-101080', 'PSIP', 'CHELTON - English Elite 100g Packing, Printed Metalized Pouches.', 19156, 'Duplicate key: no matching PART_DESCRIPTION keyword'),
(6, 7, 30, 'RM-IP-101529', 'PSIP', 'CHELTON - Noble House 100g Packing, Printed Metalized GOLD Pouches.', 3880, 'Duplicate key: no matching PART_DESCRIPTION keyword'),
(7, 7, 31, 'RM-IP-104107', 'PSIP', 'CHELTON - Noble House Supe Pekoe Bergamot 400g Packing, Printed Blak Matte Pouches with Re Closable Zipper. (2023-11)', 1000, 'Duplicate key: no matching PART_DESCRIPTION keyword'),
(8, 7, 32, 'RM-IP-104531', 'PSIP', 'CHELTON - Noble House FBOP 500g Packing Printed Blak Matte Pouches with Re Closable Zipper. (2025-8)', 800, 'Duplicate key: no matching PART_DESCRIPTION keyword'),
(9, 7, 33, 'RM-IP-104532', 'PSIP', 'CHELTON - Noble House OPA 400g Packing, Printed Blak Matte Pouches with Re Closable Zipper. (2025-8)', 1000, 'Duplicate key: no matching PART_DESCRIPTION keyword'),
(10, 7, 49, 'RM-TP-100003', 'ACTP', 'PVC Tapes. 48MM x 50M - 2 INCHES', 37.12, 'Duplicate key: no matching PART_DESCRIPTION keyword'),
(11, 7, 56, 'SF-FU-PT-100039', 'FRPT', 'Lemon Peel Coarse Cut', 8, 'No active Qty Rule'),
(12, 7, 69, 'SF-PR-IP-103471', 'PSIP', 'CHELTON - Noble House Supe Pekoe Bergamot 400g Packing, Printed Blak Matte Pouches with Re Closable Zipper. (2023-11)', 1000, 'Duplicate key: no matching PART_DESCRIPTION keyword'),
(13, 7, 70, 'SF-PR-IP-105005', 'PSIP', 'CHELTON - Noble House FBOP 500g Packing Printed Blak Matte Pouches with Re Closable Zipper. (2025-8)', 800, 'Duplicate key: no matching PART_DESCRIPTION keyword'),
(14, 7, 71, 'SF-PR-IP-105014', 'PSIP', 'CHELTON - Noble House OPA 400g Packing, Printed Blak Matte Pouches with Re Closable Zipper. (2025-8)', 1000, 'Duplicate key: no matching PART_DESCRIPTION keyword'),
(43, 10, 15, 'RM-BP-101088', 'OWBP', 'CHELTON - EE 100g Packing Both Side Heat Sealable Transparent BOPP Sheets.', 1920, 'Same KEY has different HS Code sets; check Qty Rules'),
(44, 10, 16, 'RM-BP-101115', 'OWBP', 'CHELTON - ER 100g Packing Both Side Heat Sealable Transparent BOPP Sheets.', 16320, 'Same KEY has different HS Code sets; check Qty Rules'),
(45, 10, 17, 'RM-BP-101116', 'OWBP', 'CHELTON - ES 100g Packing Both Side Heat Sealable Transparent BOPP Sheets.', 720, 'Same KEY has different HS Code sets; check Qty Rules'),
(46, 10, 18, 'RM-BP-101611', 'OWBP', 'CHELTON - Noble House 100g Packing Both Side Heat Sealable Transparent BOPP Sheets,', 3840, 'Same KEY has different HS Code sets; check Qty Rules'),
(47, 10, 56, 'SF-FU-PT-100039', 'FRPT', 'Lemon Peel Coarse Cut', 8, 'No active Qty Rule for KEY'),
(60, 19, 51, 'RM-PE-104313', 'FPPE', 'CHELTON NH 24 x 100g Packing, Un Printed Clear LDPE Bags.', 563, 'No active Qty Rule for KEY'),
(61, 19, 52, 'RM-PE-104314', 'FPPE', 'CHELTON NH 18 x 200g Packing, Un Printed Clear LDPE Bags.', 553, 'No active Qty Rule for KEY'),
(62, 19, 53, 'RM-PE-104315', 'FPPE', 'CHELTON NH OPA 18 x 200g Packing, Un Printed Clear LDPE Bags.', 176, 'No active Qty Rule for KEY'),
(63, 19, 116, 'STD-1411', 'GREIM', 'CHINEES GT - 1411(100%) - IM', 6.6667, 'No active Qty Rule for KEY'),
(64, 19, 125, 'STD-J169', 'GREIM', 'JASMINE - IM', 594, 'No active Qty Rule for KEY'),
(70, 38, 51, 'RM-PE-104313', 'FPPE', 'CHELTON NH 24 x 100g Packing, Un Printed Clear LDPE Bags.', 563, 'No active Qty Rule for KEY'),
(71, 38, 52, 'RM-PE-104314', 'FPPE', 'CHELTON NH 18 x 200g Packing, Un Printed Clear LDPE Bags.', 553, 'No active Qty Rule for KEY'),
(72, 38, 53, 'RM-PE-104315', 'FPPE', 'CHELTON NH OPA 18 x 200g Packing, Un Printed Clear LDPE Bags.', 176, 'No active Qty Rule for KEY'),
(73, 38, 116, 'STD-1411', 'GREIM', 'CHINEES GT - 1411(100%) - IM', 6.6667, 'No active Qty Rule for KEY'),
(74, 38, 125, 'STD-J169', 'GREIM', 'JASMINE - IM', 594, 'No active Qty Rule for KEY');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `full_name` varchar(80) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` varchar(10) DEFAULT NULL,
  `active` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `full_name`, `email`, `password_hash`, `role`, `active`, `created`) VALUES
(1, 'malintha', 'malintha', 'malinthagh@gmail.com', 'scrypt:32768:8:1$CF6LDtWwGe3INbiv$b494ace27d0735311965ae636eceed08d517137beb00809e3d3e924526acf4e43ae454066205dab70ab2f6641142e0fc9394009b57c499c246fcd133d7aeb139', 'admin', 1, '2026-11-06 09:17:18'),
(2, 'user', 'user', 'malinthagh@gmail.com', 'scrypt:32768:8:1$ch1AfuebSjeU25Oc$2cef671d4723bb1b347872e85b00659e5b0371d487ed9c57093922ac18d71006c015c1499ae8d69fbbd21dba61da8d23827ca7b654a6a5d063f5bce3c2867472', 'user', 0, '2026-11-13 09:41:09');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `imports`
--
ALTER TABLE `imports`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_imports_description` (`description`),
  ADD KEY `ix_imports_entry_no` (`entry_no`);

--
-- Indexes for table `ledger`
--
ALTER TABLE `ledger`
  ADD PRIMARY KEY (`id`),
  ADD KEY `line_id` (`line_id`),
  ADD KEY `ix_ledger_shipment_id` (`shipment_id`),
  ADD KEY `ix_ledger_import_id` (`import_id`);

--
-- Indexes for table `mapping`
--
ALTER TABLE `mapping`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `qty_rules`
--
ALTER TABLE `qty_rules`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `shipments`
--
ALTER TABLE `shipments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `shipment_lines`
--
ALTER TABLE `shipment_lines`
  ADD PRIMARY KEY (`id`),
  ADD KEY `shipment_id` (`shipment_id`);

--
-- Indexes for table `unmatched_ifs`
--
ALTER TABLE `unmatched_ifs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_unmatched_ifs_shipment_id` (`shipment_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `imports`
--
ALTER TABLE `imports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=157;

--
-- AUTO_INCREMENT for table `ledger`
--
ALTER TABLE `ledger`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=89;

--
-- AUTO_INCREMENT for table `mapping`
--
ALTER TABLE `mapping`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `qty_rules`
--
ALTER TABLE `qty_rules`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT for table `shipments`
--
ALTER TABLE `shipments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `shipment_lines`
--
ALTER TABLE `shipment_lines`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=434;

--
-- AUTO_INCREMENT for table `unmatched_ifs`
--
ALTER TABLE `unmatched_ifs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=75;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ledger`
--
ALTER TABLE `ledger`
  ADD CONSTRAINT `ledger_ibfk_1` FOREIGN KEY (`import_id`) REFERENCES `imports` (`id`),
  ADD CONSTRAINT `ledger_ibfk_2` FOREIGN KEY (`shipment_id`) REFERENCES `shipments` (`id`),
  ADD CONSTRAINT `ledger_ibfk_3` FOREIGN KEY (`line_id`) REFERENCES `shipment_lines` (`id`);

--
-- Constraints for table `shipment_lines`
--
ALTER TABLE `shipment_lines`
  ADD CONSTRAINT `shipment_lines_ibfk_1` FOREIGN KEY (`shipment_id`) REFERENCES `shipments` (`id`);

--
-- Constraints for table `unmatched_ifs`
--
ALTER TABLE `unmatched_ifs`
  ADD CONSTRAINT `unmatched_ifs_ibfk_1` FOREIGN KEY (`shipment_id`) REFERENCES `shipments` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
