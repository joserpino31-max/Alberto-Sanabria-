from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
from datetime import datetime
import json

from database import (
    init_db,
    get_all_staff,
    get_staff_by_id,
    get_staff_by_id_number,
    create_staff,
    update_staff,
    delete_staff,
    get_all_courses,
    get_stats
)
from export_utils import generate_staff_csv, generate_courses_csv, export_json_backup

app = Flask(__name__)
app.secret_key = "escuela-alberto-sanabria-mppe-secret-key-2026"

# Initialize database schema upon app creation (ensures tables exist under Gunicorn)
init_db()

# Context processor for templates
@app.context_processor
def inject_globals():
    return {
        "current_year": datetime.now().year,
        "school_name": "Unidad Educativa Alberto Sanabria",
        "mppe_title": "Ministerio del Poder Popular para la Educación"
    }

@app.route("/")
def index():
    stats = get_stats()
    # Get 5 most recently updated or added staff
    recent_staff = get_all_staff()[:6]
    return render_template("index.html", stats=stats, recent_staff=recent_staff)

@app.route("/staff")
def staff_list():
    category = request.args.get("category", "Todos")
    status = request.args.get("status", "Todos")
    condition = request.args.get("condition", "Todos")
    search = request.args.get("search", "").strip()

    staff_members = get_all_staff(
        category=category,
        status=status,
        condition=condition,
        search=search
    )
    
    return render_template(
        "staff_list.html",
        staff_members=staff_members,
        selected_category=category,
        selected_status=status,
        selected_condition=condition,
        search_query=search,
        total_count=len(staff_members)
    )

@app.route("/staff/new", methods=["GET", "POST"])
def staff_create():
    if request.method == "POST":
        id_number = request.form.get("id_number", "").strip()
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        category = request.form.get("category", "").strip()
        position = request.form.get("position", "").strip()
        mppe_entry_date = request.form.get("mppe_entry_date", "").strip()

        # Validation
        if not id_number or not first_name or not last_name or not category or not position or not mppe_entry_date:
            flash("Por favor complete todos los campos obligatorios marcados con (*).", "danger")
            return render_template("staff_form.html", form_data=request.form, is_edit=False)

        # Check existing cédula
        existing = get_staff_by_id_number(id_number)
        if existing:
            flash(f"Error: Ya existe un registro con la cédula {id_number} ({existing['first_name']} {existing['last_name']}).", "danger")
            return render_template("staff_form.html", form_data=request.form, is_edit=False)

        # Parse dynamic courses
        courses = []
        course_names = request.form.getlist("course_name[]")
        institutions = request.form.getlist("course_institution[]")
        hours_list = request.form.getlist("course_hours[]")
        years_list = request.form.getlist("course_year[]")
        modalities = request.form.getlist("course_modality[]")
        cert_codes = request.form.getlist("course_cert[]")

        for i in range(len(course_names)):
            c_name = course_names[i].strip() if i < len(course_names) else ""
            if c_name:
                courses.append({
                    "course_name": c_name,
                    "institution": institutions[i].strip() if i < len(institutions) else "",
                    "hours": hours_list[i].strip() if i < len(hours_list) else "",
                    "year_completed": years_list[i].strip() if i < len(years_list) else "",
                    "modality": modalities[i].strip() if i < len(modalities) else "Presencial",
                    "certificate_code": cert_codes[i].strip() if i < len(cert_codes) else ""
                })

        data = {
            "nationality": request.form.get("nationality", "V"),
            "id_number": id_number,
            "first_name": first_name,
            "last_name": last_name,
            "gender": request.form.get("gender", ""),
            "birth_date": request.form.get("birth_date", ""),
            "phone": request.form.get("phone", "").strip(),
            "email": request.form.get("email", "").strip(),
            "address": request.form.get("address", "").strip(),
            "category": category,
            "position": position,
            "mppe_entry_date": mppe_entry_date,
            "school_entry_date": request.form.get("school_entry_date", ""),
            "employment_condition": request.form.get("employment_condition", "Fijo / Titular"),
            "shift": request.form.get("shift", "Mañana"),
            "assigned_area": request.form.get("assigned_area", "").strip(),
            "education_level": request.form.get("education_level", ""),
            "specialization": request.form.get("specialization", "").strip(),
            "status": request.form.get("status", "Activo"),
            "notes": request.form.get("notes", "").strip()
        }

        new_id = create_staff(data, courses)
        flash(f"¡Trabajador {first_name} {last_name} registrado exitosamente!", "success")
        return redirect(url_for("staff_detail", staff_id=new_id))

    return render_template("staff_form.html", form_data={}, courses=[], is_edit=False)

@app.route("/staff/<int:staff_id>")
def staff_detail(staff_id):
    staff = get_staff_by_id(staff_id)
    if not staff:
        flash("El trabajador solicitado no fue encontrado.", "warning")
        return redirect(url_for("staff_list"))
    return render_template("staff_detail.html", staff=staff)

