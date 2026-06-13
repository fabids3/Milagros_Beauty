# Migración de contraseñas legadas

## Contexto

La tabla `usuarios` contenía tres tipos de contraseñas mezcladas:

| Tipo | Ejemplo | Origen |
|---|---|---|
| Texto plano | `'123'`, `'123123'` | Inserts manuales viejos |
| Bcrypt PHP | `$2y$10$...` | Sistema anterior en PHP |
| Bcrypt Python | `$2b$12$...` | Sistema nuevo (Flask-Bcrypt) |

## Estrategia adoptada (transparente para el usuario)

No se ejecuta un script masivo de migración. En cambio:

1. **Verificación inteligente en `AuthService._verificar_password`**:
   - Si el password almacenado empieza por `$2a$`, `$2b$` o `$2y$`, se verifica con bcrypt (normalizando `$2y$` → `$2b$` para compatibilidad PHP/Python).
   - Si no, se compara como texto plano contra el password ingresado.

2. **Migración automática al primer login exitoso**:
   - Cuando un usuario con password plano inicia sesión correctamente, su contraseña se reemplaza por el hash bcrypt equivalente en la misma transacción.
   - El usuario no se entera: usa su contraseña normal.

3. **Garantías**:
   - Cualquier registro nuevo creado por `/registrar` ya se almacena hasheado.
   - Los logins funcionan con cualquiera de los tres formatos.
   - Tras un par de logins, la base queda 100% en formato bcrypt moderno.

## Si la propietaria prefiere migrar todo de golpe

Ejecutar esta consulta para identificar usuarios pendientes:

```sql
SELECT id_usuario, correo
FROM usuarios
WHERE password NOT LIKE '$2_$%';
```

Luego, contactarlos para que hagan login una sola vez. La migración ocurrirá automáticamente.
