# --- 5. شاشة الدخول والاشتراك (الربط الكامل بالشيت) ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.markdown("<div class='lock-gold'>🔐</div>", unsafe_allow_html=True)
    
    tab_log, tab_reg = st.tabs(["🔐 تسجيل دخول", "📝 اشتراك جديد"])
    
    with tab_log:
        u = st.text_input("الأسم أو الإيميل", key="log_u", label_visibility="collapsed", placeholder="Username / Email")
        p = st.text_input("كلمة السر", type="password", key="log_p", label_visibility="collapsed", placeholder="Password")
        if st.button("دخول للمنصة 🚀", use_container_width=True):
            if p == "2026": # كود دخول المطور المباشر
                st.session_state.auth, st.session_state.current_user = True, "Admin"
                st.rerun()
            else:
                user = login_user(u, p)
                if user:
                    st.session_state.auth, st.session_state.current_user = True, user
                    st.rerun()
                else: 
                    st.error("❌ بيانات الدخول غير صحيحة")
    
    with tab_reg:
        # حقول الاشتراك المطلوبة للربط مع Apps Script
        reg_n = st.text_input("الاسم بالكامل", key="reg_name", placeholder="Full Name")
        reg_e = st.text_input("البريد الإلكتروني (Gmail)", key="reg_email", placeholder="example@gmail.com")
        reg_p = st.text_input("كلمة السر", type="password", key="reg_pass", placeholder="Password")
        reg_w = st.text_input("رقم الواتساب", key="reg_wa", placeholder="01xxxxxxxxx")
        reg_c = st.text_input("اسم الشركة", key="reg_comp", placeholder="Company Name")
        
        if st.button("تأكيد الاشتراك وحفظ البيانات ✅", use_container_width=True):
            if reg_n and reg_e and reg_p:
                # إرسال البيانات إلى السكريبت المربوط بالجوجل شيت
                with st.spinner("جاري تسجيل بياناتك في السيرفر..."):
                    success = signup_user(reg_n, reg_p, reg_e, reg_w, reg_c)
                    if success:
                        st.success("✅ تم تسجيل حسابك بنجاح في الجوجل شيت!")
                        st.balloons()
                        st.info("يمكنك الآن العودة لتبويب 'تسجيل الدخول' للبدء.")
                    else: 
                        st.error("⚠️ حدثت مشكلة أثناء الاتصال بالسيرفر. تأكد من إعدادات Apps Script.")
            else: 
                st.warning("⚠️ يرجى ملء الحقول الأساسية (الاسم، الإيميل، وكلمة السر)")
                
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()
