from database import init_db, get_connection, create_staff, get_all_staff

def seed():
    init_db()
    
    # Check if data already exists
    existing = get_all_staff()
    if existing:
        print("La base de datos ya contiene registros. No se duplicará la información.")
        return

    sample_staff = [
        {
            "data": {
                "nationality": "V",
                "id_number": "16452891",
                "first_name": "María Elena",
                "last_name": "Paredes Rivas",
                "gender": "Femenino",
                "birth_date": "1983-05-14",
                "phone": "0414-7892341",
                "email": "maria.paredes@educacion.gob.ve",
                "address": "Av. Bolívar, Sector Centro, Casa #45",
                "category": "Docente",
                "position": "Docente de Aula",
                "mppe_entry_date": "2009-09-15",
                "school_entry_date": "2013-10-01",
                "employment_condition": "Fijo / Titular",
                "shift": "Mañana",
                "assigned_area": "3er Grado Sección 'A'",
                "education_level": "Licenciatura",
                "specialization": "Educación Integral",
                "status": "Activo",
                "notes": "Excelente desempeño pedagógico. Tutora de proyectos de aula socio-productivos."
            },
            "courses": [
                {
                    "course_name": "Estrategias Lúdicas para la Enseñanza de la Lectoescritura",
                    "institution": "CENAMEC / MPPE",
                    "hours": 60,
                    "year_completed": 2021,
                    "modality": "Presencial",
                    "certificate_code": "CEN-2021-4821"
                },
                {
                    "course_name": "Diplomado en Pedagogía del Amor, el Ejemplo y la Curiosidad",
                    "institution": "UNEM Samuel Robinson",
                    "hours": 180,
                    "year_completed": 2023,
                    "modality": "Mixto",
                    "certificate_code": "UNEM-DIP-892"
                },
                {
                    "course_name": "Manejo de Recursos para el Aprendizaje y Colección Bicentenario",
                    "institution": "Zona Educativa",
                    "hours": 40,
                    "year_completed": 2019,
                    "modality": "Presencial",
                    "certificate_code": "ZE-REC-1109"
                }
            ]
        },
        {
            "data": {
                "nationality": "V",
                "id_number": "13890123",
                "first_name": "Carlos Alberto",
                "last_name": "Gómez Mendoza",
                "gender": "Masculino",
                "birth_date": "1978-11-20",
                "phone": "0424-3321908",
                "email": "carlos.gomez@educacion.gob.ve",
                "address": "Urb. Los Rosales, Calle 3, Casa #12",
                "category": "Docente",
                "position": "Coordinador Pedagógico",
                "mppe_entry_date": "2003-01-16",
                "school_entry_date": "2010-09-16",
                "employment_condition": "Fijo / Titular",
                "shift": "Integral / Doble turno",
                "assigned_area": "Coordinación de Evaluación y Control de Estudios",
                "education_level": "Maestría",
                "specialization": "Gerencia Educativa y Currículo",
                "status": "Activo",
                "notes": "Responsable de la supervisión y acompañamiento pedagógico docente."
            },
            "courses": [
                {
                    "course_name": "Planificación y Evaluación por Proyectos de Aprendizaje",
                    "institution": "UNEM Samuel Robinson",
                    "hours": 120,
                    "year_completed": 2022,
                    "modality": "En línea / Virtual",
                    "certificate_code": "UNEM-PE-2022-77"
                },
                {
                    "course_name": "Supervisión Educativa y Acompañamiento Pedagógico Integral",
                    "institution": "MPPE - Dirección General de Formación",
                    "hours": 90,
                    "year_completed": 2020,
                    "modality": "Presencial",
                    "certificate_code": "MPPE-SUP-904"
                }
            ]
        },
        {
            "data": {
                "nationality": "V",
                "id_number": "21456789",
                "first_name": "Gabriela Soledad",
                "last_name": "Navarro Díaz",
                "gender": "Femenino",
                "birth_date": "1994-08-03",
                "phone": "0412-5558912",
                "email": "gabriela.navarro@gmail.com",
                "address": "Sector Campo Alegre, Vereda 5, Casa #8",
                "category": "Docente",
                "position": "Docente de Educación Física",
                "mppe_entry_date": "2019-10-01",
                "school_entry_date": "2021-01-15",
                "employment_condition": "Contratado",
                "shift": "Mañana",
                "assigned_area": "Educación Física Primaria",
                "education_level": "Licenciatura",
                "specialization": "Educación Física, Deporte y Recreación",
                "status": "Activo",
                "notes": "Coordinadora de los Juegos Intercursos y actividades recreativas institucionales."
            },
            "courses": [
                {
                    "course_name": "Primeros Auxilios y Prevención de Accidentes Escolares",
                    "institution": "Cruz Roja Venezolana",
                    "hours": 48,
                    "year_completed": 2023,
                    "modality": "Presencial",
                    "certificate_code": "CRV-PA-2023-145"
                },
                {
                    "course_name": "Arbitraje y Organización de Torneos Escolares",
                    "institution": "Instituto Nacional de Deportes (IND)",
                    "hours": 60,
                    "year_completed": 2022,
                    "modality": "Presencial",
                    "certificate_code": "IND-ARB-2022"
                }
            ]
        },
        {
            "data": {
                "nationality": "V",
                "id_number": "18945612",
                "first_name": "Yelitza Coromoto",
                "last_name": "Silva Hernández",
                "gender": "Femenino",
                "birth_date": "1988-02-27",
                "phone": "0416-6412093",
                "email": "yelitza.silva@albertosanabria.edu.ve",
                "address": "Barrio Santa Inés, Calle Principal #22",
                "category": "Administrativo",
                "position": "Secretaria I",
                "mppe_entry_date": "2012-04-01",
                "school_entry_date": "2015-09-15",
                "employment_condition": "Fijo / Titular",
                "shift": "Mañana",
                "assigned_area": "Secretaría del Plantel y Archivo Central",
                "education_level": "T.S.U.",
                "specialization": "Administración de Recursos Humanos",
                "status": "Activo",
                "notes": "Encargada del libro de matrículas y expedientes del personal."
            },
            "courses": [
                {
                    "course_name": "Gestión del Sistema Nacional de Registro Escolar (SIGE)",
                    "institution": "MPPE - Oficina de Tecnologías de Información",
                    "hours": 40,
                    "year_completed": 2023,
                    "modality": "En línea / Virtual",
                    "certificate_code": "SIGE-CAP-2023-019"
                },
                {
                    "course_name": "Redacción de Correspondencia Oficial y Archivo Digital",
                    "institution": "INCES",
                    "hours": 80,
                    "year_completed": 2020,
                    "modality": "Presencial",
                    "certificate_code": "INCES-ADM-890"
                }
            ]
        },
        {
            "data": {
                "nationality": "V",
                "id_number": "15340987",
                "first_name": "Marcos Aurelio",
                "last_name": "Torres Bravo",
                "gender": "Masculino",
                "birth_date": "1981-12-09",
                "phone": "0426-8901234",
                "email": "marcos.torres@gmail.com",
                "address": "Sector El Carmen, Calle Junín #55",
                "category": "Administrativo",
                "position": "Bibliotecario Escolar",
                "mppe_entry_date": "2015-02-01",
                "school_entry_date": "2017-03-01",
                "employment_condition": "Fijo / Titular",
                "shift": "Tarde",
                "assigned_area": "Biblioteca Escolar 'Andrés Bello'",
                "education_level": "Licenciatura",
                "specialization": "Bibliotecología y Archivología",
                "status": "Activo",
                "notes": "Facilitador de círculos de lectura para estudiantes de primaria."
            },
            "courses": [
                {
                    "course_name": "Catalogación y Conservación Preventiva del Libro Escolar",
                    "institution": "Biblioteca Nacional de Venezuela",
                    "hours": 75,
                    "year_completed": 2021,
                    "modality": "Presencial",
                    "certificate_code": "BNV-CAT-2021-33"
                }
            ]
        },
        {
            "data": {
                "nationality": "V",
                "id_number": "17203451",
                "first_name": "Rosa Isabel",
                "last_name": "Chirinos Mora",
                "gender": "Femenino",
                "birth_date": "1985-07-19",
                "phone": "0414-9988771",
                "email": "rosa.chirinos@hotmail.com",
                "address": "Comunidad 23 de Enero, Manzana 4, Lote 10",
                "category": "Obrero / Apoyo",
                "position": "Cocinera de la Patria (PAE)",
                "mppe_entry_date": "2016-09-01",
                "school_entry_date": "2016-09-01",
                "employment_condition": "Fijo / Titular",
                "shift": "Mañana",
                "assigned_area": "Comedor Escolar / Cocina PAE",
                "education_level": "Bachiller",
                "specialization": "Alimentación y Gastronomía",
                "status": "Activo",
                "notes": "Líder de la brigada de comedor escolar. Control estricto de insumos alimenticios."
            },
            "courses": [
                {
                    "course_name": "Manipulación Higiénica y Conservación de Alimentos",
                    "institution": "INCES / Corporación Nacional de Alimentación Escolar (CNAE)",
                    "hours": 45,
                    "year_completed": 2023,
                    "modality": "Presencial",
                    "certificate_code": "CNAE-MAN-2023-412"
                },
                {
                    "course_name": "Nutrición y Balance Dietético en Edad Escolar",
                    "institution": "Instituto Nacional de Nutrición (INN)",
                    "hours": 30,
                    "year_completed": 2022,
                    "modality": "Presencial",
                    "certificate_code": "INN-NUT-2022-881"
                }
            ]
        },
        {
            "data": {
                "nationality": "V",
                "id_number": "12567843",
                "first_name": "José Ramón",
                "last_name": "Medina Castillo",
                "gender": "Masculino",
                "birth_date": "1974-04-05",
                "phone": "0412-1234567",
                "email": "jose.medina@albertosanabria.edu.ve",
                "address": "Calle Las Flores, Diagonal al Ambulatorio",
                "category": "Obrero / Apoyo",
                "position": "Personal de Mantenimiento y Servicios Generales",
                "mppe_entry_date": "2007-06-15",
                "school_entry_date": "2007-06-15",
                "employment_condition": "Fijo / Titular",
                "shift": "Integral / Doble turno",
                "assigned_area": "Mantenimiento de Infraestructura Escolar",
                "education_level": "Bachiller",
                "specialization": "Mantenimiento General / Electricidad Básica",
                "status": "Activo",
                "notes": "Encargado de la supervisión de servicios básicos de electricidad, plomería y áreas verdes."
            },
            "courses": [
                {
                    "course_name": "Seguridad y Salud en el Trabajo para Espacios Educativos",
                    "institution": "INPSASEL / MPPE",
                    "hours": 50,
                    "year_completed": 2021,
                    "modality": "Presencial",
                    "certificate_code": "INP-SST-2021-04"
                },
                {
                    "course_name": "Plomería y Mantenimiento Hidráulico Básico",
                    "institution": "INCES",
                    "hours": 60,
                    "year_completed": 2018,
                    "modality": "Presencial",
                    "certificate_code": "INCES-PLM-2018"
                }
            ]
        }
    ]

    for item in sample_staff:
        create_staff(item["data"], item.get("courses", []))

    print(f"Base de datos inicializada con éxito. Se cargaron {len(sample_staff)} trabajadores de prueba.")

if __name__ == "__main__":
    seed()
