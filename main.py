def get_users_df():
    try:
        # v=time.time للتأكد من جلب أحدث بيانات بدون تخزين مؤقت (Cache)
        response = requests.get(f"{USER_SHEET_URL}?v={time.time()}")
        df = pd.read_csv(io.StringIO(response.text))
        # تنظيف أسماء الأعمدة من المسافات
        df.columns = [c.strip() for c in df.columns]
        # تنظيف البيانات نفسها من المسافات الزائدة
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except Exception as e:
        st.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")
        return pd.DataFrame()

# تعديل منطق تسجيل الدخول داخل الـ Tab1
with tab1:
    u = st.text_input("User", placeholder="الاسم أو الإيميل", label_visibility="collapsed", key="login_u")
    p = st.text_input("Pass", type="password", placeholder="كلمة المرور", label_visibility="collapsed", key="login_p")
    
    if st.button("SIGN IN", use_container_width=True):
        if p == "2026": # كود المطور دايماً شغال
            st.session_state.auth = True
            st.rerun()
        
        df_u = get_users_df()
        if not df_u.empty:
            # تحويل المدخلات لنصوص للمقارنة الدقيقة
            u_str = str(u).strip()
            p_str = str(p).strip()
            
            # البحث عن المستخدم (سواء بالاسم أو بالإيميل)
            user_match = df_u[
                ((df_u['Name'].astype(str) == u_str) | (df_u['Email'].astype(str) == u_str)) & 
                (df_u['Password'].astype(str) == p_str)
            ]
            
            if not user_match.empty:
                st.session_state.auth = True
                st.success("تم تسجيل الدخول بنجاح")
                time.sleep(1)
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
        else:
            st.error("تعذر الوصول لسجل المشتركين حالياً")
