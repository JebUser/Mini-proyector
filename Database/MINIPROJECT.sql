-- phpMyAdmin SQL Dump
-- version 5.2.1deb3
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 21-09-2024 a las 02:03:39
-- Versión del servidor: 8.0.39-0ubuntu0.24.04.1
-- Versión de PHP: 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `MINIPROJECT`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Cliente`
--

CREATE TABLE `Cliente` (
  `Cedula` int NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Correo` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `Cliente`
--

INSERT INTO `Cliente` (`Cedula`, `Nombre`, `Correo`) VALUES
(21, 'goku', 'veta'),
(65, 'kkljl', 'khuhk'),
(78, 'uyu', 'xo'),
(89, 'ayu', 'wa'),
(444, 'hermes', 'becerra'),
(655, 'kkljl', 'khuhk'),
(665, 'alex', 'smih'),
(777, 'junes', 'kssds'),
(999, 'alejo', 'sarmi'),
(1443, 'sss', 'khuhk'),
(4443, 'sss', 'khuhk'),
(4567, 'Josedani', 'josedani@dani.com'),
(6768, 'pruebita', 'pruebon'),
(6769, 'lolitoff', 'lolls.com'),
(8547, 'peppte', 'pepote@'),
(8888, 'ddss', 'sdsds'),
(11111, 'Pepito', 'prueba@gmail.com'),
(34349, 'Karlos', 'kastro'),
(57589, 'Josedaiel', 'cvxxdddd'),
(67679, 'hhh', 'hhhh'),
(212121, 'Daniella', 'dada'),
(1919133, 'fer', 'fernandodeeff');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int NOT NULL,
  `nombre` varchar(200) DEFAULT NULL,
  `precio` float DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `descripcion` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `precio`, `cantidad`, `descripcion`) VALUES
(1, 'Laptop HP', 750, 6, 'Laptop HP con procesador Intel Core i5, 8GB RAM, 256GB SSD.'),
(2, 'Smartphone Samsung Galaxy', 500, 17, 'Smartphone Samsung Galaxy con pantalla AMOLED de 6.4 pulgadas y cámara de 48 MP.'),
(3, 'Audífonos Sony WH-1000XM4', 300, 9, 'Audífonos inalámbricos Sony con cancelación de ruido y hasta 30 horas de batería.'),
(4, 'Monitor Dell 27\"', 200, 0, 'Monitor Dell de 27 pulgadas con resolución 4K UHD y tecnología IPS.'),
(5, 'Teclado Mecánico Logitech G Pro', 100, 12, 'Teclado mecánico para gaming con switches GX Blue y retroiluminación RGB.'),
(6, 'Dauntless Manifesto (Vinyl)', 69420, 69, 'He looking at that aura on you.'),
(7, 'Tarjeta de Steam ($50)', 50, 480, 'Tarjeta con codigo para redimir $50 (en dolares) en la plataforma de videojuegos Steam'),
(8, 'XBOX 720', 500, 1, 'LA HPTA XBOX 720 MI GENTE!!!'),
(9, 'Consolador RGB 2024', 300000, 8, 'Uno para cada alumno ;)');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prod_venta`
--

CREATE TABLE `prod_venta` (
  `NroVenta` int NOT NULL,
  `ID_Producto` int NOT NULL,
  `Cantidad` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `prod_venta`
--

INSERT INTO `prod_venta` (`NroVenta`, `ID_Producto`, `Cantidad`) VALUES
(67, 1, 2),
(67, 2, 1),
(68, 5, 1),
(68, 7, 1),
(69, 3, 1),
(69, 5, 1),
(69, 6, 1),
(70, 1, 1),
(70, 4, 2),
(70, 7, 1),
(71, 1, 3),
(71, 7, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE `rol` (
  `id` int NOT NULL,
  `nombre` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `rol`
--

INSERT INTO `rol` (`id`, `nombre`) VALUES
(1, 'Administrador'),
(2, 'Vendedor'),
(3, 'Superusuario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

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
  `rol_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre1`, `nombre2`, `apellido1`, `apellido2`, `usuario`, `contrasena`, `correo`, `cc`, `rol_id`) VALUES
(1, 'Alejandro', '', 'Sarmiento', 'Rivera', 'alesansarive', '$2b$12$vFwG3n6eA5Mblu/Dr49vQeX4myXNqRvFId.15MllD7CmK.HjVY8Ee', 'alesansarive@javerianacali.edu.co', 1116328190, 1),
(2, 'Juan', 'Esteban', 'Becerra', 'Gutierrez', 'junes', '$2b$12$L.CS.vkvGA3qpQh2ItrZDOCcqMH7fHNY2nAMlT/TVQgFPhSZeKwOi', 'junesbecerra04@javerianacali.edu.co', 1112038890, 2),
(3, 'Maria', 'Jose', 'Pava', 'Echeverry', 'majo', '$2b$12$eMF6vhQDQtGU5qESh7zlTuwc4hKPXBvFhPaJNSZHArU95YOhlod/K', 'majo@javerianacali.edu.co', 1166222999, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `venta`
--

CREATE TABLE `venta` (
  `NroVenta` int NOT NULL,
  `ID_Cliente` int NOT NULL,
  `ID_Empleado` int NOT NULL,
  `Fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `venta`
