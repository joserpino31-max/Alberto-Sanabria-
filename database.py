import sqlite3
import os
from datetime import datetime, date

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "escuela_sanabria.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nationality TEXT DEFAULT 'V',
        id_number TEXT UNIQUE NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender TEXT,
        birth_date TEXT,
        phone TEXT,
        email TEXT,
        address TEXT,
        category TEXT NOT NULL,          -- 'Docente', 'Administrativo', 'Obrero / Apoyo'
        position TEXT NOT NULL,          -- e.g. 'Docente de Aula', 'Secretaria', 'Aseador'
        mppe_entry_date TEXT NOT NULL,   -- YYYY-MM-DD
        school_entry_date TEXT,         -- YYYY-MM-DD
        employment_condition TEXT,       -- 'Fijo / Titular', 'Contratado', 'Interino', 'Suplente'
        shift TEXT,                      -- 'Mañana', 'Tarde', 'Integral / Doble turno'
        assigned_area TEXT,              -- e.g. '4to Grado B', 'Control de Estudio', 'Mantenimiento General'
        education_level TEXT,            -- 'Bachiller', 'Técnico Medio', 'T.S.U.', 'Licenciatura', 'Especialización', 'Maestría', 'Doctorado'
        specialization TEXT,             -- e.g. 'Educación Integral', 'Informática', 'Administración'
        status TEXT DEFAULT 'Activo',    -- 'Activo', 'Reposo Médico', 'Permiso', 'Comisión de Servicio', 'Jubilado'
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        staff_id INTEGER NOT NULL,
        course_name TEXT NOT NULL,
        institution TEXT,
        hours INTEGER,
        year_completed INTEGER,
        modality TEXT,                  -- 'Presencial', 'En línea / Virtual', 'Mixto'
        certificate_code TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (staff_id) REFERENCES staff (id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()

def calculate_years(date_str):
    """Calculate elapsed years from a YYYY-MM-DD string to today."""
    if not date_str:
        return 0
    try:
        parts = [int(p) for p in date_str.split("-")]
        if len(parts) == 3:
            d = date(parts[0], parts[1], parts[2])
            today = date.today()
            return today.year - d.year - ((today.month, today.day) < (d.month, d.day))
    except Exception:
        pass
    return 0

def get_all_staff(category=None, status=None, condition=None, search=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT s.*, 
               (SELECT COUNT(*) FROM courses c WHERE c.staff_id = s.id) as course_count
        FROM staff s
        WHERE 1=1
    """
    params = []

    if category and category != 'Todos':
        query += " AND s.category = ?"
        params.append(category)

    if status and status != 'Todos':
        query += " AND s.status = ?"
        params.append(status)

    if condition and condition != 'Todos':
        query += " AND s.employment_condition = ?"
        params.append(condition)

    if search:
        search_pattern = f"%{search.strip()}%"
        query += """ AND (
            s.id_number LIKE ? OR
            s.first_name LIKE ? OR
            s.last_name LIKE ? OR
            s.position LIKE ? OR
            s.assigned_area LIKE ? OR
            s.specialization LIKE ?
        )"""
        params.extend([search_pattern] * 6)

    query += " ORDER BY s.last_name ASC, s.first_name ASC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    staff_list = []
    for row in rows:
        item = dict(row)
        item['years_of_service'] = calculate_years(item.get('mppe_entry_date'))
        item['age'] = calculate_years(item.get('birth_date'))
        staff_list.append(item)

    conn.close()
    return staff_list

def get_staff_by_id(staff_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM staff WHERE id = ?", (staff_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    
    staff = dict(row)
    staff['years_of_service'] = calculate_years(staff.get('mppe_entry_date'))
    staff['age'] = calculate_years(staff.get('birth_date'))
    
    # Get courses
    cursor.execute("SELECT * FROM courses WHERE staff_id = ? ORDER BY year_completed DESC, id DESC", (staff_id,))
    courses = [dict(c) for c in cursor.fetchall()]
    staff['courses'] = courses
    
    conn.close()
    return staff

def get_staff_by_id_number(id_number, exclude_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if exclude_id:
        cursor.execute("SELECT * FROM staff WHERE id_number = ? AND id != ?", (id_number.strip(), exclude_id))
    else:
        cursor.execute("SELECT * FROM staff WHERE id_number = ?", (id_number.strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create_staff(data, courses=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO staff (
            nationality, id_number, first_name, last_name, gender, birth_date,
            phone, email, address, category, position, mppe_entry_date,
            school_entry_date, employment_condition, shift, assigned_area,
            education_level, specialization, status, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('nationality', 'V'),
        data.get('id_number', '').strip(),
        data.get('first_name', '').strip(),
        data.get('last_name', '').strip(),
        data.get('gender', ''),
        data.get('birth_date', ''),
        data.get('phone', '').strip(),
        data.get('email', '').strip(),
        data.get('address', '').strip(),
        data.get('category', 'Docente'),
        data.get('position', '').strip(),
        data.get('mppe_entry_date', ''),
        data.get('school_entry_date', '') or None,
        data.get('employment_condition', 'Fijo / Titular'),
        data.get('shift', 'Mañana'),
        data.get('assigned_area', '').strip(),
        data.get('education_level', ''),
        data.get('specialization', '').strip(),
        data.get('status', 'Activo'),
        data.get('notes', '').strip()
    ))
    staff_id = cursor.lastrowid

    if courses:
        for c in courses:
            if c.get('course_name') and c.get('course_name').strip():
                cursor.execute("""
                    INSERT INTO courses (staff_id, course_name, institution, hours, year_completed, modality, certificate_code)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    staff_id,
                    c.get('course_name', '').strip(),
                    c.get('institution', '').strip(),
                    int(c.get('hours')) if str(c.get('hours', '')).isdigit() else None,
                    int(c.get('year_completed')) if str(c.get('year_completed', '')).isdigit() else None,
                    c.get('modality', 'Presencial'),
                    c.get('certificate_code', '').strip()
                ))

    conn.commit()
    conn.close()
    return staff_id

