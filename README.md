### 🧊 Sistema de Gestión Integral - Frío y Agroindustrias SpA

### 📋 Descripción General del Proyecto
El proyecto Frío y Agroindustrias SpA es una plataforma web desarrollada en Django diseñada específicamente para optimizar y automatizar los procesos administrativos, operativos y de control interno de una empresa agroindustrial. El sistema centraliza la gestión de recursos clave, abarcando desde el registro y validación de entidades financieras (clientes y proveedores) hasta el control de acceso de los trabajadores, inventarios y obras.

### 🏗️ Arquitectura y Módulos Principales
1. Módulo de Finanzas:
Gestión de Proveedores y Clientes: Administración completa de entidades comerciales mediante vistas basadas en clases (Class-Based Views) y funciones, permitiendo registrar, actualizar y eliminar perfiles de manera segura.

* Validación de RUT Chileno: Integración de validadores algorítmicos personalizados (validar_rut_chileno) para asegurar la integridad de los datos tributarios y evitar registros erróneos o duplicados en las tablas de clientes y proveedores.

* Formularios Dinámicos: Implementación de ProveedorForm y ClienteForm con integración nativa de estilos de Bootstrap para una experiencia de usuario fluida y validación en tiempo real.

2. Módulo de Usuarios y Seguridad:
* Autenticación Personalizada: Control de acceso robusto mediante un sistema de inicio de sesión (custom_login), gestión de sesiones y cierre de sesión seguro por método POST.

* Control de Roles y Permisos: Restricción de vistas administrativas y de creación mediante LoginRequiredMixin y UserPassesTestMixin, permitiendo que únicamente perfiles autorizados (como superusuarios o personal de gerencia) puedan registrar o modificar trabajadores.

* Listado de Trabajadores (TrabajadorListView): Visualización centralizada del personal activo dentro de la organización bajo estrictas políticas de seguridad.

3. Interfaz de Usuario y Estilos (Frontend)
* Diseño Responsivo: Integración del framework Bootstrap 5.3 a través de CDN en una plantilla base unificada (base.html), garantizando adaptabilidad en dispositivos móviles y de escritorio.

* Estilos Personalizados (style.css): Hojas de estilo dedicadas para estilización de tarjetas, barras de navegación oscuras, tipografías y paletas de colores corporativas.

* Sistema de Alertas Dinámicas: Notificaciones flotantes (messages de Django) integradas para dar feedback inmediato al usuario tras realizar acciones CRUD (creación, edición o eliminación exitosa).

### 🛠️ Tecnologías Utilizadas
* Backend: Python / Django (Vistas basadas en clases y funciones, ORM, sistema de autenticación y migraciones).

* Frontend: HTML5, CSS3, Bootstrap 5.3, JavaScript.

* Base de Datos: SQLite (Entorno de desarrollo local).

* Control de Versiones: Git / GitHub (Flujo de ramas y Pull Requests).

* Frontend: HTML5, CSS3, Bootstrap 5.3, JavaScript.

* Base de Datos: SQLite (Entorno de desarrollo local).

* Control de Versiones: Git / GitHub (Flujo de ramas y Pull Requests).
