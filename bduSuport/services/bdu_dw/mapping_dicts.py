student_key_mapping = {
    "cccd": "id_card",
    "created_at": "created_at",
    "dan_toc": "ethnicity",
    "email": "email",
    "gioi_tinh": "gender",
    "hien_dien": "attendance",
    "ho_khau": "residence",
    "ho_sv": "last_name",
    "ma_chuyen_nganh": "major_code",
    "ma_cvht": "advisor_code",
    "ma_he_dao_tao": "education_system_code",
    "ma_khoa": "faculty_code",
    "ma_lop": "class_code",
    "ma_nganh": "field_code",
    "mssv": "student_id",
    "ngay_sinh": "date_of_birth",
    "nguon": "source",
    "nk": "academic_year",
    "noi_sinh": "place_of_birth",
    "sdt": "phone_number",
    "ten_bac_hoc": "degree_name",
    "ten_chuyen_nganh": "major_name",
    "ten_cvht": "advisor_name",
    "ten_day_du": "full_name",
    "ten_khoa": "faculty_name",
    "ten_lop": "class_name",
    "ten_nganh": "field_name",
    "ten_sv": "first_name",
    "ton_giao": "religion",
    "updated_at": "updated_at"
}

attendance_key_mapping = {
    "buoi": "lesson",
    "created_at": "created_at",
    "diem_danh": "status",
    "ma_diem_danh": "attendance_id",
    "ma_mon_hoc": "subject_code",
    "ten_mon_hoc": "subject_name",
    "ma_nhom": "group_code",
    "mssv": "student_code",
    "ngay": "attendance_datetime",
    "ngay_origin": "attendance_date",
    "updated_at": "updated_at"
}

score_key_mapping = {
    "mssv": "student_id",
    "ten_mon_hoc": "subject_name",
    "ho_ten": "full_name",
    "lop": "class_name",
    "ma_khoa": "department_code",
    "nien_khoa_format": "academic_year",
    "nkhk": "semester_code",
    "hoc_ki": "semester",
    "ma_nhom": "subject_group",
    "dat_hp": "passed",
    "diem_chu_hp": "letter_grade",
    "diem_hp": "final_score_10",
    "diem_hp_4": "final_score_4",
    "k1": "midterm_score",
    "k1pt": "midterm_weight",
    "t1": "final_exam_score",
    "t1pt": "final_exam_weight",
    "b1": "library_score",
    "tv": "library_weight",
    "created_at": "created_at",
    "updated_at": "updated_at"
}

time_table_mapping = {
    "buoi_thu": "lesson_number",
    "danh_sach_sv": "student_list",
    "ma_giang_vien": "lecturer_code",
    "ma_lop": "class_code",
    "ma_mon_hoc": "subject_code",
    "ma_nhom": "group_code",
    "ma_phong": "room_code",
    "ngay_hoc": "lesson_date",
    "nhom_hoc": "group_number",
    "nkhk": "semester_code",
    "so_tiet": "periods",
    "ten_giang_vien": "lecturer_name",
    "ten_mon_hoc": "subject_name",
    "thu_kieu_so": "weekday_number",
    "tiet_bat_dau": "start_period",
    "tuan_bat_dau": "start_week"
}

event_key_mapping = {
    "id": "id",
    "mssv": "student_code",
    "ngay_dien_ra": "event_date",
    "nkhk": "semester_code",
    "ten_su_kien": "event_name",
    "ten_sv": "student_name",
    "loai": "type"
}

classification_key_mapping = {
    "date": "date",
    "diem": "score",
    "ho_ten": "full_name",
    "mssv": "student_id",
    "nkhk": "semester_code",
    "xep_loai": "classification"
}