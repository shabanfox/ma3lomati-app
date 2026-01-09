import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f1f5f9; 
    }

    /* كروت المقارنة */
    .comp-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        border: 2px solid #e2e8f0;
        text-align: center;
        height: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .comp-header { color: #003366; font-weight: 900; font-size: 1.4rem; margin-bottom: 10px; border-bottom: 2px solid #f1f5f9; padding-bottom: 10px; }
    .comp-price { color: #D4AF37; font-weight: 800; font-size: 1.2rem; margin: 10px 0; }
    .comp-label { color: #64748b; font-size: 0.85rem; }
    .comp-value { color: #003366; font-weight: 700; display: block; margin-bottom: 10px; }

    /* الكروت الرمادية الأساسية */
    .project-card-container { 
        background-color: #edf2f7; border-radius: 10px; 
        margin-bottom: 8px !important; display: flex;
        align-items: center; border: 1px solid #e2e8f0; overflow: hidden;
    }
    
    div.stButton > button {
        background-color: #003366 !important; color: white !important;
        border-radius: 6px !important; padding: 4px 15px !important;
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

# إدارة الجلسة
if 'compare_list' not in st.session_state: st.session_state.compare_list = []
if 'page' not in st.session_state: st.session_state.page = 'main'

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    st.markdown('<div style="text-align:right;"><div style="color:#003366; font-weight:900; font-size:1.8rem;">منصة معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)

    if df is not None:
        # شريط المقارنة
        if st.session_state.compare_list:
            c_top1, c_top2 = st.columns([4, 1])
            with c_top1: st.info(f"📋 المطورين المختارين: {', '.join(st.session_state.compare_list)}")
            with c_top2:
                if st.button("📊 ابدأ المقارنة"):
                    st.session_state.page = 'compare'
                    st.rerun()

        # الفلتر
        s_dev = st.text_input("🔍 ابحث عن مطور...")
        
        f_df = df.copy()
        if s_dev: f_df = f_df[f_df['Developer'].astype(str).str.contains(s_dev, case=False, na=False)]

        for i, row in f_df.iterrows():
            st.markdown('<div class="project-card-container">', unsafe_allow_html=True)
            col_content, col_img = st.columns([4, 1])
            with col_content:
                txt_c, btn_c = st.columns([3, 1])
                with txt_c:
                    st.markdown(f"""
                        <div style="text-align: right; padding: 15px;">
                            <div style="color: #003366; font-weight: 900; font-size: 1.3rem;">{row.get('Developer')}</div>
                            <div style="color: #64748b; font-size: 0.85rem;">📍 {row.get('Area')} | {row.get('Price')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with btn_c:
                    st.write("")
                    dev_name = str(row['Developer'])
                    is_in = dev_name in st.session_state.compare_list
                    if st.button("➕ مقارنة" if not is_in else "❌ إزالة", key=f"comp_{i}"):
                        if not is_in: st.session_state.compare_list.append(dev_name)
                        else: st.session_state.compare_list.remove(dev_name)
                        st.rerun()
            with col_img:
                img_url = row.get('Image_URL', 'https://via.placeholder.com/400')
                st.markdown(f'<div style="height: 100px; background-image: url(\'{img_url}\'); background-size: cover; background-position: center;"></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة المقارنة ---
elif st.session_state.page == 'compare':
    st.markdown("<h2 style='text-align:center; color:#003366;'>📊 لوحة المقارنة</h2>", unsafe_allow_html=True)
    if st.button("⬅️ عودة"):
        st.session_state.page = 'main'; st.rerun()
    
    compare_df = df[df['Developer'].isin(st.session_state.compare_list)]
    
    # توزيع المطورين في أعمدة
    cols = st.columns(len(compare_df) if len(compare_df) > 0 else 1)
    
    for idx, (i, row) in enumerate(compare_df.iterrows()):
        with cols[idx]:
            st.markdown(f"""
                <div class="comp-card">
                    <div class="comp-header">{row.get('Developer')}</div>
                    <div class="comp-price">{row.get('Price')}</div>
                    <span class="comp-label">📍 المنطقة</span>
                    <span class="comp-value">{row.get('Area')}</span>
                    <span class="comp-label">⏳ سنوات القسط</span>
                    <span class="comp-value">{row.get('Installments', '-')} سنوات</span>
                    <span class="comp-label">🏢 المالك</span>
                    <span class="comp-value">{row.get('Owner', '-')}</span>
                </div>
            """, unsafe_allow_html=True)