--

INSERT INTO `venta` (`NroVenta`, `ID_Cliente`, `ID_Empleado`, `Fecha`) VALUES
(32, 6769, 1, '2024-09-04'),
(33, 444, 1, '2024-09-04'),
(34, 444, 1, '2024-09-04'),
(35, 777, 1, '2024-09-04'),
(36, 89, 1, '2024-09-04'),
(37, 78, 1, '2024-09-04'),
(38, 21, 1, '2024-09-04'),
(39, 65, 1, '2024-09-04'),
(40, 65, 1, '2024-09-04'),
(41, 65, 1, '2024-09-04'),
(42, 65, 1, '2024-09-04'),
(43, 11111, 1, '2024-09-04'),
(44, 655, 1, '2024-09-04'),
(45, 11111, 1, '2024-09-04'),
(46, 11111, 1, '2024-09-04'),
(49, 11111, 1, '2024-09-04'),
(60, 11111, 1, '2024-09-04'),
(61, 11111, 1, '2024-09-04'),
(62, 11111, 1, '2024-09-04'),
(63, 11111, 1, '2024-09-04'),
(64, 11111, 1, '2024-09-04'),
(66, 11111, 1, '2024-09-04'),
(67, 11111, 1, '2024-09-04'),
(68, 34349, 1, '2024-09-04'),
(69, 4567, 1, '2024-09-04'),
(70, 57589, 1, '2024-09-04'),
(71, 4567, 1, '2024-09-16');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `Cliente`
--
ALTER TABLE `Cliente`
  ADD PRIMARY KEY (`Cedula`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `prod_venta`
--
ALTER TABLE `prod_venta`
  ADD PRIMARY KEY (`NroVenta`,`ID_Producto`),
  ADD KEY `ID_Producto` (`ID_Producto`);

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuarios_rol_fk` (`rol_id`);

--
-- Indices de la tabla `venta`
--
ALTER TABLE `venta`
  ADD PRIMARY KEY (`NroVenta`),
  ADD KEY `ID_Cliente` (`ID_Cliente`),
  ADD KEY `ID_Empleado` (`ID_Empleado`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `venta`
--
ALTER TABLE `venta`
  MODIFY `NroVenta` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=72;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `prod_venta`
--
ALTER TABLE `prod_venta`
  ADD CONSTRAINT `prod_venta_ibfk_1` FOREIGN KEY (`NroVenta`) REFERENCES `venta` (`NroVenta`),
  ADD CONSTRAINT `prod_venta_ibfk_2` FOREIGN KEY (`ID_Producto`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_rol_fk` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`);

--
-- Filtros para la tabla `venta`
--
ALTER TABLE `venta`
  ADD CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`ID_Cliente`) REFERENCES `Cliente` (`Cedula`),
  ADD CONSTRAINT `venta_ibfk_2` FOREIGN KEY (`ID_Empleado`) REFERENCES `usuarios` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
