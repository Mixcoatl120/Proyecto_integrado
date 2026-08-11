# Proyecto Integrado
Es una aplicacion que realice cuando realice mi servicio social tuvo como objetivo la creación de un sistema capaz de gestionar tramites y visualizar estadísticas del día.
Aplicación web en Flask para gestión de trámites internos con roles de administrador y usuario.

## Descripción

Esta aplicación permite:
- Autenticación de usuarios con Flask-Login.
- Gestión de ingresos de trámites y asuntos.
- Consulta de expedientes y generación de reportes en Excel.
- Turnado y actualización de registros.
- Generación de cédulas en PDF para trámites.
- Diferenciación entre rutas y vistas para administradores y usuarios normales.

## Características principales

- Login y logout.
- Rutas separadas para administración (`admin/`) y usuarios (`users/`).
- Modelos de datos definidos con SQLAlchemy en `dbModel.py`.
- Conexión a PostgreSQL.
- Exportación de datos en formato Excel (`.xlsx`).
- Descarga de archivos desde la carpeta `doc/`.
- Vistas basadas en plantillas Jinja2.

## Estructura del proyecto

- `app.py`: aplicación principal y registro de blueprints.
- `dbModel.py`: definición de modelos SQLAlchemy.
- `login/`: login, modelos de usuario y rutas de autenticación.
- `admin/`: rutas y plantillas para funciones de administrador.
- `users/`: rutas y plantillas para usuarios generales.
- `static/`: CSS, JavaScript y recursos estáticos.
- `templates/`: plantillas base compartidas.
- `doc/`: archivos Excel generados o asociados al proyecto.
- `requirements.txt`: dependencias del proyecto.

## Dependencias

El proyecto utiliza estas librerías principales:

- Flask
- Flask-Login
- Flask-SQLAlchemy
- Flask-WTF
- psycopg2
- pandas
- openpyxl
- reportlab

## Instalación

1. Crear un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar la base de datos PostgreSQL:

- En `app.py` se define la conexión:
  `postgresql://postgres:Mixcoatl120.@localhost/siset`
- Ajustar el usuario, contraseña y nombre de la base de datos según el entorno.

4. Crear las tablas y datos necesarios en PostgreSQL según la estructura esperada por `dbModel.py`.

## Ejecución

```bash
python app.py
```

La aplicación correrá en `http://127.0.0.1:5000/` por defecto.

## Uso

- Ingresar en la ruta `/login`.
- Si el usuario es `admin`, accederá a las funciones de administrador.
- Los demás usuarios acceden a rutas de usuario (`home_u`, `ingreso_u`, `turnado_u`, `consulta_u`, `cedula_u`).

## Notas importantes

- El proyecto depende de una base de datos existente con tablas como `seguimiento`, `cat_tipo_ingreso`, `cat_materia`, `admin_users`, entre otras.
- La carpeta `doc/` se utiliza para guardar y descargar archivos Excel generados por la aplicación.
- El archivo `app.py` usa `debug=True`, por lo que no es recomendado en producción.

## Recomendaciones

- Cambiar `SECRET_KEY` a un valor seguro en producción.
- No exponer credenciales de base de datos en el código.
- Utilizar migraciones (Flask-Migrate) para administrar el esquema de base de datos si el proyecto crece.

## Funcionamiento

<img width="1365" height="768" alt="Gemini_Generated_Image_col68ocol68ocol6" src="https://github.com/user-attachments/assets/3f5faa34-58c4-4105-80bf-b512529aaa3e" />

