-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 27, 2025 at 11:42 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `clg_placement_portal`
--

-- --------------------------------------------------------

--
-- Table structure for table `application`
--

CREATE TABLE `application` (
  `id` int(200) NOT NULL,
  `ssc` double NOT NULL,
  `hsc` double NOT NULL,
  `cgpa` double NOT NULL,
  `aggregate` double NOT NULL,
  `branch` varchar(200) NOT NULL,
  `year` varchar(200) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp(),
  `status` varchar(200) NOT NULL DEFAULT 'Pending',
  `user_resume` varchar(200) NOT NULL,
  `user_id` int(100) NOT NULL,
  `job_id` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `application`
--

INSERT INTO `application` (`id`, `ssc`, `hsc`, `cgpa`, `aggregate`, `branch`, `year`, `date`, `status`, `user_resume`, `user_id`, `job_id`) VALUES
(1, 25, 25, 25, 25, 'Computer Science', '2025', '2025-03-23', '', 'screencapture-file-C-Users-Novo-Desktop-demo-hospital-demo-hospital-30-html-2025-03-18-11_54_14.pdf', 11, 4),
(2, 60.55, 89.3, 8.5, 75, 'Computer Science', '2024', '2025-03-23', 'Accepted', 'Prajwal_Babhulkar.pdf', 11, 1),
(3, 92, 85.5, 8.9, 88, 'Computer Science', '2024', '2025-03-23', 'Pending', 'Intelligent_Negotiation_Bot_using_Machine_Learning_Techniques.pdf', 15, 5),
(4, 85, 98, 8.5, 88.5, 'Computer Science', '2024', '2025-03-24', 'Accepted', 'Prajwal_Babhulkar.pdf', 11, 7);

-- --------------------------------------------------------

--
-- Table structure for table `education`
--

CREATE TABLE `education` (
  `id` int(100) NOT NULL,
  `user_id` int(100) NOT NULL,
  `ssc` double NOT NULL,
  `hsc` double NOT NULL,
  `cgpa` double NOT NULL,
  `aggregate` double NOT NULL,
  `branch` varchar(100) NOT NULL,
  `year` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `education`
--

INSERT INTO `education` (`id`, `user_id`, `ssc`, `hsc`, `cgpa`, `aggregate`, `branch`, `year`) VALUES
(1, 11, 85.4, 75.4, 7.6, 81.4, 'Computer Science', '2024'),
(2, 16, 88, 92.3, 5.9, 78.5, 'Computer Science', '2024');

-- --------------------------------------------------------

--
-- Table structure for table `jobpost`
--

CREATE TABLE `jobpost` (
  `job_id` int(100) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` varchar(200) NOT NULL,
  `location` varchar(200) NOT NULL,
  `jobtype` varchar(100) NOT NULL,
  `salary` varchar(100) NOT NULL,
  `resume` varchar(100) NOT NULL,
  `category` varchar(200) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp(),
  `cname` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jobpost`
--

INSERT INTO `jobpost` (`job_id`, `title`, `description`, `location`, `jobtype`, `salary`, `resume`, `category`, `date`, `cname`) VALUES
(1, 'Backend Developer', 'create a web page and write a backendd code ', 'Pune', 'full-time', '650000', '', 'IT', '2025-03-22', 'Wipro'),
(2, 'rr', 'rgrde', 'drgsd', 'full-time', '5345', '', 'IT', '2025-03-22', ''),
(3, 'BPO', 'fndsjfns', 'nfdsfnl', 'full-time', '5646', '', 'IT', '2025-03-22', ''),
(5, 'Full Stack Developer', 'A job description is a document that outlines the duties and responsibilities of a job role.', 'Pune', 'full-time', '540000', 'e9807e3aa8c24fccb1d0c8fe2e6435a8_tcs.png', 'IT', '2025-03-23', 'TCS'),
(6, 'Chat Process', 'A job description is a document that outlines the duties and responsibilities of a job role.', 'Nagpur', 'full-time', '240000', 'd17c5af64fcf4a59a5d5175418a70c24_wipro.png', 'BPO', '2025-03-23', 'wipro'),
(7, 'CA', 'A job description is a document that outlines the duties and responsibilities of a job role.', 'Amravati', 'full-time', '400000', 'f581968b95ac489dbc89c99e8a177135_google.png', 'Accounts', '2025-03-23', 'Google');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `email` varchar(120) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `address` varchar(120) NOT NULL,
  `password` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `phone`, `address`, `password`) VALUES
(11, 'prashik', 'prashik@gmail.com', '7897898965', 'amravati', 'prashik'),
(12, 'Ram Patil', 'ram@gmail.com', '7878998987', 'Amravati', 'ram123'),
(13, 'ravi', 'ravi@gmail.com', '7878998987', 'Pune', 'scrypt:32768:8:1$DRQCYqxGLqdfnQsR$f40ced754c77158bc4de1deb74'),
(14, 'ishan', 'ishan@gmail.com', '7878998987', 'pune', 'scrypt:32768:8:1$Lce8kS7x9LtTWjCX$31fff1f0416bc38e85dde82ee4'),
(15, 'chetan', 'chetan@gmail.com', '7878998987', 'Amravati', 'chetan'),
(16, 'ram1', 'ram1@gmail.com', '7878998955', 'Pune', 'ram1');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `application`
--
ALTER TABLE `application`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `education`
--
ALTER TABLE `education`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `jobpost`
--
ALTER TABLE `jobpost`
  ADD PRIMARY KEY (`job_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `application`
--
ALTER TABLE `application`
  MODIFY `id` int(200) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `education`
--
ALTER TABLE `education`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `jobpost`
--
ALTER TABLE `jobpost`
  MODIFY `job_id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
