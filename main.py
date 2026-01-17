# 5. نظام إدارة المستخدمين (التسجيل والدخول)
if 'user_db' not in st.session_state:
    st.session_state.user_db = {"admin": "2026"}  # مستخدم افتراضي

if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:50px;'><h1 style='color:#f59e0b; font-size:50px;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    
    # تبديل بين الدخول والتسجيل
    tab_login, tab_signup = st.tabs(["🔐 تسجيل دخول", "📝 إنشاء حساب جديد"])
    
    with tab_login:
        _, c2, _ = st.columns([1,1,1])
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            user_in = st.text_input("اسم المستخدم", placeholder="User Name", key="login_user")
            pass_in = st.text_input("كلمة السر", type="password", placeholder="Password", key="login_pass")
            if st.button("دخول للنظام 🚀", use_container_width=True):
                if user_in in st.session_state.user_db and st.session_state.user_db[user_in] == pass_in:
                    st.session_state.auth = True
                    st.session_state.current_user = user_in
                    st.success("تم تسجيل الدخول بنجاح!")
                    st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة السر خطأ")

    with tab_signup:
        _, c2, _ = st.columns([1,1,1])
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            new_user = st.text_input("اسم المستخدم الجديد", placeholder="اختر اسم مستخدم")
            new_pass = st.text_input("كلمة سر قوية", type="password", placeholder="اختر كلمة سر")
            confirm_pass = st.text_input("تأكيد كلمة السر", type="password")
            
            if st.button("إنشاء الحساب 🆕", use_container_width=True):
                if new_user in st.session_state.user_db:
                    st.warning("هذا المستخدم موجود بالفعل!")
                elif new_pass != confirm_pass:
                    st.error("كلمات السر غير متطابقة")
                elif len(new_pass) < 4:
                    st.error("كلمة السر ضعيفة جداً")
                else:
                    st.session_state.user_db[new_user] = new_pass
                    st.success("تم إنشاء الحساب! يمكنك الآن الدخول من تبويب 'تسجيل دخول'")
    
    st.stop() # يمنع ظهور باقي التطبيق لو لسه مسجلش دخول
