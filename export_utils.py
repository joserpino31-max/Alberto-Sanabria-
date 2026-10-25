import csv
import io
import json
from database import get_all_staff, get_all_courses, get_staff_by_id, create_staff, get_connection

def generate_staff_csv(category=None, status=None, condition=None):
    """
    Generates a CSV string formatted for Excel with UTF-8-SIG (BOM)
    containing full staff information and their courses count.
    """
    staff_list = get_all_staff(category=category, status=status, condition=condition)
    
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    
    # Headers in Spanish
    writer.writerow([
        "Cédula",
        "Apellidos",
        "Nombres",
        "Sexo",
        "Fecha de Nacimiento",
        "Edad",
        "Teléfono",
        "Correo Electrónico",
        "Dirección",
        "Tipo de Personal",
        "Cargo",
        "Condición Laboral",
        "Fecha Ingreso MPPE",
        "Años de Servicio MPPE",
        "Fecha Ingreso al Plantel",
        "Turno",
        "Área / Grado Asignado",
        "Nivel Académico",
        "Especialidad",
        "Estatus",
        "Cantidad de Cursos",
        "Observaciones"
    ])
    
    for s in staff_list:
        cedula = f"{s.get('nationality', 'V')}-{s.get('id_number', '')}"
        writer.writerow([
            cedula,
            s.get('last_name', ''),
            s.get('first_name', ''),
            s.get('gender', ''),
            s.get('birth_date', ''),
            s.get('age', ''),
            s.get('phone', ''),
            s.get('email', ''),
            s.get('address', ''),
            s.get('category', ''),
            s.get('position', ''),
            s.get('employment_condition', ''),
            s.get('mppe_entry_date', ''),
            s.get('years_of_service', ''),
            s.get('school_entry_date', '') or '',
            s.get('shift', ''),
            s.get('assigned_area', ''),
            s.get('education_level', ''),
            s.get('specialization', ''),
            s.get('status', ''),
            s.get('course_count', 0),
            s.get('notes', '')
        ])
        
    # Return as bytes with UTF-8 BOM
    return output.getvalue().encode('utf-8-sig')

def generate_courses_csv():
    """
    Generates a CSV string of all courses completed by all staff members.
    """
    courses = get_all_courses()
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    
    writer.writerow([
        "Cédula",
        "Nombre del Trabajador",
        "Tipo de Personal",
        "Cargo",
        "Nombre del Curso / Formación",
        "Institución / Ente Emisor",
        "Horas Académicas",
        "Año de Culminación",
        "Modalidad",
        "Nº de Certificado"
    ])
    
    for c in courses:
        cedula = f"{c.get('nationality', 'V')}-{c.get('id_number', '')}"
        nombre = f"{c.get('first_name', '')} {c.get('last_name', '')}"
        writer.writerow([
            cedula,
            nombre,
            c.get('category', ''),
            c.get('position', ''),
            c.get('course_name', ''),
            c.get('institution', '') or 'No especificada',
            c.get('hours', '') or '',
            c.get('year_completed', '') or '',
            c.get('modality', ''),
            c.get('certificate_code', '') or ''
        ])
        
    return output.getvalue().encode('utf-8-sig')

def export_json_backup():
    """
    Exports complete database as JSON dictionary.
    """
    staff_list = get_all_staff()
    full_data = []
    for s in staff_list:
        detailed = get_staff_by_id(s['id'])
        if detailed:
            full_data.append(detailed)
            
    return json.dumps({
        "school": "Escuela Alberto Sanabria",
        "institution": "Ministerio del Poder Popular para la Educación (MPPE)",
        "exported_at": str(import_datetime().now()),
        "staff": full_data
    }, indent=2, ensure_ascii=False).encode('utf-8')

def import_datetime():
    from datetime import datetime
    return datetime
