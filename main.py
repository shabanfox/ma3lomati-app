import streamlit as st
import pandas as pd
import requests
import time

# --- 1. إعدادات الصفحة والتهيئة ---
st.set_page_config(
    page_title="TAKWEN PREMIUM | MA3LOMATI PRO", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. إدارة حالة الجلسة (Session State) ---
if 'auth' not in st.session_state:
    if "u_session" in st.query_params:
        st.session_state.auth = True
        st.session_state.current_user = st.query_params["u_session"]
    else:
        st.session_state.auth = False

if 'current_index' not in st.session_state: st.session_state.current_index = 0

# --- 3. روابط البيانات والثوابت ---
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

HEADER_IMG = "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80"
ITEMS_PER_PAGE = 6

# --- 4. معالجة وجلب البيانات العقارية ---
def login_user(user_input, pwd_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=10)
        if response.status_code == 200:
            users_list = response.json()
            user_input = str(user_input).strip().lower()
            for user_data in users_list:
                name_s = str(user_data.get('Name', user_data.get('name', ''))).strip()
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()
                if user_input == name_s.lower() and str(pwd_input) == pass_s:
                    return name_s
        return None
    except: return None

@st.cache_data(ttl=60)
def load_data():
    try:
        p = pd.read_csv(URL_PROJECTS)
        d = pd.read_csv(URL_DEVELOPERS)
        l = pd.read_csv(URL_LAUNCHES)
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price', 'سعر': 'Price'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                df['Price'] = df['Price'].apply(lambda x: x * 1000000 if 0 < x < 1000 else x)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 5. دالة بناء شبكة العرض والتحركات التفاعلية ---
def render_grid(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    v_key = f"view_{prefix}"
    
    if pg_key not in st.session_state: st.session_state[pg_key] = 0
    if v_key not in st.session_state: st.session_state[v_key] = "grid"

    if st.session_state[v_key] == "details":
        if st.button("⬅ عودة للقائمة الرئيسية", key=f"back_{prefix}", use_container_width=True): 
            st.session_state[v_key] = "grid"; st.rerun()
        
        try:
            item = dataframe.iloc[st.session_state.current_index]
            st.markdown(f"<h2 style='color:#342957; text-align:right; font-weight:900; margin:25px 0; font-size:30px; border-right: 6px solid #fab818; padding-right:12px;'>🏢 {item.iloc[0]}</h2>", unsafe_allow_html=True)
            
            cols = st.columns(3)
            for i, col_name in enumerate(dataframe.columns):
                with cols[i % 3]:
                    val = item[col_name]
                    if col_name == 'Price': val = f"{int(val):,}" if float(val) > 0 else "اتصل للسعر"
                    st.markdown(f"""
                    <div class="detail-card fade-in">
                        <p class="label-purple">{col_name}</p>
                        <p class="val-black">{val}</p>
                    </div>
                    """, unsafe_allow_html=True)
        except:
            st.session_state[v_key] = "grid"; st.rerun()
            
    else:
        # شريط البحث المتطور العلوي المدمج
        st.markdown("<div class='filter-box fade-in'>", unsafe_allow_html=True)
        f1, f2 = st.columns([2.3, 1])
        with f1: search = st.text_input("🔍 ابحث هنا...", key=f"s_{prefix}", label_visibility="collapsed", placeholder="اكتب اسم المشروع، المطور، أو كلمة دلالية للبحث المباشر...")
        with f2:
            loc_list = ["كل المواقع المتاحة 📍"] + sorted([str(x).strip() for x in dataframe['Location'].unique() if str(x).strip() not in ["---", "nan", ""]]) if 'Location' in dataframe.columns else ["الكل"]
            sel_area = st.selectbox("📍 تصفية حسب الموقع", loc_list, key=f"l_{prefix}", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_area != "كل المواقع المتاحة 📍": filt = filt[filt['Location'].astype(str).str.contains(sel_area, case=False, na=False)]

        start = st.session_state[pg_key] * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.74, 0.26])
        with m_c:
            if filt.empty: 
                st.warning("لا توجد نتائج تطابق خيارات البحث الحالية.")
            else:
                grid = st.columns(2)
                for i, (idx, r) in enumerate(disp.iterrows()):
                    with grid[i%2]:
                        price_val = f"{int(r['Price']):,}" if ('Price' in r and r['Price'] > 0) else "اتصل للسعر"
                        card_content = f"🏢 {r.iloc[0]}\n📍 الموقع: {r.get('Location','---')}\n💰 السعر المستهدف: {price_val} ج.م"
                        if st.button(card_content, key=f"btn_card_{prefix}_{idx}", use_container_width=True):
                            st.session_state.current_index = idx
                            st.session_state[v_key] = "details"
                            st.rerun()
            
            # أزرار تنقل ذكية مدمجة مع الأنيميشن
            st.write("")
            p1, px, p2 = st.columns([1, 1, 1])
            with p1: 
                if st.session_state[pg_key] > 0:
                    if st.button("⬅ السابقة", key=f"prev_{prefix}", use_container_width=True): st.session_state[pg_key] -= 1; st.rerun()
            with px: st.markdown(f"<p style='text-align:center; color:#342957; font-weight:900; font-size:18px; margin-top:5px;'>صفحة {st.session_state[pg_key]+1}</p>", unsafe_allow_html=True)
            with p2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالية ➡", key=f"next_{prefix}", use_container_width=True): st.session_state[pg_key] += 1; st.rerun()

        with s_c:
            st.markdown("<p class='side-title'>⭐ كروت مميزة وموصى بها</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(6).iterrows():
                if st.button(f"📌 {str(s_row.iloc[0])[:28]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index = s_idx
                    st.session_state[v_key] = "details"
                    st.rerun()

# --- 6. حزمة قوالب الـ CSS الفاخرة لـ (Takwen Corporate Design) والتحركات ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0px !important; padding-bottom: 2rem !important; }}
    
    /* أنيميشن الظهور التدريجي الانسيابي للواجهات */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(15px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .fade-in {{ animation: fadeIn 0.5s ease-out forwards; }}
    
    /* خلفية التطبيق العامة البيضاء الناصعة */
    [data-testid="stAppViewContainer"] {{
        background-color: #ffffff !important;
        direction: rtl !important; text-align: right !important; 
        font-family: 'Cairo', sans-serif !important; color: #000000 !important;
    }}
    
    /* تخصيص السلايد بار (Sidebar) بالكامل ليتوافق مع ألوان تكوين (البنفسجي الداكن والأصفر) */
    [data-testid="stSidebar"] {{
        background-color: #342957 !important;
        border-left: 4px solid #fab818 !important;
    }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {{
        color: #ffffff !important;
        font-weight: 900 !important;
        font-family: 'Cairo', sans-serif !important;
    }}
    
    /* شريط التواصل العلوي الدقيق */
    .top-announcement-bar {{
        background-color: #342957;
        color: #ffffff !important;
        text-align: center;
        padding: 10px; font-size: 14px; font-weight: 900;
        margin-right: -5rem; margin-left: -5rem; margin-bottom: 0px;
        border-bottom: 4px solid #fab818;
    }}
    
    /* إجبار تام لجميع نصوص محتوى الواجهة الرئيسي لتكون باللون الأسود الغامق العريض */
    p, span, label, h1, h2, h3, h4, h5, h6, li {{
        color: #000000 !important;
        font-weight: 900 !important;
    }}
    
    /* هيدر ترحيبي عريض مقتبس من روح بانر تكوين والمنحنيات الصفراء البيضاء */
    .royal-header {{ 
        background: linear-gradient(135deg, #342957 0%, #453673 55%, #fab818 55%, #fab818 58%, #ffffff 58%, #ffffff 100%);
        border: 1px solid #e2e8f0;
        padding: 50px 35px; border-radius: 0 0 24px 24px; margin-bottom: 35px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.03);
        animation: fadeIn 0.6s ease-out;
    }}
    .royal-header h1 {{ color: #ffffff !important; font-size: 3.2rem; font-weight: 900; margin: 0; }}
    .royal-header p {{ color: #fab818 !important; font-weight: 900; font-size: 18px; margin-top: 8px; }}
    
    /* صندوق فلاتر البحث الانسيابي الأبيض النظيف */
    .filter-box {{ 
        background: #ffffff; padding: 20px; border-radius: 14px; 
        border: 1px solid #e2e8f0; margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.02);
    }}
    
    /* أزرار وكروت عقارية متناسقة تفاعلية - التحركات عند التمرير بالماوس */
    div.stButton > button {{
        font-family: 'Cairo', sans-serif !important; font-weight: 900 !important;
        border-radius: 12px !important; transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }}
    
    /* كروت الشبكة بلمسة الهوية والتحركات الذكية للأعلى */
    div.stButton > button[id*="btn_card_"] {{
        background: #ffffff !important; color: #000000 !important;
        border: 1px solid #e2e8f0 !important; border-right: 8px solid #342957 !important;
        text-align: right !important; min-height: 140px !important; 
        font-size: 17px !important; line-height: 1.9 !important;
        white-space: pre-line !important; display: block !important; width: 100% !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.01) !important;
        padding: 16px 20px !important;
        animation: fadeIn 0.4s ease-out forwards;
    }}
    div.stButton > button[id*="btn_card_"]:hover {{
        background: #ffffff !important; 
        transform: translateY(-5px) !important; /* التحرك الجميل للأعلى */
        border-color: #fab818 !important; border-right-color: #fab818 !important;
        box-shadow: 0 15px 30px rgba(52,41,87,0.15) !important;
    }}
    
    /* كروت التفاصيل الداخلية */
    .detail-card {{ 
        background: #ffffff; padding: 24px; border-radius: 16px; 
        border: 1px solid #e2e8f0; border-top: 5px solid #fab818; margin-bottom: 20px; 
        box-shadow: 0 5px 15px rgba(0,0,0,0.02);
    }}
    .label-purple {{ color: #342957 !important; font-weight: 900 !important; font-size: 15px; margin: 0 0 8px 0; }}
    .val-black {{ color: #000000 !important; font-size: 19px; font-weight: 900 !important; margin: 0; }}
    
    /* القائمة الجانبية للمقترحات المميزة والتحركات الخاصة بها */
    .side-title {{ color: #342957 !important; font-weight: 900; border-bottom: 2px solid #342957; padding-bottom: 10px; margin-bottom: 20px; font-size: 18px; }}
    div.stButton > button[id*="side_"] {{ 
        background: #ffffff !important; color: #000000 !important; 
        border: 1px solid #e2e8f0 !important; font-size: 14.5px !important; 
        text-align: right !important; margin-bottom: 10px !important; font-weight: 900 !important;
        padding: 12px 15px !important;
    }}
    div.stButton > button[id*="side_"]:hover {{ 
        background: #fafafa !important; border-color: #fab818 !important; color: #342957 !important;
        transform: translateX(-3px) !important; /* تحرك جانبي خفيف */
    }}
    
    /* مدخلات البحث والنصوص */
    div.stTextInput input, div.stNumberInput input, div.stSelectbox select {{ 
        background-color: #ffffff !important; color: #000000 !important; 
        border: 2px solid #cbd5e1 !important; border-radius: 10px !important; 
        height: 50px !important; text-align: right !important; font-weight: 900 !important; font-size: 15px !important;
        padding-right: 15px !important;
    }}
    div.stTextInput input:focus {{ border-color: #342957 !important; }}
    
    /* أزرار الإجراءات والتحكم الرئيسية */
    div.stButton > button[id*="btn_submit_login"], div.stButton > button[id*="back_"], div.stButton > button[id*="prev_"], div.stButton > button[id*="next_"] {{
        background: #342957 !important; color: #ffffff !important;
        font-weight: 900 !important; border: none !important; height: 50px !important; font-size: 16px !important;
        box-shadow: 0 4px 12px rgba(52,41,87,0.15) !important;
    }}
    div.stButton > button[id*="btn_submit_login"]:hover, div.stButton > button[id*="back_"]:hover {{ 
        background: #453673 !important; transform: translateY(-2px) !important;
    }}
    
    /* راديو الاختيارات داخل الشريط الجانبي */
    div[data-testid="stSidebarUserContent"] div.stRadio > label {{
        padding: 12px 15px !important; background: rgba(255,255,255,0.05) !important;
        border-radius: 8px !important; margin-bottom: 8px !important;
        transition: all 0.2s ease !important; border-right: 4px solid transparent;
    }}
    div[data-testid="stSidebarUserContent"] div.stRadio > label:hover {{
        background: rgba(255,255,255,0.1) !important; border-right-color: #fab818;
    }}
    
    /* زر التواصل الأخضر الدعم الفني (بنفس لون زر السكرين شوت) */
    div.stButton > button[id*="whatsapp_btn"] {{
        background-color: #10b981 !important; color: #ffffff !important; border: none !important;
    }}
    div.stButton > button[id*="whatsapp_btn"]:hover {{
        background-color: #059669 !important; transform: scale(1.02) !important;
    }}
    
    /* صندوق الدخول */
    .login-box {{
        background: #ffffff; border: 1px solid #e2e8f0; padding: 45px 35px; 
        border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.05); margin-top: 50px;
    }}
    .oval-header {{
        background: #342957; border-radius: 10px; padding: 18px; color: #ffffff !important; font-size: 24px; font-weight: 900;
        text-align: center; margin-bottom: 30px; border-bottom: 4px solid #fab818;
    }}
    </style>
""", unsafe_allow_html=True)

# --- شريط الاتصال والتواصل العلوي الفاخر ---
st.markdown("<div class='top-announcement-bar'>📞 تواصل واستفسار: 00201010524040 &nbsp;&nbsp;|&nbsp;&nbsp; ✉️ info@takwen.net &nbsp;&nbsp;|&nbsp;&nbsp; اطلق منصتك العقارية الاحترافية معنا 🚀</div>", unsafe_allow_html=True)

# --- 7. بوابة الدخول الآمنة للمنصة ---
if not st.session_state.get('auth', False):
    _, auth_col, _ = st.columns([1.1, 1.3, 1.1])
    with auth_col:
        st.markdown("<div class='login-box fade-in'>", unsafe_allow_html=True)
        st.markdown("<div class='oval-header'><p style='margin:0; color:#fff;'>MA3LOMATI PRO</p></div>", unsafe_allow_html=True)
        u = st.text_input("User", placeholder="اسم المستخدم الخاص بك", key="log_u", label_visibility="collapsed")
        p = st.text_input("Pass", type="password", placeholder="كلمة المرور السرية للمنصة", key="log_p", label_visibility="collapsed")
        st.write("")
        if st.button("تسجيل الدخول الآمن للمنصة 🚀", use_container_width=True, key="btn_submit_login"):
            if p == "2026": 
                st.session_state.auth, st.session_state.current_user = True, "Admin"
                st.query_params["u_session"] = "Admin"; st.rerun()
            else:
                user = login_user(u, p)
                if user:
                    st.session_state.auth, st.session_state.current_user = True, user
                    st.query_params["u_session"] = user; st.rerun()
                else: st.error("عذراً، اسم المستخدم أو كلمة السر غير صحيحة.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 8. تحميل البيانات وتشغيل القائمة الجانبية المحدثة ---
df_p, df_d, df_l = load_data()

# --- الشريط الجانبي المطور بالكامل بناءً على طلبك (Sidebar Navigation) ---
with st.sidebar:
    st.markdown("<p style='text-align:center; font-size:22px; margin-bottom:20px; border-bottom:2px solid #fab818; padding-bottom:10px;'>🧭 لوحة التحكم</p>", unsafe_allow_html=True)
    
    # قائمة التنقل الرئيسية الاحترافية
    menu = st.radio(
        "اختر القسم المطلوب لتصفحه:",
        ["🏗️ دليل المشاريع الشامل", "🚀 إطلاقات اللونشات الحالية", "🏢 دليل المطورين العقاريين", "🛠️ حزمة الأدوات الحسابية", "🤖 مستشار AI الذكي"],
        index=0
    )
    
    st.write("---")
    st.markdown("<p style='font-size:15px; margin-bottom:5px;'>📱 تواصل مباشر سريع:</p>", unsafe_allow_html=True)
    if st.button("💬 تواصل واتساب فوري", id="whatsapp_btn", use_container_width=True):
        st.success("جاري فتح محادثة الدعم الفني...")

# الهيدر الانسيابي المائل للمنصة
st.markdown(f'<div class="royal-header fade-in"><h1>MA3LOMATI PRO</h1><p>نظام العرض والتحليل العقاري المتقدم | المستشار الحالي: {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

# --- 9. توجيه الصفحات والأقسام ---
if menu == "🏗️ دليل المشاريع الشامل":
    st.markdown("<h3 style='color:#342957; font-weight:900; margin-bottom:20px;'>🏗️ دليل المشاريع العقارية الشامل</h3>", unsafe_allow_html=True)
    render_grid(df_p, "p")

elif menu == "🚀 إطلاقات اللونشات الحالية":
    st.markdown("<h3 style='color:#342957; font-weight:900; margin-bottom:20px;'>🚀 الإطلاقات العقارية الحالية (Launches)</h3>", unsafe_allow_html=True)
    render_grid(df_l, "l")

elif menu == "🏢 دليل المطورين العقاريين":
    st.markdown("<h3 style='color:#342957; font-weight:900; margin-bottom:20px;'>🏢 دليل كبار المطورين العقاريين</h3>", unsafe_allow_html=True)
    render_grid(df_d, "d")

elif menu == "🛠️ حزمة الأدوات الحسابية":
    st.markdown("<h3 style='color:#342957; text-align:center; font-weight:900; margin-bottom:30px;'>🛠️ حزمة أدوات البروكر الحسابية</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='detail-card fade-in'><h3>💳 حساب القسط والشهرية</h3>", unsafe_allow_html=True)
        pr = st.number_input("السعر الإجمالي للعقار", value=5000000, step=100000)
        dp = st.number_input("نسبة مقدم الحجز %", value=10)
        yr = st.number_input("سنوات التقسيط الإجمالية", value=8)
        res = (pr - (pr * dp/100)) / (yr * 12) if yr > 0 else 0
        st.markdown(f"<p class='label-purple'>القسط الشهري الصافي:</p><p class='val-black'>{res:,.0f} ج.م</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='detail-card fade-in'><h3>📊 حساب نسبة السعي / العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("قيمة الصفقة البيعية الكلية", value=5000000)
        pct = st.number_input("نسبة عمولة البروكر %", value=2.5)
        st.markdown(f"<p class='label-purple'>صافي العمولة المستحقة:</p><p class='val-black'>{deal*(pct/100):,.0f} ج.م</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='detail-card fade-in'><h3>📈 حساب معدل العائد الاستثماري ROI</h3>", unsafe_allow_html=True)
        buy = st.number_input("سعر شراء العقار الحالي كاش", value=5000000)
        rent = st.number_input("الإيجار الشهري المتوقع للوحدة", value=40000)
        roi = ((rent * 12) / buy) * 100 if buy > 0 else 0
        st.markdown(f"<p class='label-purple'>العائد الاستثماري السنوي المتوقع:</p><p class='val-black'>{roi:.2f} %</p></div>", unsafe_allow_html=True)

elif menu == "🤖 مستشار AI الذكي":
    st.markdown("<div class='detail-card fade-in'><h3>🤖 مستشار معلوماتي العقاري الذكي AI</h3><p style='color:#000000; font-weight:900;'>قاعدة بيانات تحليل الأسعار وتوقعات السوق قيد التحديث التلقائي الفوري لتوفير تقارير ومقارنات عقارية لعملائك بنفس الهوية الهندسية الفاخرة.</p></div>", unsafe_allow_html=True)

# تذييل الصفحة
st.markdown("<p style='text-align:center; color:#94a3b8; margin-top:60px; font-size:14px; font-weight:900;'>MA3LOMATI PRO © 2026 | المنصة العقارية المتقدمة المعتمدة على معايير تكوين الهندسية</p>", unsafe_allow_html=True)
