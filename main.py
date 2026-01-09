import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلوماتى العقارية - نسخة البروكر", layout="wide")

# 2. كود التصميم (CSS) - الشكل القديم مع لمسة احترافية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f1f5f9; 
    }

    .block-container { max-width: 1100px; margin: auto; padding: 1rem 3% !important; }

    .header-nav { text-align: right; padding: 15px 0; margin-bottom: 5px; }

    .filter-box { 
        background: white; padding: 15px; border-radius: 12px; 
        margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .project-card-container { 
        background-color: #edf2f7; border-radius: 10px; 
        margin-bottom: 5px !important; padding: 0;
        display: flex; align-items: center; border: 1px solid #e2e8f0;
    }

    /* شارات التميز (Badges) */
    .badge {
        display: inline-block; padding: 2px 10px; border-radius: 5px;
        font-size: 0.75rem; font-weight: 700; margin-left: 5px; color: white;
    }
    .badge-green { background-color: #28a745; }
    .badge-blue { background-color: #007bff; }
    .badge-gold { background-color: #D4AF37; }

    div.stButton > button {
        background-color: #003366 !important; color: white !important;
        border-radius: 6px !important; padding: 4px 15px !important;
        font-size: 0.85rem !important; font-weight: 700 !important;
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
        return df
    except: return None

df = load_data()

if 'page' not in st.session_state:
    st.session_state.page = 'main'
    st.session_state.selected_item = None

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    st.markdown('<div class="header-nav"><div style="color:#003366; font-weight:900; font-size:1.8rem;">منصة معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)

    if df is not None:
        # الفلاتر المطورة للبروكر
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: search_dev = st.text_input("🔍 المطور")
        with c2: search_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(list(df['Area'].dropna().unique())))
        with c3: 
            install_list = ["الكل"] + sorted(list(df['Installments'].dropna().unique().astype(str))) if 'Installments' in df.columns else ["الكل"]
            search_install = st.selectbox("⏳ سنوات القسط", install_list)
        with c4: search_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(list(df['Type'].dropna().unique()))) if 'Type' in df.columns else st.selectbox("🏠 النوع", ["الكل"])
        st.markdown('</div>', unsafe_allow_html=True)

        f_df = df.copy()
        if search_dev: f_df = f_df[f_df['Developer'].str.contains(search_dev, case=False, na=False)]
        if search_area != "الكل": f_df = f_df[f_df['Area'] == search_area]
        if search_install != "الكل": f_df = f_df[f_df['Installments'].astype(str) == search_install]

        # عرض الكروت
        for _, row in f_df.iterrows():
            st.markdown('<div class="project-card-container">', unsafe_allow_html=True)
            col_content, col_img = st.columns([4, 1])
            
            with col_content:
                txt_c, btn_c = st.columns([3, 1])
                with txt_c:
                    # إضافة الشارات الذكية بناءً على البيانات
                    badges_html = ""
                    if 'Delivery' in row and "فوري" in str(row['Delivery']):
                        badges_html += '<span class="badge badge-green">استلام فوري</span>'
                    if 'Installments' in row and int(row['Installments']) >= 8:
                        badges_html += '<span class="badge badge-blue">قسط طويل</span>'
                    
                    st.markdown(f"""
                        <div style="text-align: right; padding: 15px;">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <span style="color: #003366; font-weight: 900; font-size: 1.3rem;">{row.get('Developer')}</span>
                                {badges_html}
                            </div>
                            <div style="color: #D4AF37; font-weight: 700; font-size: 0.9rem;">المالك: {row.get('Owner')}</div>
                            <div style="color: #64748b; font-size: 0.8rem;">📍 {row.get('Area')} | قسط: {row.get('Installments')} سنين | {row.get('Price')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with btn_c:
                    st.write("")
                    st.write("")
                    if st.button("التفاصيل", key=f"btn_{row.get('Developer')}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'
                        st.rerun()

            with col_img:
                img_url = row.get('Image_URL', 'https://via.placeholder.com/400')
                st.markdown(f'<div style="height: 100px; border-radius: 0 10px 10px 0; background-image: url(\'{img_url}\'); background-size: cover; background-position: center;"></div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التفاصيل ---
else:
    item = st.session_state.selected_item
    st.markdown('<div style="background:white; padding:30px; border-radius:15px; margin-top:10px; border: 1px solid #e2e8f0;">', unsafe_allow_html=True)
    if st.button("⬅️ عودة للقائمة"):
        st.session_state.page = 'main'; st.rerun()
    
    st.markdown(f"<h2 style='color:#003366;'>{item.get('Developer')}</h2>", unsafe_allow_html=True)
    st.write(f"**المنطقة:** {item.get('Area')}")
    st.write(f"**نظام السداد:** {item.get('Installments')} سنوات")
    st.markdown("---")
    st.write(f"**التفاصيل:** {item.get('Description', 'جاري التحديث...')}")
