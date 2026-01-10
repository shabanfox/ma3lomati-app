import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS المتطور (الألوان والتنسيق)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] > section:first-child > div:first-child { padding-top: 0rem !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f4f4f4; 
    }

    /* العنوان البيضاوي */
    .hero-oval-header {
        background: linear-gradient(180deg, #000 0%, #1a1a1a 100%); 
        border: 4px solid #f59e0b; border-top: none; 
        padding: 30px 20px; border-radius: 0px 0px 500px 500px; 
        text-align: center; width: 100%; max-width: 900px; margin: 0 auto 30px auto;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.3);
    }
    .hero-oval-header h1 { color: #f59e0b; font-weight: 900; font-size: 2.5rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }

    /* أزرار التنقل العلوية */
    .nav-container { display: flex; gap: 15px; justify-content: center; margin-bottom: 30px; }
    
    /* كروت المطورين - شبكة منظمة */
    .dev-card {
        background: white; border-radius: 15px; padding: 20px;
        border: 2px solid #e0e0e0; transition: all 0.3s ease;
        text-align: center; cursor: pointer; height: 100%;
        box-shadow: 5px 5px 0px #000;
    }
    .dev-card:hover { border-color: #f59e0b; transform: translateY(-5px); box-shadow: 8px 8px 0px #f59e0b; }
    .dev-name { font-weight: 900; color: #000; font-size: 1.2rem; margin-bottom: 10px; }

    /* ستايل صفحة الأدوات - لوحة تحكم */
    .tool-box {
        background: #fff; border-left: 10px solid #f59e0b;
        padding: 25px; border-radius: 15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px; border-top: 1px solid #eee; border-right: 1px solid #eee; border-bottom: 1px solid #eee;
    }
    .tool-title { font-weight: 900; color: #000; font-size: 1.5rem; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
    
    .result-box {
        background: #000; color: #f59e0b; padding: 15px; border-radius: 10px;
        text-align: center; margin-top: 15px; border: 2px solid #f59e0b;
    }

    /* Tags للمشاريع */
    .project-tag {
        background: #fef3c7; color: #92400e; padding: 5px 12px; 
        border-radius: 8px; font-size: 0.85rem; font-weight: 700;
        display: inline-block; margin: 4px; border: 1px solid #f59e0b;
    }

    /* الأزرار */
    div.stButton > button {
        border-radius: 12px !important; font-weight: 900 !important;
        transition: 0.3s !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة الجلسة والبيانات
if 'auth' not in st.session_state: st.session_state.auth = False
if 'view' not in st.session_state: st.session_state.view = 'comp' 
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None

@st.cache_data(ttl=300)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except: return pd.DataFrame()

# 4. شاشة الدخول
if not st.session_state.auth:
    st.markdown('<div class="hero-oval-header"><h1>منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown('<div style="text-align:center; font-size:50px;">🔓</div>', unsafe_allow_html=True)
        pwd = st.text_input("كلمة المرور", type="password", placeholder="أدخل الباسورد")
        if st.button("دخول آمن", use_container_width=True):
            if pwd == "Ma3lomati_2026": st.session_state.auth = True; st.rerun()
            else: st.error("❌ الباسورد غير صحيح")
    st.stop()

# --- المحتوى الرئيسي ---
df = load_data()
st.markdown('<div class="hero-oval-header"><h1>منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# أزرار التنقل الرئيسية (Navigation)
n1, n2 = st.columns(2)
with n1:
    if st.button("🏢 دليل المطورين الشامل", use_container_width=True):
        st.session_state.view = 'comp'; st.session_state.selected_dev = None; st.rerun()
with n2:
    if st.button("🛠️ أدوات البروكر الذكية", use_container_width=True):
        st.session_state.view = 'tools'; st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# --- سيناريو دليل المطورين ---
if st.session_state.view == 'comp':
    if st.session_state.selected_dev:
        # صفحة تفاصيل المطور المبهجة
        name = st.session_state.selected_dev
        row = df[df['Developer'] == name].iloc[0]
        if st.button("🔙 العودة للقائمة"): st.session_state.selected_dev = None; st.rerun()
        
        col_r, col_l = st.columns([1.3, 1])
        with col_r:
            st.markdown(f'''<div class="tool-box">
                <div class="tool-title">👤 عن المطور</div>
                <p><b>المالك:</b> {row.get("Owner", "-")}</p>
                <p style="text-align:justify;"><b>فلسفة الشركة:</b> {row.get("Description", "-")}</p>
                <div class="tool-title" style="margin-top:20px;">🏗️ محفظة المشاريع</div>
            ''', unsafe_allow_html=True)
            for p in str(row.get("Projects", "-")).split(","):
                st.markdown(f'<span class="project-tag">{p.strip()}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_l:
            st.markdown(f'''<div class="tool-box">
                <div class="tool-title">📊 تفاصيل تجارية</div>
                <p><b>📍 المناطق:</b> {row.get("Area", "-")}</p>
                <p><b>💰 متوسط السعر:</b> {row.get("Price", "-")}</p>
                <p><b>💵 أنظمة السداد:</b> {row.get("Installments", "-")}</p>
                <p><b>📅 المقدم:</b> {row.get("Down_Payment", "-")}</p>
            </div>''', unsafe_allow_html=True)
    else:
        # شبكة المطورين (Grid)
        c_main, c_side = st.columns([0.8, 0.2])
        with c_side:
            st.markdown('<div class="tool-box" style="padding:15px;"><h4>📍 تصفية</h4></div>', unsafe_allow_html=True)
            areas = ["الكل"] + sorted(list(set([a.strip() for sublist in df['Area'].dropna().str.split(',') for a in sublist])))
            sel_area = st.selectbox("المنطقة", areas)
            
        with c_main:
            search = st.text_input("🔍 ابحث عن مطور أو مشروع محدد...")
            # فلترة البيانات
            f_df = df.copy()
            if sel_area != "الكل": f_df = f_df[f_df['Area'].str.contains(sel_area, na=False)]
            if search: f_df = f_df[f_df['Developer'].str.contains(search, na=False, case=False) | f_df['Projects'].str.contains(search, na=False, case=False)]
            
            dev_list = f_df['Developer'].unique()
            # عرض الشبكة
            for i in range(0, len(dev_list), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i+j < len(dev_list):
                        d_name = dev_list[i+j]
                        with cols[j]:
                            st.markdown(f'<div class="dev-card"><div class="dev-name">{d_name}</div>', unsafe_allow_html=True)
                            if st.button("عرض التفاصيل", key=f"btn_{d_name}", use_container_width=True):
                                st.session_state.selected_dev = d_name; st.rerun()
                            st.markdown('</div>', unsafe_allow_html=True)

# --- سيناريو أدوات البروكر ---
elif st.session_state.view == 'tools':
    st.markdown('<div style="text-align:center; margin-bottom:30px;"><h2>🛠️ لوحة الأدوات الذكية</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="tool-box"><div class="tool-title">💰 حاسبة التمويل والقسط</div>', unsafe_allow_html=True)
        total_price = st.number_input("إجمالي سعر الوحدة (ج.م)", min_value=0, step=100000)
        dp_pct = st.slider("نسبة المقدم (%)", 0, 50, 10)
        years = st.select_slider("مدة التقسيط (سنوات)", options=list(range(1, 21)), value=7)
        
        if total_price > 0:
            dp_val = total_price * (dp_pct / 100)
            monthly = (total_price - dp_val) / (years * 12)
            st.markdown(f'''<div class="result-box">
                <p>قيمة المقدم: {dp_val:,.0f} ج.م</p>
                <h3>القسط الشهري: {monthly:,.0f} ج.م</h3>
            </div>''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="tool-box"><div class="tool-title">📈 حاسبة الاستثمار ROI</div>', unsafe_allow_html=True)
        inv_amt = st.number_input("قيمة شراء العقار", min_value=0, step=100000)
        exp_rent = st.number_input("الإيجار الشهري المتوقع", min_value=0, step=1000)
        
        if inv_amt > 0 and exp_rent > 0:
            annual_income = exp_rent * 12
            roi = (annual_income / inv_amt) * 100
            st.markdown(f'''<div class="result-box">
                <p>الدخل السنوي المتوقع: {annual_income:,.0f} ج.م</p>
                <h3>نسبة العائد السنوي: {roi:.2f} %</h3>
            </div>''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # أداة إضافية سريعة
        st.markdown('<div class="tool-box"><div class="tool-title">📝 ملاحظة سريعة</div><p style="font-size:0.9rem; color:#666;">استخدم هذه الحاسبة لإعطاء عميلك أرقاماً تقريبية سريعة تساعده في اتخاذ القرار.</p></div>', unsafe_allow_html=True)