@app.route("/staff/<int:staff_id>/edit", methods=["GET", "POST"])
def staff_edit(staff_id):
    staff = get_staff_by_id(staff_id)
    if not staff:
        flash("El trabajador solicitado no fue encontrado.", "warning")
        return redirect(url_for("staff_list"))

    if request.method == "POST":
        id_number = request.form.get("id_number", "").strip()
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        category = request.form.get("category", "").strip()
        position = request.form.get("position", "").strip()
        mppe_entry_date = request.form.get("mppe_entry_date", "").strip()

        # Validation
        if not id_number or not first_name or not last_name or not category or not position or not mppe_entry_date:
            flash("Por favor complete todos los campos obligatorios marcados con (*).", "danger")
            return render_template("staff_form.html", form_data=request.form, courses=staff.get("courses", []), is_edit=True, staff_id=staff_id)

        # Check existing cédula excluding current ID
        existing = get_staff_by_id_number(id_number, exclude_id=staff_id)
        if existing:
            flash(f"Error: La cédula {id_number} ya está registrada a nombre de {existing['first_name']} {existing['last_name']}.", "danger")
            return render_template("staff_form.html", form_data=request.form, courses=staff.get("courses", []), is_edit=True, staff_id=staff_id)

        # Parse courses
        courses = []
        course_names = request.form.getlist("course_name[]")
        institutions = request.form.getlist("course_institution[]")
        hours_list = request.form.getlist("course_hours[]")
        years_list = request.form.getlist("course_year[]")
        modalities = request.form.getlist("course_modality[]")
        cert_codes = request.form.getlist("course_cert[]")

        for i in range(len(course_names)):
            c_name = course_names[i].strip() if i < len(course_names) else ""
            if c_name:
                courses.append({
                    "course_name": c_name,
                    "institution": institutions[i].strip() if i < len(institutions) else "",
                    "hours": hours_list[i].strip() if i < len(hours_list) else "",
                    "year_completed": years_list[i].strip() if i < len(years_list) else "",
                    "modality": modalities[i].strip() if i < len(modalities) else "Presencial",
                    "certificate_code": cert_codes[i].strip() if i < len(cert_codes) else ""
                })

        data = {
            "nationality": request.form.get("nationality", "V"),
            "id_number": id_number,
            "first_name": first_name,
            "last_name": last_name,
            "gender": request.form.get("gender", ""),
            "birth_date": request.form.get("birth_date", ""),
            "phone": request.form.get("phone", "").strip(),
            "email": request.form.get("email", "").strip(),
            "address": request.form.get("address", "").strip(),
            "category": category,
            "position": position,
            "mppe_entry_date": mppe_entry_date,
            "school_entry_date": request.form.get("school_entry_date", ""),
            "employment_condition": request.form.get("employment_condition", "Fijo / Titular"),
            "shift": request.form.get("shift", "Mañana"),
            "assigned_area": request.form.get("assigned_area", "").strip(),
            "education_level": request.form.get("education_level", ""),
            "specialization": request.form.get("specialization", "").strip(),
            "status": request.form.get("status", "Activo"),
            "notes": request.form.get("notes", "").strip()
        }

        update_staff(staff_id, data, courses)
        flash(f"¡Datos de {first_name} {last_name} actualizados exitosamente!", "success")
        return redirect(url_for("staff_detail", staff_id=staff_id))

    return render_template("staff_form.html", form_data=staff, courses=staff.get("courses", []), is_edit=True, staff_id=staff_id)

@app.route("/staff/<int:staff_id>/delete", methods=["POST"])
def staff_delete(staff_id):
    staff = get_staff_by_id(staff_id)
    if staff:
        name = f"{staff['first_name']} {staff['last_name']}"
        delete_staff(staff_id)
        flash(f"El registro de {name} ha sido eliminado satisfactoriamente.", "info")
    else:
        flash("No se encontró el registro para eliminar.", "warning")
    return redirect(url_for("staff_list"))

@app.route("/staff/<int:staff_id>/print")
def staff_ficha_print(staff_id):
    staff = get_staff_by_id(staff_id)
    if not staff:
        flash("Trabajador no encontrado.", "danger")
        return redirect(url_for("staff_list"))
    return render_template("staff_ficha_print.html", staff=staff)

@app.route("/courses")
def courses_list():
    courses = get_all_courses()
    search = request.args.get("search", "").strip().lower()
    
    if search:
        courses = [
            c for c in courses
            if search in c["course_name"].lower()
            or search in (c["institution"] or "").lower()
            or search in c["first_name"].lower()
            or search in c["last_name"].lower()
            or search in c["id_number"]
        ]
        
    return render_template("courses_list.html", courses=courses, search_query=search, total_courses=len(courses))

@app.route("/export/staff.csv")
def export_staff():
    category = request.args.get("category")
    status = request.args.get("status")
    condition = request.args.get("condition")
    csv_bytes = generate_staff_csv(category, status, condition)
    
    filename = f"Nomina_Personal_Escuela_Alberto_Sanabria_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    return Response(
        csv_bytes,
        mimetype="text/csv; charset=utf-8-sig",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.route("/export/courses.csv")
def export_courses():
    csv_bytes = generate_courses_csv()
    filename = f"Formaciones_Cursos_Alberto_Sanabria_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    return Response(
        csv_bytes,
        mimetype="text/csv; charset=utf-8-sig",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.route("/export/backup.json")
def export_backup():
    json_bytes = export_json_backup()
    filename = f"Backup_Escuela_Alberto_Sanabria_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    return Response(
        json_bytes,
        mimetype="application/json; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

if __name__ == "__main__":
    init_db()
    print("Iniciando Sistema de Personal - Escuela Alberto Sanabria (MPPE)...")
    print("Abra su navegador en: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
