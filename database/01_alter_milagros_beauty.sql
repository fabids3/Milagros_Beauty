-- =============================================================================
-- 01_alter_milagros_beauty.sql
-- -----------------------------------------------------------------------------
-- Script complementario al volcado original `milagros_beauty_vr7.sql`.
-- Aplica:
--   1) Eliminación de los triggers de password (incompatibles con bcrypt).
--   2) Conversión de `subtotal` en `pedido_detalle` a columna GENERADA.
--   3) Adición de FOREIGN KEYS faltantes.
--   4) UNIQUE en `correo` (ya existía, se deja por seguridad).
--   5) Limpieza opcional de datos huérfanos antes de aplicar FKs.
--
-- Cómo aplicarlo:
--   1) Importa primero `milagros_beauty_vr7.sql` desde phpMyAdmin.
--   2) Ejecuta este archivo a continuación.
--
-- IMPORTANTE: este script asume que ya importaste el volcado original.
-- =============================================================================

USE milagros_beauty_vr7;

-- -----------------------------------------------------------------------------
-- 1) DROP de triggers de password
-- -----------------------------------------------------------------------------
-- Por qué: el regex del trigger se aplicaba al valor INSERTADO. Como ahora
-- guardamos el HASH bcrypt ($2b$12$....), el regex falla siempre y bloquea
-- cualquier registro o actualización. La validación se hace ahora en el
-- servicio Python (app/utils/validators.py) ANTES de hashear.
-- -----------------------------------------------------------------------------
DROP TRIGGER IF EXISTS validar_password;
DROP TRIGGER IF EXISTS actualizar_password;

-- -----------------------------------------------------------------------------
-- 2) `pedido_detalle.subtotal` como columna generada
-- -----------------------------------------------------------------------------
-- En el código original esta columna se dejaba en NULL para evitar un error 500.
-- Una columna generada (GENERATED) la calcula automáticamente la BD.
-- Es la solución correcta: ni el código Python ni el SQL de INSERT tienen
-- que recordar calcularla.
-- -----------------------------------------------------------------------------
ALTER TABLE pedido_detalle
    DROP COLUMN subtotal;

ALTER TABLE pedido_detalle
    ADD COLUMN subtotal DECIMAL(10,2)
    GENERATED ALWAYS AS (cantidad * precio_unitario) STORED;

-- -----------------------------------------------------------------------------
-- 3) Limpieza preventiva: el producto id=38 tiene id_marca = NULL.
--    Antes de añadir la FK no nula, lo reasignamos a la marca por defecto (1).
-- -----------------------------------------------------------------------------
UPDATE productos SET id_marca = 1 WHERE id_marca IS NULL;

-- -----------------------------------------------------------------------------
-- 4) FOREIGN KEYS faltantes
-- -----------------------------------------------------------------------------
-- Garantizan integridad referencial. Sin estas FKs, el modelo permite registros
-- huérfanos (un pedido apuntando a un usuario que no existe, etc.).
-- -----------------------------------------------------------------------------

-- usuarios.id_rol → roles.id_rol
ALTER TABLE usuarios
    ADD CONSTRAINT fk_usuarios_rol
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol);

-- pedidos.id_usuario → usuarios.id_usuario
ALTER TABLE pedidos
    ADD CONSTRAINT fk_pedidos_usuario
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario);

-- pedidos.id_estado → estados_pedido.id_estado
ALTER TABLE pedidos
    ADD CONSTRAINT fk_pedidos_estado
    FOREIGN KEY (id_estado) REFERENCES estados_pedido(id_estado);

-- productos.id_categoria → categorias.id_categoria
ALTER TABLE productos
    ADD CONSTRAINT fk_productos_categoria
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria);

-- productos.id_marca → marcas.id_marca
ALTER TABLE productos
    ADD CONSTRAINT fk_productos_marca
    FOREIGN KEY (id_marca) REFERENCES marcas(id_marca);

-- -----------------------------------------------------------------------------
-- 5) Índices auxiliares para consultas frecuentes
-- -----------------------------------------------------------------------------
CREATE INDEX idx_productos_estado    ON productos(estado);
CREATE INDEX idx_productos_categoria ON productos(id_categoria);
CREATE INDEX idx_pedidos_fecha       ON pedidos(fecha_pedido);

-- -----------------------------------------------------------------------------
-- Fin del script
-- -----------------------------------------------------------------------------
