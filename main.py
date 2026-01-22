import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Luxury CSS (إجبار التنسيق على شكل كروت) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الهيدر الافتراضي */
    header, [data-testid="stHeader"] { visibility: hidden; height: 0px; }
    
    body, [data-testid="stAppViewContainer"] {
        background-color: #0e1117;
        direction: rtl;
        font-family: 'Cairo', sans-serif;
    }

    /* تنسيق الكارت */
    .dev-card-ui {
        background: #1d2129;
        border: 1px solid #383e4b;
        border-right: 5px solid #f59e0b;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 10px;
        transition: 0.3s ease;
    }
    .dev-card-ui:hover {
        border-color: #f59e0b;
        background: #252a34;
        transform: translateY(-2px);
    }
    .card-title { color: #f59e0b; font-size: 20px; font-weight: 900; margin-bottom: 5px; }
    .card-subtitle { color: #888; font-size: 14px; }

    /* تنسيق صفحة التفاصيل */
    .detail-box {
        background: #161b22;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #30363d;
    }
    .section-header {
        color: #f59e0b;
        font-size: 1.3rem;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 10px;
        border-bottom: 1px solid #333;
        padding-bottom: 5px;
    }
    .section-content {
        color: #ffffff;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. Data Loading ---
@st.cache_data(ttl=10)
def load_dev_data():
    # الرابط اللي بعته للمطورين
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    try:
        df = pd.read_csv(url).fillna("---")
        df.columns = [c.strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['Developer', 'Owner / Chairman', 'Company Details', 'Key Projects'])

df_d = load_dev_data()

# --- 4. Session State ---
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'selected_idx' not in st.session_state: st.session_state.selected_idx = 0

# --- 5. Navigation ---
st.markdown("<h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
menu = option_menu(None, ["الأدوات", "المطورين", "المشاريع", "اللونشات"], 
    icons=['tools', 'building', 'house', 'rocket'], 
    default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- 6. Logic ---

if menu == "المطورين":
    if st.session_state.view == "details":
        # --- صفحة التفاصيل ---
        item = df_d.iloc[st.session_state.selected_idx]
        if st.button("⬅ عودة للقائمة"):
            st.session_state.view = "grid"
            st.rerun()
        
        st.markdown(f"""
        <div class="detail-box">
            <h1 style="color:#f59e0b; border-bottom: 2px solid #f59e0b; padding-bottom:10px;">{item['Developer']}</h1>
            
            <div class="section-header">👤 المالك / رئيس مجلس الإدارة</div>
            <div class="section-content">{item['Owner / Chairman']}</div>
            
            <div class="section-header">🏢 عن الشركة</div>
            <div class="section-content">{item['Company Details']}</div>
            
            <div class="section-header">🏗️ أهم المشاريع</div>
            <div class="section-content">{item['Key Projects']}</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # --- صفحة الكروت (الشبكة) ---
        search = st.text_input("🔍 ابحث عن مطور...")
        filtered_df = df_d[df_d['Developer'].str.contains(search, case=False)] if search else df_d
        
        # توزيع الكروت في صفين
        col1, col2 = st.columns(2)
        for i, (idx, row) in enumerate(filtered_df.iterrows()):
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                # عرض تصميم الكارت
                st.markdown(f"""
                <div class="dev-card-ui">
                    <div class="card-title">{row['Developer']}</div>
                    <div class="card-subtitle">📍 {str(row['Owner / Chairman'])[:40]}...</div>
                </div>
                """, unsafe_allow_html=True)
                
                # زرار خفي فوق الكارت عشان يفتحه
                if st.button(f"تفاصيل {row['Developer']}", key=f"btn_{idx}"):
                    st.session_state.selected_idx = idx
                    st.session_state.view = "details"
                    st.rerun()
else:
    st.info("القسم قيد التجهيز.. اختر 'المطورين' لتجربة الكروت الجديدة.")
