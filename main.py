import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    .block-container { padding-top: 1rem !important; }
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; background-color: #f4f7f9; 
    }
    .advanced-search-box {
        background: #ffffff; padding: 25px; border-radius: 15px;
        border: 1px solid #e2e8f0; margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    .small-grid-card {
        background: white; border-radius: 12px; padding: 18px;
        border: 1px solid #e2e8f0; border-right: 6px solid #003366;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب ومعالجة البيانات (الإصلاح هنا)
@st.cache_data(ttl=60)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        
        # تنظيف البيانات لتحويلها لأرقام (للفلترة الصحيحة)
        if 'Downpayment' in df.columns:
            df['Down_Num'] = pd.to_numeric(df['Downpayment'].astype(str).str.extract('(\2026)')[0], errors='coerce').fillna(0)
        if 'Years' in df.columns:
            df['Years_Num'] = pd.to_numeric(df['Years'].astype(str).str.extract('(\2026)')[0], errors='coerce').fillna(0)
            
        return df
    except: return None

df = load_data()

# إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'current_page' not in st.session_state: st.session_state.current_page = 1

# --- الهيدر ---
st.markdown('<div style="background:white; padding:15px; border-radius:15px; box-shadow:0 2px 10px rgba(0,0,0,0.05); margin-bottom:20px; text-align:right;">'
            '<span style="color:#003366; font-weight:900; font-size:1.8rem;">منصة معلوماتى العقارية</span></div>', unsafe_allow_html=True)

if st.session_state.page == 'main' and df is not None:
    
    # --- مربع البحث المتطور ---
    st.markdown('<div class="advanced-search-box">', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        s_name = st.text_input("🔍 اسم المطور / المشروع")
    with c2:
        areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
        s_area = st.selectbox("📍 المنطقة", areas)
    with c3:
        years_opt = ["الكل", "3 سنوات", "5 سنوات", "7 سنوات", "10 سنوات"]
        s_years = st.selectbox("⏳ مدة التقسيط", years_opt)

    c4, c5, c6 = st.columns(3)
    with c4:
        down_opt = ["الكل", "0%", "5%", "10%", "15%", "20%"]
        s_down = st.selectbox("💰 نسبة المقدم", down_opt)
    with c5:
        budget_opt = ["الكل", "أقل من 5 مليون", "5 - 10 مليون", "أكثر من 10 مليون"]
        s_budget = st.selectbox("💵 الميزانية", budget_opt)
    with c6:
        st.write("") # محاذاة
        if st.button("🔄 إعادة ضبط الفلاتر", use_container_width=True): st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- منطق الفلترة الفعلي (الإصلاح الجوهري) ---
    f_df = df.copy()
    
    if s_name:
        f_df = f_df[f_df['Developer'].astype(str).str.contains(s_name, case=False, na=False)]
    
    if s_area != "الكل":
        f_df = f_df[f_df['Area'] == s_area]
        
    if s_years != "الكل":
        # استخراج الرقم من الاختيار (مثلاً "7 سنوات" تصبح 7)
        y_val = int(''.join(filter(str.isdigit, s_years)))
        f_df = f_df[f_df['Years_Num'] >= y_val]

    if s_down != "الكل":
        d_val = int(''.join(filter(str.isdigit, s_down)))
        f_df = f_df[f_df['Down_Num'] <= d_val]

    # --- عرض النتائج ---
    col_main, col_side = st.columns([2.3, 1])
    with col_main:
        items_per_page = 6
        start_idx = (st.session_state.current_page - 1) * items_per_page
        page_items = f_df.iloc[start_idx : start_idx + items_per_page]

        if f_df.empty:
            st.info("لم نجد نتائج تطابق هذه الفلاتر.")
        else:
            grid = st.columns(2)
            for idx, (i, row) in enumerate(page_items.reset_index().iterrows()):
                with grid[idx % 2]:
                    st.markdown(f"""
                        <div class="small-grid-card">
                            <div style="font-weight:900; color:#003366; font-size:1.1rem;">{row.get('Developer')}</div>
                            <div style="color:#64748b; font-size:0.85rem;">📍 {row.get('Area')}</div>
                            <div style="margin-top:10px;">
                                <span style="background:#eef2ff; color:#003366; padding:2px 8px; border-radius:5px; font-size:0.8rem;">💰 مقدم: {row.get('Downpayment')}</span>
                                <span style="background:#fff7ed; color:#9a3412; padding:2px 8px; border-radius:5px; font-size:0.8rem;">⏳ {row.get('Years')}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("التفاصيل", key=f"btn_{i}", use_container_width=True):
                        st.session_state.selected_item = row.to_dict(); st.session_state.page = 'details'; st.rerun()

    with col_side:
        st.markdown(f'<div style="background:white; padding:20px; border-radius:15px; border:1px solid #e2e8f0; text-align:center;">'
                    f'<h5 style="color:#64748b; margin:0;">النتائج</h5><h2 style="color:#003366;">{len(f_df)}</h2></div>', unsafe_allow_html=True)

# صفحة التفاصيل
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 عودة"): st.session_state.page = 'main'; st.rerun()
    st.markdown(f'<div style="background:white; padding:30px; border-radius:15px; border-right:10px solid #003366;">'
                f'<h1>{item.get("Developer")}</h1><hr><p>{item.get("Detailed_Info")}</p></div>', unsafe_allow_html=True)
