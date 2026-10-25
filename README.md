# Sistema de Gestión de Personal - Escuela "Alberto Sanabria" (MPPE)

Aplicación web desarrollada para el registro, control, seguimiento y generación de fichas oficiales del personal **Docente**, **Administrativo** y **Obrero / Apoyo** adscrito a la Escuela Alberto Sanabria bajo los lineamientos del Ministerio del Poder Popular para la Educación (MPPE).

---

## 📋 Información y Campos Gestionados

La aplicación recopila de manera estructurada los siguientes datos requeridos por la institución:

1. **Datos Personales y de Identidad**:
   - Cédula de Identidad (V / E) con validación única para evitar duplicados.
   - Nombres y Apellidos completos.
   - Sexo / Género.
   - Fecha de nacimiento y cálculo automático de edad actual.
   - Teléfono de contacto y correo electrónico.
   - Dirección de habitación.

2. **Datos Laborales e Institucionales MPPE**:
   - **Tipo de Personal**: *Docente*, *Administrativo*, o *Obrero / Apoyo*.
   - **Cargo o Función Desempeñada**: (Ej: Docente de Aula, Subdirector, Secretaria I, Personal de Mantenimiento, Cocinero de la Patria PAE, etc.).
   - **Fecha de Ingreso al MPPE** y cálculo dinámico de **años de servicio** acumulados.
   - **Fecha de Ingreso al Plantel** escolar.
   - **Condición Laboral**: Fijo / Titular, Contratado, Interino, Suplente.
   - **Turno de Trabajo**: Mañana, Tarde, Integral / Doble turno, Nocturno.
   - **Área o Grado Asignado**: Grado/sección o departamento asignado.
   - **Estatus Laboral**: Activo, Reposo Médico, Permiso, Comisión de Servicio, Jubilado.

3. **Nivel Académico y Formación de Base**:
   - Nivel de Instrucción: Bachiller, Técnico Medio, T.S.U., Licenciatura / Profesor, Especialización, Maestría, Doctorado.
   - Título o Especialidad (Educación Integral, Recursos Humanos, Informática, etc.).

4. **Cursos y Formaciones Realizadas (Acreditaciones)**:
   - Capacidad dinámica de registrar múltiples cursos o talleres por cada trabajador:
     - Nombre del curso, taller o diplomado.
     - Institución u organismo emisor (MPPE, CENAMEC, UNEM Samuel Robinson, INCES, etc.).
     - Cantidad de horas académicas.
     - Año de culminación.
     - Modalidad (Presencial, En línea / Virtual, Mixta).
     - Número de folio o código de certificado.

5. **Observaciones Generales y Expediente**:
   - Notas pedagógicas, comisiones de servicio o datos especiales de cada trabajador.

---

## 🚀 Cómo Iniciar la Aplicación

### Opción 1: Con Docker y Gunicorn (Producción Recomendada)
1. Construir la imagen Docker:
   ```bash
   docker build -t alberto-sanabria-staff .
   ```
2. Ejecutar el contenedor (con persistencia de base de datos):
   ```bash
   docker run -d -p 5000:5000 --name escuela_personal -v $(pwd)/escuela_sanabria.db:/app/escuela_sanabria.db alberto-sanabria-staff
   ```
   *O alternativamente con Docker Compose:*
   ```bash
   docker compose up -d
   ```
3. Abra su navegador en: **`http://localhost:5000`**

### Opción 2: Inicio Rápido en Windows con un Clic (Local)
Haga doble clic en el archivo:
```text
iniciar_aplicacion.bat
```
Este archivo iniciará el servidor local y abrirá automáticamente la aplicación en su navegador web preferido en `http://127.0.0.1:5000`.

### Opción 3: Desde la Terminal / Consola de Comandos
1. Abra una terminal en la carpeta del proyecto:
   ```powershell
   cd "C:\Users\JOSÉ P\.gemini\antigravity\scratch\alberto-sanabria-staff"
   ```
2. Ejecute el servidor:
   ```powershell
   python app.py
   ```
3. Abra su navegador web en:
   ```text
   http://127.0.0.1:5000
   ```

---

## 🖨️ Ficha Oficial Imprimible (Formato MPPE)
Cada trabajador dispone de un botón **"Imprimir Ficha Oficial MPPE"** que genera una hoja de registro lista para imprimir en hoja tamaño carta, con el membrete oficial del MPPE, datos laborales, desglose de cursos y casillas de firma del trabajador y sello de la dirección del plantel para su archivo físico en carpeta institucional.

---

## 📊 Exportación y Respaldo
- **Descarga de Nómina en Excel (.csv con UTF-8)**: Exporta el listado completo o filtrado directamente compatible con Microsoft Excel.
- **Historial de Cursos (.csv)**: Exporta todas las formaciones realizadas por el personal.
- **Copia de Seguridad (.json)**: Permite respaldar toda la base de datos de manera íntegra.

---

## 🗄️ Base de Datos
Los datos se almacenan de forma local y persistente en la base de datos SQLite:
`escuela_sanabria.db` (ubicada en la misma carpeta del proyecto, sin requerir servidores externos).
