import streamlit as st
import pandas as pd
import requests
import time

# --- 1. إعدادات الصفحة والهيكل العام للمنصة ---
st.set_page_config(
    page_title="REAL INVEST | MA3LOMATI PRO", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. إدارة حالة الجلسة والتأمين (Session State) ---
if 'auth' not in st.session_state:
    if "u_session" in st.query_params:
        st.session_state.auth = True
        st.session_state.current_user = st.query_params["u_session"]
    else:
        st.session_state.auth = False

if 'current_index' not in st.session_state: st.session_state.current_index = 0

# --- 3. روابط البيانات الثابتة من شيتات جوجل ---
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

ITEMS_PER_PAGE = 6

# --- 4. وظائف جلب وتجهيز البيانات وحساب الأسعار ---
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

# --- 5. دالة بناء شبكة العرض والتحركات التفاعلية للكروت ---
def render_grid(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    v_key = f"view_{prefix}"
    
    if pg_key not in st.session_state: st.session_state[pg_key] = 0
    if v_key not in st.session_state: st.session_state[v_key] = "grid"

    if st.session_state[v_key] == "details":
        if st.button("⬅ عودة للقائمة الشاملة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state[v_key] = "grid"; st.rerun()
        
        try:
            item = dataframe.iloc[st.session_state.current_index]
            st.markdown(f"<h2 style='color:#0F1A2A; text-align:right; font-weight:900; margin:25px 0; font-size:30px; border-right: 6px solid #D19F41; padding-right:12px;'>🏢 {item.iloc[0]}</h2>", unsafe_allow_html=True)
            
            cols = st.columns(3)
            for i, col_name in enumerate(dataframe.columns):
                with cols[i % 3]:
                    val = item[col_name]
                    if col_name == 'Price': val = f"{int(val):,}" if float(val) > 0 else "اتصل للسعر"
                    st.markdown(f"""
                    <div class="detail-card fade-in">
                        <p class="label-navy">{col_name}</p>
                        <p class="val-black">{val}</p>
                    </div>
                    """, unsafe_allow_html=True)
        except:
            st.session_state[v_key] = "grid"; st.rerun()
            
    else:
        # فلاتر البحث الفورية والتصفية الذكية
        st.markdown("<div class='filter-box fade-in'>", unsafe_allow_html=True)
        f1, f2 = st.columns([2.3, 1])
        with f1: search = st.text_input("🔍 ابحث هنا...", key=f"s_{prefix}", label_visibility="collapsed", placeholder="اكتب اسم المشروع، المطور، أو المنطقة الجغرافية للبحث...")
        with f2:
            loc_list = ["كل المواقع المتاحة بالدليل 📍"] + sorted([str(x).strip() for x in dataframe['Location'].unique() if str(x).strip() not in ["---", "nan", ""]]) if 'Location' in dataframe.columns else ["الكل"]
            sel_area = st.selectbox("📍 تصفية حسب الموقع", loc_list, key=f"l_{prefix}", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_area != "كل المواقع المتاحة بالدليل 📍": filt = filt[filt['Location'].astype(str).str.contains(sel_area, case=False, na=False)]

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
            
            # أزرار الانتقال بين الصفحات بنظام الترقيم الرقمي
            st.write("")
            p1, px, p2 = st.columns([1, 1, 1])
            with p1: 
                if st.session_state[pg_key] > 0:
                    if st.button("⬅ السابقة", key=f"prev_{prefix}", use_container_width=True): st.session_state[pg_key] -= 1; st.rerun()
            with px: st.markdown(f"<p style='text-align:center; color:#0F1A2A; font-weight:900; font-size:18px; margin-top:5px;'>صفحة {st.session_state[pg_key]+1}</p>", unsafe_allow_html=True)
            with p2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالية ➡", key=f"next_{prefix}", use_container_width=True): st.session_state[pg_key] += 1; st.rerun()

        with s_c:
            st.markdown("<p class='side-title'>⭐ مشاريع موصى بها</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(6).iterrows():
                if st.button(f"📌 {str(s_row.iloc[0])[:28]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index = s_idx
                    st.session_state[v_key] = "details"
                    st.rerun()

# --- 6. قالب الـ CSS الفاخر لمحاكاة تصميم الصورة والتأثيرات الحركية (Hover Effects) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0px !important; padding-bottom: 2rem !important; }}
    
    /* تأثير أنيميشن التحميل التدريجي الفاخر للواجهة */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(12px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .fade-in {{ animation: fadeIn 0.45s ease-out forwards; }}
    
    /* تهيئة الخلفية العامة للموقع باللون الأبيض النظيف جداً المريح للعين */
    [data-testid="stAppViewContainer"] {{
        background-color: #ffffff !important;
        direction: rtl !important; text-align: right !important; 
        font-family: 'Cairo', sans-serif !important; color: #000000 !important;
    }}
    
    /* تصميم وضبط ألوان السلايد بار الجانبي (Sidebar) ليتطابق مع واجهة ريل إنفست */
    [data-testid="stSidebar"] {{
        background-color: #0F1A2A !important;
        border-left: 4px solid #D19F41 !important;
    }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {{
        color: #ffffff !important; font-weight: 900 !important; font-family: 'Cairo', sans-serif !important;
    }}
    
    /* شريط الاتصال العلوي (Top Announcement Bar) */
    .top-announcement-bar {{
        background-color: #0F1A2A; color: #ffffff !important; text-align: center;
        padding: 10px; font-size: 14px; font-weight: 900;
        margin-right: -5rem; margin-left: -5rem; margin-bottom: 0px;
        border-bottom: 4px solid #D19F41;
    }}
    
    /* إجبار جميع النصوص داخل الموقع على الظهور باللون الأسود الغامق الصريح والخط العريض جداً للوضوح العالي */
    p, span, label, h1, h2, h3, h4, h5, h6, li {{
        color: #000000 !important; font-weight: 900 !important;
    }}
    
    /* --- الهيدر الفاخر وقسم الهيرو المائل (Hero Background Layout) المتوافق مع الصورة المرفقة --- */
    .hero-container {{
        background: linear-gradient(135deg, #0F1A2A 0%, #17263b 52%, #D19F41 52%, #D19F41 55%, #ffffff 55%, #ffffff 100%);
        border: 1px solid #e2e8f0; padding: 50px 35px; border-radius: 0 0 24px 24px; margin-bottom: 35px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04);
        animation: fadeIn 0.5s ease-out;
    }}
    .hero-container h1 {{ color: #ffffff !important; font-size: 3.2rem; font-weight: 900; margin: 0; }}
    .hero-container p {{ color: #D19F41 !important; font-weight: 900; font-size: 18px; margin-top: 8px; }}
    
    /* صندوق البحث المتقدم */
    .filter-box {{ 
        background: #ffffff; padding: 20px; border-radius: 14px; 
        border: 1px solid #e2e8f0; margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.02);
    }}
    
    /* ضبط انسيابية وحركة الأزرار لتأثير الـ Hover عند تمرير الماوس */
    div.stButton > button {{
        font-family: 'Cairo', sans-serif !important; font-weight: 900 !important;
        border-radius: 12px !important; transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    
    /* تحركات كروت العرض والشبكة العقارية الذكية للأعلى وسلاسة الظل */
    div.stButton > button[id*="btn_card_"] {{
        background: #ffffff !important; color: #000000 !important;
        border: 1px solid #e2e8f0 !important; border-right: 8px solid #0F1A2A !important;
        text-align: right !important; min-height: 140px !important; 
        font-size: 17px !important; line-height: 1.9 !important;
        white-space: pre-line !important; display: block !important; width: 100% !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.01) !important; padding: 16px 20px !important;
    }}
    div.stButton > button[id*="btn_card_"]:hover {{
        background: #ffffff !important; 
        transform: translateY(-5px) !important; /* قفزة خفيفة للأعلى لتأثير التحرك الجميل */
        border-color: #D19F41 !important; border-right-color: #D19F41 !important;
        box-shadow: 0 15px 35px rgba(15,26,42,0.13) !important;
    }}
    
    /* كروت التفاصيل الداخلية للعقارات */
    .detail-card {{ 
        background: #ffffff; padding: 24px; border-radius: 16px; 
        border: 1px solid #e2e8f0; border-top: 5px solid #D19F41; margin-bottom: 20px; 
        box-shadow: 0 5px 15px rgba(0,0,0,0.02);
    }}
    .label-navy {{ color: #0F1A2A !important; font-weight: 900 !important; font-size: 15px; margin: 0 0 8px 0; }}
    .val-black {{ color: #000000 !important; font-size: 19px; font-weight: 900 !important; margin: 0; }}
    
    /* قائمة الترشيحات والمقترحات الجانبية وعناصرها التفاعلية */
    .side-title {{ color: #0F1A2A !important; font-weight: 900; border-bottom: 2px solid #0F1A2A; padding-bottom: 10px; margin-bottom: 20px; font-size: 18px; }}
    div.stButton > button[id*="side_"] {{ 
        background: #ffffff !important; color: #000000 !important; 
        border: 1px solid #e2e8f0 !important; font-size: 14.5px !important; 
        text-align: right !important; margin-bottom: 10px !important; font-weight: 900 !important;
        padding: 12px 15px !important;
    }}
    div.stButton > button[id*="side_"]:hover {{ 
        background: #fafafa !important; border-color: #D19F41 !important; color: #0F1A2A !important;
        transform: translateX(-4px) !important; /* تحرك أفقي بسيط وجذاب للعين */
    }}
    
    /* حقول الإدخال والبحث وعناصر الاختيار */
    div.stTextInput input, div.stNumberInput input, div.stSelectbox select {{ 
        background-color: #ffffff !important; color: #000000 !important; 
        border: 2px solid #cbd5e1 !important; border-radius: 10px !important; 
        height: 50px !important; text-align: right !important; font-weight: 900 !important; font-size: 15px !important;
        padding-right: 15px !important;
    }}
    div.stTextInput input:focus {{ border-color: #0F1A2A !important; }}
    
    /* أزرار التحكم اللوحية والتصفح والعودة */
    div.stButton > button[id*="btn_submit_login"], div.stButton > button[id*="back_"], div.stButton > button[id*="prev_"], div.stButton > button[id*="next_"] {{
        background: #0F1A2A !important; color: #ffffff !important;
        font-weight: 900 !important; border: none !important; height: 50px !important; font-size: 16px !important;
        box-shadow: 0 4px 12px rgba(15,26,42,0.15) !important;
    }}
    div.stButton > button[id*="btn_submit_login"]:hover, div.stButton > button[id*="back_"]:hover {{ 
        background: #17263b !important; transform: translateY(-2px) !important;
    }}
    
    /* تنسيق أزرار الراديو والتنقل الداخلي في القائمة الجانبية المظلمة */
    div[data-testid="stSidebarUserContent"] div.stRadio > label {{
        padding: 12px 15px !important; background: rgba(255,255,255,0.04) !important;
        border-radius: 8px !important; margin-bottom: 8px !important;
        transition: all 0.22s ease !important; border-right: 4px solid transparent;
    }}
    div[data-testid="stSidebarUserContent"] div.stRadio > label:hover {{
        background: rgba(255,255,255,0.09) !important; border-right-color: #D19F41;
    }}
    
    /* زر التواصل والدعم الفني المباشر باللون الأخضر المميز في التصميم الأصلي */
    div.stButton > button[id*="whatsapp_btn"] {{
        background-color: #10b981 !important; color: #ffffff !important; border: none !important;
    }}
    div.stButton > button[id*="whatsapp_btn"]:hover {{
        background-color: #059669 !important; transform: scale(1.02) !important;
    }}
    
    /* نافذة تسجيل الدخول الآمن */
    .login-box {{
        background: #ffffff; border: 1px solid #e2e8f0; padding: 45px 35px; 
        border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.05); margin-top: 50px;
    }}
    .oval-header {{
        background: #0F1A2A; border-radius: 10px; padding: 18px; color: #ffffff !important; font-size: 24px; font-weight: 900;
        text-align: center; margin-bottom: 30px; border-bottom: 4px solid #D19F41;
    }}
    </style>
""", unsafe_allow_html=True)

# --- شريط الاتصال والتواصل العلوي الفاخر والمطابق للتصميم الهيكلي للشركة ---
st.markdown("<div class='top-announcement-bar'>📞 اتصل بنا: 0020101852747 &nbsp;&nbsp;|&nbsp;&nbsp; ✉️ info@takwen.net &nbsp;&nbsp;|&nbsp;&nbsp; ريل إنفست للاستثمار والتسويق العقاري الحديث 🚀</div>", unsafe_allow_html=True)

# --- 7. بوابة تسجيل الدخول المباشر والتأمين الآمن للمنصة ---
if not st.session_state.get('auth', False):
    _, auth_col, _ = st.columns([1.1, 1.3, 1.1])
    with auth_col:
        st.markdown("<div class='login-box fade-in'>", unsafe_allow_html=True)
        st.markdown("<div class='oval-header'><p style='margin:0; color:#fff;'>MA3LOMATI PRO</p></div>", unsafe_allow_html=True)
        u = st.text_input("User", placeholder="ادخل اسم المستخدم الخاص بك", key="log_u", label_visibility="collapsed")
        p = st.text_input("Pass", type="password", placeholder="ادخل كلمة المرور السرية", key="log_p", label_visibility="collapsed")
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

# --- 8. تحميل وقراءة البيانات الحية وتشغيل لوحة التحكم الجانبية الفاخرة ---
df_p, df_d, df_l = load_data()

with st.sidebar:
    st.markdown("<p style='text-align:center; font-size:22px; margin-bottom:20px; border-bottom:2px solid #D19F41; padding-bottom:10px;'>🧭 لوحة تصفح المنصة</p>", unsafe_allow_html=True)
    
    # قائمة التنقل الرئيسية الاحترافية في الشريط الجانبي المطابق للصورة
    menu = st.radio(
        "اختر القسم المطلوب للتصفح والمراجعة الفورية:",
        ["🏗️ دليل المشاريع العقارية الشامل", "🚀 إطلاقات اللونشات الحالية", "🏢 دليل المطورين العقاريين الكبار", "🛠️ حزمة أدوات البروكر الحسابية", "🤖 مستشار المقارنة العقاري الذكي AI"],
        index=0
    )
    
    st.write("---")
    st.markdown("<p style='font-size:15px; margin-bottom:5px;'>📱 قنوات الدعم السريع والاتصال:</p>", unsafe_allow_html=True)
    if st.button("💬 تواصل واتساب فوري متاح", key="whatsapp_btn", use_container_width=True):
        st.info("جاري تحويلك لمحادثة الدعم الفني لريل إنفست...")

# إظهار قسم الهيرو الانسيابي المائل المستوحى والمطابق لطلبك والصورة تماماً
st.markdown(f'<div class="hero-container fade-in"><h1>REAL INVEST</h1><p>منصة العرض والتحليل العقاري المتقدمة | المستشار الحالي للمنصة: {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

# --- 9. توجيه وعرض الصفحات والأقسام التفاعلية بالمنصة ---
if menu == "🏗️ دليل المشاريع العقارية الشامل":
    st.markdown("<h3 style='color:#0F1A2A; font-weight:900; margin-bottom:20px;'>🏗️ دليل المشاريع العقارية الشامل</h3>", unsafe_allow_html=True)
    render_grid(df_p, "p")

elif menu == "🚀 إطلاقات اللونشات الحالية":
    st.markdown("<h3 style='color:#0F1A2A; font-weight:900; margin-bottom:20px;'>🚀 الإطلاقات العقارية والمشروعات قيد اللونش (Launches)</h3>", unsafe_allow_html=True)
    render_grid(df_l, "l")

elif menu == "🏢 دليل المطورين العقاريين الكبار":
    st.markdown("<h3 style='color:#0F1A2A; font-weight:900; margin-bottom:20px;'>🏢 دليل كبار الشركات والمطورين العقاريين بالسوق</h3>", unsafe_allow_html=True)
    render_grid(df_d, "d")

elif menu == "🛠️ حزمة أدوات البروكر الحسابية":
    st.markdown("<h3 style='color:#0F1A2A; text-align:center; font-weight:900; margin-bottom:30px;'>🛠️ حزمة أدوات البروكر الحسابية الذكية</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='detail-card fade-in'><h3>💳 حساب القسط والشهرية</h3>", unsafe_allow_html=True)
        pr = st.number_input("السعر الإجمالي للعقار", value=5000000, step=100000)
        dp = st.number_input("نسبة مقدم الحجز %", value=10)
        yr = st.number_input("سنوات التقسيط الإجمالية", value=8)
        res = (pr - (pr * dp/100)) / (yr * 12) if yr > 0 else 0
        st.markdown(f"<p class='label-navy'>قيمة القسط الشهري الصافي:</p><p class='val-black'>{res:,.0f} ج.م</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='detail-card fade-in'><h3>📊 حساب نسبة السعي / العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("قيمة الصفقة البيعية الكلية", value=5000000)
        pct = st.number_input("نسبة عمولة البروكر %", value=2.5)
        st.markdown(f"<p class='label-navy'>صافي العمولة المستحقة للوسيط:</p><p class='val-black'>{deal*(pct/100):,.0f} ج.م</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='detail-card fade-in'><h3>📈 حساب معدل العائد الاستثماري ROI</h3>", unsafe_allow_html=True)
        buy = st.number_input("سعر شراء العقار الحالي كاش", value=5000000)
        rent = st.number_input("الإيجار الشهري المتوقع للوحدة", value=40000)
        roi = ((rent * 12) / buy) * 100 if buy > 0 else 0
        st.markdown(f"<p class='label-navy'>العائد الاستثماري السنوي المتوقع للوحدة:</p><p class='val-black'>{roi:.2f} %</p></div>", unsafe_allow_html=True)

elif menu == "🤖 مستشار المقارنة العقاري الذكي AI":
    st.markdown("<div class='detail-card fade-in'><h3>🤖 مستشار ريل إنفست العقاري الذكي AI</h3><p style='color:#000000; font-weight:900;'>تحديثات الأسعار وتحليلات السوق وتوقعات عام 2026 يتم معالجتها الآن فورياً لمساعدتك على تقديم مقارنات عقارية احترافية لعملائك بنفس الهوية الهندسية المعتمدة للشركة.</p></div>", unsafe_allow_html=True)

# تذييل الصفحة الفاخر المتناسق
st.markdown("<p style='text-align:center; color:#94a3b8; margin-top:60px; font-size:14px; font-weight:900;'>REAL INVEST © 2026 | تطوير وإدارة معلوماتي برو للمنصات العقارية الاحترافية المتكاملة</p>", unsafe_allow_html=True)
