-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: localhost    Database: sys
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `Cliente`
--

DROP TABLE IF EXISTS `Cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Cliente` (
  `Cedula` int NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Correo` varchar(50) NOT NULL,
  PRIMARY KEY (`Cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cliente`
--

LOCK TABLES `Cliente` WRITE;
/*!40000 ALTER TABLE `Cliente` DISABLE KEYS */;
INSERT INTO `Cliente` VALUES (21,'goku','veta'),(65,'kkljl','khuhk'),(78,'uyu','xo'),(89,'ayu','wa'),(444,'hermes','becerra'),(655,'kkljl','khuhk'),(665,'alex','smih'),(777,'junes','kssds'),(999,'alejo','sarmi'),(1443,'sss','khuhk'),(4443,'sss','khuhk'),(4567,'Josedani','josedani@dani.com'),(6768,'pruebita','pruebon'),(6769,'lolitoff','lolls.com'),(8547,'peppte','pepote@'),(8888,'ddss','sdsds'),(11111,'Pepito','prueba@gmail.com'),(34349,'Karlos','kastro'),(57589,'Josedaiel','cvxxdddd'),(67679,'hhh','hhhh'),(212121,'Daniella','dada'),(1919133,'fer','fernandodeeff');
/*!40000 ALTER TABLE `Cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prod_venta`
--

DROP TABLE IF EXISTS `prod_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prod_venta` (
  `NroVenta` int NOT NULL,
  `ID_Producto` int NOT NULL,
  `Cantidad` int NOT NULL,
  PRIMARY KEY (`NroVenta`,`ID_Producto`),
  KEY `ID_Producto` (`ID_Producto`),
  CONSTRAINT `prod_venta_ibfk_1` FOREIGN KEY (`NroVenta`) REFERENCES `venta` (`NroVenta`),
  CONSTRAINT `prod_venta_ibfk_2` FOREIGN KEY (`ID_Producto`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prod_venta`
--

LOCK TABLES `prod_venta` WRITE;
/*!40000 ALTER TABLE `prod_venta` DISABLE KEYS */;
INSERT INTO `prod_venta` VALUES (67,1,2),(67,2,1),(68,5,1),(68,7,1),(69,3,1),(69,5,1),(69,6,1),(70,1,1),(70,4,2),(70,7,1),(71,1,3),(71,7,6);
/*!40000 ALTER TABLE `prod_venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id` int NOT NULL,
  `nombre` varchar(200) DEFAULT NULL,
  `precio` float DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `descripcion` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'Laptop HP',750,6,'Laptop HP con procesador Intel Core i5, 8GB RAM, 256GB SSD.'),(2,'Smartphone Samsung Galaxy',500,17,'Smartphone Samsung Galaxy con pantalla AMOLED de 6.4 pulgadas y cámara de 48 MP.'),(3,'Audífonos Sony WH-1000XM4',300,9,'Audífonos inalámbricos Sony con cancelación de ruido y hasta 30 horas de batería.'),(4,'Monitor Dell 27\"',200,0,'Monitor Dell de 27 pulgadas con resolución 4K UHD y tecnología IPS.'),(5,'Teclado Mecánico Logitech G Pro',100,12,'Teclado mecánico para gaming con switches GX Blue y retroiluminación RGB.'),(6,'Dauntless Manifesto (Vinyl)',69420,69,'He looking at that aura on you.'),(7,'Tarjeta de Steam ($50)',50,480,'Tarjeta con codigo para redimir $50 (en dolares) en la plataforma de videojuegos Steam'),(8,'XBOX 720',500,1,'LA HPTA XBOX 720 MI GENTE!!!'),(9,'Consolador RGB 2024',300000,8,'Uno para cada alumno ;)');
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rol`
--

DROP TABLE IF EXISTS `rol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rol` (
  `id` int NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rol`
--

LOCK TABLES `rol` WRITE;
/*!40000 ALTER TABLE `rol` DISABLE KEYS */;
INSERT INTO `rol` VALUES (1,'Administrador'),(2,'Vendedor'),(3,'Superusuario');
/*!40000 ALTER TABLE `rol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL,
  `nombre1` varchar(50) DEFAULT NULL,
  `nombre2` varchar(50) DEFAULT NULL,
  `apellido1` varchar(50) DEFAULT NULL,
  `apellido2` varchar(50) DEFAULT NULL,
  `usuario` varchar(100) DEFAULT NULL,
  `contrasena` varchar(100) DEFAULT NULL,
  `correo` varchar(150) DEFAULT NULL,
  `cc` int DEFAULT NULL,
  `rol_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuarios_rol_fk` (`rol_id`),
  CONSTRAINT `usuarios_rol_fk` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Alejandro',NULL,'Sarmiento','Rivera','alesansarive','admin','alesansarive@javerianacali.edu.co',1116328190,1),(2,'Juan','Esteban','Becerra','Gutierrez','junes','ci','juanesbecerra04@javerianacali.edu.co',1112038890,2),(3,'Maria','Jose','Pava','Echeverry','majo','superuser','majo@javerianacali.edu.co',1166222999,3);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `NroVenta` int NOT NULL AUTO_INCREMENT,
  `ID_Cliente` int NOT NULL,
  `ID_Empleado` int NOT NULL,
  `Fecha` date NOT NULL,
  PRIMARY KEY (`NroVenta`),
  KEY `ID_Cliente` (`ID_Cliente`),
  KEY `ID_Empleado` (`ID_Empleado`),
  CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`ID_Cliente`) REFERENCES `Cliente` (`Cedula`),
  CONSTRAINT `venta_ibfk_2` FOREIGN KEY (`ID_Empleado`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
INSERT INTO `venta` VALUES (32,6769,1,'2024-09-04'),(33,444,1,'2024-09-04'),(34,444,1,'2024-09-04'),(35,777,1,'2024-09-04'),(36,89,1,'2024-09-04'),(37,78,1,'2024-09-04'),(38,21,1,'2024-09-04'),(39,65,1,'2024-09-04'),(40,65,1,'2024-09-04'),(41,65,1,'2024-09-04'),(42,65,1,'2024-09-04'),(43,11111,1,'2024-09-04'),(44,655,1,'2024-09-04'),(45,11111,1,'2024-09-04'),(46,11111,1,'2024-09-04'),(49,11111,1,'2024-09-04'),(60,11111,1,'2024-09-04'),(61,11111,1,'2024-09-04'),(62,11111,1,'2024-09-04'),(63,11111,1,'2024-09-04'),(64,11111,1,'2024-09-04'),(66,11111,1,'2024-09-04'),(67,11111,1,'2024-09-04'),(68,34349,1,'2024-09-04'),(69,4567,1,'2024-09-04'),(70,57589,1,'2024-09-04'),(71,4567,1,'2024-09-16');
/*!40000 ALTER TABLE `venta` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-18  7:23:16
