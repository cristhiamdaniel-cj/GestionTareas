
# 🗂️ **Matriz de Eisenhower - Gestión de Tareas**

La **Matriz de Eisenhower** es una aplicación web diseñada para ayudar a organizar y priorizar tareas según su **urgencia** e **importancia**. Este proyecto está desarrollado en **Django** y está accesible a través de un dominio seguro utilizando **NGROK**.

---

## ✨ **Características principales**

✅ Gestión y clasificación de tareas en cuadrantes:
- **Importante y Urgente**: ¡Prioridad máxima!  
- **No Importante pero Urgente**: Planifícalas.  
- **Importante pero No Urgente**: Delegables.  
- **No Importante ni Urgente**: Considéralas como descartables.  

✅ Funciones disponibles:  
- Crear, actualizar, completar y mover tareas.  
- Solicitar una **solución detallada** al completar una tarea.  
- Registro de auditoría de acciones realizadas (solo para superusuarios).  
- Clasificación visual mediante drag-and-drop.  

✅ Control de acceso basado en roles:  
- 👑 **Superusuario (danielcampos)**: Acceso completo.  
- 👩‍💻 **Usuarios estándar (danielamazuera, sofiapuerto)**: Sin acceso a eliminar tareas ni ver auditorías.

---

## 🏗️ **Estructura del proyecto**

```plaintext
GestionTareas/
├── db.sqlite3                # Base de datos SQLite
├── manage.py                 # Herramienta de gestión de Django
├── MatrizEisenhower/         # Configuración principal
│   ├── settings.py           # Configuración general
│   ├── urls.py               # Rutas principales
├── Procfile                  # Configuración para despliegue
├── requirements.txt          # Dependencias
├── taskmanager/              # Lógica de la aplicación
│   ├── data_seed.py          # Creación de usuarios iniciales
│   ├── forms.py              # Formularios personalizados
│   ├── models.py             # Modelos de datos
│   ├── urls.py               # Rutas específicas
│   ├── views.py              # Lógica de negocio
├── templates/                # Plantillas HTML
│   ├── matrix.html           # Pantalla principal
│   ├── create_task.html      # Crear tarea
│   ├── update_task.html      # Actualizar tarea
│   ├── delete_task.html      # Eliminar tarea
│   ├── mark_completed.html   # Completar tarea
│   ├── audit_log.html        # Registro de auditoría
```

---

## 🚀 **Cómo empezar**

### 1️⃣ **Requisitos previos**
- Python 3.9+
- Django 5.x
- NGROK para dominio seguro  
  *(¡Instálalo desde [ngrok.com](https://ngrok.com/)!)*
- SQLite (incluido por defecto)

### 2️⃣ **Instalar el proyecto**

```bash
git clone https://github.com/tu-usuario/matriz-eisenhower.git
cd matriz-eisenhower
```

### 3️⃣ **Configurar el entorno virtual**

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
.venv\Scripts\activate     # Windows
```

### 4️⃣ **Instalar dependencias**

```bash
pip install -r requirements.txt
```

### 5️⃣ **Configurar las variables sensibles**

Crea un archivo `.env` en la raíz del proyecto:

```plaintext
SUPERUSER_PASS=tu_contraseña_segura
USER1_PASS=tu_contraseña_segura
USER2_PASS=tu_contraseña_segura
```

**Nota:** Este archivo está en `.gitignore` para evitar subir datos sensibles al repositorio.

### 6️⃣ **Migrar la base de datos**

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7️⃣ **Cargar los usuarios iniciales**

Ejecuta el siguiente comando para registrar usuarios:

```bash
python manage.py runscript data_seed
```

### 8️⃣ **Iniciar la aplicación**

Ejecuta Django en el servidor local y habilita NGROK:

```bash
# Inicia el servidor de Django
python manage.py runserver 0.0.0.0:8000

# Activa NGROK con un dominio personalizado
ngrok http --hostname=matriz.ngrok.dev 8000
```

Accede a la aplicación en:  
🌐 **https://matriz.ngrok.dev**

---

## 👥 **Roles y accesos**

| Usuario          | Contraseña       | Rol            | Permisos                                              |
|-------------------|------------------|----------------|------------------------------------------------------|
| **danielcampos**  | `SUPERUSER_PASS` | Superusuario   | Crear, actualizar, completar, eliminar, ver auditoría |
| **danielamazuera**| `USER1_PASS`     | Usuario estándar | Crear, actualizar, completar tareas                 |
| **sofiapuerto**   | `USER2_PASS`     | Usuario estándar | Crear, actualizar, completar tareas                 |

---

## 🔐 **Seguridad**

🔒 Contraseñas sensibles están gestionadas en el archivo `.env` usando `python-decouple`.  
🔒 Las contraseñas de usuarios están cifradas con el sistema de autenticación de Django.  
🔒 Roles y permisos definidos para evitar accesos no autorizados.  

---

## 🎯 **Próximos pasos (Versión 2.0)**

✨ Mejoras de diseño con un equipo de frontend.  
✨ Implementación de notificaciones por correo electrónico.  
✨ Reportes exportables en formatos PDF y Excel.  
✨ Optimización para dispositivos móviles.  

---

## 💻 **Créditos**

- **Desarrollador Principal**: Cristhiam Daniel  
- **Colaboradores**: Equipo de despacho de Daniela y Sofia  

---

## 📝 **Licencia**

Este proyecto está bajo la licencia MIT. Para más información, consulta el archivo [LICENSE](LICENSE).
