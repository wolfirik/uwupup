-- phpMyAdmin SQL Dump
-- version 4.6.5.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 25, 2016 at 12:46 PM
-- Server version: 10.1.20-MariaDB-1~trusty
-- PHP Version: 5.6.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `discord`
--

-- --------------------------------------------------------

--
-- Table structure for table `leave`
--

CREATE TABLE `leave` (
  `server` bigint(20) NOT NULL,
  `channel` bigint(20) NOT NULL,
  `message` text COLLATE utf8mb4_unicode_ci,
  `user` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `welcome`
--

CREATE TABLE `welcome` (
  `server` bigint(20) NOT NULL,
  `channel` bigint(20) NOT NULL,
  `message` text COLLATE utf8mb4_unicode_ci,
  `user` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--


--
-- Indexes for table `leave`
--
ALTER TABLE `leave`
  ADD UNIQUE KEY `server` (`server`);

--
-- Indexes for table `logs`
--
ALTER TABLE `logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`),
  ADD KEY `server_index` (`server`),
  ADD KEY `channel_index` (`channel`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`messages_id`),
  ADD KEY `messages_id` (`messages_id`) USING BTREE,
  ADD KEY `server_index` (`server`),
  ADD KEY `user_id_index` (`user_id`),
  ADD KEY `channel_index` (`channel`),
  ADD KEY `action_index` (`action`);

--
-- Indexes for table `muted`
--
ALTER TABLE `muted`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`);

--
-- Indexes for table `reminders`
--
ALTER TABLE `reminders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `stats`
--
ALTER TABLE `stats`
  ADD PRIMARY KEY (`shard`);

--
-- Indexes for table `tags`
--
ALTER TABLE `tags`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tracking`
--
ALTER TABLE `tracking`
  ADD KEY `id` (`id`),
  ADD KEY `server_index` (`server`),
  ADD KEY `channel_index` (`channel`);

--
-- Indexes for table `verification`
--
ALTER TABLE `verification`
  ADD UNIQUE KEY `server` (`server`);

--
-- Indexes for table `welcome`
--
ALTER TABLE `welcome`
  ADD UNIQUE KEY `server` (`server`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