def update_staff(staff_id, data, courses=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE staff SET
            nationality = ?,
            id_number = ?,
            first_name = ?,
            last_name = ?,
            gender = ?,
            birth_date = ?,
            phone = ?,
            email = ?,
            address = ?,
            category = ?,
            position = ?,
            mppe_entry_date = ?,
            school_entry_date = ?,
            employment_condition = ?,
            shift = ?,
            assigned_area = ?,
            education_level = ?,
            specialization = ?,
            status = ?,
            notes = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (
        data.get('nationality', 'V'),
        data.get('id_number', '').strip(),
        data.get('first_name', '').strip(),
        data.get('last_name', '').strip(),
        data.get('gender', ''),
        data.get('birth_date', ''),
        data.get('phone', '').strip(),
        data.get('email', '').strip(),
        data.get('address', '').strip(),
        data.get('category', 'Docente'),
        data.get('position', '').strip(),
        data.get('mppe_entry_date', ''),
        data.get('school_entry_date', '') or None,
        data.get('employment_condition', 'Fijo / Titular'),
        data.get('shift', 'Mañana'),
        data.get('assigned_area', '').strip(),
        data.get('education_level', ''),
        data.get('specialization', '').strip(),
        data.get('status', 'Activo'),
        data.get('notes', '').strip(),
        staff_id
    ))

    # Replace courses
    cursor.execute("DELETE FROM courses WHERE staff_id = ?", (staff_id,))
    if courses:
        for c in courses:
            if c.get('course_name') and c.get('course_name').strip():
                cursor.execute("""
                    INSERT INTO courses (staff_id, course_name, institution, hours, year_completed, modality, certificate_code)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    staff_id,
                    c.get('course_name', '').strip(),
                    c.get('institution', '').strip(),
                    int(c.get('hours')) if str(c.get('hours', '')).isdigit() else None,
                    int(c.get('year_completed')) if str(c.get('year_completed', '')).isdigit() else None,
                    c.get('modality', 'Presencial'),
                    c.get('certificate_code', '').strip()
                ))

    conn.commit()
    conn.close()

def delete_staff(staff_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM staff WHERE id = ?", (staff_id,))
    conn.commit()
    conn.close()

def get_all_courses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.*, s.first_name, s.last_name, s.id_number, s.nationality, s.category, s.position
        FROM courses c
        JOIN staff s ON c.staff_id = s.id
        ORDER BY c.year_completed DESC, c.id DESC
    """)
    courses = [dict(c) for c in cursor.fetchall()]
    conn.close()
    return courses

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM staff")
    total_staff = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM staff WHERE category = 'Docente'")
    total_docentes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM staff WHERE category = 'Administrativo'")
    total_administrativos = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM staff WHERE category = 'Obrero / Apoyo'")
    total_obreros = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM staff WHERE status = 'Activo'")
    total_activos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM staff WHERE status != 'Activo'")
    total_otros_estatus = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM courses")
    total_courses = cursor.fetchone()[0]

    # Breakdown by condition
    cursor.execute("SELECT employment_condition, COUNT(*) as count FROM staff GROUP BY employment_condition")
    by_condition = {row['employment_condition'] or 'Sin especificar': row['count'] for row in cursor.fetchall()}

    # Breakdown by education level
    cursor.execute("SELECT education_level, COUNT(*) as count FROM staff GROUP BY education_level")
    by_education = {row['education_level'] or 'Sin especificar': row['count'] for row in cursor.fetchall()}

    conn.close()
    return {
        'total_staff': total_staff,
        'total_docentes': total_docentes,
        'total_administrativos': total_administrativos,
        'total_obreros': total_obreros,
        'total_activos': total_activos,
        'total_otros_estatus': total_otros_estatus,
        'total_courses': total_courses,
        'by_condition': by_condition,
        'by_education': by_education
    }
