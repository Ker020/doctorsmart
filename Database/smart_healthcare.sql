-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jul 01, 2026 at 03:28 PM
-- Server version: 11.8.6-MariaDB-0+deb13u1 from Debian
-- PHP Version: 8.4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smart_healthcare`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `appointment_date` datetime NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`id`, `doctor_id`, `patient_id`, `appointment_date`, `status`, `type`, `created_at`) VALUES
(1, 1, 1, '2025-12-28 10:00:00', 'confirmed', 'consultation', '2025-12-27 16:06:08'),
(2, 1, 1, '2026-01-01 11:00:00', 'confirmed', 'consultation', '2025-12-31 18:31:59'),
(3, 1, 1, '2026-01-06 13:00:00', 'pending', 'consultation', '2026-01-05 09:44:34'),
(4, 2, 1, '2026-01-28 14:00:00', 'confirmed', 'consultation', '2026-01-26 13:10:10'),
(5, 1, 1, '2026-01-28 13:00:00', 'pending', 'consultation', '2026-01-26 13:10:33'),
(6, 6, 1, '2026-02-02 10:30:00', 'pending', 'consultation', '2026-01-30 19:51:12'),
(7, 12, 1, '2026-01-31 13:00:00', 'confirmed', 'consultation', '2026-01-30 19:51:39'),
(8, 1, 1, '2026-01-31 12:00:00', 'confirmed', 'consultation', '2026-01-30 19:51:43'),
(9, 3, 1, '2026-02-02 10:30:00', 'pending', 'consultation', '2026-02-01 10:38:03'),
(10, 1, 1, '2026-02-01 16:00:00', 'confirmed', 'consultation', '2026-02-01 10:38:16'),
(11, 2, 1, '2026-02-16 11:00:00', 'pending', 'consultation', '2026-02-15 15:14:45'),
(12, 11, 1, '2026-02-16 10:30:00', 'confirmed', 'consultation', '2026-02-15 15:16:18'),
(13, 1, 1, '2026-02-21 10:00:00', 'pending', 'consultation', '2026-02-19 13:28:00'),
(14, 1, 1, '2026-02-20 12:00:00', 'completed', 'consultation', '2026-02-19 13:28:13'),
(15, 11, 1, '2026-02-24 14:00:00', 'confirmed', 'consultation', '2026-02-20 14:17:56'),
(16, 24, 1, '2026-02-22 15:00:00', 'pending', 'consultation', '2026-02-20 23:49:51'),
(17, 24, 1, '2026-02-23 15:00:00', 'confirmed', 'consultation', '2026-02-20 23:50:05'),
(18, 22, 1, '2026-02-22 11:00:00', 'pending', 'consultation', '2026-02-21 00:21:18'),
(19, 22, 1, '2026-02-23 11:00:00', 'confirmed', 'consultation', '2026-02-21 00:21:31');

-- --------------------------------------------------------

--
-- Table structure for table `audit_logs`
--

CREATE TABLE `audit_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `action` varchar(100) NOT NULL,
  `resource_type` varchar(50) DEFAULT NULL,
  `resource_id` int(11) DEFAULT NULL,
  `details` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`details`)),
  `ip_address` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `audit_logs`
--

INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `resource_type`, `resource_id`, `details`, `ip_address`, `created_at`) VALUES
(1, 2, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-01-26 13:12:24'),
(2, 2, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-01-26 13:12:46'),
(3, 46, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-01-30 20:06:55'),
(4, 46, 'prescription_created', 'prescription', 21, '{\"patient_id\": \"1\", \"diagnosis\": \"\\u062a\\u062a\"}', NULL, '2026-01-30 20:07:13'),
(5, 5, 'qr_access_granted', 'patient', 1, '{\"token_id\": 25}', NULL, '2026-02-09 23:43:02'),
(6, 25, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-02-15 15:22:20'),
(7, 2, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-02-18 21:37:56'),
(8, 2, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-02-21 00:29:59'),
(9, 2, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-02-21 00:47:20'),
(10, 2, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-02-21 00:54:01'),
(11, 2, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-02-21 00:58:10'),
(12, 2, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-02-21 16:35:25'),
(13, 2, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-02-21 16:38:07'),
(14, 2, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-02-21 16:57:59'),
(15, 2, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-02-21 17:45:17'),
(16, 2, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-02-21 17:49:41'),
(17, 5, 'qr_access_granted', 'patient', 1, '{\"token_id\": 55}', NULL, '2026-02-21 18:28:49'),
(18, 5, 'qr_access_granted', 'patient', 1, '{\"token_id\": 55}', NULL, '2026-02-21 18:32:11'),
(19, 4, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-02-21 18:47:55'),
(20, 4, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-02-21 18:48:30'),
(21, 4, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-02-21 18:55:42'),
(22, 2, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-03-15 12:30:27'),
(23, 2, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-04-12 16:43:45'),
(24, 2, 'qr_access_granted', 'patient', 1, 'null', NULL, '2026-04-18 13:43:26');

-- --------------------------------------------------------

--
-- Table structure for table `chat_messages`
--

CREATE TABLE `chat_messages` (
  `id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `receiver_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `is_read` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `prescription_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `chat_messages`
--

INSERT INTO `chat_messages` (`id`, `sender_id`, `receiver_id`, `message`, `is_read`, `created_at`, `prescription_id`) VALUES
(1, 2, 3, 'hi john', 1, '2025-12-27 16:07:51', NULL),
(2, 3, 16, 'hi', 0, '2026-01-26 13:10:19', NULL),
(3, 3, 46, 'ger', 0, '2026-01-30 19:54:22', NULL),
(4, 3, 46, 'اهلا', 0, '2026-01-30 19:54:54', NULL),
(5, 3, 2, '9خ8', 1, '2026-02-01 10:39:03', NULL),
(6, 3, 25, 'Malaria', 1, '2026-02-15 15:17:43', NULL),
(7, 25, 3, 'rgo', 1, '2026-02-15 15:19:02', NULL),
(8, 3, 2, 'قاتهخ', 1, '2026-02-19 13:34:38', NULL),
(9, 3, 2, 'kero', 1, '2026-02-19 13:36:07', NULL),
(10, 3, 2, 'kero', 1, '2026-02-19 13:36:11', NULL),
(11, 2, 3, 'hi', 1, '2026-02-19 13:41:09', NULL),
(12, 2, 26, 'ااا', 0, '2026-02-20 14:25:14', NULL),
(13, 3, 59, 'hi doctor', 1, '2026-02-20 23:50:19', NULL),
(14, 59, 3, 'hi john', 1, '2026-02-20 23:52:02', NULL),
(15, 59, 3, 'can i help you', 1, '2026-02-20 23:53:17', NULL),
(16, 3, 59, 'no', 1, '2026-02-20 23:53:25', NULL),
(17, 3, 57, 'hi doctor samir', 0, '2026-02-21 00:21:51', NULL),
(18, 57, 3, 'hi john', 1, '2026-02-21 00:22:52', NULL),
(19, 3, 57, 'can you help me', 0, '2026-02-21 00:23:18', NULL),
(20, 57, 3, '..', 1, '2026-02-21 00:23:26', NULL),
(21, 57, 3, '..', 1, '2026-02-21 00:23:31', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `complaints`
--

CREATE TABLE `complaints` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `target_role` varchar(50) DEFAULT NULL,
  `target_id` int(11) DEFAULT NULL,
  `admin_response` text DEFAULT NULL,
  `responded_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `complaints`
--

INSERT INTO `complaints` (`id`, `user_id`, `subject`, `description`, `status`, `created_at`, `target_role`, `target_id`, `admin_response`, `responded_at`) VALUES
(1, 3, 'gwrh', 'egerh', 'Pending', '2026-01-30 19:59:19', 'doctor', 12, NULL, NULL),
(2, 3, 'ىىى', 'ىى', 'Pending', '2026-01-30 20:01:05', 'lab', 7, NULL, NULL),
(3, 3, 'سيل', 'يلي', 'Pending', '2026-02-19 13:12:45', NULL, NULL, NULL, NULL),
(4, 3, 'ريبع', 'بصقل\r\n', 'Pending', '2026-02-19 13:12:58', NULL, NULL, NULL, NULL),
(5, 3, 'عدم تعقيم الادوات', 'ثلقلقفلفقلث', 'Pending', '2026-02-21 00:16:44', 'doctor', NULL, NULL, NULL),
(6, 3, 'not qualified ', 'this is doctor not qualified to work ', 'Pending', '2026-02-21 00:25:19', 'doctor', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `doctors`
--

CREATE TABLE `doctors` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `specialty` varchar(100) NOT NULL,
  `license_number` varchar(50) NOT NULL,
  `price` float DEFAULT NULL,
  `bio` text DEFAULT NULL,
  `profile_image` varchar(255) DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `total_patients` int(11) DEFAULT NULL,
  `is_featured` tinyint(1) DEFAULT NULL,
  `locations` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`locations`)),
  `available_slots` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`available_slots`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `doctors`
--

INSERT INTO `doctors` (`id`, `user_id`, `specialty`, `license_number`, `price`, `bio`, `profile_image`, `rating`, `total_patients`, `is_featured`, `locations`, `available_slots`) VALUES
(1, 2, 'Diagnostician', 'LIC-2', 300, 'Experienced', 'default_doctor.png', 5, 10, 0, '[{\"name\": \"Main Hospital\", \"address\": \"Princeton-Plainsboro\"}]', '[{\"day\": \"Tuesday\", \"times\": [\"11:00\", \"12:00\", \"13:00\", \"14:00\", \"15:00\", \"16:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"12:00\", \"13:00\", \"14:00\", \"15:00\", \"16:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"12:00\", \"13:00\", \"14:00\", \"15:00\", \"16:00\"]}, {\"day\": \"Friday\", \"times\": [\"10:00\", \"11:00\", \"12:00\", \"13:00\", \"14:00\", \"15:00\", \"16:00\"]}, {\"day\": \"Saturday\", \"times\": [\"10:00\", \"11:00\", \"12:00\", \"13:00\", \"14:00\", \"15:00\", \"16:00\"]}, {\"day\": \"Sunday\", \"times\": [\"09:00\", \"10:00\", \"11:00\", \"12:00\", \"13:00\", \"14:00\", \"15:00\", \"16:00\", \"17:00\", \"18:00\", \"19:00\", \"20:00\", \"21:00\", \"22:00\", \"23:00\"]}]'),
(2, 16, 'Cardiology', 'LIC-20726', 260, 'خبرة 10 سنوات في مجال Cardiology.', 'doctor_default.jpg', 4.4, 402, 0, '[{\"name\": \"East Alison Clinic\", \"address\": \"5304 Gina Alley Apt. 668\\nJacksonside, GU 13157\"}, {\"name\": \"Main Hospital\", \"address\": \"Downtown, Cairo\"}]', '[{\"day\": \"Monday\", \"times\": [\"10:00\", \"10:30\", \"11:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"14:00\", \"14:30\", \"15:00\"]}]'),
(3, 17, 'Ophthalmology', 'LIC-23141', 320, 'استشاري Ophthalmology بمستشفى القصر العيني.', 'doctor_default.jpg', 4.6, 236, 1, '[{\"name\": \"Meghanburgh Clinic\", \"address\": \"87993 Walter Crescent\\nAustinfurt, SD 91752\"}, {\"name\": \"Main Hospital\", \"address\": \"Downtown, Cairo\"}]', '[{\"day\": \"Monday\", \"times\": [\"10:00\", \"10:30\", \"11:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"14:00\", \"14:30\", \"15:00\"]}]'),
(4, 18, 'Cardiology', 'LIC-57712', 140, 'استشاري Cardiology بمستشفى القصر العيني.', 'doctor_default.jpg', 4.7, 160, 0, '[{\"name\": \"East Erikaton Clinic\", \"address\": \"04460 Figueroa Locks Apt. 277\\nEast Brandon, MO 55272\"}, {\"name\": \"Main Hospital\", \"address\": \"Downtown, Cairo\"}]', '[{\"day\": \"Monday\", \"times\": [\"10:00\", \"10:30\", \"11:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"14:00\", \"14:30\", \"15:00\"]}]'),
(5, 19, 'Internal Medicine', 'LIC-93332', 200, 'متخصص في الحالات الحرجة وعلاج Internal Medicine.', 'doctor_default.jpg', 4.9, 438, 0, '[{\"name\": \"Richardshire Clinic\", \"address\": \"1904 Joshua Shoals Suite 356\\nMyersville, PA 04643\"}, {\"name\": \"Main Hospital\", \"address\": \"Downtown, Cairo\"}]', '[{\"day\": \"Monday\", \"times\": [\"10:00\", \"10:30\", \"11:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"14:00\", \"14:30\", \"15:00\"]}]'),
(6, 20, 'Internal Medicine', 'LIC-38428', 380, 'حاصل على دكتوراه في Internal Medicine.', 'doctor_default.jpg', 4.8, 68, 1, '[{\"name\": \"Alexanderland Clinic\", \"address\": \"44197 Mason Glens\\nLake Richard, TN 00745\"}, {\"name\": \"Main Hospital\", \"address\": \"Downtown, Cairo\"}]', '[{\"day\": \"Monday\", \"times\": [\"10:00\", \"10:30\", \"11:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"14:00\", \"14:30\", \"15:00\"]}]'),
(7, 21, 'Dentistry', 'LIC-49777', 420, 'خبرة 10 سنوات في مجال Dentistry.', 'doctor_default.jpg', 4.5, 155, 1, '[{\"name\": \"Lake Barbaraland Clinic\", \"address\": \"060 Johnson Courts\\nGonzalezport, FL 65190\"}, {\"name\": \"Main Hospital\", \"address\": \"Downtown, Cairo\"}]', '[{\"day\": \"Monday\", \"times\": [\"10:00\", \"10:30\", \"11:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"14:00\", \"14:30\", \"15:00\"]}]'),
(8, 22, 'Cardiology', 'LIC-55373', 410, 'خبرة 10 سنوات في مجال Cardiology.', 'doctor_default.jpg', 4, 499, 1, '[{\"name\": \"East Tiffany Clinic\", \"address\": \"3783 Travis Port Suite 574\\nEast Joe, MP 94372\"}, {\"name\": \"Main Hospital\", \"address\": \"Downtown, Cairo\"}]', '[{\"day\": \"Monday\", \"times\": [\"10:00\", \"10:30\", \"11:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"14:00\", \"14:30\", \"15:00\"]}]'),
(9, 23, 'Orthopedics', 'LIC-13616', 460, 'استشاري Orthopedics بمستشفى القصر العيني.', 'doctor_default.jpg', 4.6, 435, 1, '[{\"name\": \"Richardport Clinic\", \"address\": \"7197 Knight Mews Suite 849\\nRobinsonland, NJ 69625\"}, {\"name\": \"Main Hospital\", \"address\": \"Downtown, Cairo\"}]', '[{\"day\": \"Monday\", \"times\": [\"10:00\", \"10:30\", \"11:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"14:00\", \"14:30\", \"15:00\"]}]'),
(10, 24, 'Pediatrics', 'LIC-13299', 360, 'حاصل على دكتوراه في Pediatrics.', 'doctor_default.jpg', 4.5, 392, 1, '[{\"name\": \"East Judith Clinic\", \"address\": \"785 Smith Wells Apt. 671\\nMariabury, MT 97977\"}, {\"name\": \"Main Hospital\", \"address\": \"Downtown, Cairo\"}]', '[{\"day\": \"Monday\", \"times\": [\"10:00\", \"10:30\", \"11:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"14:00\", \"14:30\", \"15:00\"]}]'),
(11, 25, 'Dermatology', 'LIC-24232', 260, 'متخصص في الحالات الحرجة وعلاج Dermatology.', 'doctor_default.jpg', 3.8, 189, 1, '[{\"name\": \"Port Lindseyberg Clinic\", \"address\": \"25913 Carol Heights Apt. 418\\nRobertland, MH 44836\"}, {\"name\": \"Main Hospital\", \"address\": \"Downtown, Cairo\"}]', '[{\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"12:00\", \"13:00\", \"14:00\", \"15:00\", \"16:00\"]}]'),
(12, 46, 'cardiology ', 'LIC-46-202601', 600, 'اشطر دكتور هتخف من غير ما تحس ', 'default_doctor.png', 5, 0, 1, '[{\"name\": \"Main Clinic\", \"address\": \"General Hospital\"}]', '[]'),
(13, 48, 'General Surgery', 'LIC-GEN-0048', 560, 'Experienced General Surgery specialist (جراحة عامة). Providing quality healthcare services.', 'default_doctor.png', 4.8, 405, 1, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(14, 49, 'Neurosurgery', 'LIC-NEU-0049', 520, 'Experienced Neurosurgery specialist (جراحة مخ وأعصاب). Providing quality healthcare services.', 'default_doctor.png', 4, 216, 0, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(15, 50, 'Plastic Surgery', 'LIC-PLA-0050', 845, 'Experienced Plastic Surgery specialist (تجميل). Providing quality healthcare services.', 'default_doctor.png', 4.6, 272, 1, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(16, 51, 'Vascular Surgery', 'LIC-VAS-0051', 656, 'Experienced Vascular Surgery specialist (جراحة أوعية دموية). Providing quality healthcare services.', 'default_doctor.png', 4.3, 267, 0, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(17, 52, 'Gastroenterology', 'LIC-GAS-0052', 386, 'Experienced Gastroenterology specialist (جهاز هضمي). Providing quality healthcare services.', 'default_doctor.png', 4.3, 283, 0, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(18, 53, 'Endocrinology', 'LIC-END-0053', 348, 'Experienced Endocrinology specialist (غدد صماء وسكري). Providing quality healthcare services.', 'default_doctor.png', 4.8, 256, 0, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(19, 54, 'Nephrology', 'LIC-NEP-0054', 424, 'Experienced Nephrology specialist (كلى). Providing quality healthcare services.', 'default_doctor.png', 4.5, 353, 0, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(20, 55, 'Pulmonology', 'LIC-PUL-0055', 358, 'Experienced Pulmonology specialist (صدر وجهاز تنفسي). Providing quality healthcare services.', 'default_doctor.png', 4.2, 75, 0, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(21, 56, 'Rheumatology', 'LIC-RHE-0056', 366, 'Experienced Rheumatology specialist (روماتيزم ومفاصل). Providing quality healthcare services.', 'default_doctor.png', 4.2, 402, 0, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(22, 57, 'Hematology', 'LIC-HEM-0057', 454, 'Experienced Hematology specialist (أمراض دم). Providing quality healthcare services.', 'default_doctor.png', 4.9, 419, 1, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(23, 58, 'Oncology', 'LIC-ONC-0058', 611, 'Experienced Oncology specialist (أورام). Providing quality healthcare services.', 'default_doctor.png', 4.1, 196, 0, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(24, 59, 'Neurology', 'LIC-NEU-0059', 396, 'Experienced Neurology specialist (مخ وأعصاب). Providing quality healthcare services.', 'default_doctor.png', 4, 380, 0, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(25, 60, 'Radiology', 'LIC-RAD-0060', 231, 'Experienced Radiology specialist (أشعة). Providing quality healthcare services.', 'default_doctor.png', 4.4, 323, 0, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(26, 61, 'Pathology', 'LIC-PAT-0061', 296, 'Experienced Pathology specialist (باثولوجي). Providing quality healthcare services.', 'default_doctor.png', 4.4, 309, 0, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(27, 62, 'Anesthesiology', 'LIC-ANE-0062', 497, 'Experienced Anesthesiology specialist (تخدير). Providing quality healthcare services.', 'default_doctor.png', 4.6, 144, 1, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(28, 63, 'Psychiatry', 'LIC-PSY-0063', 268, 'Experienced Psychiatry specialist (نفسية). Providing quality healthcare services.', 'default_doctor.png', 4.5, 301, 1, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(29, 64, 'Urology', 'LIC-URO-0064', 443, 'Experienced Urology specialist (مسالك بولية). Providing quality healthcare services.', 'default_doctor.png', 4.3, 420, 1, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(30, 65, 'ENT', 'LIC-ENT-0065', 258, 'Experienced ENT specialist (أنف وأذن وحنجرة). Providing quality healthcare services.', 'default_doctor.png', 4, 383, 1, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(31, 66, 'Obstetrics & Gynecology', 'LIC-OBS-0066', 267, 'Experienced Obstetrics & Gynecology specialist (نساء وتوليد). Providing quality healthcare services.', 'default_doctor.png', 4.7, 142, 1, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(32, 67, 'Emergency Medicine', 'LIC-EME-0067', 241, 'Experienced Emergency Medicine specialist (طوارئ). Providing quality healthcare services.', 'default_doctor.png', 4.4, 76, 0, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(33, 68, 'Family Medicine', 'LIC-FAM-0068', 269, 'Experienced Family Medicine specialist (طب أسرة). Providing quality healthcare services.', 'default_doctor.png', 4.6, 398, 1, '[{\"name\": \"Main Clinic\", \"address\": \"Cairo Medical Center\"}, {\"name\": \"Branch\", \"address\": \"Nasr City Healthcare\"}]', '[{\"day\": \"Sunday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Monday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Tuesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Wednesday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}, {\"day\": \"Thursday\", \"times\": [\"10:00\", \"11:00\", \"14:00\", \"15:00\"]}]'),
(35, 3, 'dentest', 'LIC-3-202602', 400, 'New doctor profile', 'default_doctor.png', 5, 0, 0, '[{\"name\": \"Main Clinic\", \"address\": \"General Hospital\"}]', '[]');

-- --------------------------------------------------------

--
-- Table structure for table `follow_up_appointments`
--

CREATE TABLE `follow_up_appointments` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `original_appointment_id` int(11) DEFAULT NULL,
  `scheduled_date` datetime NOT NULL,
  `reason` text DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `labs`
--

CREATE TABLE `labs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `license_number` varchar(100) DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `available_slots` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`available_slots`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `labs`
--

INSERT INTO `labs` (`id`, `user_id`, `name`, `address`, `license_number`, `rating`, `available_slots`) VALUES
(1, 4, 'Central Diagnostics Lab', '123 Science Dr.', 'LAB-4', 4.8, '{\"start\": \"09:00\", \"end\": \"20:00\", \"days\": [\"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\"]}'),
(2, 36, 'المختبر المركزي', '316 Aaron Land, Nasr City', 'LAB-14811', 4.4, '{\"start\": \"08:00\", \"end\": \"22:00\", \"days\": [\"Sun\", \"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Sat\"]}'),
(3, 37, 'معامل الشفاء', '439 Brown Tunnel, Heliopolis', 'LAB-14753', 4.1, '{\"start\": \"08:00\", \"end\": \"18:00\", \"days\": [\"Sun\", \"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Sat\"]}'),
(4, 38, 'مختبرات النور', '59 Cook Spring, Maadi', 'LAB-33908', 4.2, '{\"start\": \"07:00\", \"end\": \"22:00\", \"days\": [\"Sun\", \"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Sat\"]}'),
(5, 39, 'معامل الدقة', '516 Nancy Stravenue, Dokki', 'LAB-21465', 5, '{\"start\": \"09:00\", \"end\": \"18:00\", \"days\": [\"Sun\", \"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Sat\"]}'),
(6, 40, 'المختبر الطبي الحديث', '210 Fox Meadow, Zamalek', 'LAB-47568', 4.4, '{\"start\": \"08:00\", \"end\": \"18:00\", \"days\": [\"Sun\", \"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Sat\"]}'),
(7, 41, 'معامل الأمل', '828 Roberts Junction, New Cairo', 'LAB-53430', 4.9, '{\"start\": \"08:00\", \"end\": \"20:00\", \"days\": [\"Sun\", \"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Sat\"]}'),
(8, 42, 'مختبرات الصحة', '389 David Mews, 6th October', 'LAB-90033', 4.7, '{\"start\": \"08:00\", \"end\": \"18:00\", \"days\": [\"Sun\", \"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Sat\"]}'),
(9, 43, 'المعمل التخصصي', '116 William Rapids, Mohandessin', 'LAB-74388', 4.7, '{\"start\": \"09:00\", \"end\": \"20:00\", \"days\": [\"Sun\", \"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Sat\"]}'),
(10, 44, 'معامل الرعاية', '456 Robbins Estate, Downtown', 'LAB-66945', 4.9, '{\"start\": \"07:00\", \"end\": \"22:00\", \"days\": [\"Sun\", \"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Sat\"]}'),
(11, 45, 'مختبرات التشخيص', '307 Rhonda Extensions, Giza', 'LAB-34405', 4.2, '{\"start\": \"07:00\", \"end\": \"22:00\", \"days\": [\"Sun\", \"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Sat\"]}'),
(12, 69, 'معامل سمارت التخصصية', '15 شارع القصر العيني، القاهرة', 'LAB-2024-001', 5, '\"{\\\"days\\\": [\\\"Saturday\\\", \\\"Sunday\\\", \\\"Monday\\\", \\\"Tuesday\\\", \\\"Wednesday\\\", \\\"Thursday\\\"], \\\"start\\\": \\\"08:00\\\", \\\"end\\\": \\\"22:00\\\"}\"');

-- --------------------------------------------------------

--
-- Table structure for table `lab_appointments`
--

CREATE TABLE `lab_appointments` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `lab_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `appointment_date` datetime NOT NULL,
  `status` varchar(50) DEFAULT NULL,
  `result_file` varchar(255) DEFAULT NULL,
  `result_notes` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `lab_appointments`
--

INSERT INTO `lab_appointments` (`id`, `patient_id`, `lab_id`, `service_id`, `appointment_date`, `status`, `result_file`, `result_notes`, `created_at`) VALUES
(1, 1, 2, 7, '2026-02-19 10:00:00', 'Confirmed', NULL, NULL, '2026-02-19 01:48:33'),
(2, 1, 12, 62, '2026-02-19 18:00:00', 'Confirmed', NULL, NULL, '2026-02-19 13:27:14'),
(3, 1, 12, 93, '2026-02-21 17:00:00', 'Confirmed', NULL, NULL, '2026-02-20 14:09:12'),
(6, 1, 12, 94, '2026-02-21 10:00:00', 'Confirmed', NULL, NULL, '2026-02-21 00:05:51'),
(7, 1, 12, 94, '2026-02-21 11:00:00', 'Pending', NULL, NULL, '2026-02-21 00:06:04'),
(8, 1, 12, 93, '2026-02-21 13:00:00', 'Confirmed', NULL, NULL, '2026-02-21 00:24:17');

-- --------------------------------------------------------

--
-- Table structure for table `lab_services`
--

CREATE TABLE `lab_services` (
  `id` int(11) NOT NULL,
  `lab_id` int(11) NOT NULL,
  `test_type_id` int(11) NOT NULL,
  `price` float NOT NULL,
  `preparation_instructions` text DEFAULT NULL,
  `turnaround_time` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `lab_services`
--

INSERT INTO `lab_services` (`id`, `lab_id`, `test_type_id`, `price`, `preparation_instructions`, `turnaround_time`, `description`) VALUES
(1, 1, 1, 50, 'Fasting for 8 hours', '24 Hours', NULL),
(2, 1, 31, 120, 'Remove metal objects', '2 Hours', NULL),
(3, 1, 9, 75, 'Fasting required (10-12 hours)', '24 Hours', NULL),
(4, 1, 15, 60, 'None', '24 Hours', NULL),
(5, 1, 33, 450, 'Remove all metal. Notify if claustrophobic.', '48 Hours', NULL),
(6, 1, 25, 100, 'Nasal swab collection', '12 Hours', NULL),
(7, 2, 31, 480, 'Fasting for 8-12 hours', '2 Hours', NULL),
(8, 2, 25, 430, 'No special preparation needed', '24 Hours', NULL),
(9, 2, 9, 410, 'Bring ID and previous reports', '24 Hours', NULL),
(10, 3, 25, 230, 'Bring ID and previous reports', '2 Hours', NULL),
(11, 3, 1, 400, 'Fasting for 8-12 hours', '1 Week', NULL),
(12, 3, 9, 170, 'Remove metal objects', '24 Hours', NULL),
(13, 4, 15, 260, 'Bring ID and previous reports', '1 Week', NULL),
(14, 4, 33, 150, 'Bring ID and previous reports', '1 Week', NULL),
(15, 4, 9, 310, 'Fasting for 8-12 hours', '24 Hours', NULL),
(16, 5, 9, 360, 'Fasting for 8-12 hours', '48 Hours', NULL),
(17, 5, 33, 390, 'Fasting for 8-12 hours', '2 Hours', NULL),
(18, 6, 1, 390, 'Fasting for 8-12 hours', '48 Hours', NULL),
(19, 6, 33, 450, 'Remove metal objects', '2 Hours', NULL),
(20, 6, 15, 110, 'No special preparation needed', '24 Hours', NULL),
(21, 6, 9, 400, 'No special preparation needed', '1 Week', NULL),
(22, 7, 9, 360, 'No special preparation needed', '48 Hours', NULL),
(23, 7, 1, 110, 'Bring ID and previous reports', '24 Hours', NULL),
(24, 8, 15, 460, 'No special preparation needed', '2 Hours', NULL),
(25, 8, 33, 240, 'Fasting for 8-12 hours', '48 Hours', NULL),
(26, 9, 31, 350, 'Remove metal objects', '1 Week', NULL),
(27, 9, 15, 60, 'Bring ID and previous reports', '2 Hours', NULL),
(28, 9, 25, 80, 'No special preparation needed', '24 Hours', NULL),
(29, 10, 9, 170, 'Remove metal objects', '24 Hours', NULL),
(30, 10, 1, 50, 'Bring ID and previous reports', '24 Hours', NULL),
(31, 11, 25, 200, 'Remove metal objects', '48 Hours', NULL),
(32, 11, 9, 320, 'Bring ID and previous reports', '2 Hours', NULL),
(33, 12, 1, 150, NULL, '24-48 Hours', NULL),
(34, 12, 2, 150, NULL, '24-48 Hours', NULL),
(35, 12, 3, 150, NULL, '24-48 Hours', NULL),
(36, 12, 4, 150, NULL, '24-48 Hours', NULL),
(37, 12, 5, 150, NULL, '24-48 Hours', NULL),
(38, 12, 6, 150, NULL, '24-48 Hours', NULL),
(39, 12, 7, 150, NULL, '24-48 Hours', NULL),
(40, 12, 8, 150, NULL, '24-48 Hours', NULL),
(41, 12, 9, 150, NULL, '24-48 Hours', NULL),
(42, 12, 10, 150, NULL, '24-48 Hours', NULL),
(43, 12, 11, 150, NULL, '24-48 Hours', NULL),
(44, 12, 12, 150, NULL, '24-48 Hours', NULL),
(45, 12, 13, 150, NULL, '24-48 Hours', NULL),
(46, 12, 14, 150, NULL, '24-48 Hours', NULL),
(47, 12, 15, 150, NULL, '24-48 Hours', NULL),
(48, 12, 16, 150, NULL, '24-48 Hours', NULL),
(49, 12, 17, 150, NULL, '24-48 Hours', NULL),
(50, 12, 18, 150, NULL, '24-48 Hours', NULL),
(51, 12, 19, 150, NULL, '24-48 Hours', NULL),
(52, 12, 20, 150, NULL, '24-48 Hours', NULL),
(53, 12, 21, 150, NULL, '24-48 Hours', NULL),
(54, 12, 22, 150, NULL, '24-48 Hours', NULL),
(55, 12, 23, 150, NULL, '24-48 Hours', NULL),
(56, 12, 24, 150, NULL, '24-48 Hours', NULL),
(57, 12, 25, 150, NULL, '24-48 Hours', NULL),
(58, 12, 26, 150, NULL, '24-48 Hours', NULL),
(59, 12, 27, 150, NULL, '24-48 Hours', NULL),
(60, 12, 28, 150, NULL, '24-48 Hours', NULL),
(61, 12, 29, 150, NULL, '24-48 Hours', NULL),
(62, 12, 30, 150, NULL, '24-48 Hours', NULL),
(63, 12, 31, 150, NULL, '24-48 Hours', NULL),
(64, 12, 32, 150, NULL, '24-48 Hours', NULL),
(65, 12, 33, 150, NULL, '24-48 Hours', NULL),
(66, 12, 34, 150, NULL, '24-48 Hours', NULL),
(67, 12, 35, 150, NULL, '24-48 Hours', NULL),
(68, 12, 36, 150, NULL, '24-48 Hours', NULL),
(69, 12, 37, 150, NULL, '24-48 Hours', NULL),
(70, 12, 38, 150, NULL, '24-48 Hours', NULL),
(71, 12, 39, 150, NULL, '24-48 Hours', NULL),
(72, 12, 40, 150, NULL, '24-48 Hours', NULL),
(73, 12, 41, 150, NULL, '24-48 Hours', NULL),
(74, 12, 42, 150, NULL, '24-48 Hours', NULL),
(75, 12, 43, 150, NULL, '24-48 Hours', NULL),
(76, 12, 44, 150, NULL, '24-48 Hours', NULL),
(77, 12, 45, 150, NULL, '24-48 Hours', NULL),
(78, 12, 46, 150, NULL, '24-48 Hours', NULL),
(79, 12, 47, 150, NULL, '24-48 Hours', NULL),
(80, 12, 48, 150, NULL, '24-48 Hours', NULL),
(81, 12, 49, 150, NULL, '24-48 Hours', NULL),
(82, 12, 50, 150, NULL, '24-48 Hours', NULL),
(83, 12, 51, 150, NULL, '24-48 Hours', NULL),
(84, 12, 52, 150, NULL, '24-48 Hours', NULL),
(85, 12, 53, 150, NULL, '24-48 Hours', NULL),
(86, 12, 54, 150, NULL, '24-48 Hours', NULL),
(87, 12, 55, 150, NULL, '24-48 Hours', NULL),
(88, 12, 56, 150, NULL, '24-48 Hours', NULL),
(89, 12, 57, 150, NULL, '24-48 Hours', NULL),
(90, 12, 58, 150, NULL, '24-48 Hours', NULL),
(91, 12, 59, 150, NULL, '24-48 Hours', NULL),
(92, 12, 60, 150, NULL, '24-48 Hours', NULL),
(93, 12, 61, 150, NULL, '24-48 Hours', NULL),
(94, 12, 62, 150, NULL, '24-48 Hours', NULL),
(95, 12, 63, 150, NULL, '24-48 Hours', NULL),
(96, 1, 30, 500, '6', '12', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `lab_tests`
--

CREATE TABLE `lab_tests` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `doctor_id` int(11) DEFAULT NULL,
  `test_name` varchar(200) NOT NULL,
  `test_type` varchar(100) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `results` text DEFAULT NULL,
  `file_path` varchar(255) DEFAULT NULL,
  `ordered_date` datetime DEFAULT NULL,
  `completed_date` datetime DEFAULT NULL,
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `lab_tests`
--

INSERT INTO `lab_tests` (`id`, `patient_id`, `doctor_id`, `test_name`, `test_type`, `status`, `results`, `file_path`, `ordered_date`, `completed_date`, `notes`) VALUES
(48, 1, NULL, 'Uploaded: cbc_report_65_risk.pdf', 'report', 'completed', '{\"patient_summary\": {\"patient_name\": \"John Doe\", \"patient_id\": null, \"age\": 36, \"gender\": \"male\", \"pregnant\": false, \"test_date\": \"26-02-19\", \"lab_name\": \"Smart Healthcare Lab Report\"}, \"test_results\": {\"RBC\": {\"test_name\": \"RBC\", \"value\": 4.1, \"unit\": \"x10^6/\\u00b5L\", \"reference_range\": {\"min\": 4.5, \"max\": 5.9}, \"status\": \"Low\", \"deviation_percentage\": 8.89}, \"Hematocrit\": {\"test_name\": \"Hematocrit\", \"value\": 36.5, \"unit\": \"%\", \"reference_range\": {\"min\": 40.0, \"max\": 54.0}, \"status\": \"Low\", \"deviation_percentage\": 8.75}, \"MCV\": {\"test_name\": \"MCV\", \"value\": 79.0, \"unit\": \"fL\", \"reference_range\": {\"min\": 80.0, \"max\": 100.0}, \"status\": \"Low\", \"deviation_percentage\": 1.25}, \"MCH\": {\"test_name\": \"MCH\", \"value\": 25.5, \"unit\": \"pg\", \"reference_range\": {\"min\": 27.0, \"max\": 33.0}, \"status\": \"Low\", \"deviation_percentage\": 5.56}, \"MCHC\": {\"test_name\": \"MCHC\", \"value\": 31.2, \"unit\": \"g/dL\", \"reference_range\": {\"min\": 32.0, \"max\": 36.0}, \"status\": \"Low\", \"deviation_percentage\": 2.5}, \"WBC\": {\"test_name\": \"WBC\", \"value\": 11.8, \"unit\": \"x10^3/\\u00b5L\", \"reference_range\": {\"min\": 4.0, \"max\": 11.0}, \"status\": \"High\", \"deviation_percentage\": 7.27}, \"Platelets\": {\"test_name\": \"Platelets\", \"value\": 420.0, \"unit\": \"x10^3/\\u00b5L\", \"reference_range\": {\"min\": 150.0, \"max\": 400.0}, \"status\": \"High\", \"deviation_percentage\": 5.0}}, \"abnormal_parameters\": [{\"test_name\": \"RBC\", \"value\": 4.1, \"expected_range\": \"4.5 - 5.9\", \"status\": \"Low\", \"deviation_percentage\": 8.89, \"clinical_significance\": \"\\u0639\\u062f\\u062f \\u0643\\u0631\\u064a\\u0627\\u062a \\u0627\\u0644\\u062f\\u0645 \\u0627\\u0644\\u062d\\u0645\\u0631\\u0627\\u0621 \\u0642\\u0644\\u064a\\u0644 - \\u0645\\u0645\\u0643\\u0646 \\u062a\\u062d\\u0633 \\u0628\\u062a\\u0639\\u0628\"}, {\"test_name\": \"Hematocrit\", \"value\": 36.5, \"expected_range\": \"40.0 - 54.0\", \"status\": \"Low\", \"deviation_percentage\": 8.75, \"clinical_significance\": \"\\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\"}, {\"test_name\": \"WBC\", \"value\": 11.8, \"expected_range\": \"4.0 - 11.0\", \"status\": \"High\", \"deviation_percentage\": 7.27, \"clinical_significance\": \"\\u0645\\u0645\\u0643\\u0646 \\u064a\\u0643\\u0648\\u0646 \\u0641\\u064a\\u0647 \\u0639\\u062f\\u0648\\u0649 \\u0623\\u0648 \\u0627\\u0644\\u062a\\u0647\\u0627\\u0628 \\u0641\\u064a \\u0627\\u0644\\u062c\\u0633\\u0645\"}, {\"test_name\": \"MCH\", \"value\": 25.5, \"expected_range\": \"27.0 - 33.0\", \"status\": \"Low\", \"deviation_percentage\": 5.56, \"clinical_significance\": \"\\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\"}, {\"test_name\": \"Platelets\", \"value\": 420.0, \"expected_range\": \"150.0 - 400.0\", \"status\": \"High\", \"deviation_percentage\": 5.0, \"clinical_significance\": \"\\u0645\\u0645\\u0643\\u0646 \\u062e\\u0637\\u0631 \\u062a\\u062c\\u0644\\u0637 - \\u064a\\u062d\\u062a\\u0627\\u062c \\u0645\\u062a\\u0627\\u0628\\u0639\\u0629\"}, {\"test_name\": \"MCHC\", \"value\": 31.2, \"expected_range\": \"32.0 - 36.0\", \"status\": \"Low\", \"deviation_percentage\": 2.5, \"clinical_significance\": \"\\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\"}, {\"test_name\": \"MCV\", \"value\": 79.0, \"expected_range\": \"80.0 - 100.0\", \"status\": \"Low\", \"deviation_percentage\": 1.25, \"clinical_significance\": \"\\u0643\\u0631\\u064a\\u0627\\u062a \\u0627\\u0644\\u062f\\u0645 \\u0635\\u063a\\u064a\\u0631\\u0629 - \\u063a\\u0627\\u0644\\u0628\\u0627\\u064b \\u0646\\u0642\\u0635 \\u062d\\u062f\\u064a\\u062f\"}], \"risk_score\": 5, \"severity_level\": \"Low\", \"detected_patterns\": [{\"condition\": \"Possible Acute Infection or Inflammation\", \"confidence\": 70, \"supporting_findings\": [\"Elevated WBC (11.8 x10^3/\\u00b5L)\"], \"suggested_specialty\": \"Internal Medicine / \\u0627\\u0644\\u0628\\u0627\\u0637\\u0646\\u0629\", \"arabic_name\": \"\\u0627\\u062d\\u062a\\u0645\\u0627\\u0644 \\u0648\\u062c\\u0648\\u062f \\u0639\\u062f\\u0648\\u0649 \\u0623\\u0648 \\u0627\\u0644\\u062a\\u0647\\u0627\\u0628 \\u062d\\u0627\\u062f\"}], \"suggested_specialty\": \"Internal Medicine / \\u0627\\u0644\\u0628\\u0627\\u0637\\u0646\\u0629\", \"arabic_explanation\": \"\\ud83d\\udcca **\\u0634\\u0631\\u062d \\u0646\\u062a\\u064a\\u062c\\u0629 \\u0627\\u0644\\u062a\\u062d\\u0644\\u064a\\u0644**\\n\\n\\ud83d\\udccb **\\u0645\\u0644\\u062e\\u0635 \\u0627\\u0644\\u0646\\u062a\\u0627\\u0626\\u062c:**\\n\\u2022 \\u0625\\u062c\\u0645\\u0627\\u0644\\u064a \\u0627\\u0644\\u062a\\u062d\\u0627\\u0644\\u064a\\u0644: 7\\n\\u2022 \\u0637\\u0628\\u064a\\u0639\\u064a: 0 \\u2705\\n\\u2022 \\u063a\\u064a\\u0631 \\u0637\\u0628\\u064a\\u0639\\u064a: 7 \\u26a0\\ufe0f\\n\\n\\ud83d\\udd0d **\\u0627\\u0644\\u062a\\u062d\\u0627\\u0644\\u064a\\u0644 \\u0627\\u0644\\u0644\\u064a \\u0645\\u062d\\u062a\\u0627\\u062c\\u0629 \\u0627\\u0646\\u062a\\u0628\\u0627\\u0647:**\\n\\n\\u2022 **RBC**: 4.1\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 4.5 - 5.9)\\n  \\ud83d\\udca1 \\u0639\\u062f\\u062f \\u0643\\u0631\\u064a\\u0627\\u062a \\u0627\\u0644\\u062f\\u0645 \\u0627\\u0644\\u062d\\u0645\\u0631\\u0627\\u0621 \\u0642\\u0644\\u064a\\u0644 - \\u0645\\u0645\\u0643\\u0646 \\u062a\\u062d\\u0633 \\u0628\\u062a\\u0639\\u0628\\n\\n\\u2022 **Hematocrit**: 36.5\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 40.0 - 54.0)\\n  \\ud83d\\udca1 \\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\\n\\n\\u2022 **WBC**: 11.8\\n  \\ud83d\\udcc8 \\u0623\\u0639\\u0644\\u0649 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 4.0 - 11.0)\\n  \\ud83d\\udca1 \\u0645\\u0645\\u0643\\u0646 \\u064a\\u0643\\u0648\\u0646 \\u0641\\u064a\\u0647 \\u0639\\u062f\\u0648\\u0649 \\u0623\\u0648 \\u0627\\u0644\\u062a\\u0647\\u0627\\u0628 \\u0641\\u064a \\u0627\\u0644\\u062c\\u0633\\u0645\\n\\n\\u2022 **MCH**: 25.5\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 27.0 - 33.0)\\n  \\ud83d\\udca1 \\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\\n\\n\\u2022 **Platelets**: 420.0\\n  \\ud83d\\udcc8 \\u0623\\u0639\\u0644\\u0649 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 150.0 - 400.0)\\n  \\ud83d\\udca1 \\u0645\\u0645\\u0643\\u0646 \\u062e\\u0637\\u0631 \\u062a\\u062c\\u0644\\u0637 - \\u064a\\u062d\\u062a\\u0627\\u062c \\u0645\\u062a\\u0627\\u0628\\u0639\\u0629\\n\\n\\u2022 **MCHC**: 31.2\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 32.0 - 36.0)\\n  \\ud83d\\udca1 \\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\\n\\n\\u2022 **MCV**: 79.0\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 80.0 - 100.0)\\n  \\ud83d\\udca1 \\u0643\\u0631\\u064a\\u0627\\u062a \\u0627\\u0644\\u062f\\u0645 \\u0635\\u063a\\u064a\\u0631\\u0629 - \\u063a\\u0627\\u0644\\u0628\\u0627\\u064b \\u0646\\u0642\\u0635 \\u062d\\u062f\\u064a\\u062f\\n\\n\\ud83e\\udde0 **\\u0627\\u0644\\u062a\\u0642\\u064a\\u064a\\u0645 \\u0627\\u0644\\u0637\\u0628\\u064a \\u0627\\u0644\\u0645\\u0628\\u062f\\u0626\\u064a:**\\n\\n\\u2022 **\\u0627\\u062d\\u062a\\u0645\\u0627\\u0644 \\u0648\\u062c\\u0648\\u062f \\u0639\\u062f\\u0648\\u0649 \\u0623\\u0648 \\u0627\\u0644\\u062a\\u0647\\u0627\\u0628 \\u062d\\u0627\\u062f**\\n  \\ud83d\\udcca \\u0627\\u062d\\u062a\\u0645\\u0627\\u0644\\u064a\\u0629: 70%\\n  \\ud83d\\udd2c \\u0628\\u0646\\u0627\\u0621\\u064b \\u0639\\u0644\\u0649:\\n    - Elevated WBC (11.8 x10^3/\\u00b5L)\\n\\n\\u26a0\\ufe0f **\\u062a\\u0642\\u064a\\u064a\\u0645 \\u0627\\u0644\\u062e\\u0637\\u0648\\u0631\\u0629:** 5%\\n\\ud83d\\udcca **\\u0645\\u0633\\u062a\\u0648\\u0649 \\u0627\\u0644\\u062e\\u0637\\u0648\\u0631\\u0629:** \\u0645\\u0646\\u062e\\u0641\\u0636\\n\\n\\ud83d\\udc8a **\\u0627\\u0644\\u062a\\u0648\\u0635\\u064a\\u0627\\u062a:**\\n\\n\\u2022 \\u0631\\u0627\\u062c\\u0639 \\u062f\\u0643\\u062a\\u0648\\u0631 \\u0639\\u0627\\u062f\\u064a \\u0644\\u0644\\u0645\\u062a\\u0627\\u0628\\u0639\\u0629\\n\\u2022 \\u0645\\u0641\\u064a\\u0634 \\u062f\\u0627\\u0639\\u064a \\u0644\\u0644\\u0642\\u0644\\u0642\\u060c \\u0628\\u0633 \\u0645\\u062a\\u0627\\u0628\\u0639\\u0629 \\u0631\\u0648\\u062a\\u064a\\u0646\\u064a\\u0629\\n\\n\\ud83d\\udc68\\u200d\\u2695\\ufe0f **\\u0627\\u0644\\u062a\\u062e\\u0635\\u0635 \\u0627\\u0644\\u0645\\u0642\\u062a\\u0631\\u062d:** \\u0627\\u0644\\u0628\\u0627\\u0637\\u0646\\u0629\\n\\n\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\n\\u26a0\\ufe0f **\\u0645\\u0644\\u062d\\u0648\\u0638\\u0629 \\u0645\\u0647\\u0645\\u0629:**\\n\\u062f\\u0647 \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0623\\u0648\\u0644\\u064a \\u0628\\u064a\\u0633\\u0627\\u0639\\u062f\\u0643 \\u062a\\u0641\\u0647\\u0645 \\u0627\\u0644\\u0646\\u062a\\u064a\\u062c\\u0629\\u060c \\u0644\\u0643\\u0646 **\\u0645\\u0634 \\u0628\\u062f\\u064a\\u0644 \\u0639\\u0646 \\u0627\\u0633\\u062a\\u0634\\u0627\\u0631\\u0629 \\u0627\\u0644\\u062f\\u0643\\u062a\\u0648\\u0631**.\\n\\u0627\\u0644\\u062f\\u0643\\u062a\\u0648\\u0631 \\u0647\\u0648 \\u0627\\u0644\\u0644\\u064a \\u064a\\u0642\\u062f\\u0631 \\u064a\\u0634\\u062e\\u0635 \\u0648\\u064a\\u0639\\u0645\\u0644 \\u062e\\u0637\\u0629 \\u0639\\u0644\\u0627\\u062c \\u0645\\u0646\\u0627\\u0633\\u0628\\u0629 \\u0644\\u064a\\u0643.\\n\", \"english_summary\": \"\\ud83d\\udccb **COMPLETE BLOOD COUNT (CBC) ANALYSIS REPORT**\\n\\n**Patient Information:**\\nName: John Doe\\nAge: 36 years | Gender: Male\\nTest Date: 26-02-19\\n\\n**RESULTS SUMMARY:**\\nTotal Parameters Tested: 7\\nWithin Normal Range: 0\\nAbnormal Values: 7\\n\\n**ABNORMAL FINDINGS:**\\n\\n\\ud83d\\udcc8 **Elevated Values:**\\n\\u2022 WBC: 11.8 (Expected: 4.0 - 11.0)\\n\\u2022 Platelets: 420.0 (Expected: 150.0 - 400.0)\\n\\n\\ud83d\\udcc9 **Decreased Values:**\\n\\u2022 RBC: 4.1 (Expected: 4.5 - 5.9)\\n\\u2022 Hematocrit: 36.5 (Expected: 40.0 - 54.0)\\n\\u2022 MCH: 25.5 (Expected: 27.0 - 33.0)\\n\\u2022 MCHC: 31.2 (Expected: 32.0 - 36.0)\\n\\u2022 MCV: 79.0 (Expected: 80.0 - 100.0)\\n\\n**CLINICAL INTERPRETATION:**\\n\\n1. **Possible Acute Infection or Inflammation** (Confidence: 70%)\\n   Supporting Findings:\\n   \\u2022 Elevated WBC (11.8 x10^3/\\u00b5L)\\n   Suggested Specialty: Internal Medicine\\n\\n**RISK ASSESSMENT:**\\nCalculated Risk Score: 5/100\\nSeverity Level: Low\\n\\n**CLINICAL RECOMMENDATIONS:**\\n\\u2022 Schedule routine follow-up with primary care physician\\n\\u2022 Consider lifestyle modifications if applicable\\n\\n\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\n**IMPORTANT NOTICE:**\\nThis analysis is for informational purposes only and does not constitute\\nmedical advice, diagnosis, or treatment. Please consult with a qualified\\nhealthcare professional for proper medical evaluation and management.\\n\", \"recommendations\": [\"Schedule a routine follow-up with your doctor\", \"Monitor your symptoms\", \"Discuss possible acute infection or inflammation with your physician\"], \"visual_risk\": \"\\ud83d\\udfe2 Low Risk\\n\\u2588\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591 5%\"}', '1771497799.290599_cbc_report_65_risk.pdf', '2026-02-19 12:43:19', '2026-02-19 12:43:19', NULL),
(49, 1, NULL, 'Uploaded: high_risk_cbc.pdf', 'report', 'completed', '{\"patient_summary\": {\"patient_name\": \"John Doe\", \"patient_id\": null, \"age\": 36, \"gender\": \"male\", \"pregnant\": false, \"test_date\": \"26-02-19\", \"lab_name\": \"CITY MEDICAL LABORATORIES\"}, \"test_results\": {\"WBC\": {\"test_name\": \"WBC\", \"value\": 24.0, \"unit\": \"x10^3/\\u00b5L\", \"reference_range\": {\"min\": 4.0, \"max\": 11.0}, \"status\": \"Critical High\", \"deviation_percentage\": 118.18}, \"Platelets\": {\"test_name\": \"Platelets\", \"value\": 55.0, \"unit\": \"x10^3/\\u00b5L\", \"reference_range\": {\"min\": 150.0, \"max\": 400.0}, \"status\": \"Critical Low\", \"deviation_percentage\": 63.33}, \"RBC\": {\"test_name\": \"RBC\", \"value\": 3.1, \"unit\": \"x10^6/\\u00b5L\", \"reference_range\": {\"min\": 4.5, \"max\": 5.9}, \"status\": \"Critical Low\", \"deviation_percentage\": 31.11}, \"Hematocrit\": {\"test_name\": \"Hematocrit\", \"value\": 22.0, \"unit\": \"%\", \"reference_range\": {\"min\": 40.0, \"max\": 54.0}, \"status\": \"Critical Low\", \"deviation_percentage\": 45.0}, \"MCV\": {\"test_name\": \"MCV\", \"value\": 68.0, \"unit\": \"fL\", \"reference_range\": {\"min\": 80.0, \"max\": 100.0}, \"status\": \"Low\", \"deviation_percentage\": 15.0}, \"MCH\": {\"test_name\": \"MCH\", \"value\": 19.0, \"unit\": \"pg\", \"reference_range\": {\"min\": 27.0, \"max\": 33.0}, \"status\": \"Low\", \"deviation_percentage\": 29.63}, \"MCHC\": {\"test_name\": \"MCHC\", \"value\": 28.0, \"unit\": \"g/dL\", \"reference_range\": {\"min\": 32.0, \"max\": 36.0}, \"status\": \"Low\", \"deviation_percentage\": 12.5}}, \"abnormal_parameters\": [{\"test_name\": \"WBC\", \"value\": 24.0, \"expected_range\": \"4.0 - 11.0\", \"status\": \"Critical High\", \"deviation_percentage\": 118.18, \"clinical_significance\": \"\\u0645\\u0645\\u0643\\u0646 \\u064a\\u0643\\u0648\\u0646 \\u0641\\u064a\\u0647 \\u0639\\u062f\\u0648\\u0649 \\u0623\\u0648 \\u0627\\u0644\\u062a\\u0647\\u0627\\u0628 \\u0641\\u064a \\u0627\\u0644\\u062c\\u0633\\u0645\"}, {\"test_name\": \"Platelets\", \"value\": 55.0, \"expected_range\": \"150.0 - 400.0\", \"status\": \"Critical Low\", \"deviation_percentage\": 63.33, \"clinical_significance\": \"\\u062e\\u0637\\u0631 \\u0646\\u0632\\u064a\\u0641 - \\u062e\\u0644\\u064a \\u0628\\u0627\\u0644\\u0643 \\u0645\\u0646 \\u0627\\u0644\\u062c\\u0631\\u0648\\u062d\"}, {\"test_name\": \"Hematocrit\", \"value\": 22.0, \"expected_range\": \"40.0 - 54.0\", \"status\": \"Critical Low\", \"deviation_percentage\": 45.0, \"clinical_significance\": \"\\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\"}, {\"test_name\": \"RBC\", \"value\": 3.1, \"expected_range\": \"4.5 - 5.9\", \"status\": \"Critical Low\", \"deviation_percentage\": 31.11, \"clinical_significance\": \"\\u0639\\u062f\\u062f \\u0643\\u0631\\u064a\\u0627\\u062a \\u0627\\u0644\\u062f\\u0645 \\u0627\\u0644\\u062d\\u0645\\u0631\\u0627\\u0621 \\u0642\\u0644\\u064a\\u0644 - \\u0645\\u0645\\u0643\\u0646 \\u062a\\u062d\\u0633 \\u0628\\u062a\\u0639\\u0628\"}, {\"test_name\": \"MCH\", \"value\": 19.0, \"expected_range\": \"27.0 - 33.0\", \"status\": \"Low\", \"deviation_percentage\": 29.63, \"clinical_significance\": \"\\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\"}, {\"test_name\": \"MCV\", \"value\": 68.0, \"expected_range\": \"80.0 - 100.0\", \"status\": \"Low\", \"deviation_percentage\": 15.0, \"clinical_significance\": \"\\u0643\\u0631\\u064a\\u0627\\u062a \\u0627\\u0644\\u062f\\u0645 \\u0635\\u063a\\u064a\\u0631\\u0629 - \\u063a\\u0627\\u0644\\u0628\\u0627\\u064b \\u0646\\u0642\\u0635 \\u062d\\u062f\\u064a\\u062f\"}, {\"test_name\": \"MCHC\", \"value\": 28.0, \"expected_range\": \"32.0 - 36.0\", \"status\": \"Low\", \"deviation_percentage\": 12.5, \"clinical_significance\": \"\\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\"}], \"risk_score\": 63, \"severity_level\": \"High\", \"detected_patterns\": [{\"condition\": \"Possible Acute Infection or Inflammation\", \"confidence\": 90, \"supporting_findings\": [\"Significantly elevated WBC (24.0 x10^3/\\u00b5L)\"], \"suggested_specialty\": \"Internal Medicine / \\u0627\\u0644\\u0628\\u0627\\u0637\\u0646\\u0629\", \"arabic_name\": \"\\u0627\\u062d\\u062a\\u0645\\u0627\\u0644 \\u0648\\u062c\\u0648\\u062f \\u0639\\u062f\\u0648\\u0649 \\u0623\\u0648 \\u0627\\u0644\\u062a\\u0647\\u0627\\u0628 \\u062d\\u0627\\u062f\"}, {\"condition\": \"Thrombocytopenia - Bleeding Risk\", \"confidence\": 90, \"supporting_findings\": [\"Critically low platelet count (55.0 x10^3/\\u00b5L)\"], \"suggested_specialty\": \"Hematology / \\u0623\\u0645\\u0631\\u0627\\u0636 \\u0627\\u0644\\u062f\\u0645\", \"arabic_name\": \"\\u0646\\u0642\\u0635 \\u0627\\u0644\\u0635\\u0641\\u0627\\u0626\\u062d \\u0627\\u0644\\u062f\\u0645\\u0648\\u064a\\u0629 - \\u062e\\u0637\\u0631 \\u0627\\u0644\\u0646\\u0632\\u064a\\u0641\"}], \"suggested_specialty\": \"Internal Medicine / \\u0627\\u0644\\u0628\\u0627\\u0637\\u0646\\u0629\", \"arabic_explanation\": \"\\ud83d\\udcca **\\u0634\\u0631\\u062d \\u0646\\u062a\\u064a\\u062c\\u0629 \\u0627\\u0644\\u062a\\u062d\\u0644\\u064a\\u0644**\\n\\n\\ud83d\\udccb **\\u0645\\u0644\\u062e\\u0635 \\u0627\\u0644\\u0646\\u062a\\u0627\\u0626\\u062c:**\\n\\u2022 \\u0625\\u062c\\u0645\\u0627\\u0644\\u064a \\u0627\\u0644\\u062a\\u062d\\u0627\\u0644\\u064a\\u0644: 7\\n\\u2022 \\u0637\\u0628\\u064a\\u0639\\u064a: 0 \\u2705\\n\\u2022 \\u063a\\u064a\\u0631 \\u0637\\u0628\\u064a\\u0639\\u064a: 7 \\u26a0\\ufe0f\\n\\n\\ud83d\\udd0d **\\u0627\\u0644\\u062a\\u062d\\u0627\\u0644\\u064a\\u0644 \\u0627\\u0644\\u0644\\u064a \\u0645\\u062d\\u062a\\u0627\\u062c\\u0629 \\u0627\\u0646\\u062a\\u0628\\u0627\\u0647:**\\n\\n\\u2022 **WBC**: 24.0\\n  \\ud83d\\udcc8 \\u0623\\u0639\\u0644\\u0649 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 4.0 - 11.0)\\n  \\ud83d\\udca1 \\u0645\\u0645\\u0643\\u0646 \\u064a\\u0643\\u0648\\u0646 \\u0641\\u064a\\u0647 \\u0639\\u062f\\u0648\\u0649 \\u0623\\u0648 \\u0627\\u0644\\u062a\\u0647\\u0627\\u0628 \\u0641\\u064a \\u0627\\u0644\\u062c\\u0633\\u0645\\n\\n\\u2022 **Platelets**: 55.0\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 150.0 - 400.0)\\n  \\ud83d\\udca1 \\u062e\\u0637\\u0631 \\u0646\\u0632\\u064a\\u0641 - \\u062e\\u0644\\u064a \\u0628\\u0627\\u0644\\u0643 \\u0645\\u0646 \\u0627\\u0644\\u062c\\u0631\\u0648\\u062d\\n\\n\\u2022 **Hematocrit**: 22.0\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 40.0 - 54.0)\\n  \\ud83d\\udca1 \\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\\n\\n\\u2022 **RBC**: 3.1\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 4.5 - 5.9)\\n  \\ud83d\\udca1 \\u0639\\u062f\\u062f \\u0643\\u0631\\u064a\\u0627\\u062a \\u0627\\u0644\\u062f\\u0645 \\u0627\\u0644\\u062d\\u0645\\u0631\\u0627\\u0621 \\u0642\\u0644\\u064a\\u0644 - \\u0645\\u0645\\u0643\\u0646 \\u062a\\u062d\\u0633 \\u0628\\u062a\\u0639\\u0628\\n\\n\\u2022 **MCH**: 19.0\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 27.0 - 33.0)\\n  \\ud83d\\udca1 \\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\\n\\n\\u2022 **MCV**: 68.0\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 80.0 - 100.0)\\n  \\ud83d\\udca1 \\u0643\\u0631\\u064a\\u0627\\u062a \\u0627\\u0644\\u062f\\u0645 \\u0635\\u063a\\u064a\\u0631\\u0629 - \\u063a\\u0627\\u0644\\u0628\\u0627\\u064b \\u0646\\u0642\\u0635 \\u062d\\u062f\\u064a\\u062f\\n\\n\\u2022 **MCHC**: 28.0\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 32.0 - 36.0)\\n  \\ud83d\\udca1 \\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\\n\\n\\ud83e\\udde0 **\\u0627\\u0644\\u062a\\u0642\\u064a\\u064a\\u0645 \\u0627\\u0644\\u0637\\u0628\\u064a \\u0627\\u0644\\u0645\\u0628\\u062f\\u0626\\u064a:**\\n\\n\\u2022 **\\u0627\\u062d\\u062a\\u0645\\u0627\\u0644 \\u0648\\u062c\\u0648\\u062f \\u0639\\u062f\\u0648\\u0649 \\u0623\\u0648 \\u0627\\u0644\\u062a\\u0647\\u0627\\u0628 \\u062d\\u0627\\u062f**\\n  \\ud83d\\udcca \\u0627\\u062d\\u062a\\u0645\\u0627\\u0644\\u064a\\u0629: 90%\\n  \\ud83d\\udd2c \\u0628\\u0646\\u0627\\u0621\\u064b \\u0639\\u0644\\u0649:\\n    - Significantly elevated WBC (24.0 x10^3/\\u00b5L)\\n\\n\\u2022 **\\u0646\\u0642\\u0635 \\u0627\\u0644\\u0635\\u0641\\u0627\\u0626\\u062d \\u0627\\u0644\\u062f\\u0645\\u0648\\u064a\\u0629 - \\u062e\\u0637\\u0631 \\u0627\\u0644\\u0646\\u0632\\u064a\\u0641**\\n  \\ud83d\\udcca \\u0627\\u062d\\u062a\\u0645\\u0627\\u0644\\u064a\\u0629: 90%\\n  \\ud83d\\udd2c \\u0628\\u0646\\u0627\\u0621\\u064b \\u0639\\u0644\\u0649:\\n    - Critically low platelet count (55.0 x10^3/\\u00b5L)\\n\\n\\u26a0\\ufe0f **\\u062a\\u0642\\u064a\\u064a\\u0645 \\u0627\\u0644\\u062e\\u0637\\u0648\\u0631\\u0629:** 63%\\n\\ud83d\\udcca **\\u0645\\u0633\\u062a\\u0648\\u0649 \\u0627\\u0644\\u062e\\u0637\\u0648\\u0631\\u0629:** \\u0639\\u0627\\u0644\\u064a\\n\\n\\ud83d\\udc8a **\\u0627\\u0644\\u062a\\u0648\\u0635\\u064a\\u0627\\u062a:**\\n\\n\\u26a0\\ufe0f \\u064a\\u064f\\u0641\\u0636\\u0644 \\u062a\\u0631\\u0627\\u062c\\u0639 \\u062f\\u0643\\u062a\\u0648\\u0631 \\u0628\\u0633\\u0631\\u0639\\u0629\\n\\u2022 \\u0627\\u0644\\u0646\\u062a\\u0627\\u0626\\u062c \\u0645\\u062d\\u062a\\u0627\\u062c\\u0629 \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\\n\\n\\ud83d\\udc68\\u200d\\u2695\\ufe0f **\\u0627\\u0644\\u062a\\u062e\\u0635\\u0635 \\u0627\\u0644\\u0645\\u0642\\u062a\\u0631\\u062d:** \\u0627\\u0644\\u0628\\u0627\\u0637\\u0646\\u0629\\n\\n\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\n\\u26a0\\ufe0f **\\u0645\\u0644\\u062d\\u0648\\u0638\\u0629 \\u0645\\u0647\\u0645\\u0629:**\\n\\u062f\\u0647 \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0623\\u0648\\u0644\\u064a \\u0628\\u064a\\u0633\\u0627\\u0639\\u062f\\u0643 \\u062a\\u0641\\u0647\\u0645 \\u0627\\u0644\\u0646\\u062a\\u064a\\u062c\\u0629\\u060c \\u0644\\u0643\\u0646 **\\u0645\\u0634 \\u0628\\u062f\\u064a\\u0644 \\u0639\\u0646 \\u0627\\u0633\\u062a\\u0634\\u0627\\u0631\\u0629 \\u0627\\u0644\\u062f\\u0643\\u062a\\u0648\\u0631**.\\n\\u0627\\u0644\\u062f\\u0643\\u062a\\u0648\\u0631 \\u0647\\u0648 \\u0627\\u0644\\u0644\\u064a \\u064a\\u0642\\u062f\\u0631 \\u064a\\u0634\\u062e\\u0635 \\u0648\\u064a\\u0639\\u0645\\u0644 \\u062e\\u0637\\u0629 \\u0639\\u0644\\u0627\\u062c \\u0645\\u0646\\u0627\\u0633\\u0628\\u0629 \\u0644\\u064a\\u0643.\\n\", \"english_summary\": \"\\ud83d\\udccb **COMPLETE BLOOD COUNT (CBC) ANALYSIS REPORT**\\n\\n**Patient Information:**\\nName: John Doe\\nAge: 36 years | Gender: Male\\nTest Date: 26-02-19\\n\\n**RESULTS SUMMARY:**\\nTotal Parameters Tested: 7\\nWithin Normal Range: 0\\nAbnormal Values: 7\\n\\n**ABNORMAL FINDINGS:**\\n\\n\\ud83d\\udd34 **Critical Values:**\\n\\u2022 WBC: 24.0 (Expected: 4.0 - 11.0)\\n  Status: Critical High - Deviation: 118.2%\\n\\u2022 Platelets: 55.0 (Expected: 150.0 - 400.0)\\n  Status: Critical Low - Deviation: 63.3%\\n\\u2022 Hematocrit: 22.0 (Expected: 40.0 - 54.0)\\n  Status: Critical Low - Deviation: 45.0%\\n\\u2022 RBC: 3.1 (Expected: 4.5 - 5.9)\\n  Status: Critical Low - Deviation: 31.1%\\n\\n\\ud83d\\udcc9 **Decreased Values:**\\n\\u2022 MCH: 19.0 (Expected: 27.0 - 33.0)\\n\\u2022 MCV: 68.0 (Expected: 80.0 - 100.0)\\n\\u2022 MCHC: 28.0 (Expected: 32.0 - 36.0)\\n\\n**CLINICAL INTERPRETATION:**\\n\\n1. **Possible Acute Infection or Inflammation** (Confidence: 90%)\\n   Supporting Findings:\\n   \\u2022 Significantly elevated WBC (24.0 x10^3/\\u00b5L)\\n   Suggested Specialty: Internal Medicine\\n\\n2. **Thrombocytopenia - Bleeding Risk** (Confidence: 90%)\\n   Supporting Findings:\\n   \\u2022 Critically low platelet count (55.0 x10^3/\\u00b5L)\\n   Suggested Specialty: Hematology\\n\\n**RISK ASSESSMENT:**\\nCalculated Risk Score: 63/100\\nSeverity Level: High\\n\\n**CLINICAL RECOMMENDATIONS:**\\n\\u2022 Prompt medical evaluation recommended within 2-3 days\\n\\u2022 Further diagnostic testing likely required\\n\\n\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\n**IMPORTANT NOTICE:**\\nThis analysis is for informational purposes only and does not constitute\\nmedical advice, diagnosis, or treatment. Please consult with a qualified\\nhealthcare professional for proper medical evaluation and management.\\n\", \"recommendations\": [\"Seek medical attention within 2-3 days\", \"Do not delay consultation\", \"Some values are critical - prioritize medical evaluation\"], \"visual_risk\": \"\\ud83d\\udfe0 High Risk\\n\\u2588\\u2588\\u2588\\u2588\\u2588\\u2588\\u2588\\u2588\\u2588\\u2588\\u2588\\u2588\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591 63%\"}', '1771498702.086099_high_risk_cbc.pdf', '2026-02-19 12:58:22', '2026-02-19 12:58:22', NULL),
(50, 1, NULL, 'Uploaded: high_risk_cbc.pdf', 'report', 'completed', '{\"patient_summary\": {\"patient_name\": \"John Doe\", \"patient_id\": null, \"age\": 36, \"gender\": \"male\", \"pregnant\": false, \"test_date\": \"26-02-19\", \"lab_name\": \"CITY MEDICAL LABORATORIES\"}, \"test_results\": {\"WBC\": {\"test_name\": \"WBC\", \"value\": 24.0, \"unit\": \"x10^3/\\u00b5L\", \"reference_range\": {\"min\": 4.0, \"max\": 11.0}, \"status\": \"Critical High\", \"deviation_percentage\": 118.18}, \"Platelets\": {\"test_name\": \"Platelets\", \"value\": 55.0, \"unit\": \"x10^3/\\u00b5L\", \"reference_range\": {\"min\": 150.0, \"max\": 400.0}, \"status\": \"Critical Low\", \"deviation_percentage\": 63.33}, \"RBC\": {\"test_name\": \"RBC\", \"value\": 3.1, \"unit\": \"x10^6/\\u00b5L\", \"reference_range\": {\"min\": 4.5, \"max\": 5.9}, \"status\": \"Critical Low\", \"deviation_percentage\": 31.11}, \"Hematocrit\": {\"test_name\": \"Hematocrit\", \"value\": 22.0, \"unit\": \"%\", \"reference_range\": {\"min\": 40.0, \"max\": 54.0}, \"status\": \"Critical Low\", \"deviation_percentage\": 45.0}, \"MCV\": {\"test_name\": \"MCV\", \"value\": 68.0, \"unit\": \"fL\", \"reference_range\": {\"min\": 80.0, \"max\": 100.0}, \"status\": \"Low\", \"deviation_percentage\": 15.0}, \"MCH\": {\"test_name\": \"MCH\", \"value\": 19.0, \"unit\": \"pg\", \"reference_range\": {\"min\": 27.0, \"max\": 33.0}, \"status\": \"Low\", \"deviation_percentage\": 29.63}, \"MCHC\": {\"test_name\": \"MCHC\", \"value\": 28.0, \"unit\": \"g/dL\", \"reference_range\": {\"min\": 32.0, \"max\": 36.0}, \"status\": \"Low\", \"deviation_percentage\": 12.5}}, \"abnormal_parameters\": [{\"test_name\": \"WBC\", \"value\": 24.0, \"expected_range\": \"4.0 - 11.0\", \"status\": \"Critical High\", \"deviation_percentage\": 118.18, \"clinical_significance\": \"\\u0645\\u0645\\u0643\\u0646 \\u064a\\u0643\\u0648\\u0646 \\u0641\\u064a\\u0647 \\u0639\\u062f\\u0648\\u0649 \\u0623\\u0648 \\u0627\\u0644\\u062a\\u0647\\u0627\\u0628 \\u0641\\u064a \\u0627\\u0644\\u062c\\u0633\\u0645\"}, {\"test_name\": \"Platelets\", \"value\": 55.0, \"expected_range\": \"150.0 - 400.0\", \"status\": \"Critical Low\", \"deviation_percentage\": 63.33, \"clinical_significance\": \"\\u062e\\u0637\\u0631 \\u0646\\u0632\\u064a\\u0641 - \\u062e\\u0644\\u064a \\u0628\\u0627\\u0644\\u0643 \\u0645\\u0646 \\u0627\\u0644\\u062c\\u0631\\u0648\\u062d\"}, {\"test_name\": \"Hematocrit\", \"value\": 22.0, \"expected_range\": \"40.0 - 54.0\", \"status\": \"Critical Low\", \"deviation_percentage\": 45.0, \"clinical_significance\": \"\\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\"}, {\"test_name\": \"RBC\", \"value\": 3.1, \"expected_range\": \"4.5 - 5.9\", \"status\": \"Critical Low\", \"deviation_percentage\": 31.11, \"clinical_significance\": \"\\u0639\\u062f\\u062f \\u0643\\u0631\\u064a\\u0627\\u062a \\u0627\\u0644\\u062f\\u0645 \\u0627\\u0644\\u062d\\u0645\\u0631\\u0627\\u0621 \\u0642\\u0644\\u064a\\u0644 - \\u0645\\u0645\\u0643\\u0646 \\u062a\\u062d\\u0633 \\u0628\\u062a\\u0639\\u0628\"}, {\"test_name\": \"MCH\", \"value\": 19.0, \"expected_range\": \"27.0 - 33.0\", \"status\": \"Low\", \"deviation_percentage\": 29.63, \"clinical_significance\": \"\\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\"}, {\"test_name\": \"MCV\", \"value\": 68.0, \"expected_range\": \"80.0 - 100.0\", \"status\": \"Low\", \"deviation_percentage\": 15.0, \"clinical_significance\": \"\\u0643\\u0631\\u064a\\u0627\\u062a \\u0627\\u0644\\u062f\\u0645 \\u0635\\u063a\\u064a\\u0631\\u0629 - \\u063a\\u0627\\u0644\\u0628\\u0627\\u064b \\u0646\\u0642\\u0635 \\u062d\\u062f\\u064a\\u062f\"}, {\"test_name\": \"MCHC\", \"value\": 28.0, \"expected_range\": \"32.0 - 36.0\", \"status\": \"Low\", \"deviation_percentage\": 12.5, \"clinical_significance\": \"\\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\"}], \"risk_score\": 63, \"severity_level\": \"High\", \"detected_patterns\": [{\"condition\": \"Possible Acute Infection or Inflammation\", \"confidence\": 90, \"supporting_findings\": [\"Significantly elevated WBC (24.0 x10^3/\\u00b5L)\"], \"suggested_specialty\": \"Internal Medicine / \\u0627\\u0644\\u0628\\u0627\\u0637\\u0646\\u0629\", \"arabic_name\": \"\\u0627\\u062d\\u062a\\u0645\\u0627\\u0644 \\u0648\\u062c\\u0648\\u062f \\u0639\\u062f\\u0648\\u0649 \\u0623\\u0648 \\u0627\\u0644\\u062a\\u0647\\u0627\\u0628 \\u062d\\u0627\\u062f\"}, {\"condition\": \"Thrombocytopenia - Bleeding Risk\", \"confidence\": 90, \"supporting_findings\": [\"Critically low platelet count (55.0 x10^3/\\u00b5L)\"], \"suggested_specialty\": \"Hematology / \\u0623\\u0645\\u0631\\u0627\\u0636 \\u0627\\u0644\\u062f\\u0645\", \"arabic_name\": \"\\u0646\\u0642\\u0635 \\u0627\\u0644\\u0635\\u0641\\u0627\\u0626\\u062d \\u0627\\u0644\\u062f\\u0645\\u0648\\u064a\\u0629 - \\u062e\\u0637\\u0631 \\u0627\\u0644\\u0646\\u0632\\u064a\\u0641\"}], \"suggested_specialty\": \"Internal Medicine / \\u0627\\u0644\\u0628\\u0627\\u0637\\u0646\\u0629\", \"arabic_explanation\": \"\\ud83d\\udcca **\\u0634\\u0631\\u062d \\u0646\\u062a\\u064a\\u062c\\u0629 \\u0627\\u0644\\u062a\\u062d\\u0644\\u064a\\u0644**\\n\\n\\ud83d\\udccb **\\u0645\\u0644\\u062e\\u0635 \\u0627\\u0644\\u0646\\u062a\\u0627\\u0626\\u062c:**\\n\\u2022 \\u0625\\u062c\\u0645\\u0627\\u0644\\u064a \\u0627\\u0644\\u062a\\u062d\\u0627\\u0644\\u064a\\u0644: 7\\n\\u2022 \\u0637\\u0628\\u064a\\u0639\\u064a: 0 \\u2705\\n\\u2022 \\u063a\\u064a\\u0631 \\u0637\\u0628\\u064a\\u0639\\u064a: 7 \\u26a0\\ufe0f\\n\\n\\ud83d\\udd0d **\\u0627\\u0644\\u062a\\u062d\\u0627\\u0644\\u064a\\u0644 \\u0627\\u0644\\u0644\\u064a \\u0645\\u062d\\u062a\\u0627\\u062c\\u0629 \\u0627\\u0646\\u062a\\u0628\\u0627\\u0647:**\\n\\n\\u2022 **WBC**: 24.0\\n  \\ud83d\\udcc8 \\u0623\\u0639\\u0644\\u0649 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 4.0 - 11.0)\\n  \\ud83d\\udca1 \\u0645\\u0645\\u0643\\u0646 \\u064a\\u0643\\u0648\\u0646 \\u0641\\u064a\\u0647 \\u0639\\u062f\\u0648\\u0649 \\u0623\\u0648 \\u0627\\u0644\\u062a\\u0647\\u0627\\u0628 \\u0641\\u064a \\u0627\\u0644\\u062c\\u0633\\u0645\\n\\n\\u2022 **Platelets**: 55.0\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 150.0 - 400.0)\\n  \\ud83d\\udca1 \\u062e\\u0637\\u0631 \\u0646\\u0632\\u064a\\u0641 - \\u062e\\u0644\\u064a \\u0628\\u0627\\u0644\\u0643 \\u0645\\u0646 \\u0627\\u0644\\u062c\\u0631\\u0648\\u062d\\n\\n\\u2022 **Hematocrit**: 22.0\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 40.0 - 54.0)\\n  \\ud83d\\udca1 \\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\\n\\n\\u2022 **RBC**: 3.1\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 4.5 - 5.9)\\n  \\ud83d\\udca1 \\u0639\\u062f\\u062f \\u0643\\u0631\\u064a\\u0627\\u062a \\u0627\\u0644\\u062f\\u0645 \\u0627\\u0644\\u062d\\u0645\\u0631\\u0627\\u0621 \\u0642\\u0644\\u064a\\u0644 - \\u0645\\u0645\\u0643\\u0646 \\u062a\\u062d\\u0633 \\u0628\\u062a\\u0639\\u0628\\n\\n\\u2022 **MCH**: 19.0\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 27.0 - 33.0)\\n  \\ud83d\\udca1 \\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\\n\\n\\u2022 **MCV**: 68.0\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 80.0 - 100.0)\\n  \\ud83d\\udca1 \\u0643\\u0631\\u064a\\u0627\\u062a \\u0627\\u0644\\u062f\\u0645 \\u0635\\u063a\\u064a\\u0631\\u0629 - \\u063a\\u0627\\u0644\\u0628\\u0627\\u064b \\u0646\\u0642\\u0635 \\u062d\\u062f\\u064a\\u062f\\n\\n\\u2022 **MCHC**: 28.0\\n  \\ud83d\\udcc9 \\u0623\\u0642\\u0644 \\u0645\\u0646 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a (\\u0627\\u0644\\u0645\\u0641\\u0631\\u0648\\u0636: 32.0 - 36.0)\\n  \\ud83d\\udca1 \\u064a\\u062d\\u062a\\u0627\\u062c \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\\n\\n\\ud83e\\udde0 **\\u0627\\u0644\\u062a\\u0642\\u064a\\u064a\\u0645 \\u0627\\u0644\\u0637\\u0628\\u064a \\u0627\\u0644\\u0645\\u0628\\u062f\\u0626\\u064a:**\\n\\n\\u2022 **\\u0627\\u062d\\u062a\\u0645\\u0627\\u0644 \\u0648\\u062c\\u0648\\u062f \\u0639\\u062f\\u0648\\u0649 \\u0623\\u0648 \\u0627\\u0644\\u062a\\u0647\\u0627\\u0628 \\u062d\\u0627\\u062f**\\n  \\ud83d\\udcca \\u0627\\u062d\\u062a\\u0645\\u0627\\u0644\\u064a\\u0629: 90%\\n  \\ud83d\\udd2c \\u0628\\u0646\\u0627\\u0621\\u064b \\u0639\\u0644\\u0649:\\n    - Significantly elevated WBC (24.0 x10^3/\\u00b5L)\\n\\n\\u2022 **\\u0646\\u0642\\u0635 \\u0627\\u0644\\u0635\\u0641\\u0627\\u0626\\u062d \\u0627\\u0644\\u062f\\u0645\\u0648\\u064a\\u0629 - \\u062e\\u0637\\u0631 \\u0627\\u0644\\u0646\\u0632\\u064a\\u0641**\\n  \\ud83d\\udcca \\u0627\\u062d\\u062a\\u0645\\u0627\\u0644\\u064a\\u0629: 90%\\n  \\ud83d\\udd2c \\u0628\\u0646\\u0627\\u0621\\u064b \\u0639\\u0644\\u0649:\\n    - Critically low platelet count (55.0 x10^3/\\u00b5L)\\n\\n\\u26a0\\ufe0f **\\u062a\\u0642\\u064a\\u064a\\u0645 \\u0627\\u0644\\u062e\\u0637\\u0648\\u0631\\u0629:** 63%\\n\\ud83d\\udcca **\\u0645\\u0633\\u062a\\u0648\\u0649 \\u0627\\u0644\\u062e\\u0637\\u0648\\u0631\\u0629:** \\u0639\\u0627\\u0644\\u064a\\n\\n\\ud83d\\udc8a **\\u0627\\u0644\\u062a\\u0648\\u0635\\u064a\\u0627\\u062a:**\\n\\n\\u26a0\\ufe0f \\u064a\\u064f\\u0641\\u0636\\u0644 \\u062a\\u0631\\u0627\\u062c\\u0639 \\u062f\\u0643\\u062a\\u0648\\u0631 \\u0628\\u0633\\u0631\\u0639\\u0629\\n\\u2022 \\u0627\\u0644\\u0646\\u062a\\u0627\\u0626\\u062c \\u0645\\u062d\\u062a\\u0627\\u062c\\u0629 \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0637\\u0628\\u064a\\n\\n\\ud83d\\udc68\\u200d\\u2695\\ufe0f **\\u0627\\u0644\\u062a\\u062e\\u0635\\u0635 \\u0627\\u0644\\u0645\\u0642\\u062a\\u0631\\u062d:** \\u0627\\u0644\\u0628\\u0627\\u0637\\u0646\\u0629\\n\\n\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\n\\u26a0\\ufe0f **\\u0645\\u0644\\u062d\\u0648\\u0638\\u0629 \\u0645\\u0647\\u0645\\u0629:**\\n\\u062f\\u0647 \\u062a\\u0642\\u064a\\u064a\\u0645 \\u0623\\u0648\\u0644\\u064a \\u0628\\u064a\\u0633\\u0627\\u0639\\u062f\\u0643 \\u062a\\u0641\\u0647\\u0645 \\u0627\\u0644\\u0646\\u062a\\u064a\\u062c\\u0629\\u060c \\u0644\\u0643\\u0646 **\\u0645\\u0634 \\u0628\\u062f\\u064a\\u0644 \\u0639\\u0646 \\u0627\\u0633\\u062a\\u0634\\u0627\\u0631\\u0629 \\u0627\\u0644\\u062f\\u0643\\u062a\\u0648\\u0631**.\\n\\u0627\\u0644\\u062f\\u0643\\u062a\\u0648\\u0631 \\u0647\\u0648 \\u0627\\u0644\\u0644\\u064a \\u064a\\u0642\\u062f\\u0631 \\u064a\\u0634\\u062e\\u0635 \\u0648\\u064a\\u0639\\u0645\\u0644 \\u062e\\u0637\\u0629 \\u0639\\u0644\\u0627\\u062c \\u0645\\u0646\\u0627\\u0633\\u0628\\u0629 \\u0644\\u064a\\u0643.\\n\", \"english_summary\": \"\\ud83d\\udccb **COMPLETE BLOOD COUNT (CBC) ANALYSIS REPORT**\\n\\n**Patient Information:**\\nName: John Doe\\nAge: 36 years | Gender: Male\\nTest Date: 26-02-19\\n\\n**RESULTS SUMMARY:**\\nTotal Parameters Tested: 7\\nWithin Normal Range: 0\\nAbnormal Values: 7\\n\\n**ABNORMAL FINDINGS:**\\n\\n\\ud83d\\udd34 **Critical Values:**\\n\\u2022 WBC: 24.0 (Expected: 4.0 - 11.0)\\n  Status: Critical High - Deviation: 118.2%\\n\\u2022 Platelets: 55.0 (Expected: 150.0 - 400.0)\\n  Status: Critical Low - Deviation: 63.3%\\n\\u2022 Hematocrit: 22.0 (Expected: 40.0 - 54.0)\\n  Status: Critical Low - Deviation: 45.0%\\n\\u2022 RBC: 3.1 (Expected: 4.5 - 5.9)\\n  Status: Critical Low - Deviation: 31.1%\\n\\n\\ud83d\\udcc9 **Decreased Values:**\\n\\u2022 MCH: 19.0 (Expected: 27.0 - 33.0)\\n\\u2022 MCV: 68.0 (Expected: 80.0 - 100.0)\\n\\u2022 MCHC: 28.0 (Expected: 32.0 - 36.0)\\n\\n**CLINICAL INTERPRETATION:**\\n\\n1. **Possible Acute Infection or Inflammation** (Confidence: 90%)\\n   Supporting Findings:\\n   \\u2022 Significantly elevated WBC (24.0 x10^3/\\u00b5L)\\n   Suggested Specialty: Internal Medicine\\n\\n2. **Thrombocytopenia - Bleeding Risk** (Confidence: 90%)\\n   Supporting Findings:\\n   \\u2022 Critically low platelet count (55.0 x10^3/\\u00b5L)\\n   Suggested Specialty: Hematology\\n\\n**RISK ASSESSMENT:**\\nCalculated Risk Score: 63/100\\nSeverity Level: High\\n\\n**CLINICAL RECOMMENDATIONS:**\\n\\u2022 Prompt medical evaluation recommended within 2-3 days\\n\\u2022 Further diagnostic testing likely required\\n\\n\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\n**IMPORTANT NOTICE:**\\nThis analysis is for informational purposes only and does not constitute\\nmedical advice, diagnosis, or treatment. Please consult with a qualified\\nhealthcare professional for proper medical evaluation and management.\\n\", \"recommendations\": [\"Seek medical attention within 2-3 days\", \"Do not delay consultation\", \"Some values are critical - prioritize medical evaluation\"], \"visual_risk\": \"\\ud83d\\udfe0 High Risk\\n\\u2588\\u2588\\u2588\\u2588\\u2588\\u2588\\u2588\\u2588\\u2588\\u2588\\u2588\\u2588\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591 63%\"}', '1771624121.861199_high_risk_cbc.pdf', '2026-02-20 23:48:42', '2026-02-20 23:48:42', NULL),
(51, 1, NULL, 'Uploaded: sample_cbc.pdf', 'report', 'completed', '{\"patient_summary\": {\"patient_name\": \"John Doe\", \"patient_id\": null, \"age\": 36, \"gender\": \"male\", \"pregnant\": false, \"test_date\": \"26-02-19\", \"lab_name\": \"Smart Healthcare Lab Report\"}, \"test_results\": {\"RBC\": {\"test_name\": \"RBC\", \"value\": 4.8, \"unit\": \"x10^6/\\u00b5L\", \"reference_range\": {\"min\": 4.5, \"max\": 5.9}, \"status\": \"Normal\", \"deviation_percentage\": 0}, \"Hematocrit\": {\"test_name\": \"Hematocrit\", \"value\": 42.0, \"unit\": \"%\", \"reference_range\": {\"min\": 40.0, \"max\": 54.0}, \"status\": \"Normal\", \"deviation_percentage\": 0}, \"MCV\": {\"test_name\": \"MCV\", \"value\": 88.0, \"unit\": \"fL\", \"reference_range\": {\"min\": 80.0, \"max\": 100.0}, \"status\": \"Normal\", \"deviation_percentage\": 0}, \"MCH\": {\"test_name\": \"MCH\", \"value\": 29.0, \"unit\": \"pg\", \"reference_range\": {\"min\": 27.0, \"max\": 33.0}, \"status\": \"Normal\", \"deviation_percentage\": 0}, \"MCHC\": {\"test_name\": \"MCHC\", \"value\": 33.5, \"unit\": \"g/dL\", \"reference_range\": {\"min\": 32.0, \"max\": 36.0}, \"status\": \"Normal\", \"deviation_percentage\": 0}, \"WBC\": {\"test_name\": \"WBC\", \"value\": 6.8, \"unit\": \"x10^3/\\u00b5L\", \"reference_range\": {\"min\": 4.0, \"max\": 11.0}, \"status\": \"Normal\", \"deviation_percentage\": 0}, \"Platelets\": {\"test_name\": \"Platelets\", \"value\": 250.0, \"unit\": \"x10^3/\\u00b5L\", \"reference_range\": {\"min\": 150.0, \"max\": 400.0}, \"status\": \"Normal\", \"deviation_percentage\": 0}}, \"abnormal_parameters\": [], \"risk_score\": 0, \"severity_level\": \"Normal\", \"detected_patterns\": [], \"suggested_specialty\": null, \"arabic_explanation\": \"\\ud83d\\udcca **\\u0634\\u0631\\u062d \\u0646\\u062a\\u064a\\u062c\\u0629 \\u0627\\u0644\\u062a\\u062d\\u0644\\u064a\\u0644**\\n\\n\\u2705 **\\u0627\\u0644\\u062d\\u0645\\u062f \\u0644\\u0644\\u0647\\u060c \\u0643\\u0644 \\u0627\\u0644\\u062a\\u062d\\u0627\\u0644\\u064a\\u0644 \\u0637\\u0628\\u064a\\u0639\\u064a\\u0629!**\\n\\n\\ud83d\\udccb \\u062a\\u0645 \\u0641\\u062d\\u0635 7 \\u062a\\u062d\\u0644\\u064a\\u0644 \\u0648\\u0643\\u0644\\u0647\\u0645 \\u0641\\u064a \\u0627\\u0644\\u0645\\u0639\\u062f\\u0644 \\u0627\\u0644\\u0637\\u0628\\u064a\\u0639\\u064a.\\n\", \"english_summary\": \"\\ud83d\\udccb **COMPLETE BLOOD COUNT (CBC) ANALYSIS REPORT**\\n\\n**Patient Information:**\\nName: John Doe\\nAge: 36 years | Gender: Male\\nTest Date: 26-02-19\\n\\n**RESULTS SUMMARY:**\\nTotal Parameters Tested: 7\\nWithin Normal Range: 7\\nAbnormal Values: 0\\n\\n\\u2705 **All parameters within normal reference ranges.**\\nNo significant abnormalities detected.\\n\", \"recommendations\": [\"Continue regular health checkups\", \"Maintain a balanced diet and healthy lifestyle\"], \"visual_risk\": \"\\u2705 Normal\\n\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591\\u2591 0%\"}', '1771626008.844648_sample_cbc.pdf', '2026-02-21 00:20:09', '2026-02-21 00:20:09', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `lab_test_types`
--

CREATE TABLE `lab_test_types` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `lab_test_types`
--

INSERT INTO `lab_test_types` (`id`, `name`, `category`, `description`) VALUES
(1, 'CBC (Complete Blood Count)', 'Hematology', NULL),
(2, 'Hemoglobin A1c', 'Hematology', NULL),
(3, 'ESR (Erythrocyte Sedimentation Rate)', 'Hematology', NULL),
(4, 'Prothrombin Time (PT/INR)', 'Hematology', NULL),
(5, 'Iron Studies', 'Hematology', NULL),
(6, 'Vitamin B12 & Folate', 'Hematology', NULL),
(7, 'Comprehensive Metabolic Panel (CMP)', 'Biochemistry', NULL),
(8, 'Basic Metabolic Panel (BMP)', 'Biochemistry', NULL),
(9, 'Lipid Panel', 'Biochemistry', NULL),
(10, 'Liver Function Test (LFT)', 'Biochemistry', NULL),
(11, 'Kidney Function Test (KFT)', 'Biochemistry', NULL),
(12, 'Thyroid Function Test (TSH, T3, T4)', 'Biochemistry', NULL),
(13, 'Uric Acid', 'Biochemistry', NULL),
(14, 'C-Reactive Protein (CRP)', 'Biochemistry', NULL),
(15, 'Vitamin D Levels', 'Biochemistry', NULL),
(16, 'Electrolytes Panel', 'Biochemistry', NULL),
(17, 'Testosterone Total/Free', 'Hormones', NULL),
(18, 'Estrogen / Progesterone', 'Hormones', NULL),
(19, 'FSH & LH', 'Hormones', NULL),
(20, 'Cortisol Level', 'Hormones', NULL),
(21, 'Insulin Level', 'Hormones', NULL),
(22, 'PSA (Prostate Specific Antigen)', 'Tumor Markers', NULL),
(23, 'CA-125 (Ovarian Cancer Marker)', 'Tumor Markers', NULL),
(24, 'CEA (Carcinoembryonic Antigen)', 'Tumor Markers', NULL),
(25, 'PCR COVID-19', 'Microbiology', NULL),
(26, 'Urine Culture', 'Microbiology', NULL),
(27, 'Stool Analysis', 'Microbiology', NULL),
(28, 'Hepatitis Panel (A, B, C)', 'Serology', NULL),
(29, 'HIV Screen', 'Serology', NULL),
(30, 'Blood Culture', 'Microbiology', NULL),
(31, 'X-Ray Chest', 'Imaging', NULL),
(32, 'X-Ray Limbs (Arm/Leg)', 'Imaging', NULL),
(33, 'MRI Brain', 'Imaging', NULL),
(34, 'MRI Spine', 'Imaging', NULL),
(35, 'CT Scan Abdomen', 'Imaging', NULL),
(36, 'CT Scan Head', 'Imaging', NULL),
(37, 'Ultrasound Abdomen', 'Imaging', NULL),
(38, 'Echocardiogram', 'Cardiology', NULL),
(39, 'ECG / EKG', 'Cardiology', NULL),
(40, 'Urinalysis', 'Pathology', NULL),
(41, 'Pap Smear', 'Pathology', NULL),
(42, 'Biopsy (Tissue Analysis)', 'Pathology', NULL),
(43, 'Complete Blood Count (CBC)', 'Hematology', NULL),
(44, 'Lipid Profile', 'Biochemistry', NULL),
(45, 'Liver Function Tests (LFT)', 'Biochemistry', NULL),
(46, 'Kidney Function Tests (KFT)', 'Biochemistry', NULL),
(47, 'Fasting Blood Sugar', 'Biochemistry', NULL),
(48, 'HbA1c', 'Biochemistry', NULL),
(49, 'Thyroid Profile (TSH, FT3, FT4)', 'Endocrinology', NULL),
(50, 'Urine Analysis', 'General', NULL),
(51, 'Vitamin D', 'Biochemistry', NULL),
(52, 'Vitamin B12', 'Biochemistry', NULL),
(53, 'Sodium / Potassium / Chloride', 'Electrolytes', NULL),
(54, 'ESR', 'Hematology', NULL),
(55, 'Ferritin', 'Hematology', NULL),
(56, 'Iron Profile', 'Hematology', NULL),
(57, 'Calcium (Total / Ionized)', 'Biochemistry', NULL),
(58, 'Hepatitis B & C Screening', 'Serology', NULL),
(59, 'HIV Screening', 'Serology', NULL),
(60, 'Pregnancy Test (Beta-HCG)', 'Serology', NULL),
(61, 'CA-125', 'Tumor Markers', NULL),
(62, 'CEA', 'Tumor Markers', NULL),
(63, 'Blood Group & RH', 'Hematology', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `medical_files`
--

CREATE TABLE `medical_files` (
  `id` int(11) NOT NULL,
  `history_id` int(11) NOT NULL,
  `file_type` varchar(20) DEFAULT NULL,
  `file_path` varchar(255) NOT NULL,
  `uploaded_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `medical_history`
--

CREATE TABLE `medical_history` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `doctor_id` int(11) DEFAULT NULL,
  `diagnosis` text NOT NULL,
  `notes` text DEFAULT NULL,
  `risk_level` varchar(50) DEFAULT NULL,
  `specialty_suggested` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `medical_reports`
--

CREATE TABLE `medical_reports` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `doctor_id` int(11) DEFAULT NULL,
  `report_type` varchar(50) DEFAULT NULL,
  `title` varchar(200) NOT NULL,
  `description` text DEFAULT NULL,
  `diagnosis` text DEFAULT NULL,
  `recommendations` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `deletion_requested` tinyint(1) DEFAULT NULL,
  `deletion_reason` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `medical_reports`
--

INSERT INTO `medical_reports` (`id`, `patient_id`, `doctor_id`, `report_type`, `title`, `description`, `diagnosis`, `recommendations`, `created_at`, `deletion_requested`, `deletion_reason`) VALUES
(1, 2, 3, 'consultation', 'Consultation for الأنفلونزا الحادة (Severe Flu)', 'Eius natus distinctio beatae. Laudantium dolore aspernatur numquam minima. Quaerat esse dignissimos earum veritatis aspernatur iure beatae. Deserunt enim assumenda cumque debitis incidunt sapiente.', 'الأنفلونزا الحادة (Severe Flu)', 'Fuga deleniti quod expedita ipsum temporibus sed. Quidem doloremque saepe. Exercitationem fugit odio amet fuga rem.', '2025-12-27 16:29:05', 0, NULL),
(2, 2, 3, 'diagnosis', 'Consultation for ارتفاع ضغط الدم (Hypertension)', 'Reiciendis earum ducimus illo iste consequatur. Expedita atque repudiandae voluptates placeat delectus.\nIpsum recusandae optio perferendis.', 'ارتفاع ضغط الدم (Hypertension)', 'Voluptates maxime accusamus eius illo ipsum. Ullam corrupti facere beatae nisi mollitia.', '2025-12-27 16:29:05', 0, NULL),
(5, 4, 3, 'diagnosis', 'Consultation for السكري النوع الثاني (Type 2 Diabetes)', 'Reprehenderit distinctio alias quidem voluptas ad. Ut optio totam expedita vero in.\nDoloribus eos architecto laboriosam. Fugit et quo saepe mollitia. Neque debitis tempore corrupti error quos beatae.', 'السكري النوع الثاني (Type 2 Diabetes)', 'Delectus eligendi laboriosam pariatur occaecati id. Autem perspiciatis quae dolore eveniet numquam. Dolore quibusdam excepturi rerum itaque repudiandae cumque.', '2025-12-27 16:29:05', 0, NULL),
(6, 4, 3, 'consultation', 'Consultation for التهاب المفاصل (Arthritis)', 'Ipsa ipsa distinctio a. Voluptate odio eos excepturi assumenda. Rerum rem odit error optio aut.\nMaxime fugiat possimus sed nulla quae.', 'التهاب المفاصل (Arthritis)', 'Praesentium asperiores est quam in rerum. Atque odit totam odit commodi placeat tempora placeat. Debitis autem ipsum saepe optio aspernatur aperiam.', '2025-12-27 16:29:05', 0, NULL),
(7, 5, 3, 'diagnosis', 'Consultation for التهاب المفاصل (Arthritis)', 'Sunt eum quidem facilis deserunt. Minima beatae voluptatem omnis cupiditate quidem.\nExplicabo rem sed aperiam. Deserunt illo iure occaecati quidem ipsum reprehenderit.', 'التهاب المفاصل (Arthritis)', 'Ullam voluptatum vitae accusamus. Hic aliquam eaque adipisci ex consectetur sapiente mollitia. Error a asperiores amet libero delectus culpa.', '2025-12-27 16:29:05', 0, NULL),
(8, 5, 3, 'consultation', 'Consultation for كسر في الساق (Leg Fracture)', 'Nulla tenetur error exercitationem quaerat. Est reiciendis optio aliquid unde perspiciatis. Impedit fugiat in voluptate cupiditate.', 'كسر في الساق (Leg Fracture)', 'Ad a natus voluptatum exercitationem nobis minima adipisci. Facilis inventore asperiores illum suscipit quas itaque reiciendis.', '2025-12-27 16:29:05', 0, NULL),
(9, 5, 3, 'consultation', 'Consultation for السكري النوع الثاني (Type 2 Diabetes)', 'Eligendi quos nostrum ratione aut.\nNatus ad ipsam a quaerat ex. Animi tempore vel cupiditate. Deserunt asperiores nesciunt dolor ab.', 'السكري النوع الثاني (Type 2 Diabetes)', 'Cupiditate ut sunt autem inventore. Illo esse a error harum praesentium aperiam.', '2025-12-27 16:29:05', 0, NULL),
(10, 6, 2, 'diagnosis', 'Consultation for صداع نصفي (Migraine)', 'Illo suscipit aliquid qui commodi illo tenetur.\nOptio quia quae. Aspernatur quasi reprehenderit eius blanditiis labore quae. Vero soluta illo veniam consequuntur voluptatem ducimus error.', 'صداع نصفي (Migraine)', 'Assumenda voluptatibus cupiditate maxime illo magnam. Nam eveniet earum itaque. Temporibus magni consequatur ducimus occaecati.', '2025-12-27 16:29:05', 0, NULL),
(15, 9, 10, 'consultation', 'Consultation for صداع نصفي (Migraine)', 'Excepturi debitis magnam quae laboriosam saepe. Accusantium adipisci ea minus sequi illum.\nNecessitatibus voluptatem explicabo amet enim. Ex tenetur quae. Quod soluta quasi maxime error.', 'صداع نصفي (Migraine)', 'Et dolores repellat. Error minus cumque iusto dolor. Minus modi laborum nemo officia ea.', '2025-12-27 16:29:05', 0, NULL),
(16, 9, 10, 'consultation', 'Consultation for صداع نصفي (Migraine)', 'Aut hic ipsum exercitationem magnam tempore illum tenetur. Fugit consectetur officiis sunt consequatur voluptas. Explicabo illum suscipit et vel consequatur culpa nemo.', 'صداع نصفي (Migraine)', 'Aperiam maxime quae.', '2025-12-27 16:29:05', 0, NULL),
(17, 9, 10, 'consultation', 'Consultation for الأنفلونزا الحادة (Severe Flu)', 'Quas vel minus possimus iste harum omnis. Necessitatibus vero aspernatur molestiae laboriosam enim veritatis. Totam corporis fugiat repellendus.\nAt quam cumque consequuntur.', 'الأنفلونزا الحادة (Severe Flu)', 'Amet ipsam reprehenderit tenetur nesciunt consectetur. Consequatur voluptatem ex dignissimos id occaecati magnam iure. Deleniti occaecati eum magni occaecati.', '2025-12-27 16:29:05', 0, NULL),
(18, 10, 5, 'diagnosis', 'Consultation for صداع نصفي (Migraine)', 'Perferendis deleniti quaerat qui aliquam. At dolores ipsam ex illum error doloribus unde. Ea distinctio illo debitis error.', 'صداع نصفي (Migraine)', 'Deserunt voluptates magni perspiciatis vero.', '2025-12-27 16:29:05', 0, NULL),
(19, 11, 6, 'diagnosis', 'Consultation for الربو (Asthma)', 'Fugit voluptates quidem accusantium inventore voluptate. Molestias ipsam officiis nostrum labore repudiandae.', 'الربو (Asthma)', 'Mollitia deserunt totam blanditiis hic modi. Cumque iusto mollitia possimus ea.', '2025-12-27 16:29:05', 0, NULL),
(20, 11, 6, 'consultation', 'Consultation for كسر في الساق (Leg Fracture)', 'Quae ipsum repellendus harum laudantium. Sit at aspernatur provident earum. Id nobis non corporis exercitationem asperiores cum excepturi.', 'كسر في الساق (Leg Fracture)', 'Ipsa maiores sapiente aperiam enim rerum mollitia. Omnis ea numquam tempora atque assumenda. Odio voluptatibus culpa dolor aspernatur dolorem reiciendis.', '2025-12-27 16:29:05', 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `medications`
--

CREATE TABLE `medications` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `active_ingredient` varchar(100) NOT NULL,
  `side_effects` text DEFAULT NULL,
  `contraindications` text DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `medications`
--

INSERT INTO `medications` (`id`, `name`, `active_ingredient`, `side_effects`, `contraindications`, `quantity`, `price`, `created_at`) VALUES
(1, 'Panadol Advance', 'Paracetamol', 'Nausea, allergic reaction.', NULL, 8, 25, '2026-02-09 23:12:36'),
(2, 'Adol', 'Paracetamol', 'Stomach pain, loss of appetite.', NULL, 10, 15, '2026-02-09 23:12:36'),
(3, 'Brufen 400mg', 'Ibuprofen', 'Heartburn, nausea.', NULL, 10, 30, '2026-02-09 23:12:36'),
(4, 'Ibu-Care', 'Ibuprofen', 'Upset stomach, mild heartburn, nausea, vomiting.', NULL, 25, 22, '2026-02-09 23:12:36'),
(5, 'Augmentin 1g', 'Amoxicillin/Clavulanate', 'Diarrhea, rash.', NULL, 9, 130, '2026-02-09 23:12:36'),
(6, 'Curam 1g', 'Amoxicillin/Clavulanate', 'Indigestion.', NULL, 10, 120, '2026-02-09 23:12:36'),
(7, 'Concor 5mg', 'Bisoprolol', 'Fatigue, cold extremities.', NULL, 10, 55, '2026-02-09 23:12:36'),
(8, 'Bisocard 5mg', 'Bisoprolol', 'Dizziness.', NULL, 10, 40, '2026-02-09 23:12:36'),
(9, 'Voltaren 50mg', 'Diclofenac Sodium', 'Dizziness, stomach pain.', NULL, 10, 50, '2026-02-09 23:19:22'),
(10, 'Cataflam 50mg', 'Diclofenac Potassium', 'Stomach irritation.', NULL, 10, 45, '2026-02-09 23:19:22'),
(11, 'Zithromax 500mg', 'Azithromycin', 'Vomiting, headache.', NULL, 10, 95, '2026-02-09 23:19:22'),
(12, 'Klacid 500mg', 'Clarithromycin', 'Metallic taste.', NULL, 10, 160, '2026-02-09 23:19:22'),
(13, 'Ciprobay 500mg', 'Ciprofloxacin', 'Dizziness, nausea.', NULL, 10, 110, '2026-02-09 23:19:22'),
(14, 'Exforge 10/160', 'Amlodipine/Valsartan', 'Ankle swelling.', NULL, 10, 280, '2026-02-09 23:19:22'),
(15, 'Zestril 10mg', 'Lisinopril', 'Dry cough.', NULL, 10, 65, '2026-02-09 23:19:22'),
(16, 'Plavix 75mg', 'Clopidogrel', 'Bleeding risk.', NULL, 10, 320, '2026-02-09 23:19:22'),
(17, 'Glucophage 1000mg', 'Metformin', 'Diarrhea, gas.', NULL, 10, 40, '2026-02-09 23:19:22'),
(18, 'Diamicron MR 60mg', 'Gliclazide', 'Hypoglycemia.', NULL, 10, 65, '2026-02-09 23:19:22'),
(19, 'Januvia 100mg', 'Sitagliptin', 'Headache.', NULL, 10, 420, '2026-02-09 23:19:22'),
(20, 'Controloc 40mg', 'Pantoprazole', 'Headache.', NULL, 10, 105, '2026-02-09 23:19:22'),
(21, 'Antodine 40mg', 'Famotidine', 'Dizziness.', NULL, 10, 35, '2026-02-09 23:19:22'),
(22, 'Gaviscon liquid', 'Sodium Alginate', 'Mild bloating.', NULL, 10, 70, '2026-02-09 23:19:22'),
(23, 'Nexium 40mg', 'Esomeprazole', 'Dry mouth.', NULL, 10, 195, '2026-02-09 23:19:22'),
(24, 'Ventolin Inhaler', 'Salbutamol', 'Tremor, palpitation.', NULL, 10, 70, '2026-02-09 23:19:22'),
(25, 'Flixotide Inhaler', 'Fluticasone', 'Hoarseness, thrush.', NULL, 10, 140, '2026-02-09 23:19:22'),
(26, 'Zyrtec 10mg', 'Cetirizine', 'Drowsiness.', NULL, 10, 40, '2026-02-09 23:19:22'),
(27, 'Claritine 10mg', 'Loratadine', 'Headache.', NULL, 10, 45, '2026-02-09 23:19:22'),
(28, 'Neuroton', 'Vitamin B1, B6, B12', 'Mild nausea.', NULL, 10, 30, '2026-02-09 23:19:22'),
(29, 'Osteocare', 'Calcium, Magnesium, Zinc, Vit D', 'Constipation.', NULL, 10, 80, '2026-02-09 23:19:22'),
(30, 'Centrum Adults', 'Multivitamins', 'Upset stomach.', NULL, 10, 450, '2026-02-09 23:19:22'),
(31, 'Panadol Joint', 'Paracetamol', 'Drowsiness, liver issues if overdosed.', NULL, 10, 35, '2026-02-09 23:22:21'),
(32, 'Panadol Extra', 'Paracetamol/Caffeine', 'Insomnia, jitters.', NULL, 10, 28, '2026-02-09 23:22:21'),
(33, 'Adol 500mg', 'Paracetamol', 'Stomach pain.', NULL, 10, 18, '2026-02-09 23:22:21'),
(34, 'Abimol', 'Paracetamol', 'Allergy symptoms.', NULL, 10, 30, '2026-02-09 23:22:21'),
(35, 'Brufen 600mg', 'Ibuprofen', 'Stomach upset, ulcers.', NULL, 10, 40, '2026-02-09 23:22:21'),
(36, 'Voltaren 100mg Retard', 'Diclofenac Sodium', 'Gastritis, headache.', NULL, 10, 75, '2026-02-09 23:22:21'),
(37, 'Catafast 50mg', 'Diclofenac Potassium', 'Nausea.', NULL, 10, 55, '2026-02-09 23:22:21'),
(38, 'Antiflam 50mg', 'Diclofenac Potassium', 'Dizziness.', NULL, 10, 40, '2026-02-09 23:22:21'),
(39, 'Dolphin 50mg', 'Diclofenac Sodium', 'Upset stomach.', NULL, 10, 35, '2026-02-09 23:22:21'),
(40, 'Aspirin Protect', 'Aspirin', 'Bleeding risk, stomach pain.', NULL, 10, 25, '2026-02-09 23:22:21'),
(41, 'Jusprin 81mg', 'Aspirin', 'Bruising.', NULL, 10, 20, '2026-02-09 23:22:21'),
(42, 'Augmentin 625mg', 'Amoxicillin/Clavulanate', 'Nausea.', NULL, 10, 90, '2026-02-09 23:22:21'),
(43, 'Hibiotic 1g', 'Amoxicillin/Clavulanate', 'Upset stomach.', NULL, 10, 110, '2026-02-09 23:22:21'),
(44, 'Megamox 1g', 'Amoxicillin/Clavulanate', 'Mild diarrhea.', NULL, 10, 115, '2026-02-09 23:22:21'),
(45, 'Flumox 500mg', 'Amoxicillin/Flucloxacillin', 'Rash, nausea.', NULL, 10, 45, '2026-02-09 23:22:21'),
(46, 'Flumox 1g', 'Amoxicillin/Flucloxacillin', 'Diarrhea.', NULL, 10, 80, '2026-02-09 23:22:21'),
(47, 'Xithrone 500mg', 'Azithromycin', 'Loose stools.', NULL, 10, 85, '2026-02-09 23:22:21'),
(48, 'Zisrocin 500mg', 'Azithromycin', 'Abdominal pain.', NULL, 10, 75, '2026-02-09 23:22:21'),
(49, 'Serviflox 500mg', 'Ciprofloxacin', 'Joint pain.', NULL, 10, 80, '2026-02-09 23:22:21'),
(50, 'Tavanic 500mg', 'Levofloxacin', 'Insomnia, nausea.', NULL, 10, 180, '2026-02-09 23:22:21'),
(51, 'Levoxin 500mg', 'Levofloxacin', 'Tendon pain.', NULL, 10, 140, '2026-02-09 23:22:21'),
(52, 'Claribiotic 500mg', 'Clarithromycin', 'Headache.', NULL, 10, 130, '2026-02-09 23:22:21'),
(53, 'Flagyl 500mg', 'Metronidazole', 'Dizziness, nausea.', NULL, 10, 35, '2026-02-09 23:22:21'),
(54, 'Amrizole 500mg', 'Metronidazole', 'Metallic taste.', NULL, 10, 25, '2026-02-09 23:22:21'),
(55, 'Concor 2.5mg', 'Bisoprolol', 'Slow heart rate.', NULL, 10, 45, '2026-02-09 23:22:21'),
(56, 'Zestril 20mg', 'Lisinopril', 'Hypotension.', NULL, 10, 90, '2026-02-09 23:22:21'),
(57, 'Capoten 25mg', 'Captopril', 'Cough, skin rash.', NULL, 10, 30, '2026-02-09 23:22:21'),
(58, 'Exforge 5/160', 'Amlodipine/Valsartan', 'Dizziness.', NULL, 10, 260, '2026-02-09 23:22:21'),
(59, 'Norvasc 5mg', 'Amlodipine', 'Headache, edema.', NULL, 10, 120, '2026-02-09 23:22:21'),
(60, 'Amlodipine 5mg', 'Amlodipine', 'Fatigue.', NULL, 10, 60, '2026-02-09 23:22:21'),
(61, 'Thrombo 75mg', 'Clopidogrel', 'Bruising.', NULL, 10, 150, '2026-02-09 23:22:21'),
(62, 'Lipitor 20mg', 'Atorvastatin', 'Muscle pain, liver issues.', NULL, 10, 210, '2026-02-09 23:22:21'),
(63, 'Ator 20mg', 'Atorvastatin', 'Leg cramps.', NULL, 10, 90, '2026-02-09 23:22:21'),
(64, 'Crestor 10mg', 'Rosuvastatin', 'Weakness.', NULL, 10, 190, '2026-02-09 23:22:21'),
(65, 'Rosuvast 10mg', 'Rosuvastatin', 'Nausea.', NULL, 10, 120, '2026-02-09 23:22:21'),
(66, 'Glucophage 500mg', 'Metformin', 'Nausea.', NULL, 10, 25, '2026-02-09 23:22:21'),
(67, 'Janumet 50/1000', 'Sitagliptin/Metformin', 'Diarrhea, nausea.', NULL, 10, 450, '2026-02-09 23:22:21'),
(68, 'Forxiga 10mg', 'Dapagliflozin', 'Thirst, UTIs.', NULL, 10, 380, '2026-02-09 23:22:21'),
(69, 'Euthyrox 50mcg', 'Levothyroxine', 'Palpitations, insomnia.', NULL, 10, 50, '2026-02-09 23:22:21'),
(70, 'Euthyrox 100mcg', 'Levothyroxine', 'Anxiety.', NULL, 10, 70, '2026-02-09 23:22:21'),
(71, 'Farcolin Syrup', 'Salbutamol', 'Child hyperactivity.', NULL, 10, 25, '2026-02-09 23:22:21'),
(72, 'Flixotide 125 Inhaler', 'Fluticasone', 'Hoarseness.', NULL, 10, 150, '2026-02-09 23:22:21'),
(73, 'Symbicort 160/4.5', 'Budesonide/Formoterol', 'Throat irritation.', NULL, 10, 450, '2026-02-09 23:22:21'),
(74, 'Cetrak 10mg', 'Cetirizine', 'Dry mouth.', NULL, 10, 30, '2026-02-09 23:22:21'),
(75, 'Mousidin 10mg', 'Loratadine', 'Fatigue.', NULL, 10, 25, '2026-02-09 23:22:21'),
(76, 'Telfast 120mg', 'Fexofenadine', 'Drowsiness (low).', NULL, 10, 85, '2026-02-09 23:22:21'),
(77, 'Fexon 120mg', 'Fexofenadine', 'Dizziness.', NULL, 10, 60, '2026-02-09 23:22:21'),
(78, 'Mucosolvan Syrup', 'Ambroxol', 'Nausea.', NULL, 10, 35, '2026-02-09 23:22:21'),
(79, 'Bisolvon tablets', 'Bromhexine', 'Upset stomach.', NULL, 10, 20, '2026-02-09 23:22:21'),
(80, 'Gastroloc 40mg', 'Pantoprazole', 'Gas.', NULL, 10, 70, '2026-02-09 23:22:21'),
(81, 'Esobazole 40mg', 'Esomeprazole', 'Nausea.', NULL, 10, 130, '2026-02-09 23:22:21'),
(82, 'Gaviscon liquid 200ml', 'Sodium Alginate', 'Bloating.', NULL, 10, 85, '2026-02-09 23:22:21'),
(83, 'Maalox Plus', 'Aluminum/Magnesium Hydroxide', 'Constipation.', NULL, 10, 40, '2026-02-09 23:22:21'),
(84, 'Epicogel', 'Magaldrate', 'Diarrhea.', NULL, 10, 25, '2026-02-09 23:22:21'),
(85, 'Librax', 'Chlordiazepoxide/Clidinium', 'Dry mouth, drowsiness.', NULL, 10, 30, '2026-02-09 23:22:21'),
(86, 'Spasmomen', 'Otilonium Bromide', 'Dizziness.', NULL, 10, 65, '2026-02-09 23:22:21'),
(87, 'Buscopan 10mg', 'Hyoscine', 'Reduced sweating.', NULL, 10, 25, '2026-02-09 23:22:21'),
(88, 'Cipralex 10mg', 'Escitalopram', 'Sleep issues, nausea.', NULL, 10, 220, '2026-02-09 23:22:21'),
(89, 'Estikan 10mg', 'Escitalopram', 'Sexual dysfunction.', NULL, 10, 110, '2026-02-09 23:22:21'),
(90, 'Prozac 20mg', 'Fluoxetine', 'Anxiety, insomnia.', NULL, 10, 180, '2026-02-09 23:22:21'),
(91, 'Philozac 20mg', 'Fluoxetine', 'Nervousness.', NULL, 10, 60, '2026-02-09 23:22:21'),
(92, 'Xanax 0.5mg', 'Alprazolam', 'Drowsiness, addiction risk.', NULL, 10, 50, '2026-02-09 23:22:21'),
(93, 'Restolam 0.5mg', 'Alprazolam', 'Fatigue.', NULL, 10, 30, '2026-02-09 23:22:21'),
(94, 'Depakine Chrono 500mg', 'Valproate Sodium', 'Hair loss, weight gain.', NULL, 10, 150, '2026-02-09 23:22:21'),
(95, 'Tegretol CR 200mg', 'Carbamazepine', 'Dizziness, drowsiness.', NULL, 10, 90, '2026-02-09 23:22:21'),
(96, 'Neuroton Ampoules', 'Vitamin B1, B6, B12', 'Acne.', NULL, 10, 45, '2026-02-09 23:22:21'),
(97, 'Neurobion Ampoules', 'Vitamin B1, B6, B12', 'Sweating.', NULL, 10, 65, '2026-02-09 23:22:21'),
(98, 'Osteocare tablets', 'Calcium/Vit D/Mg/Zn', 'Constipation.', NULL, 10, 95, '2026-02-09 23:22:21'),
(99, 'Cal-Mag', 'Calcium/Magnesium', 'Gas.', NULL, 10, 50, '2026-02-09 23:22:21'),
(100, 'Centrum Lutein', 'Multivitamins', 'Upset stomach.', NULL, 10, 550, '2026-02-09 23:22:21'),
(101, 'Vitamount for Women', 'Multivitamins', 'Nausea.', NULL, 10, 60, '2026-02-09 23:22:21'),
(102, 'Sansovit Syrup', 'Multivitamins/Calcium', 'Urine color change.', NULL, 10, 45, '2026-02-09 23:22:21'),
(103, 'Feroglobin Capsules', 'Iron/B12/Folic Acid', 'Nausea, black stool.', NULL, 10, 80, '2026-02-09 23:22:21'),
(104, 'Haematon Capsules', 'Iron Complex', 'Constipation.', NULL, 10, 55, '2026-02-09 23:22:21'),
(105, 'Betadine Solution', 'Povidone-Iodine', 'Skin irritation.', NULL, 10, 40, '2026-02-09 23:22:21'),
(106, 'Fucidin Cream 20g', 'Fusidic Acid', 'Mild burning.', NULL, 10, 55, '2026-02-09 23:22:21'),
(107, 'Kenacomb Ointment', 'Nystatin/Neomycin/Gramicidin/Triamcinolone', 'Thinning of skin.', NULL, 10, 45, '2026-02-09 23:22:21'),
(108, 'Panderm Cream', 'Antifungal/Antibacterial/Steroid', 'Rash.', NULL, 10, 35, '2026-02-09 23:22:21');

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `medical_id` varchar(36) NOT NULL,
  `dob` date NOT NULL,
  `blood_type` varchar(5) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `height` float DEFAULT NULL,
  `chronic_diseases` text DEFAULT NULL,
  `national_id` varchar(14) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `governorate` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `patients`
--

INSERT INTO `patients` (`id`, `user_id`, `medical_id`, `dob`, `blood_type`, `weight`, `height`, `chronic_diseases`, `national_id`, `phone_number`, `address`, `gender`, `governorate`) VALUES
(1, 3, '91cce637-2a2f-4490-a13a-21df03ff7dd2', '1990-01-01', 'A+', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(2, 6, '998b1818-12d7-4dc3-9258-6e71225f31a8', '1990-05-02', 'AB-', 72.2461, 181.258, 'Diabetes', NULL, NULL, NULL, NULL, NULL),
(4, 8, '8e8bb99a-3c46-4ed3-8ed9-ece87fa81a4f', '1996-02-03', 'B-', 83.5844, 187.883, 'Hypertension', NULL, NULL, NULL, NULL, NULL),
(5, 9, 'b742a910-cb80-423e-b967-f227295214bc', '1975-05-20', 'AB+', 56.1901, 185.226, 'None', NULL, NULL, NULL, NULL, NULL),
(6, 10, 'fdf5938d-4be3-454a-83c5-b69906ae75a9', '1981-05-22', 'A+', 52.6335, 154.251, 'Diabetes', NULL, NULL, NULL, NULL, NULL),
(9, 13, '282ca654-f5e2-48bf-b045-ff5b6168b7aa', '1968-01-04', 'A-', 56.0813, 152.979, 'None', NULL, NULL, NULL, NULL, NULL),
(10, 14, 'ea11817e-d9c0-419b-bbac-50bfddc20cfd', '1942-06-28', 'AB-', 65.9357, 172.728, 'Diabetes', NULL, NULL, NULL, NULL, NULL),
(11, 15, '51646f11-f840-4ce3-a78c-4cb3369b27a9', '2001-05-16', 'AB-', 63.5533, 161.965, 'Asthma', NULL, NULL, NULL, NULL, NULL),
(12, 2, '25b15f41-1614-4c5f-a6e1-4223297c047c', '2004-08-11', 'A+', 76, 182, '', NULL, NULL, NULL, NULL, NULL),
(13, 5, '0d189afe-89eb-4233-8ee7-488ffee184c6', '2004-12-03', 'A+', 80, 180, '', NULL, NULL, NULL, NULL, NULL),
(15, 1, '5e83899d-3f2b-4a09-92db-b6900a744663', '2000-07-12', 'A+', 60, 170, '', NULL, NULL, NULL, NULL, NULL),
(16, 4, '47899eaa-90e5-41a2-b340-588ddf91bf51', '2000-04-03', 'A+', 160, 40, '', NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `id` int(11) NOT NULL,
  `appointment_id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `amount` float NOT NULL,
  `payment_method` varchar(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `transaction_id` varchar(100) DEFAULT NULL,
  `payment_date` datetime DEFAULT NULL,
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`id`, `appointment_id`, `patient_id`, `doctor_id`, `amount`, `payment_method`, `status`, `transaction_id`, `payment_date`, `notes`) VALUES
(1, 1, 1, 1, 300, 'cash', 'pending', NULL, '2025-12-27 16:06:08', NULL),
(2, 2, 1, 1, 300, 'cash', 'pending', NULL, '2025-12-31 18:31:59', NULL),
(3, 3, 1, 1, 300, 'card', 'pending', NULL, '2026-01-05 09:44:35', NULL),
(4, 4, 1, 2, 260, 'cash', 'pending', NULL, '2026-01-26 13:10:10', NULL),
(5, 5, 1, 1, 300, 'card', 'pending', NULL, '2026-01-26 13:10:33', NULL),
(6, 6, 1, 6, 380, 'card', 'pending', NULL, '2026-01-30 19:51:12', NULL),
(7, 7, 1, 12, 600, 'cash', 'pending', NULL, '2026-01-30 19:51:39', NULL),
(8, 8, 1, 1, 300, 'cash', 'pending', NULL, '2026-01-30 19:51:43', NULL),
(9, 9, 1, 3, 320, 'card', 'pending', NULL, '2026-02-01 10:38:03', NULL),
(10, 10, 1, 1, 300, 'cash', 'pending', NULL, '2026-02-01 10:38:16', NULL),
(11, 11, 1, 2, 260, 'card', 'pending', NULL, '2026-02-15 15:14:45', NULL),
(12, 12, 1, 11, 260, 'cash', 'pending', NULL, '2026-02-15 15:16:18', NULL),
(13, 13, 1, 1, 300, 'card', 'pending', NULL, '2026-02-19 13:28:00', NULL),
(14, 14, 1, 1, 300, 'cash', 'pending', NULL, '2026-02-19 13:28:13', NULL),
(15, 15, 1, 11, 260, 'card', 'completed', 'TRX-8259F9382EF3', '2026-02-20 14:17:56', NULL),
(16, 16, 1, 24, 396, 'card', 'pending', NULL, '2026-02-20 23:49:51', NULL),
(17, 17, 1, 24, 396, 'cash', 'pending', NULL, '2026-02-20 23:50:05', NULL),
(18, 18, 1, 22, 454, 'card', 'pending', NULL, '2026-02-21 00:21:18', NULL),
(19, 19, 1, 22, 454, 'cash', 'pending', NULL, '2026-02-21 00:21:31', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `pharmacists`
--

CREATE TABLE `pharmacists` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `pharmacy_name` varchar(100) NOT NULL,
  `license_number` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `pharmacists`
--

INSERT INTO `pharmacists` (`id`, `user_id`, `pharmacy_name`, `license_number`) VALUES
(1, 5, 'CVS Pharmacy', 'PH-5'),
(2, 26, 'Warner Pharmacy', 'PH-60577'),
(3, 27, 'Gray Pharmacy', 'PH-71071'),
(4, 28, 'Joyce Pharmacy', 'PH-81260'),
(5, 29, 'Tapia Pharmacy', 'PH-79100'),
(6, 30, 'Garrett Pharmacy', 'PH-13878'),
(7, 31, 'Smith Pharmacy', 'PH-59687'),
(8, 32, 'Mcdonald Pharmacy', 'PH-91337'),
(9, 33, 'Gentry Pharmacy', 'PH-92846'),
(10, 34, 'Lee Pharmacy', 'PH-14569'),
(11, 35, 'Johnson Pharmacy', 'PH-65803');

-- --------------------------------------------------------

--
-- Table structure for table `pharmacy_sales`
--

CREATE TABLE `pharmacy_sales` (
  `id` int(11) NOT NULL,
  `pharmacist_id` int(11) DEFAULT NULL,
  `patient_id` int(11) DEFAULT NULL,
  `total_amount` float NOT NULL,
  `payment_method` varchar(50) NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `pharmacy_sales`
--

INSERT INTO `pharmacy_sales` (`id`, `pharmacist_id`, `patient_id`, `total_amount`, `payment_method`, `created_at`) VALUES
(1, 1, NULL, 40, 'InstaPay', '2026-02-09 23:16:25'),
(2, 1, NULL, 180, 'Visa', '2026-02-09 23:34:32');

-- --------------------------------------------------------

--
-- Table structure for table `pharmacy_sale_items`
--

CREATE TABLE `pharmacy_sale_items` (
  `id` int(11) NOT NULL,
  `sale_id` int(11) DEFAULT NULL,
  `medication_id` int(11) DEFAULT NULL,
  `quantity` int(11) NOT NULL,
  `price_at_sale` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `pharmacy_sale_items`
--

INSERT INTO `pharmacy_sale_items` (`id`, `sale_id`, `medication_id`, `quantity`, `price_at_sale`) VALUES
(1, 1, 1, 2, 20),
(2, 2, 5, 1, 130),
(3, 2, 1, 2, 25);

-- --------------------------------------------------------

--
-- Table structure for table `prescriptions`
--

CREATE TABLE `prescriptions` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `appointment_id` int(11) DEFAULT NULL,
  `medications` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`medications`)),
  `instructions` text DEFAULT NULL,
  `diagnosis` varchar(200) DEFAULT NULL,
  `valid_until` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `prescription_items`
--

CREATE TABLE `prescription_items` (
  `id` int(11) NOT NULL,
  `prescription_id` int(11) NOT NULL,
  `drug_name` varchar(100) NOT NULL,
  `dosage` varchar(100) NOT NULL,
  `instructions` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `prescription_modifications`
--

CREATE TABLE `prescription_modifications` (
  `id` int(11) NOT NULL,
  `prescription_id` int(11) NOT NULL,
  `pharmacist_id` int(11) NOT NULL,
  `original_medications` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`original_medications`)),
  `proposed_medications` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`proposed_medications`)),
  `reason` text NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `doctor_response` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `reviewed_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qr_tokens`
--

CREATE TABLE `qr_tokens` (
  `id` int(11) NOT NULL,
  `token_hash` varchar(64) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `allowed_role` varchar(20) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `expires_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `qr_tokens`
--

INSERT INTO `qr_tokens` (`id`, `token_hash`, `patient_id`, `allowed_role`, `created_at`, `expires_at`) VALUES
(34, '7B6BF0CD936E', 1, 'all', '2026-02-18 20:19:34', '2026-02-18 21:19:34'),
(35, '150c91e8d52f6473d7d3f1efd9dc27a1e203cf4c9ef47fddea5cc82d4e5cf57d', 1, 'doctor', '2026-02-18 21:31:28', '2026-02-18 22:31:28'),
(36, 'be9a1b7537d90aa7739460ba0a82074535336efd73ebe94b1fcdb4f26faf719b', 1, 'doctor', '2026-02-18 22:40:56', '2026-02-18 23:40:56'),
(37, '570f24df302372bbfa08069a9292ab2bdf1a1b14ee8663169f6bfbb6658ade27', 1, 'doctor', '2026-02-19 01:01:35', '2026-02-19 02:01:35'),
(38, 'f868e32c5f1b840ea7ce307a66e65ab1c0fd93a9ba80003451ce11461a8f5881', 12, 'doctor', '2026-02-19 01:47:17', '2026-02-19 02:47:17'),
(39, 'f9108864f32a589f785d069a7f759665deb00b1098a8f30be8d3b1c4fb2ebf90', 1, 'doctor', '2026-02-19 02:02:32', '2026-02-19 03:02:32'),
(40, '3830111d03a69762a30c7f4f3822480726a1e29ea029cbda0a37316c029145d2', 13, 'doctor', '2026-02-19 02:12:56', '2026-02-19 03:12:56'),
(41, '678feb8e435850fd053817e6fdfac4cdd22f697344602e1b48b8ec3df3054d2a', 1, 'doctor', '2026-02-19 12:35:39', '2026-02-19 13:35:39'),
(42, '11ba6c34c59b27c6f401d7c70f331a6a9e40e1e89687553e9bbf106f23c1140b', 1, 'doctor', '2026-02-19 14:01:27', '2026-02-19 15:01:27'),
(43, '68cca2fba3331f5f6263908388102d7da7d12a4723fb1056a734aef7978a97bd', 1, 'doctor', '2026-02-19 21:37:22', '2026-02-19 22:37:22'),
(44, '2cbae086e015c2a55c3f1f174d8e483a458a190fa2d50efb9b9247127f02722e', 1, 'doctor', '2026-02-19 23:29:25', '2026-02-20 00:29:25'),
(45, '803f8c3e0b61462fc50aca229c3f2d25f1e7f5d05987facd8ec00548b6c1ad12', 1, 'doctor', '2026-02-20 08:12:10', '2026-02-20 09:12:10'),
(46, '5475d878ea308839c02a89cf0074f674af3131409becb30629b531281216045e', 1, 'doctor', '2026-02-20 12:33:08', '2026-02-20 13:33:08'),
(47, '1edeebb0e7f06cf985a815bc7138a7dc1f0891c347f4b68222a6560112105775', 1, 'doctor', '2026-02-20 14:07:37', '2026-02-20 15:07:37'),
(48, '578daf874d5ca386ed3fe8378e2e0a5bc8aa7048c53b486df8c8fdde422b8d0d', 12, 'doctor', '2026-02-20 14:24:05', '2026-02-20 15:24:05'),
(49, '1078794dcf97065ae9c6dfcc2c4aa684bbd5556b3dd8e0c20b42a7033f2016fe', 15, 'doctor', '2026-02-20 21:24:03', '2026-02-20 22:24:03'),
(50, '76f671420d61024992b2d69ad4c0b78a1af837ce22dbe52f951ce57e157ef90d', 1, 'doctor', '2026-02-20 22:08:25', '2026-02-20 23:08:25'),
(51, '566a47de557841f7fdea11626ef223b5905f800ff2930a6d84bd11db645391c4', 1, 'doctor', '2026-02-20 23:36:41', '2026-02-21 00:36:41'),
(52, 'b98719f8fd81ba268f95223e1ee8dc389782f9bf36a626416ec1647f3e662b0e', 1, 'doctor', '2026-02-21 00:47:07', '2026-02-21 01:47:07'),
(53, 'e8722d587d84383193b55678d5c00ce6988462ba5e9b5fcb7482fd99b6397759', 1, 'doctor', '2026-02-21 16:35:10', '2026-02-21 17:35:10'),
(54, '3872f8700ab6a662fe3626cf962b27e310dcf1c600a8d6b571299a982f2ca663', 12, 'doctor', '2026-02-21 16:40:22', '2026-02-21 17:40:22'),
(55, '1fd0128844aea6514c0bfe31e4f15066ba85550936e0811751e42baa3ce93d03', 1, 'all', '2026-02-21 17:44:21', '2026-02-21 21:44:21'),
(56, '116146de9915dfc46722cc5eae3a99b89228a19c6085ac380643bf96f57f010a', 1, 'doctor', '2026-02-21 17:45:01', '2026-02-21 18:45:01'),
(57, '52053be96bc5f83a9eb3afd84be44e087bf4ce22265b3ab8623bff622560c9db', 12, 'doctor', '2026-02-21 17:45:47', '2026-02-21 18:45:47'),
(58, '5045b00d2ba6f58aa8aa08a1cd2ec5749b0637a68e65f5ee7ff436ee3369038e', 13, 'doctor', '2026-02-21 17:55:55', '2026-02-21 18:55:55'),
(59, '72f54054847eec13f9e5f884fea4a40578194a6cd5451d29994042942e60afda', 13, 'all', '2026-02-21 18:31:39', '2126-01-28 18:31:39'),
(60, '4fac51e2bd1abafddaed464a2cde15e68ff096159bfde6379c741c7a18c15f3a', 15, 'all', '2026-02-21 18:35:45', '2126-01-28 18:35:45'),
(61, '937d3d58c660ddf64694b628263b7d4367bc9ab2c88f5cb6ad616db377ea600f', 16, 'all', '2026-02-21 18:56:23', '2126-01-28 18:56:23'),
(62, '203eeb0525c05e91b8f052adb99c5739901ea1a52954b1e7b27b794de69f9484', 1, 'all', '2026-02-23 14:00:21', '2126-01-30 14:00:21'),
(63, '91e2523aa9f35980ec880e1907669b96ad8f8407ddc210537ce711ca2c0a9264', 12, 'all', '2026-03-09 11:57:14', '2126-02-13 11:57:14');

-- --------------------------------------------------------

--
-- Table structure for table `ratings`
--

CREATE TABLE `ratings` (
  `id` int(11) NOT NULL,
  `appointment_id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `stars` int(11) NOT NULL,
  `review` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `normalized_name` varchar(255) DEFAULT NULL,
  `concurrency_stamp` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `name`, `normalized_name`, `concurrency_stamp`) VALUES
(1, 'admin', 'ADMIN', NULL),
(2, 'doctor', 'DOCTOR', NULL),
(3, 'patient', 'PATIENT', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `se_assignments`
--

CREATE TABLE `se_assignments` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `camera_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `se_cameras`
--

CREATE TABLE `se_cameras` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `ip` varchar(45) NOT NULL,
  `port` int(11) DEFAULT 80,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `se_users`
--

CREATE TABLE `se_users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `is_admin` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `se_users`
--

INSERT INTO `se_users` (`id`, `username`, `password_hash`, `is_admin`) VALUES
(1, 'admin', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL,
  `profile_image` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password_hash`, `role`, `profile_image`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'Admin User', 'admin@orcagroup.top', 'pbkdf2:sha256:600000$OFSbEbziAvCxSf1l$f880c538d9291a797464618c5c07d6a8d04bf57477f74bde18bb7298b24c0a45', 'admin', 'default_avatar.png', 1, '2025-12-25 17:24:14', '2025-12-25 17:24:14'),
(2, 'House', 'doctor@orcagroup.top', 'pbkdf2:sha256:600000$06woRsfysciHEnPs$b8d0f6450af34792c7ee2d27bb222f6b85f5c515aacbe087aca248e59aa52e03', 'doctor', 'default_avatar.png', 1, '2025-12-25 17:24:14', '2026-02-21 19:34:10'),
(3, 'John Doe', 'patient@orcagroup.top', 'pbkdf2:sha256:600000$FHNyLFSMCI0gG3d2$a558b725f7cad9000429fc466fe8ac3163beba2a4c10acd742c8e12db7c83503', 'patient', 'default_avatar.png', 1, '2025-12-25 17:24:15', '2026-02-20 22:08:56'),
(4, 'Central Lab', 'lab@orcagroup.top', 'pbkdf2:sha256:600000$9Z39SWkTURPkUsRx$f1bc1cbea7b573486283bf3f412ac7be23d80244022ad5dac8d8b197b383676a', 'lab', 'default_avatar.png', 1, '2025-12-25 17:24:15', '2026-02-21 19:34:34'),
(5, 'Pharma Guy', 'pharmacist@orcagroup.top', 'pbkdf2:sha256:600000$xhauyr4XrHMQaVE4$fad22d2975d25bf9681198a98c53e72cd81c13d956f8c276bbab4b90842d6524', 'pharmacist', 'default_avatar.png', 1, '2025-12-25 17:24:15', '2025-12-27 16:59:50'),
(6, 'Sarah Mclean', 'patient_0_7547@orcagroup.top', 'pbkdf2:sha256:600000$rhV30mp3NQMZ4CcU$da120f7203e9023c6174e9d98926ea50b8471976e8a58ad9177723322fb5f0e5', 'patient', 'default_avatar.png', 1, '2025-12-27 16:28:54', '2025-12-27 16:28:54'),
(8, 'Arthur Thomas', 'patient_2_6173@orcagroup.top', 'pbkdf2:sha256:600000$pfdz37k3YZ1U4eE7$6dab7b500a7d3cd47c4f1888ff030732094ee8daa8d2c05bf0d598f52827ab87', 'patient', 'default_avatar.png', 1, '2025-12-27 16:28:55', '2025-12-27 16:28:55'),
(9, 'Denise Holmes', 'patient_3_9842@orcagroup.top', 'pbkdf2:sha256:600000$M8OP7KMYUnrmnWuj$262145747168eabd83679eb721bc21ed0d4bef4075a021c2104d47a3d2780555', 'patient', 'default_avatar.png', 1, '2025-12-27 16:28:55', '2025-12-27 16:28:55'),
(10, 'Lindsey Stephens', 'patient_4_3261@orcagroup.top', 'pbkdf2:sha256:600000$D3SOREZ2mlkmPGUh$daa0ba38d0e15b38370f697b9b4515a5037719c9bd361200e4378cdf34dc72f0', 'patient', 'default_avatar.png', 1, '2025-12-27 16:28:55', '2025-12-27 16:28:55'),
(13, 'April Bullock', 'patient_7_9394@orcagroup.top', 'pbkdf2:sha256:600000$8RIWgHzANXgwnENO$eaafe73426764fc42fefd69eda45b240e2ab8b875c549acf41fa3cd1e26b4860', 'patient', 'default_avatar.png', 1, '2025-12-27 16:28:57', '2025-12-27 16:28:57'),
(14, 'Tiffany Cook', 'patient_8_9337@orcagroup.top', 'pbkdf2:sha256:600000$blfZ8ci8ldqgM1Lz$0f9f5464d6e1759895a057ef5cb7c5dd49ffe501300362607b3af6df6580df55', 'patient', 'default_avatar.png', 1, '2025-12-27 16:28:57', '2025-12-27 16:28:57'),
(15, 'Richard Elliott', 'patient_9_6386@orcagroup.top', 'pbkdf2:sha256:600000$zxQrVIfI9FbLLbT6$04d0d42a62b7363acbb2d59e50dcb34ccc51576e897dffb8bb45eef11458e292', 'patient', 'default_avatar.png', 1, '2025-12-27 16:28:57', '2025-12-27 16:28:57'),
(16, 'Christopher Sanders', 'doctor_0_1985@orcagroup.top', 'pbkdf2:sha256:600000$AICazk0vwkeyUMx6$c1beab53a259bfda4885ab2787b3ce8fb511ba07f71b6d8ebeb17e44a41cb74a', 'doctor', 'default_avatar.png', 1, '2025-12-27 16:28:58', '2026-02-16 12:48:33'),
(17, 'Kayla Roberts', 'doctor_1_8660@orcagroup.top', 'pbkdf2:sha256:600000$mLiLSRKyn2HkfxL7$9c6c663af7b26a8739c18ca8eda9d4742e43d18e76072648ba9e8c1ed2ab2e68', 'doctor', 'default_avatar.png', 1, '2025-12-27 16:28:58', '2026-02-16 12:48:33'),
(18, 'Fernando Smith', 'doctor_2_4488@orcagroup.top', 'pbkdf2:sha256:600000$xcu61IeMrudKmoI4$5fb5f6bb269178f0550c424df549b0eec0846cb5514b91c701c28327c6d83a75', 'doctor', 'default_avatar.png', 1, '2025-12-27 16:28:58', '2026-02-16 12:48:33'),
(19, 'Sean Lara', 'doctor_3_1949@orcagroup.top', 'pbkdf2:sha256:600000$Y4KDjzHCg9YurTVk$2c78d9ef4fadaee969be20b2634c9589fdda4ca4c2d7428bac2c6f075270a63a', 'doctor', 'default_avatar.png', 1, '2025-12-27 16:28:59', '2026-02-16 12:48:33'),
(20, 'Debra Porter', 'doctor_4_1733@orcagroup.top', 'pbkdf2:sha256:600000$gmcx5uH722VNHYIa$932d12897fe37eb2d060f763f0cc9d4863abb59c9bc87b5af34e5e49fd3badf0', 'doctor', 'default_avatar.png', 1, '2025-12-27 16:28:59', '2026-02-20 14:36:05'),
(21, 'Megan Chang', 'doctor_5_7871@orcagroup.top', 'pbkdf2:sha256:600000$GsuG2CND8KrLNN4n$d4b8b41afb5110fba2abc86e809e87f88161eab4e233ef7bce45fbd67a469753', 'doctor', 'default_avatar.png', 1, '2025-12-27 16:29:00', '2026-02-16 12:48:33'),
(22, 'Kelly Nelson', 'doctor_6_1108@orcagroup.top', 'pbkdf2:sha256:600000$YL7D5zFitRRIyS57$4e69e96fcb102a8e096d5aac57678da8a53ba32b1aab40dc10776a115bcb3e0e', 'doctor', 'default_avatar.png', 1, '2025-12-27 16:29:00', '2026-02-16 12:48:33'),
(23, 'Jessica Bennett', 'doctor_7_1131@orcagroup.top', 'pbkdf2:sha256:600000$dV1MQC43oqsLU0jd$d5da48166a70100e34e22da18d9fa4353e42dd9201b101e695f450ab7388f69f', 'doctor', 'default_avatar.png', 1, '2025-12-27 16:29:00', '2026-02-16 12:48:33'),
(24, 'Jessica Horton', 'doctor_8_1293@orcagroup.top', 'pbkdf2:sha256:600000$EvyvP5p75e64F5CF$36d122ea39aa305ec7d8f923aa69b12f249a9ac49241c1a05a0601cca9284461', 'doctor', 'default_avatar.png', 1, '2025-12-27 16:29:01', '2026-02-16 12:48:33'),
(25, 'Holly Gibson', 'doctor_9_3226@orcagroup.top', 'pbkdf2:sha256:600000$Uhf4NgIEO8oNoqLw$30675924c8823701e7150b75ec1691ae0eba040566d1eb1ddef1da0f6ba8a6e8', 'doctor', 'default_avatar.png', 1, '2025-12-27 16:29:01', '2026-02-16 12:48:33'),
(26, 'John Green', 'pharma_0_5290@orcagroup.top', 'pbkdf2:sha256:600000$UUojIQwzeorwg0XN$f41bf1b8ee3838b15a0de09d76e17cba828792e53068249d81a098fe04034828', 'pharmacist', 'default_avatar.png', 1, '2025-12-27 16:29:01', '2025-12-27 16:29:01'),
(27, 'Amber Mitchell', 'pharma_1_2577@orcagroup.top', 'pbkdf2:sha256:600000$3q8tzfKmdS2t8XGP$f4fd3fcff34d67ceb478b4d922726d9622aa4f5ab34b39e999b2f2f3403e933d', 'pharmacist', 'default_avatar.png', 1, '2025-12-27 16:29:02', '2025-12-27 16:29:02'),
(28, 'Steven Obrien', 'pharma_2_4515@orcagroup.top', 'pbkdf2:sha256:600000$SWuKPTmEfhaP5u7D$3beb17e6abf082862b3b8b95ca281481454ee23965ef6e507dfcc035dc3df6a9', 'pharmacist', 'default_avatar.png', 1, '2025-12-27 16:29:02', '2025-12-27 16:29:02'),
(29, 'Katrina Robinson', 'pharma_3_4631@orcagroup.top', 'pbkdf2:sha256:600000$UjVRD72i9XTfKFbA$41872edcd6497114029f87189b43bb1ec53db1c3f9ce5c887754685f67ef1e20', 'pharmacist', 'default_avatar.png', 1, '2025-12-27 16:29:02', '2025-12-27 16:29:02'),
(30, 'Ashley Williams', 'pharma_4_6582@orcagroup.top', 'pbkdf2:sha256:600000$5CfGeMmhduhc0bxK$92d30ee216f6eee1d1f2ffff40b1bf3df1d23fa68b68f87ba541f06a37a97b34', 'pharmacist', 'default_avatar.png', 1, '2025-12-27 16:29:03', '2025-12-27 16:29:03'),
(31, 'Jeffrey Thomas', 'pharma_5_9411@orcagroup.top', 'pbkdf2:sha256:600000$x6eB0nStYN1k3lYy$41fb7ac60cd8737a1178890fee6db7e476df0c61ea99316dd366861612287603', 'pharmacist', 'default_avatar.png', 1, '2025-12-27 16:29:03', '2025-12-27 16:29:03'),
(32, 'Sara Armstrong', 'pharma_6_7917@orcagroup.top', 'pbkdf2:sha256:600000$UWYatmUJJqB57B0c$1c8930f7ade1ccbcf76febb5b94048d4f82a194bbd5bad8791eec8e26dd51425', 'pharmacist', 'default_avatar.png', 1, '2025-12-27 16:29:03', '2026-02-20 14:36:18'),
(33, 'Dana Rivera', 'pharma_7_2358@orcagroup.top', 'pbkdf2:sha256:600000$nNzPS98QeqVN5rqv$cadffca10ef8629ee1583a8f35349b21df8d001dba7236a64fc86749c546fd31', 'pharmacist', 'default_avatar.png', 1, '2025-12-27 16:29:04', '2025-12-27 16:29:04'),
(34, 'Connie Green', 'pharma_8_2413@orcagroup.top', 'pbkdf2:sha256:600000$9mWXlaJRf02Tsq2K$934b36d358d6a991fd2cde900b71277ef2a767fd574687dea7cacecc8b3b93d4', 'pharmacist', 'default_avatar.png', 1, '2025-12-27 16:29:04', '2025-12-27 16:29:04'),
(35, 'Tamara Chambers', 'pharma_9_5637@orcagroup.top', 'pbkdf2:sha256:600000$wRKP9dn4TPeSuaId$89d851675332d2737ea635462b926101d9d1042ad54cef267f1825517c8c8453', 'pharmacist', 'default_avatar.png', 1, '2025-12-27 16:29:05', '2025-12-27 16:29:05'),
(36, 'المختبر المركزي', 'lab_0_5487@orcagroup.top', 'pbkdf2:sha256:600000$CDLB6S2popNGAk9s$dbb36c1fa8f9923dbc9060436a03e66f0d4e05c5a07775921d520d96de9a727b', 'lab', 'default_avatar.png', 1, '2025-12-27 16:31:09', '2025-12-27 16:31:09'),
(37, 'معامل الشفاء', 'lab_1_1879@orcagroup.top', 'pbkdf2:sha256:600000$KJAoyB3cpUtIZZzG$1dbd2020335750c4487d69c8515613817cbb241ec369907698834b83388d214d', 'lab', 'default_avatar.png', 1, '2025-12-27 16:31:09', '2025-12-27 16:31:09'),
(38, 'مختبرات النور', 'lab_2_4738@orcagroup.top', 'pbkdf2:sha256:600000$86SRuKw2lFpdYMu8$0d9c3dcd231374e53e15d80a48ba6296f050d2ab18047e1621dbee5990616771', 'lab', 'default_avatar.png', 1, '2025-12-27 16:31:09', '2025-12-27 16:31:09'),
(39, 'معامل الدقة', 'lab_3_2388@orcagroup.top', 'pbkdf2:sha256:600000$GmlBM2U2GYZd0tz0$18e486e41bc340b499e2ea1fdb90302e84ce54d9743f814aa42b4f3991b2c93c', 'lab', 'default_avatar.png', 1, '2025-12-27 16:31:10', '2026-02-21 19:34:30'),
(40, 'المختبر الطبي الحديث', 'lab_4_3481@orcagroup.top', 'pbkdf2:sha256:600000$XtUaXnncsyiPgsHJ$f83cc269f2ce054e1d302e7178fe89e6cf6a5e29290161736a33e2fe00b3e942', 'lab', 'default_avatar.png', 1, '2025-12-27 16:31:10', '2025-12-27 16:31:10'),
(41, 'معامل الأمل', 'lab_5_4770@orcagroup.top', 'pbkdf2:sha256:600000$irLMdbjvEzdT6vXt$ce0ef83cb7031cb69b760da2a375843b5ad0a6644b41ee8d4a0d4d7953f21599', 'lab', 'default_avatar.png', 1, '2025-12-27 16:31:11', '2025-12-27 16:31:11'),
(42, 'مختبرات الصحة', 'lab_6_2459@orcagroup.top', 'pbkdf2:sha256:600000$t365I7RQBzHltRqm$d804b1716d9c295f0967ab0b865b175af810385311d70e2bf5e27ad279512a5b', 'lab', 'default_avatar.png', 1, '2025-12-27 16:31:11', '2025-12-27 16:31:11'),
(43, 'المعمل التخصصي', 'lab_7_1176@orcagroup.top', 'pbkdf2:sha256:600000$kzxPnfr3GpehZNxb$5dec4b30852aa9b494f9462cd53587ce789db6966194f4210f6af9b738bf2cad', 'lab', 'default_avatar.png', 1, '2025-12-27 16:31:11', '2025-12-27 16:31:11'),
(44, 'معامل الرعاية', 'lab_8_5806@orcagroup.top', 'pbkdf2:sha256:600000$3X3uN0427hQdkwum$e9de3dd152a017977e1a2bd858a617e39a4afd4195ca112c005d9539b40cc2e4', 'lab', 'default_avatar.png', 1, '2025-12-27 16:31:12', '2025-12-27 16:31:12'),
(45, 'مختبرات التشخيص', 'lab_9_5117@orcagroup.top', 'pbkdf2:sha256:600000$u69eX2uGCRa0lK88$09e94593aad64f4e619866139cac5d900fa6d3ace00126bbffa8faa95a4ea628', 'lab', 'default_avatar.png', 1, '2025-12-27 16:31:12', '2025-12-27 16:31:12'),
(46, 'Adam', 'adam@gmail.com', 'pbkdf2:sha256:600000$wtDuzC6RzSfrzK6Z$da4cb0fe6b98fbe49120b2ddccfc835fca08b2e15a18312fab5575698741d3c9', 'doctor', 'default_avatar.png', 1, '2026-01-30 19:39:08', '2026-02-16 12:48:33'),
(47, 'Temp Admin', 'temp_admin_repro@orcagroup.top', 'pbkdf2:sha256:600000$h7zgdwTmg4gTN10w$9eb350bb8b9ed7a3399d732917eaaea70b380b5d777304385ecca552c7f5a565', 'admin', 'default_avatar.png', 1, '2026-01-30 19:41:22', '2026-01-30 19:41:22'),
(48, 'Omar Said', 'omar.said@healthcare.eg', 'pbkdf2:sha256:600000$gGz0edFSqtxqIPvS$264efd4b374fe5bf5689c4c2157b677005795f0171a6a207f8a86c2fbae042df', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:44', '2026-02-16 12:45:08'),
(49, 'Fatma Ahmed', 'fatma.ahmed@healthcare.eg', 'pbkdf2:sha256:600000$dYPKSwltlDWSar3J$2e316b4cd17414f95101ca75e5fbc4ba8f12139d739ab36919aeb173ab7ce998', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:44', '2026-02-16 12:45:08'),
(50, 'Yasmin Refaat', 'yasmin.refaat@healthcare.eg', 'pbkdf2:sha256:600000$TLxV4mfff7oyjjwO$a51a6d8dc88fff87c60354df275d8e22c2f38d3d6a60754afe64c6e22c07c72c', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:44', '2026-02-16 12:45:08'),
(51, 'Heba Sherif', 'heba.sherif@healthcare.eg', 'pbkdf2:sha256:600000$4RtfpImn8zF9F63K$dd4e5d21f242d57746efebd4e38c892d2ab03f90a0f503e38fa4276882c9fe37', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:45', '2026-02-16 12:45:08'),
(52, 'Nesma Galal', 'nesma.galal@healthcare.eg', 'pbkdf2:sha256:600000$NNajLiNlq1OnGpC6$c49e1db9e9b10adb14e6336c49e9a453dede90eebb7cd9b7fa5c61b7cdd609eb', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:45', '2026-02-16 12:45:08'),
(53, 'Ahmed Hassan', 'ahmed.hassan@healthcare.eg', 'pbkdf2:sha256:600000$cWxORNs25YMekxGx$110c59254095aedc3e59936fb6247ade041132a992efca8fdee537dfeed7fefe', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:45', '2026-02-16 12:45:08'),
(54, 'Karim Yasser', 'karim.yasser@healthcare.eg', 'pbkdf2:sha256:600000$JZQ1prZNphoHsAYB$1289e57717d4e3fdc37114476b53b9b4676a920bf8982ad22f2f073326d42eb3', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:46', '2026-02-16 12:45:08'),
(55, 'Nour Mahmoud', 'nour.mahmoud@healthcare.eg', 'pbkdf2:sha256:600000$keVQuT8TlFhbeznJ$8b2c0e1bfdfba167f066195e0a470736a640c483c00cb3bbb00798a6a6f1d170', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:46', '2026-02-16 12:45:08'),
(56, 'Tamer Adel', 'tamer.adel@healthcare.eg', 'pbkdf2:sha256:600000$aBpOAFBYW81tU2sw$d97cfe3c6673d8daebbe942005b278e513c649878e79dc1bc2a3c7ae586561ae', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:46', '2026-02-16 12:45:08'),
(57, 'Walid Samir', 'walid.samir@healthcare.eg', 'pbkdf2:sha256:600000$HnkuzBLDz4qzAE2r$085df7f24d0eede00da955ea959307f21f94f4a48d4681b831d97fb97d951ad0', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:47', '2026-02-16 12:45:08'),
(58, 'Mahmoud Zaki', 'mahmoud.zaki@healthcare.eg', 'pbkdf2:sha256:600000$YfcxygIb7oIg9ZpG$70fdb672b91f90aa4a538ff35288b90eb62946287bf2bc25fdd97f7e1a907e35', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:47', '2026-02-16 12:45:08'),
(59, 'Mustafa Hany', 'mustafa.hany@healthcare.eg', 'pbkdf2:sha256:600000$xcvI8RSdtzBIueIp$3166a647eba3f7de996f8026821f249c5e389a34dcde1adc9f82d02e9bebc6dd', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:47', '2026-02-16 12:45:08'),
(60, 'Youssef Nabil', 'youssef.nabil@healthcare.eg', 'pbkdf2:sha256:600000$A09TPYNJhfWb7iLS$bd7d5711f0beb116f61d1a14c949d5ab45ceb6ce49c8d41ad6dafe661cd5a2e3', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:48', '2026-02-16 12:45:08'),
(61, 'Mohamed Ali', 'mohamed.ali@healthcare.eg', 'pbkdf2:sha256:600000$ap1jXNydEwzyvyiQ$06cde6f94608c6d4913c1ce466907214f0d3eba751317d183569a9efe63f135c', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:48', '2026-02-16 12:45:08'),
(62, 'Amr Essam', 'amr.essam@healthcare.eg', 'pbkdf2:sha256:600000$NsdoRN1SjCtAUY6E$e43ce541b0ea1dbf3ba46ce002f1ecf770634b88fbcca2ad962557eac3768da1', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:48', '2026-02-16 12:45:08'),
(63, 'Dina Tarek', 'dina.tarek@healthcare.eg', 'pbkdf2:sha256:600000$viSOV0syn8OBop3G$18faa8947d7cf7a83004e041a2ba1a66b500cb6c272303d5749f8f8434132b59', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:49', '2026-02-16 12:45:08'),
(64, 'Nada Hamdy', 'nada.hamdy@healthcare.eg', 'pbkdf2:sha256:600000$qBHN7nhWaUVb9xSa$ed5269ce027678313d4baca021471218766f9e34984a11799a0e2bb7508618c1', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:49', '2026-02-16 12:45:08'),
(65, 'Sarah Ibrahim', 'sarah.ibrahim@healthcare.eg', 'pbkdf2:sha256:600000$DyHnn0aRAv6KD02e$ad3460af7195e2628fc668105ec547d95fa74ae536966ae38e077de81119c6c3', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:49', '2026-02-16 12:45:08'),
(66, 'Mariam Kamal', 'mariam.kamal@healthcare.eg', 'pbkdf2:sha256:600000$MXW740Sb7ARtv9zw$46aed70e0bd76cba0803dc93141403458a2b347adf61c0c668fc72e4ae34a76b', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:50', '2026-02-16 12:45:08'),
(67, 'Rana Magdy', 'rana.magdy@healthcare.eg', 'pbkdf2:sha256:600000$SBzJgtWl9OwMyjB7$8d617b79837c109117b72dbe00358934afe8dcfca0426687781d1b6207733f93', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:50', '2026-02-16 12:45:08'),
(68, 'Khaled Farouk', 'khaled.farouk@healthcare.eg', 'pbkdf2:sha256:600000$NC5ZGuxbEmzlATxC$25030b7877970fc4c8828dc896c28fcfe14bb88e52e0eaf3d410869c0065a66e', 'doctor', 'default_avatar.png', 1, '2026-02-16 12:43:50', '2026-02-16 12:45:08'),
(69, 'Smart Lab Cairo', 'smart_lab@orcagroup.top', 'pbkdf2:sha256:600000$UIeHkbfZS0qkwUJx$ecfc9b486fcc956d1b7b7dae11708d908ffd274b85daf95351fdf27e1977f696', 'lab', 'default_avatar.png', 1, '2026-02-19 13:04:35', '2026-02-19 13:04:35');

-- --------------------------------------------------------

--
-- Table structure for table `user_roles`
--

CREATE TABLE `user_roles` (
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `user_roles`
--

INSERT INTO `user_roles` (`user_id`, `role_id`) VALUES
(1, 1),
(2, 2),
(3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `vital_signs`
--

CREATE TABLE `vital_signs` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `recorded_by` int(11) DEFAULT NULL,
  `blood_pressure_systolic` int(11) DEFAULT NULL,
  `blood_pressure_diastolic` int(11) DEFAULT NULL,
  `heart_rate` int(11) DEFAULT NULL,
  `temperature` float DEFAULT NULL,
  `respiratory_rate` int(11) DEFAULT NULL,
  `oxygen_saturation` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `height` float DEFAULT NULL,
  `bmi` float DEFAULT NULL,
  `recorded_at` datetime DEFAULT NULL,
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `vital_signs`
--

INSERT INTO `vital_signs` (`id`, `patient_id`, `recorded_by`, `blood_pressure_systolic`, `blood_pressure_diastolic`, `heart_rate`, `temperature`, `respiratory_rate`, `oxygen_saturation`, `weight`, `height`, `bmi`, `recorded_at`, `notes`) VALUES
(1, 2, 17, 131, 76, 98, 37.5, NULL, NULL, 72.2461, 181.258, 22, '2025-12-27 16:29:05', NULL),
(2, 2, 17, 113, 70, 83, 37.5, NULL, NULL, 72.2461, 181.258, 22, '2025-12-27 16:29:05', NULL),
(3, 2, 17, 121, 80, 75, 37.3, NULL, NULL, 72.2461, 181.258, 22, '2025-12-27 16:29:05', NULL),
(4, 2, 17, 121, 86, 63, 37.4, NULL, NULL, 72.2461, 181.258, 22, '2025-12-27 16:29:05', NULL),
(5, 2, 17, 132, 87, 73, 37.4, NULL, NULL, 72.2461, 181.258, 22, '2025-12-27 16:29:05', NULL),
(7, 4, 17, 132, 85, 63, 36.6, NULL, NULL, 83.5844, 187.883, 23.7, '2025-12-27 16:29:05', NULL),
(8, 4, 17, 110, 86, 80, 37.5, NULL, NULL, 83.5844, 187.883, 23.7, '2025-12-27 16:29:05', NULL),
(9, 4, 17, 112, 80, 88, 36.9, NULL, NULL, 83.5844, 187.883, 23.7, '2025-12-27 16:29:05', NULL),
(10, 5, 17, 118, 73, 79, 37.3, NULL, NULL, 56.1901, 185.226, 16.4, '2025-12-27 16:29:05', NULL),
(11, 5, 17, 130, 87, 70, 36.9, NULL, NULL, 56.1901, 185.226, 16.4, '2025-12-27 16:29:05', NULL),
(12, 6, 16, 136, 89, 94, 36.7, NULL, NULL, 52.6335, 154.251, 22.1, '2025-12-27 16:29:05', NULL),
(13, 6, 16, 125, 87, 83, 37.1, NULL, NULL, 52.6335, 154.251, 22.1, '2025-12-27 16:29:05', NULL),
(20, 9, 24, 135, 89, 82, 36.6, NULL, NULL, 56.0813, 152.979, 24, '2025-12-27 16:29:05', NULL),
(21, 9, 24, 116, 84, 100, 36.8, NULL, NULL, 56.0813, 152.979, 24, '2025-12-27 16:29:05', NULL),
(22, 10, 19, 113, 84, 95, 37.2, NULL, NULL, 65.9357, 172.728, 22.1, '2025-12-27 16:29:05', NULL),
(23, 10, 19, 120, 71, 92, 37.3, NULL, NULL, 65.9357, 172.728, 22.1, '2025-12-27 16:29:05', NULL),
(24, 10, 19, 130, 84, 86, 36.8, NULL, NULL, 65.9357, 172.728, 22.1, '2025-12-27 16:29:05', NULL),
(25, 10, 19, 116, 84, 99, 36.7, NULL, NULL, 65.9357, 172.728, 22.1, '2025-12-27 16:29:05', NULL),
(26, 11, 20, 140, 71, 91, 37.2, NULL, NULL, 63.5533, 161.965, 24.2, '2025-12-27 16:29:05', NULL),
(27, 11, 20, 115, 88, 86, 36.7, NULL, NULL, 63.5533, 161.965, 24.2, '2025-12-27 16:29:05', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `doctor_id` (`doctor_id`),
  ADD KEY `patient_id` (`patient_id`);

--
-- Indexes for table `audit_logs`
--
ALTER TABLE `audit_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `chat_messages`
--
ALTER TABLE `chat_messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sender_id` (`sender_id`),
  ADD KEY `receiver_id` (`receiver_id`),
  ADD KEY `prescription_id` (`prescription_id`);

--
-- Indexes for table `complaints`
--
ALTER TABLE `complaints`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD UNIQUE KEY `license_number` (`license_number`);

--
-- Indexes for table `follow_up_appointments`
--
ALTER TABLE `follow_up_appointments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `doctor_id` (`doctor_id`),
  ADD KEY `original_appointment_id` (`original_appointment_id`);

--
-- Indexes for table `labs`
--
ALTER TABLE `labs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `lab_appointments`
--
ALTER TABLE `lab_appointments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `lab_id` (`lab_id`),
  ADD KEY `service_id` (`service_id`);

--
-- Indexes for table `lab_services`
--
ALTER TABLE `lab_services`
  ADD PRIMARY KEY (`id`),
  ADD KEY `lab_id` (`lab_id`),
  ADD KEY `test_type_id` (`test_type_id`);

--
-- Indexes for table `lab_tests`
--
ALTER TABLE `lab_tests`
  ADD PRIMARY KEY (`id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `doctor_id` (`doctor_id`);

--
-- Indexes for table `lab_test_types`
--
ALTER TABLE `lab_test_types`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `medical_files`
--
ALTER TABLE `medical_files`
  ADD PRIMARY KEY (`id`),
  ADD KEY `history_id` (`history_id`);

--
-- Indexes for table `medical_history`
--
ALTER TABLE `medical_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `doctor_id` (`doctor_id`);

--
-- Indexes for table `medical_reports`
--
ALTER TABLE `medical_reports`
  ADD PRIMARY KEY (`id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `doctor_id` (`doctor_id`);

--
-- Indexes for table `medications`
--
ALTER TABLE `medications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD UNIQUE KEY `medical_id` (`medical_id`),
  ADD UNIQUE KEY `national_id` (`national_id`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `transaction_id` (`transaction_id`),
  ADD KEY `appointment_id` (`appointment_id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `doctor_id` (`doctor_id`);

--
-- Indexes for table `pharmacists`
--
ALTER TABLE `pharmacists`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD UNIQUE KEY `license_number` (`license_number`);

--
-- Indexes for table `pharmacy_sales`
--
ALTER TABLE `pharmacy_sales`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pharmacy_sales_ibfk_1` (`pharmacist_id`),
  ADD KEY `pharmacy_sales_ibfk_2` (`patient_id`);

--
-- Indexes for table `pharmacy_sale_items`
--
ALTER TABLE `pharmacy_sale_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sale_id` (`sale_id`),
  ADD KEY `medication_id` (`medication_id`);

--
-- Indexes for table `prescriptions`
--
ALTER TABLE `prescriptions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `doctor_id` (`doctor_id`),
  ADD KEY `appointment_id` (`appointment_id`);

--
-- Indexes for table `prescription_items`
--
ALTER TABLE `prescription_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `prescription_id` (`prescription_id`);

--
-- Indexes for table `prescription_modifications`
--
ALTER TABLE `prescription_modifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `prescription_id` (`prescription_id`),
  ADD KEY `pharmacist_id` (`pharmacist_id`);

--
-- Indexes for table `qr_tokens`
--
ALTER TABLE `qr_tokens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token_hash` (`token_hash`),
  ADD KEY `patient_id` (`patient_id`);

--
-- Indexes for table `ratings`
--
ALTER TABLE `ratings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `appointment_id` (`appointment_id`),
  ADD KEY `doctor_id` (`doctor_id`),
  ADD KEY `patient_id` (`patient_id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `se_assignments`
--
ALTER TABLE `se_assignments`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`,`camera_id`),
  ADD KEY `camera_id` (`camera_id`);

--
-- Indexes for table `se_cameras`
--
ALTER TABLE `se_cameras`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ip` (`ip`);

--
-- Indexes for table `se_users`
--
ALTER TABLE `se_users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `user_roles`
--
ALTER TABLE `user_roles`
  ADD PRIMARY KEY (`user_id`,`role_id`);

--
-- Indexes for table `vital_signs`
--
ALTER TABLE `vital_signs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `recorded_by` (`recorded_by`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `audit_logs`
--
ALTER TABLE `audit_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `chat_messages`
--
ALTER TABLE `chat_messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `complaints`
--
ALTER TABLE `complaints`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `doctors`
--
ALTER TABLE `doctors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `follow_up_appointments`
--
ALTER TABLE `follow_up_appointments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `labs`
--
ALTER TABLE `labs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `lab_appointments`
--
ALTER TABLE `lab_appointments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `lab_services`
--
ALTER TABLE `lab_services`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=99;

--
-- AUTO_INCREMENT for table `lab_tests`
--
ALTER TABLE `lab_tests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `lab_test_types`
--
ALTER TABLE `lab_test_types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- AUTO_INCREMENT for table `medical_files`
--
ALTER TABLE `medical_files`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `medical_history`
--
ALTER TABLE `medical_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `medical_reports`
--
ALTER TABLE `medical_reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `medications`
--
ALTER TABLE `medications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=109;

--
-- AUTO_INCREMENT for table `patients`
--
ALTER TABLE `patients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `pharmacists`
--
ALTER TABLE `pharmacists`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `pharmacy_sales`
--
ALTER TABLE `pharmacy_sales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `pharmacy_sale_items`
--
ALTER TABLE `pharmacy_sale_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `prescriptions`
--
ALTER TABLE `prescriptions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `prescription_items`
--
ALTER TABLE `prescription_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `prescription_modifications`
--
ALTER TABLE `prescription_modifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qr_tokens`
--
ALTER TABLE `qr_tokens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- AUTO_INCREMENT for table `ratings`
--
ALTER TABLE `ratings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `se_assignments`
--
ALTER TABLE `se_assignments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `se_cameras`
--
ALTER TABLE `se_cameras`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `se_users`
--
ALTER TABLE `se_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT for table `vital_signs`
--
ALTER TABLE `vital_signs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `audit_logs`
--
ALTER TABLE `audit_logs`
  ADD CONSTRAINT `audit_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `chat_messages`
--
ALTER TABLE `chat_messages`
  ADD CONSTRAINT `chat_messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `chat_messages_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `chat_messages_ibfk_3` FOREIGN KEY (`prescription_id`) REFERENCES `prescriptions` (`id`);

--
-- Constraints for table `complaints`
--
ALTER TABLE `complaints`
  ADD CONSTRAINT `complaints_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `doctors`
--
ALTER TABLE `doctors`
  ADD CONSTRAINT `doctors_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `follow_up_appointments`
--
ALTER TABLE `follow_up_appointments`
  ADD CONSTRAINT `follow_up_appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `follow_up_appointments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `follow_up_appointments_ibfk_3` FOREIGN KEY (`original_appointment_id`) REFERENCES `appointments` (`id`);

--
-- Constraints for table `labs`
--
ALTER TABLE `labs`
  ADD CONSTRAINT `labs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `lab_appointments`
--
ALTER TABLE `lab_appointments`
  ADD CONSTRAINT `lab_appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lab_appointments_ibfk_2` FOREIGN KEY (`lab_id`) REFERENCES `labs` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lab_appointments_ibfk_3` FOREIGN KEY (`service_id`) REFERENCES `lab_services` (`id`);

--
-- Constraints for table `lab_services`
--
ALTER TABLE `lab_services`
  ADD CONSTRAINT `lab_services_ibfk_1` FOREIGN KEY (`lab_id`) REFERENCES `labs` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lab_services_ibfk_2` FOREIGN KEY (`test_type_id`) REFERENCES `lab_test_types` (`id`);

--
-- Constraints for table `lab_tests`
--
ALTER TABLE `lab_tests`
  ADD CONSTRAINT `lab_tests_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lab_tests_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `medical_files`
--
ALTER TABLE `medical_files`
  ADD CONSTRAINT `medical_files_ibfk_1` FOREIGN KEY (`history_id`) REFERENCES `medical_history` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `medical_history`
--
ALTER TABLE `medical_history`
  ADD CONSTRAINT `medical_history_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `medical_history_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `medical_reports`
--
ALTER TABLE `medical_reports`
  ADD CONSTRAINT `medical_reports_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `medical_reports_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `patients`
--
ALTER TABLE `patients`
  ADD CONSTRAINT `patients_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`id`),
  ADD CONSTRAINT `payments_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `payments_ibfk_3` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `pharmacists`
--
ALTER TABLE `pharmacists`
  ADD CONSTRAINT `pharmacists_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `pharmacy_sales`
--
ALTER TABLE `pharmacy_sales`
  ADD CONSTRAINT `pharmacy_sales_ibfk_1` FOREIGN KEY (`pharmacist_id`) REFERENCES `pharmacists` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `pharmacy_sales_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `pharmacy_sale_items`
--
ALTER TABLE `pharmacy_sale_items`
  ADD CONSTRAINT `pharmacy_sale_items_ibfk_1` FOREIGN KEY (`sale_id`) REFERENCES `pharmacy_sales` (`id`),
  ADD CONSTRAINT `pharmacy_sale_items_ibfk_2` FOREIGN KEY (`medication_id`) REFERENCES `medications` (`id`);

--
-- Constraints for table `prescriptions`
--
ALTER TABLE `prescriptions`
  ADD CONSTRAINT `prescriptions_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `prescriptions_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `prescriptions_ibfk_3` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`id`);

--
-- Constraints for table `prescription_items`
--
ALTER TABLE `prescription_items`
  ADD CONSTRAINT `prescription_items_ibfk_1` FOREIGN KEY (`prescription_id`) REFERENCES `prescriptions` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `prescription_modifications`
--
ALTER TABLE `prescription_modifications`
  ADD CONSTRAINT `prescription_modifications_ibfk_1` FOREIGN KEY (`prescription_id`) REFERENCES `prescriptions` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `prescription_modifications_ibfk_2` FOREIGN KEY (`pharmacist_id`) REFERENCES `pharmacists` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `qr_tokens`
--
ALTER TABLE `qr_tokens`
  ADD CONSTRAINT `qr_tokens_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `ratings`
--
ALTER TABLE `ratings`
  ADD CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `ratings_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `ratings_ibfk_3` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`);

--
-- Constraints for table `se_assignments`
--
ALTER TABLE `se_assignments`
  ADD CONSTRAINT `se_assignments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `se_users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `se_assignments_ibfk_2` FOREIGN KEY (`camera_id`) REFERENCES `se_cameras` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `vital_signs`
--
ALTER TABLE `vital_signs`
  ADD CONSTRAINT `vital_signs_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `vital_signs_ibfk_2` FOREIGN KEY (`recorded_by`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
