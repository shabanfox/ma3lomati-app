import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - تنسيقات احترافية لصفحة المطور
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f4f7f9; 
    }

    /* كروت اليمين */
    .small-grid-card {
        background: white; border-radius: 10px; padding: 12px;
        height: 100px; display: flex; flex-direction: column;
        justify-content: center; border: 1px solid #e2e8f0;
        border-right: 4px solid #003366; margin-bottom: 5px;
    }

    /* كروت التفاصيل */
    .bio-section {
        background: white; padding: 25px; border-radius: 15px;
        border-right: 8px solid #D4AF37; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    .project-tag {
        display: inline-block; background: #eef2f6; color: #003366;
        padding: 5px 15px; border-radius: 20px; margin: 5px;
        font-weight: bold; font-size: 0.9rem; border: 1px solid #cbd5e1;
    }

    .stat-card {
        background: white; padding: 20px; border-radius: 15px;
        border: 1px solid #e2e8f0; text-align: center; margin-bottom: 20px;
    }

    div.stButton > button {
        border-radius: 6px !important; font-family: 'Cairo', sans-serif !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        if 'Developer' in df.columns:
            df = df.sort_values(by='Developer', ascending=True)
        return df
    except: return None

df = load_data()

# إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'search_query' not in st.session_state: st.session_state.search_query = ""

top_10_list = ["Mountain View", "SODIC", "Emaar", "TMG", "Ora Developers", "Palm Hills", "Tatweer Misr", "Misr Italia", "Orascom", "Hassan Allam"]

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    st.markdown('<h2 style="color:#003366; font-weight:900;">منصة معلوماتى العقارية</h2>', unsafe_allow_html=True)

    if df is not None:
        col_right, col_left = st.columns([1.8, 1])

        with col_right:
            # مربع البحث
            st.markdown('<div style="background:white; padding:15px; border-radius:12px; border:1px solid #e2e8f0; margin-bottom:15px;">', unsafe_allow_html=True)
            f_c1, f_c2 = st.columns([2, 1])
            with f_c1:
                st.session_state.search_query = st.text_input("🔍 ابحث عن مطور...", value=st.session_state.search_query)
            with f_c2:
                areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
                s_area = st.selectbox("المنطقة", areas)
            st.markdown('</div>', unsafe_allow_html=True)

            # فلترة
            f_df = df.copy()
            if s_area != "الكل": f_df = f_df[f_df['Area'] == s_area]
            if st.session_state.search_query:
                f_df = f_df[f_df['Developer'].astype(str).str.contains(st.session_state.search_query, case=False, na=False)]

            # عرض الكروت
            grid_cols = st.columns(2)
            for idx, (i, row) in enumerate(f_df.reset_index().iterrows()):
                with grid_cols[idx % 2]:
                    st.markdown(f"""
                        <div class="small-grid-card">
                            <div style="color:#003366; font-weight:900; font-size:0.9rem;">{row.get('Developer')}</div>
                            <div style="color:#64748b; font-size:0.75rem;">📍 {row.get('Area')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("عرض البروفايل الكامل", key=f"det_{i}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'; st.rerun()

        with col_left:
            st.markdown(f'<div class="stat-card"><h5 style="color:#64748b;">النتائج</h5><h2 style="color:#003366;">{len(f_df)}</h2></div>', unsafe_allow_html=True)
            st.markdown('<div class="stat-card" style="text-align:right;"><h4>🏆 الشركات الكبرى</h4>', unsafe_allow_html=True)
            for company in top_10_list:
                if st.button(f"🏢 {company}", key=f"top_{company}", use_container_width=True):
                    st.session_state.search_query = company; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التفاصيل المطور (The Profile) ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 العودة للرئيسية"): st.session_state.page = 'main'; st.rerun()

    # الهيدر
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #003366 0%, #001a33 100%); padding: 40px; border-radius: 15px; color: white; text-align: center; margin-bottom: 25px;">
            <h1 style="margin:0;">{item.get('Developer')}</h1>
            <p style="font-size:1.2rem; opacity:0.8;">المقر الرئيسي والانتشار: {item.get('Area')}</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        # قسم نبذة عن الشركة
        st.markdown('<div class="bio-section"><h3>📖 نبذة عن المطور</h3>', unsafe_allow_html=True)
        st.write(item.get('Company_Bio', 'معلومات المطور غير متوفرة حالياً في قاعدة البيانات.'))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # قسم المشاريع
        st.markdown('<div class="bio-section"><h3>🏗️ سجل المشاريع</h3>', unsafe_allow_html=True)
        projects = str(item.get('Projects_List', '')).split('-') # يفترض أن المشاريع مفصولة بـ (-) في الشيت
        if projects and projects[0] != 'nan':
            for p in projects:
                if p.strip():
                    st.markdown(f'<span class="project-tag">{p.strip()}</span>', unsafe_allow_html=True)
        else:
            st.info("سيتم تحديث قائمة المشاريع قريباً.")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        # قسم الزتونة الفنية (Summary)
        st.markdown('<div class="stat-card" style="text-align:right; border-top: 5px solid #003366;">', unsafe_allow_html=True)
        st.markdown('<h3>💡 الزتونة الفنية</h3>', unsafe_allow_html=True)
        st.info(item.get('Detailed_Info', 'لا توجد ملاحظات فنية حالياً.'))
        st.markdown(f"""
            <hr>
            <p><b>👤 المالك:</b> {item.get('Owner', '-')}</p>
            <p><b>💰 متوسط الأسعار:</b> {item.get('Price', '-')}</p>
            <p><b>⏳ أنظمة السداد:</b> {item.get('Installments', '-')}</p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
