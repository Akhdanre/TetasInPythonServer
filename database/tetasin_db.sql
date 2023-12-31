-- MySQL dump 10.13  Distrib 8.0.35, for Linux (x86_64)
--
-- Host: localhost    Database: tetasin_db
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `detail_hatch_data`
--

DROP TABLE IF EXISTS `detail_hatch_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detail_hatch_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_hatch_data` int NOT NULL,
  `temp` int DEFAULT NULL,
  `humd` int DEFAULT NULL,
  `water_volume` int DEFAULT NULL,
  `time_report` varchar(12) DEFAULT NULL,
  `date_report` date DEFAULT NULL,
  `url_image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_hatch_data` (`id_hatch_data`),
  CONSTRAINT `detail_hatch_data_ibfk_1` FOREIGN KEY (`id_hatch_data`) REFERENCES `hatch_data` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detail_hatch_data`
--

LOCK TABLES `detail_hatch_data` WRITE;
/*!40000 ALTER TABLE `detail_hatch_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `detail_hatch_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hatch_data`
--

DROP TABLE IF EXISTS `hatch_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hatch_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `inkubator_id` int DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date_estimation` date DEFAULT NULL,
  `number_of_eggs` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `inkubator_id` (`inkubator_id`),
  CONSTRAINT `hatch_data_ibfk_1` FOREIGN KEY (`inkubator_id`) REFERENCES `inkubators` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hatch_data`
--

LOCK TABLES `hatch_data` WRITE;
/*!40000 ALTER TABLE `hatch_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `hatch_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inkubators`
--

DROP TABLE IF EXISTS `inkubators`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inkubators` (
  `id` int NOT NULL,
  `token` varchar(10) NOT NULL,
  `temp_limit` int DEFAULT NULL,
  `humd_limit` int DEFAULT NULL,
  `water_volume` int DEFAULT NULL,
  `temp_value` int DEFAULT NULL,
  `humd_value` int DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `inkubator_user` (`username`),
  CONSTRAINT `inkubator_user` FOREIGN KEY (`username`) REFERENCES `users` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inkubators`
--

LOCK TABLES `inkubators` WRITE;
/*!40000 ALTER TABLE `inkubators` DISABLE KEYS */;
INSERT INTO `inkubators` VALUES (1,'INKT001',38,70,100,27,94,'akeoneuefo');
/*!40000 ALTER TABLE `inkubators` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `token` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('akeoneuefo','$2b$12$YxqotAeM./I51F9DD.4zuOrn77eMC4TaxpZCm/Rg/y6TcX2SX3Q7C','akeon de supo','55c149ce-5951-436b-ba37-2d40a31eea38'),('ipul','$2b$12$1yOpAgQlctueBnjigCJEu.QgqA5yb/p/D0zIYnT7K/dU4E/IzwB4q','akeoneufo','fd11b61a-3354-4529-b394-65a9a0e2d14b');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-01 23:37:29
