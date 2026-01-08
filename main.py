import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. تهيئة حالة الجلسة (Session State)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "home"

# 3. دالة تسجيل الخروج
def logout():
    st.session_state.logged_in = False
    st.session_state.page = "login"

# 4. التنسيق (CSS) - الحفاظ على نفس التناسق السابق
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    .block-container { padding-top: 0.6rem !important; }
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
        background-color: #f4f7fa !important;
    }

    .header-nav {
        background: white; height: 70px; padding: 0 8%;
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 1px solid #e2e8f0; position: sticky; top: 0; z-index: 1000;
    }
    .logo { color: #0056b3; font-weight: 900; font-size: 1.5rem; text-decoration: none; }
    
    /* تصميم فورم الدخول */
    .login-box {
        background: white; padding: 40px; border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        max-width: 450px; margin: 50px auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- دالة صفحة تسجيل الدخول / الاشتراك ---
def show_login_page():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#0056b3;'>مرحباً بك</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])
    
    with tab1:
        email = st.text_input("البريد الإلكتروني", key="login_email")
        password = st.text_input("كلمة المرور", type="password", key="login_pass")
        if st.button("دخول", use_container_width=True):
            if email == "admin" and password == "123": # مثال بسيط
                st.session_state.logged_in = True
                st.session_state.page = "home"
                st.rerun()
            else:
                st.error("خطأ في البيانات، جرب (admin / 123)")
                
    with tab2:
        st.text_input("الاسم بالكامل")
        st.text_input("رقم الهاتف")
        st.text_input("البريد الإلكتروني", key="reg_email")
        st.text_input("كلمة المرور", type="password", key="reg_pass")
        if st.button("اشتراك الآن", use_container_width=True):
            st.success("تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- دالة الصفحة الرئيسية (المحتوى المحمي) ---
def show_home_page():
    # الهيدر مع زر خروج
    st.markdown(f"""
        <div class="header-nav">
            <div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div>
            <div style="display: flex; gap: 20px; align-items: center;">
                <span style="font-weight:600; color:#475569;">أهلاً، بك يا بطل</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # وضع زر تسجيل الخروج في السايد بار أو الهيدر (هنا استخدمنا streamlit button للوظيفة)
    if st.sidebar.button("تسجيل الخروج"):
        logout()
        st.rerun()

    # --- وضع المحتوى اللي صممناه قبل كدة هنا ---
    st.markdown("""
        <div style="padding: 0 8%; margin-top: 10px;">
            <div style="background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
            url('https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1200&q=80');
            background-size: cover; height: 300px; border-radius: 12px; display: flex; 
            flex-direction: column; justify-content: center; align-items: center; color: white;">
                <h1 style="font-weight:900;">لوحة معلومات المحترفين</h1>
                <p>تصفح المشاريع والأسعار الحصرية</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # شريط البحث والكروت
    st.markdown('<div style="padding: 0 8%; margin-top:30px;">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([2, 1, 1, 0.6])
    with c1: st.text_input("ابحث عن مشروع...", label_visibility="collapsed")
    with c2: st.selectbox("النوع", ["شقة", "فيلا"], label_visibility="collapsed")
    with c3: st.selectbox("السعر", ["الكل"], label_visibility="collapsed")
    with c4: st.button("بحث", use_container_width=True)
    
    st.markdown("<h3>أحدث المشاريع العقارية</h3>", unsafe_allow_html=True)
    # كارت مثال
    st.info("تم تسجيل الدخول بنجاح. يمكنك الآن رؤية تفاصيل المشاريع.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التحكم في عرض الصفحات ---
if not st.session_state.logged_in:
    # هيدر بسيط لصفحة الدخول
    st.markdown("""
        <div class="header-nav">
            <div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div>
            <div style="font-weight:600; color:#0056b3;">يرجى تسجيل الدخول للمتابعة</div>
        </div>
    """, unsafe_allow_html=True)
    show_login_page()
else:
    show_home_page()
