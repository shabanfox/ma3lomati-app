def login_user(u, p):
    try:
        # إضافة timeout لضمان عدم تعليق الموقع
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=10)
        if res.status_code == 200:
            data = res.json()
            for user in data:
                # التحقق مع إزالة المسافات الزائدة
                db_user = str(user.get('Name', '')).strip().lower()
                db_email = str(user.get('Email', '')).strip().lower()
                db_pass = str(user.get('Password', '')).strip()
                
                if (u.lower().strip() == db_email or u.lower().strip() == db_user) and p.strip() == db_pass:
                    return user.get('Name')
        return None
    except Exception as e:
        st.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")
        return None
