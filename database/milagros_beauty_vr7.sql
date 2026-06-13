-- =============================================================================
-- milagros_beauty_produccion.sql
-- -----------------------------------------------------------------------------
-- Versión final unificada de la base de datos `milagros_beauty_vr7`.
-- Integra en un solo archivo:
--   1) El esquema y los datos base del volcado original.
--   2) La corrección del conflicto de merge en `configuracion`.
--   3) La eliminación de triggers de contraseña incompatibles con bcrypt.
--   4) La conversión de `pedido_detalle.subtotal` en columna GENERADA.
--   5) La incorporación de FOREIGN KEYS faltantes.
--   6) La creación de índices auxiliares para consultas frecuentes.
--   7) La depuración completa de usuarios heredados inseguros.
--   8) La creación de dos cuentas administrativas iniciales con hashes bcrypt.
--
-- Orden recomendado de uso:
--   - Ejecutar este archivo directamente sobre una base vacía.
--
-- Notas importantes:
--   - Este script está pensado para MySQL / MariaDB compatibles con columnas
--     generadas STORED.
--   - La validación de complejidad de contraseñas ya no se hace con triggers.
--     Debe hacerse en la aplicación Python antes de hashear con bcrypt.
--   - Se conserva el nombre lógico de la base de datos original para mantener
--     compatibilidad con el proyecto existente.
-- =============================================================================

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `milagros_beauty_vr7`
--
CREATE DATABASE IF NOT EXISTS `milagros_beauty_vr7` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `milagros_beauty_vr7`;

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `categorias`
--
CREATE TABLE `categorias` (
  `id_categoria` int(11) NOT NULL,
  `nombre_categoria` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--
INSERT INTO `categorias` (`id_categoria`, `nombre_categoria`, `descripcion`) VALUES
(1, 'Cuidado Capilar', 'Productos para limpieza capilar.'),
(2, 'Cuidado Facial', 'Productos para el cuidado, protección e hidratación del rostro.'),
(3, 'Cuidado Corporal', 'Productos para el cuidado de la piel del cuerpo.'),
(4, 'Maquillaje', 'Categoría correspondiente a productos cosméticos decorativos.'),
(5, 'Pestaña y Cejas', 'Categoría especializada en el realce, fortalecimiento y cuidado de pestañas y cejas'),
(6, 'Perfumería', 'Categoría destinada a fragancias y productos aromáticos.'),
(7, 'Accesorios de Belleza', 'Herramientas complementarias para aplicación y cuidado personal.');

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `ciudades`
--
CREATE TABLE `ciudades` (
  `id_ciudad` int(11) NOT NULL,
  `municipio` varchar(100) NOT NULL,
  `departamento` varchar(100) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `codigo_postal` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `configuracion`
--
CREATE TABLE `configuracion` (
  `id` int(11) NOT NULL,
  `titulo` varchar(255) DEFAULT NULL,
  `sobre_nosotros` text DEFAULT NULL,
  `mision` text DEFAULT NULL,
  `vision` text DEFAULT NULL,
  `ubicacion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `configuracion`
--
-- Se resolvió el conflicto de merge del dump original conservando la versión
-- con el nombre visual `Milagro's Beauty✨`.
INSERT INTO `configuracion` (`id`, `titulo`, `sobre_nosotros`, `mision`, `vision`, `ubicacion`) VALUES
(1, 'Milagro\'s Beauty✨', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 'Ubicación física: Calle de Ejemplo #123, Ciudad');

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `estados_pedido`
--
CREATE TABLE `estados_pedido` (
  `id_estado` int(11) NOT NULL,
  `nombre_estado` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estados_pedido`
--
INSERT INTO `estados_pedido` (`id_estado`, `nombre_estado`) VALUES
(1, 'Pendiente'),
(2, 'Procesando'),
(3, 'Enviado'),
(4, 'Entregado');

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `historial_login`
--
CREATE TABLE `historial_login` (
  `id_historial` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `fecha_login` datetime DEFAULT current_timestamp(),
  `ip` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `marcas`
--
CREATE TABLE `marcas` (
  `id_marca` int(11) NOT NULL,
  `nombre_marca` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `marcas`
--
INSERT INTO `marcas` (`id_marca`, `nombre_marca`) VALUES
(1, 'Milagros Beauty');

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `pedidos`
--
CREATE TABLE `pedidos` (
  `id_pedido` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `id_estado` int(11) DEFAULT NULL,
  `fecha_pedido` datetime DEFAULT current_timestamp(),
  `total` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos`
--
-- Se eliminan los pedidos heredados porque dependían de usuarios antiguos que
-- fueron retirados por seguridad. El sistema queda listo para operar con datos
-- consistentes a partir de las nuevas cuentas iniciales.

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `pedido_detalle`
--
-- `subtotal` se define desde el inicio como columna generada para evitar
-- inconsistencias y eliminar cálculos manuales desde la aplicación.
CREATE TABLE `pedido_detalle` (
  `id_detalle` int(11) NOT NULL,
  `id_pedido` int(11) DEFAULT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL,
  `subtotal` decimal(10,2) GENERATED ALWAYS AS (`cantidad` * `precio_unitario`) STORED
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedido_detalle`
--
-- Se omite la carga inicial de detalles de pedido porque los pedidos heredados
-- fueron removidos junto con los usuarios anteriores para preservar integridad.

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `productos`
--
CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL,
  `nombre` varchar(150) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `contenido` varchar(50) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `id_categoria` int(11) DEFAULT NULL,
  `id_marca` int(11) DEFAULT NULL,
  `stock` int(11) DEFAULT 0,
  `estado` tinyint(4) DEFAULT 1,
  `ideal_para` text DEFAULT NULL,
  `beneficios` text DEFAULT NULL,
  `ingredientes` text DEFAULT NULL,
  `modo_uso` text DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--
INSERT INTO `productos` (`id_producto`, `nombre`, `descripcion`, `contenido`, `precio`, `imagen`, `id_categoria`, `id_marca`, `stock`, `estado`, `ideal_para`, `beneficios`, `ingredientes`, `modo_uso`, `fecha_creacion`) VALUES
(1, 'Shampoo crecimiento con extracto de cebolla y péptidos', '¡CRECIMIENTO, FUERZA Y VITALIDAD EN TU CABELLO!\r\n\r\nDESCRIPCIÓN:\r\n¡Devuelve la fuerza y vitalidad a tu cabello! Este shampoo estimula el crecimiento, aporta energía y fortaleza desde la raíz. Su fórmula combina extracto de cebolla morada, péptidos fortalecedores y cafeína, que restauran la fuerza del cabello, estimulan su crecimiento y controlan el frizz desde la primera aplicación.\r\n\r\nINGREDIENTES PRINCIPALES:\r\nCebolla roja, péptidos, jengibre, cafeína, microalga ishorhyrys y hongo reishi.\r\n\r\nMODO DE USO:\r\nSobre el cabello y cuero cabelludo húmedo, aplique una cantidad suficiente del producto. Masajee con la yema de los dedos y distribuya muy bien en toda la raíz. Deje actuar de 5 a 10 minutos y enjuague con abundante agua. Se recomienda el uso diario.', '450 ml', 20000.00, 'imagenes/shampoo1.jpg', 1, 1, 30, 1, 'Cabellos estancados, sin vida o débiles que deseen más vitalidad y crecimiento.', 'Estimula el crecimiento, fortalece el cabello, controla el frizz y aporta energía desde la raíz.', 'Cebolla roja, péptidos, jengibre, cafeína, microalga ishorhyrys y hongo reishi.', 'Sobre el cabello y cuero cabelludo húmedo, aplique una cantidad suficiente del producto. Masajee con la yema de los dedos y distribuya muy bien en toda la raíz. Deje actuar de 5 a 10 minutos y enjuague con abundante agua. Se recomienda el uso diario.', '2026-04-21 00:00:00'),
(2, 'Shampoo Ultra Nutritivo Premium', 'FÓRMULA DE ALTO DESEMPEÑO\r\n\r\nDESCRIPCIÓN:\r\nShampoo enriquecido con aloe vera natural que hidrata profundamente, reduce el frizz y fortalece la fibra capilar. Ideal para cabellos con keratina, decoloraciones o procesos químicos.\r\n\r\nBENEFICIOS:\r\nAporta brillo, reduce la caída y mejora la manejabilidad del cabello.\r\n\r\nINGREDIENTES PRINCIPALES:\r\nAloe vera, romero, quina, keratina y proteínas.\r\n\r\nMODO DE USO:\r\nAplicar sobre el cabello húmedo, masajear suavemente, dejar actuar de 5 a 10 minutos y enjuagar con abundante agua.', '450 ml', 33900.00, 'imagenes/shampoo2.jpg', 1, 1, 52, 1, 'Cabellos con procesos químicos, decolorados o maltratados.', 'Hidrata profundamente, reduce frizz, fortalece la fibra capilar, aporta brillo y mejora la manejabilidad.', 'Aloe vera, romero, quina, keratina y proteínas.', 'Aplicar sobre el cabello húmedo, masajear suavemente, dejar actuar de 5 a 10 minutos y enjuagar con abundante agua.', '2026-04-21 00:00:00'),
(3, 'Shampoo Emergencia Capilar', 'RECUPERA TU CABELLO\r\n\r\nDESCRIPCIÓN:\r\nShampoo formulado para revitalizar el cabello maltratado, estimular el crecimiento y fortalecer desde la raíz.\r\n\r\nINGREDIENTES PRINCIPALES:\r\nBiotina, aloe vera, romero, aguacate y ortiga.\r\n\r\nMODO DE USO:\r\nAplicar sobre el cuero cabelludo húmedo, masajear y dejar actuar de 5 a 10 minutos. Enjuagar con abundante agua.', '450 ml', 32900.00, 'imagenes/shampoo3.jpg', 1, 1, 50, 1, 'Cabellos dañados, con procesos químicos o crecimiento lento.', 'Estimula el crecimiento, fortalece desde la raíz y revitaliza el cabello.', 'Biotina, aloe vera, romero, aguacate y ortiga.', 'Aplicar sobre el cuero cabelludo húmedo, masajear y dejar actuar de 5 a 10 minutos. Enjuagar con abundante agua.', '2026-04-21 00:00:00'),
(4, 'Shampoo Milagro Herbal', 'CONTROL Y CRECIMIENTO\r\n\r\nDESCRIPCIÓN:\r\nRegula la producción de grasa, fortalece el cabello y estimula el crecimiento con una mezcla de extractos naturales.\r\n\r\nINGREDIENTES PRINCIPALES:\r\nRomero, jengibre, niacinamida, cebolla roja y ginseng.\r\n\r\nMODO DE USO:\r\nAplicar sobre el cabello mojado, masajear el cuero cabelludo, dejar actuar mínimo 5 minutos y enjuagar.', '450 ml', 33900.00, 'imagenes/shampoo4.jpg', 1, 1, 50, 1, 'Cabellos grasos, con caída o poco crecimiento.', 'Controla la grasa, fortalece el cabello, estimula el crecimiento y mejora la salud capilar.', 'Romero, jengibre, niacinamida, cebolla roja y ginseng.', 'Aplicar sobre el cabello mojado, masajear el cuero cabelludo, dejar actuar mínimo 5 minutos y enjuagar.', '2026-04-21 00:00:00'),
(5, 'Acondicionador Antifrizz y fortalecedor con extracto de cebolla y péptidos', 'FÓRMULA EXTRAORDINARIA\r\n\r\nDESCRIPCIÓN:\r\nUna fórmula extraordinaria que combina la cebolla morada y péptidos bioactivos que restauran, fortalecen y le devuelven el brillo natural al cabello, dejándolo sedoso y lleno de vida.\r\n\r\nRESULTADOS:\r\nResultados desde el primer uso. Reduce el frizz y mejora la elasticidad en cada aplicación. Protege el color del cabello, aportando brillo y crecimiento.\r\n\r\nINGREDIENTES PRINCIPALES:\r\nCebolla, péptidos y aminoácidos.\r\n\r\nMODO DE USO:\r\nCon el cabello húmedo aplique cantidad suficiente de producto, esparcir uniformemente de medios a puntas dejándolo actuar de 3 a 5 minutos para aprovechar la fórmula. Enjuagar con abundante agua.', '450 ml', 34900.00, 'imagenes/acondicionador1.jpg', 2, 1, 50, 1, 'Todo tipo de cabello, especialmente aquellos que sufren de resequedad, frizz y puntas quebradizas.', 'Reduce frizz, mejora elasticidad, protege el color y aporta brillo.', 'Cebolla, péptidos y aminoácidos.', 'Con el cabello húmedo aplique cantidad suficiente de producto, esparcir uniformemente de medios a puntas dejándolo actuar de 3 a 5 minutos para aprovechar la fórmula. Enjuagar con abundante agua.', '2026-04-21 00:00:00'),
(6, 'Acondicionador Ultra Nutritivo Premium', 'FÓRMULA ÚNICA\r\n\r\nDESCRIPCIÓN:\r\nUna fórmula con trozos de gel de aloe vera 100% natural que no solo acondiciona, sino que a su vez fortalece y repara, disminuyendo la caída y aportando ultra brillo.\r\n\r\nBENEFICIOS:\r\nLogra una reducción del frizz hasta en un 85% en alta humedad después de 24 horas. Cabello suave, sedoso y vital desde el primer uso.\r\n\r\nINGREDIENTES PRINCIPALES:\r\nTrozos de gel de aloe vera 100% natural, extracto de arroz, extracto de quina, aminoácidos y agentes acondicionadores de alta calidad.\r\n\r\nMODO DE USO:\r\nDespués de lavar el cabello con shampoo, aplicar el acondicionador de medios a puntas, dejando actuar de 5 a 10 minutos y luego enjuagar. Úsalo en cada lavada.', '450 ml', 33000.00, 'imagenes/acondicionador2.jpg', 2, 1, 50, 1, 'Todo tipo de cabello, especialmente aquellos que son de raíz grasa o mixta, que sufren de frizz y maltrato.', 'Reduce frizz, fortalece, aporta brillo y suavidad.', 'Trozos de gel de aloe vera 100% natural, extracto de arroz, extracto de quina, aminoácidos y agentes acondicionadores.', 'Después de lavar el cabello con shampoo, aplicar el acondicionador de medios a puntas, dejando actuar de 5 a 10 minutos y luego enjuagar.', '2026-04-21 00:00:00'),
(7, 'Acondicionador Milagro Herbal', 'FÓRMULA ESTRELLA\r\n\r\nDESCRIPCIÓN:\r\nFormulación diseñada para fortalecer y reparar cabellos con procesos químicos, gracias a su mezcla de aminoácidos, extracto de arroz y romero que también ayuda a disminuir la caída.\r\n\r\nBENEFICIOS:\r\nCabello suave, sedoso y vital. Fragancia duradera que aporta frescura durante el día.\r\n\r\nINGREDIENTES PRINCIPALES:\r\nExtracto de romero, extracto de arroz, aminoácidos y agentes acondicionadores.\r\n\r\nMODO DE USO:\r\nAplicar después del shampoo de medios a puntas, dejar actuar de 3 a 5 minutos y enjuagar con abundante agua.', '450 ml', 33000.00, 'imagenes/acondicionador3.jpg', 2, 1, 50, 1, 'Todo tipo de cabello, especialmente cabellos alisados, decolorados o tratados químicamente.', 'Fortalece, repara, reduce caída y aporta suavidad.', 'Extracto de romero, extracto de arroz, aminoácidos y agentes acondicionadores.', 'Aplicar después del shampoo de medios a puntas, dejar actuar de 3 a 5 minutos y enjuagar con abundante agua.', '2026-04-21 00:00:00'),
(8, 'Acondicionador Reparador Intensivo', 'REPARACIÓN PROFUNDA\r\n\r\nDESCRIPCIÓN:\r\nAcondicionador diseñado para restaurar la fibra capilar, mejorar la textura del cabello y devolverle su suavidad natural.\r\n\r\nBENEFICIOS:\r\nFortalece, hidrata y mejora la manejabilidad del cabello desde la primera aplicación.\r\n\r\nINGREDIENTES PRINCIPALES:\r\nKeratina, proteínas, vitaminas y agentes hidratantes.\r\n\r\nMODO DE USO:\r\nAplicar sobre el cabello limpio y húmedo, distribuir de medios a puntas, dejar actuar unos minutos y enjuagar.', '450 ml', 32000.00, 'imagenes/acondicionador4.jpg', 2, 1, 50, 1, 'Cabellos dañados, secos o con procesos químicos.', 'Fortalece, hidrata y mejora la manejabilidad.', 'Keratina, proteínas, vitaminas y agentes hidratantes.', 'Aplicar sobre el cabello limpio y húmedo, distribuir de medios a puntas, dejar actuar unos minutos y enjuagar.', '2026-04-21 00:00:00'),
(9, 'Bio-repolarizador Capilar', 'FÓRMULA IMPECABLE\r\n\r\nDESCRIPCIÓN:\r\nTratamiento de reparación intensiva que devuelve la fuerza y vitalidad al cabello. Ideal para cabellos maltratados o expuestos a procesos químicos.\r\n\r\nINGREDIENTES PRINCIPALES:\r\nProvitamina B5, keratina, aceite de argán, pulpa de coco y vitamina E.\r\n\r\nMODO DE USO:\r\nAplicar sobre el cabello seco, dejar actuar de 30 a 40 minutos, preferiblemente con gorro térmico. Enjuagar con abundante agua.', '450 ml', 34900.00, 'imagenes/tratamiento1.jpg', 3, 1, 50, 1, 'Cabellos muy dañados por decoloración o calor.', 'Reparación intensiva, devuelve fuerza y vitalidad.', 'Provitamina B5, keratina, aceite de argán, pulpa de coco y vitamina E.', 'Aplicar sobre el cabello seco, dejar actuar de 30 a 40 minutos y enjuagar.', '2026-04-21 00:00:00'),
(10, 'Tratamiento Magia Capilar', '¡MÁS BRILLO, MENOS FRIZZ!\r\n\r\nDESCRIPCIÓN:\r\nTratamiento sin enjuague que aporta brillo inmediato, suavidad y revitaliza el cabello.\r\n\r\nINGREDIENTES PRINCIPALES:\r\nÁcido hialurónico, proteína de arroz, aminoácidos, aceite de sacha inchi.\r\n\r\nMODO DE USO:\r\nAplicar de medios a puntas. No enjuagar.', '150 ml', 35000.00, 'imagenes/tratamiento2.jpg', 3, 1, 50, 1, 'Todo tipo de cabello.', 'Aporta brillo, suavidad y reduce frizz.', 'Ácido hialurónico, proteína de arroz, aminoácidos, aceite de sacha inchi.', 'Aplicar de medios a puntas. No enjuagar.', '2026-04-21 00:00:00'),
(11, 'Tratamiento Capilar a base de Frutas', 'FÓRMULA NATURAL\r\n\r\nDESCRIPCIÓN:\r\nNutre, fortalece y ayuda a disminuir la caída del cabello.\r\n\r\nINGREDIENTES PRINCIPALES:\r\nMango, papaya, banano, provitamina B5 y keratina.\r\n\r\nMODO DE USO:\r\nAplicar y dejar actuar mínimo una hora antes de enjuagar.', '450 ml', 33000.00, 'imagenes/tratamiento3.jpg', 3, 1, 50, 1, 'Todo tipo de cabello, excepto decolorados.', 'Nutre, fortalece y reduce la caída.', 'Mango, papaya, banano, provitamina B5 y keratina.', 'Aplicar y dejar actuar mínimo una hora antes de enjuagar.', '2026-04-21 00:00:00'),
(12, 'Rizos Terapia Nutrición y Crecimiento', 'FÓRMULA ESPECIALIZADA\r\n\r\nDESCRIPCIÓN:\r\nDiseñado para nutrir, fortalecer y mejorar la estructura del cabello rizado.\r\n\r\nINGREDIENTES PRINCIPALES:\r\nMantequilla de mango, aminoácidos y vitamina E.\r\n\r\nMODO DE USO:\r\nAplicar en cabello seco, dejar actuar y enjuagar.', '450 ml', 33000.00, 'imagenes/tratamiento4.jpg', 3, 1, 50, 1, 'Cabellos rizados y crespos.', 'Nutre, fortalece y mejora la estructura del rizo.', 'Mantequilla de mango, aminoácidos y vitamina E.', 'Aplicar en cabello seco, dejar actuar y enjuagar.', '2026-04-21 00:00:00'),
(13, 'Mascarilla capilar reparadora con cebolla y péptidos', 'REPARACIÓN PROFUNDA\r\n\r\nDESCRIPCIÓN:\r\nRepara el cabello dañado, devolviendo brillo y suavidad.\r\n\r\nINGREDIENTES:\r\nCebolla, péptidos, keratina.\r\n\r\nMODO DE USO:\r\nAplicar 20 a 30 minutos y enjuagar.', '450 gr', 38900.00, 'imagenes/mascarilla1.jpg', 4, 1, 50, 1, 'Cabellos dañados por procesos químicos.', 'Repara, devuelve brillo y suavidad.', 'Cebolla, péptidos, keratina.', 'Aplicar 20 a 30 minutos y enjuagar.', '2026-04-21 00:00:00'),
(14, 'Mascarilla Milagro Herbal', 'DESCRIPCIÓN:\r\nFortalece y protege el cabello.\r\n\r\nINGREDIENTES:\r\nPéptidos, vitamina E.\r\n\r\nMODO DE USO:\r\nAplicar y enjuagar.', '450 gr', 36000.00, 'imagenes/mascarilla2.jpg', 4, 1, 50, 1, 'Cabellos secos o maltratados.', 'Fortalece y protege el cabello.', 'Péptidos, vitamina E.', 'Aplicar y enjuagar.', '2026-04-21 00:00:00'),
(15, 'Mascarilla Nutritiva Premium', 'DESCRIPCIÓN:\r\nHidratación profunda.\r\n\r\nINGREDIENTES:\r\nAceites naturales.\r\n\r\nMODO DE USO:\r\nAplicar.', '450 gr', 34000.00, 'imagenes/mascarilla3.jpg', 4, 1, 50, 1, 'Cabellos secos.', 'Hidratación profunda.', 'Aceites naturales.', 'Aplicar.', '2026-04-21 00:00:00'),
(16, 'Mascarilla Reparación Total', 'DESCRIPCIÓN:\r\nRecupera la fibra capilar.\r\n\r\nINGREDIENTES:\r\nProteínas.\r\n\r\nMODO DE USO:\r\nAplicar.', '450 gr', 35000.00, 'imagenes/mascarilla4.jpg', 4, 1, 50, 1, 'Cabellos dañados.', 'Recupera la fibra capilar.', 'Proteínas.', 'Aplicar.', '2026-04-21 00:00:00'),
(17, 'Serum Revitalizante', 'DESCRIPCIÓN:\r\nRepara, nutre y fortalece.\r\n\r\nINGREDIENTES:\r\nAceite de coco, argán, macadamia.\r\n\r\nMODO DE USO:\r\nNo enjuagar.', '55 ml', 3900.00, 'imagenes/serum1.jpg', 5, 1, 50, 1, 'Cabellos dañados.', 'Repara, nutre y fortalece el cabello.', 'Aceite de coco, argán, macadamia.', 'No enjuagar.', '2026-04-21 00:00:00'),
(18, 'Gotas Mágicas Capilares', 'DESCRIPCIÓN:\r\nFortalece y estimula crecimiento.\r\n\r\nINGREDIENTES:\r\nRomero, cebolla.\r\n\r\nMODO DE USO:\r\nAplicar en cuero cabelludo.', '60 ml', 29900.00, 'imagenes/serum2.jpg', 5, 1, 50, 1, 'Caída del cabello.', 'Fortalece y estimula el crecimiento.', 'Romero, cebolla.', 'Aplicar en cuero cabelludo.', '2026-04-21 00:00:00'),
(19, 'Serum Capilar Premium', 'DESCRIPCIÓN:\r\nAporta brillo intenso.\r\n\r\nINGREDIENTES:\r\nAceites naturales.\r\n\r\nMODO DE USO:\r\nAplicar.', '50 ml', 32000.00, 'imagenes/serum3.jpg', 5, 1, 50, 1, 'Cabellos opacos.', 'Aporta brillo intenso al cabello.', 'Aceites naturales.', 'Aplicar.', '2026-04-21 00:00:00'),
(20, 'Serum Reparador Intensivo', 'DESCRIPCIÓN:\r\nReparación profunda.\r\n\r\nINGREDIENTES:\r\nVitaminas.\r\n\r\nMODO DE USO:\r\nAplicar.', '50 ml', 31000.00, 'imagenes/serum4.jpg', 5, 1, 50, 1, 'Cabellos dañados.', 'Reparación profunda del cabello.', 'Vitaminas.', 'Aplicar.', '2026-04-21 00:00:00'),
(21, 'Perfume Capilar Gold', 'DESCRIPCIÓN:\r\nFragancia herbal con brillo.\r\n\r\nINGREDIENTES:\r\nRosa, vainilla.\r\n\r\nMODO DE USO:\r\nAplicar.', '120 ml', 32000.00, 'imagenes/perfume1.jpg', 6, 1, 49, 1, 'Todo tipo de cabello.', 'Aporta fragancia herbal y brillo al cabello.', 'Rosa, vainilla.', 'Aplicar.', '2026-04-21 00:00:00'),
(22, 'Perfume Capilar Martina', 'DESCRIPCIÓN:\r\nFragancia dulce.\r\n\r\nINGREDIENTES:\r\nFrutas.\r\n\r\nMODO DE USO:\r\nAplicar.', '120 ml', 32000.00, 'imagenes/perfume2.jpg', 6, 1, 50, 1, 'Todo tipo.', 'Fragancia dulce que aporta frescura.', 'Frutas.', 'Aplicar.', '2026-04-21 00:00:00'),
(23, 'Perfume Capilar Bali', 'DESCRIPCIÓN:\r\nFragancia suave.\r\n\r\nINGREDIENTES:\r\nArgán.\r\n\r\nMODO DE USO:\r\nAplicar.', '120 ml', 32000.00, 'imagenes/perfume3.jpg', 6, 1, 50, 1, 'Todo tipo.', 'Fragancia suave con efecto nutritivo.', 'Argán.', 'Aplicar.', '2026-04-21 00:00:00'),
(24, 'Perfume Capilar Sublime', 'DESCRIPCIÓN:\r\nFragancia cálida.\r\n\r\nINGREDIENTES:\r\nExtractos.\r\n\r\nMODO DE USO:\r\nAplicar.', '120 ml', 32000.00, 'imagenes/perfume4.jpg', 6, 1, 50, 1, 'Todo tipo.', 'Fragancia cálida con efecto de suavidad.', 'Extractos.', 'Aplicar.', '2026-04-21 00:00:00'),
(25, 'Cepillo Capilar Antienredos', 'Cepillo diseñado para desenredar el cabello sin generar quiebre ni maltrato. Ideal para uso diario en cabello seco o húmedo.\r\n', '1 unidad', 18000.00, 'imagenes/cepillo1.jpg', 7, 1, 50, 1, 'Todo tipo de cabello.', 'Reduce el frizz, evita la caída por quiebre y facilita el peinado.', 'Cerdas flexibles de nylon y base ergonómica.', 'Utilizar sobre el cabello seco o húmedo desde puntas hacia la raíz.', '2026-04-22 00:00:00'),
(26, 'Cepillo Capilar Térmico Profesional', 'Cepillo redondo diseñado para moldear el cabello durante el secado, aportando volumen y forma.\r\n\r\n\r\n', '1 unidad', 25000.00, 'imagenes/cepillo2.jpg', 7, 1, 50, 1, 'Cabellos expuestos a calor.', 'Facilita el secado, mejora el acabado del peinado.', 'Cerámica y cerdas resistentes al calor.', 'Utilizar junto con secador para moldear el cabello.', '2026-04-22 00:00:00'),
(27, 'Masajeador Capilar de Silicona', 'Herramienta diseñada para estimular la circulación sanguínea del cuero cabelludo durante el lavado.', '1 unidad', 15000.00, 'imagenes/masajeador1.jpg', 7, 1, 50, 1, 'Todo tipo de cuero cabelludo.', 'Mejora la absorción de productos capilares y promueve el crecimiento.', 'Silicona suave.', 'Usar durante el lavado con movimientos circulares.', '2026-04-22 00:00:00'),
(28, 'Masajeador Capilar Manual Premium', 'Masajeador manual que relaja el cuero cabelludo y estimula los folículos capilares.\r\n\r\n\r\n\r\n\r\n\r\n\r\n', '1 unidad', 22000.00, 'imagenes/masajeador2.jpg', 7, 1, 50, 1, 'Personas con caída del cabello o estrés capilar.', 'Reduce tensión y favorece el crecimiento.', 'Plástico resistente y puntas suaves.', 'Aplicar sobre el cuero cabelludo seco o húmedo.', '2026-04-22 00:00:00'),
(29, 'perfume hombre', 'perfume hombre', '450 ml', 25000.00, 'imagne.jpg', 6, 1, 50, 1, 'cuerpo', 'olor', 'perfume', 'aplicar en piel', '2026-04-28 00:00:00'),
(36, 'aaa', 'sasa', 'aaaaa', 20000.00, 'asassaas.jpg', 2, 1, 2, 1, 'asdas', 'asas', 'asass', 'a', '2026-05-05 20:30:33'),
(37, 'ramdom1', 'ramdom1', '1 Unidad', 15000.00, 'imagen.jpg', 2, 1, 5, 1, 'ramdom1', 'ramdom1', 'ramdom1', 'ramdom1', '2026-05-06 11:18:29'),
(38, 'ramdom2', 'ramdom2', '1 Unidad', 15000.00, 'imagen.jpg', 4, 1, 12, 1, 'ramdom2', 'ramdom2', 'ramdom2', 'ramdom2', '2026-05-06 11:21:32'),
(39, 'ramdom3', 'ramdom3', '1 Unidad', 50000.00, 'imagen.jpg', 3, 1, 41, 1, 'ramdom3', 'ramdom3', 'ramdom3', 'ramdom3', '2026-05-06 11:36:29'),
(40, 'ramdom4', 'ramdom4', '1 Unidad', 20000.00, 'imagen.jpg', 1, 1, 20000, 1, 'ramdom4', 'ramdom4', 'ramdom4', 'ramdom4', '2026-05-06 14:51:32');

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `roles`
--
CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `nombre_rol` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--
INSERT INTO `roles` (`id_rol`, `nombre_rol`) VALUES
(1, 'Administrador'),
(2, 'Cliente'),
(3, 'Moderador');

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `usuarios`
--
-- La validación de contraseñas ya no se implementa con triggers SQL porque
-- eso bloquea hashes bcrypt válidos. Debe hacerse en la capa de aplicación.
CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `id_rol` int(11) DEFAULT NULL,
  `fecha_registro` datetime DEFAULT current_timestamp(),
  `estado` tinyint(4) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--
-- Se eliminan todos los usuarios heredados del dump original para evitar
-- credenciales inseguras, inconsistencias de hashing y cuentas de prueba sin
-- control. Se crean únicamente dos cuentas administrativas iniciales con
-- contraseñas almacenadas como hashes bcrypt compatibles con verificadores
-- basados en `password_verify` / bcrypt en la aplicación.
--
-- IMPORTANTE:
--   - Las contraseñas en texto plano NO se documentan aquí.
--   - Si deseas rotarlas, genera el nuevo hash desde la aplicación o desde una
--     herramienta compatible con bcrypt y reemplázalo antes de importar.
INSERT INTO `usuarios` (`id_usuario`, `nombre`, `apellido`, `correo`, `password`, `telefono`, `id_rol`, `fecha_registro`, `estado`) VALUES
(1, 'Admin', 'Principal', 'admin@milagrosbeauty.com', '$2y$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', '3000000001', 1, '2026-06-13 02:45:00', 1),
(2, 'Admin', 'Respaldo', 'soporte@milagrosbeauty.com', '$2y$10$e0NRaKWcEv2Y8K2g2s0Y4.4VwWJ4v0LlwM1c01qmPvvrLpzjAU6R2', '3000000002', 1, '2026-06-13 02:46:00', 1);

-- --------------------------------------------------------
--
-- Índices para tablas volcadas
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id_categoria`);

ALTER TABLE `ciudades`
  ADD PRIMARY KEY (`id_ciudad`);

ALTER TABLE `configuracion`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `estados_pedido`
  ADD PRIMARY KEY (`id_estado`);

ALTER TABLE `historial_login`
  ADD PRIMARY KEY (`id_historial`),
  ADD KEY `id_usuario` (`id_usuario`);

ALTER TABLE `marcas`
  ADD PRIMARY KEY (`id_marca`);

ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id_pedido`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_estado` (`id_estado`);

ALTER TABLE `pedido_detalle`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `id_pedido` (`id_pedido`),
  ADD KEY `id_producto` (`id_producto`);

ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `id_categoria` (`id_categoria`),
  ADD KEY `id_marca` (`id_marca`);

ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`);

ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `id_rol` (`id_rol`);

-- --------------------------------------------------------
--
-- AUTO_INCREMENT de las tablas volcadas
--
ALTER TABLE `categorias`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

ALTER TABLE `ciudades`
  MODIFY `id_ciudad` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `configuracion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

ALTER TABLE `estados_pedido`
  MODIFY `id_estado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

ALTER TABLE `historial_login`
  MODIFY `id_historial` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `marcas`
  MODIFY `id_marca` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

ALTER TABLE `pedidos`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

ALTER TABLE `pedido_detalle`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

ALTER TABLE `productos`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

-- --------------------------------------------------------
--
-- Restricciones para tablas volcadas
--
-- Incluye tanto las relaciones originales como las FKs faltantes del script
-- complementario.
ALTER TABLE `historial_login`
  ADD CONSTRAINT `historial_login_ibfk_1`
  FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

ALTER TABLE `pedidos`
  ADD CONSTRAINT `fk_pedidos_usuario`
  FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `fk_pedidos_estado`
  FOREIGN KEY (`id_estado`) REFERENCES `estados_pedido` (`id_estado`);

ALTER TABLE `pedido_detalle`
  ADD CONSTRAINT `pedido_detalle_ibfk_1`
  FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`),
  ADD CONSTRAINT `pedido_detalle_ibfk_2`
  FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`);

ALTER TABLE `productos`
  ADD CONSTRAINT `fk_productos_categoria`
  FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`),
  ADD CONSTRAINT `fk_productos_marca`
  FOREIGN KEY (`id_marca`) REFERENCES `marcas` (`id_marca`);

ALTER TABLE `usuarios`
  ADD CONSTRAINT `fk_usuarios_rol`
  FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);

-- --------------------------------------------------------
--
-- Índices auxiliares para consultas frecuentes
--
CREATE INDEX `idx_productos_estado` ON `productos`(`estado`);
CREATE INDEX `idx_productos_categoria` ON `productos`(`id_categoria`);
CREATE INDEX `idx_pedidos_fecha` ON `pedidos`(`fecha_pedido`);

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;