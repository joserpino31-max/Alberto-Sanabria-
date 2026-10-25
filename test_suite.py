from app import app
from database import get_staff_by_id_number, delete_staff

client = app.test_client()

# 1. Test home page
r = client.get('/')
assert r.status_code == 200, f'Home failed: {r.status_code}'
print('[✓] Home / Dashboard: OK (200)')

# 2. Test staff list
r = client.get('/staff')
assert r.status_code == 200, f'Staff list failed: {r.status_code}'
print('[✓] Staff directory: OK (200)')

# 3. Test courses list
r = client.get('/courses')
assert r.status_code == 200, f'Courses list failed: {r.status_code}'
print('[✓] Courses list: OK (200)')

# 4. Test staff creation
post_data = {
    'nationality': 'V',
    'id_number': '19999888',
    'first_name': 'Prueba',
    'last_name': 'Docente Test',
    'gender': 'Femenino',
    'birth_date': '1990-01-01',
    'phone': '0414-0000000',
    'email': 'test@escuela.com',
    'address': 'Calle Test',
    'category': 'Docente',
    'position': 'Docente de Matemáticas',
    'mppe_entry_date': '2015-09-16',
    'school_entry_date': '2016-10-01',
    'employment_condition': 'Fijo / Titular',
    'shift': 'Mañana',
    'assigned_area': '5to Grado A',
    'education_level': 'Licenciatura',
    'specialization': 'Matemática',
    'status': 'Activo',
    'notes': 'Registro de prueba',
    'course_name[]': ['Curso de Didáctica de la Matemática'],
    'course_institution[]': ['CENAMEC'],
    'course_hours[]': ['60'],
    'course_year[]': ['2022'],
    'course_modality[]': ['Presencial'],
    'course_cert[]': ['CERT-2022-99']
}
r = client.post('/staff/new', data=post_data, follow_redirects=True)
assert r.status_code == 200, f'Staff create failed: {r.status_code}'
assert b'Prueba' in r.data, 'Created staff name not found in response'
print('[✓] Staff creation with dynamic courses: OK (200)')

# 5. Test export CSV
r = client.get('/export/staff.csv')
assert r.status_code == 200, f'Staff export CSV failed: {r.status_code}'
assert 'text/csv' in r.content_type, 'Not CSV content type'
print('[✓] Export staff CSV: OK (200)')

# 6. Test export courses CSV
r = client.get('/export/courses.csv')
assert r.status_code == 200, f'Courses export CSV failed: {r.status_code}'
assert 'text/csv' in r.content_type, 'Not CSV content type'
print('[✓] Export courses CSV: OK (200)')

# 7. Test backup JSON
r = client.get('/export/backup.json')
assert r.status_code == 200, f'Backup JSON failed: {r.status_code}'
assert 'application/json' in r.content_type, 'Not JSON content type'
print('[✓] Export backup JSON: OK (200)')

# 8. Test print dossier
created_staff = get_staff_by_id_number('19999888')
assert created_staff is not None, 'Could not retrieve created test staff'
staff_id = created_staff['id']
r = client.get(f'/staff/{staff_id}/print')
assert r.status_code == 200, f'Print dossier failed: {r.status_code}'
print('[✓] Printable MPPE official dossier: OK (200)')

# 9. Clean up test staff
delete_staff(staff_id)
print('[✓] Cleanup test staff: OK')
print('=== ALL TESTS PASSED SUCCESSFULLY! ===')
