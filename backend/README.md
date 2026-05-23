# Milagro's Beauty — Backend (Refactor MVC + Blueprints)

Backend del proyecto formativo ADSO reorganizado bajo el patrón **MVC con Blueprints**, con capa de servicios, repositorios, decoradores de seguridad y manejo global de errores.

## Estructura

```
backend/
├── app/
│   ├── __init__.py          ← Application Factory
│   ├── config.py            ← Configuración por entorno (.env)
│   ├── extensions.py        ← Bcrypt, CORS
│   ├── database/            ← Conexión MySQL + context manager
│   ├── models/              ← Entidades del dominio
│   ├── repositories/        ← SQL aislado por entidad
│   ├── services/            ← Reglas de negocio
│   ├── routes/              ← Blueprints (endpoints HTTP)
│   ├── decorators/          ← @login_required, @requiere_rol
│   ├── errors/              ← Excepciones + handler global
│   ├── utils/               ← Validadores, helpers
│   ├── static/              ← CSS, JS, imágenes
│   └── templates/           ← HTML
├── tests/                   ← Pruebas (opcionales)
├── .env                     ← Variables locales (no se sube)
├── .env.example             ← Plantilla pública
├── requirements.txt
└── run.py                   ← Punto de entrada
```

## Instalación

```bash
# 1) Crear entorno virtual
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

# 2) Instalar dependencias
pip install -r requirements.txt

# 3) Copiar configuración
copy .env.example .env         # Windows
# cp .env.example .env         # Linux/Mac
# Editar .env y poner credenciales reales si difieren

# 4) Asegurar que la base de datos esté importada
#    a) Importar database/milagros_beauty_vr7.sql en phpMyAdmin.
#    b) Ejecutar database/01_alter_milagros_beauty.sql después.

# 5) Levantar la aplicación
python run.py
```

Abre http://127.0.0.1:5000

## Comandos útiles

- `python run.py` → modo desarrollo (debug ON).
- `set FLASK_ENV=production && python run.py` → producción local.

## Decisiones técnicas (resumen)

| Tema | Decisión | Razón |
|---|---|---|
| Arquitectura | MVC + Blueprints | Enseñado en ADSO, defendible en sustentación |
| Hashing | bcrypt (Flask-Bcrypt) | Estándar OWASP |
| Sesiones | flask.session firmada | Suficiente para monolito |
| Configuración | .env + python-dotenv | 12-Factor App |
| Errores | Excepciones tipadas + handler global | Respuestas uniformes |

Ver `database/02_notas_migracion_passwords.md` para el detalle de la migración de contraseñas legadas.
