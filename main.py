import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) المطور
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f8fafc; 
    }

    /* كارت البحث المطور */
    .search-section {
        background: linear-gradient(135deg, #003366 0%, #001a33 100%);
        padding: 40px;
        border-radius: 20px;
        margin-bottom: 30px;
        color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }

    /* الكارت الشبكي المربع */
    .grid-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 10px;
        border-bottom: 4px solid #D4AF37;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.3s ease;
    }
    .grid-card:hover { 
        transform: translateY(-8px);
        border-bottom: 4px solid #003366;
    }

    /* تنسيق الأزرار */
    div.stButton > button {
        background-color: #f1f5f9 !important; color: #003366 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important; font-size: 0.85rem !important;
        font-weight: bold !important; width: 100%; height: 38px;
        font-family: 'Cairo', sans-serif;
    }
    div.stButton > button:hover {
        background-color: #003366 !important; color: white !important;
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

# إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'compare_list' not in st.session_state: st.session_state.compare_list = []

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    # الهيدر الملكي
    st.markdown("""
        <div class="search-section">
            <h1 style="text-align: center; margin:0; font-size: 2.5rem;">منصة معلوماتى <span style="color:#D4AF37;">العقارية</span></h1>
            <p style="text-align: center; opacity: 0.8;">ابحث عن "الزتونة" في أكثر من 100 مطور عقاري</p>
        </div>
    """, unsafe_allow_html=True)

    if df is not None:
        # شريط البحث الذكي
        search_query = st.text_input("🔍 البحث الذكي (اكتب اسم المطور، المنطقة، أو حتى ميزة مثل 'لاجون')", placeholder="ابحث هنا...")

        # منطق الفلترة المطور (Search Engine)
        if search_query:
            filtered_df = df[
                df['Developer'].astype(str).str.contains(search_query, case=False, na=False) |
                df['Area'].astype(str).str.contains(search_query, case=False, na=False) |
                df.get('Detailed_Info', '').astype(str).str.contains(search_query, case=False, na=False)
            ]
        else:
            filtered_df = df

        # عرض النتائج بنظام الشبكة (3 أعمدة)
        st.markdown(f"<h5>إجمالي النتائج: {len(filtered_df)}</h5>", unsafe_allow_html=True)
        
        # إنشاء الصفوف
        cols = st.columns(3)
        for idx, (i, row) in enumerate(filtered_df.reset_index().iterrows()):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="grid-card">
                        <div style="color: #003366; font-weight: 900; font-size: 1.15rem;">{row.get('Developer')}</div>
                        <div style="color: #64748b; font-size: 0.85rem; margin-top:5px;">📍 {row.get('Area')}</div>
                        <div style="color: #003366; font-weight: bold; font-size: 0.9rem; margin-top:10px;">💵 {row.get('Price')}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # أزرار الأكشن
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("👁️ تفاصيل", key=f"det_{i}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'; st.rerun()
                with btn_col2:
                    name = str(row['Developer'])
                    is_in = name in st.session_state.compare_list
                    if st.button("➕ مقارنة" if not is_in else "❌ إزالة", key=f"comp_{i}"):
                        if not is_in: st.session_state.compare_list.append(name)
                        else: st.session_state.compare_list.remove(name)
                        st.rerun()
                st.markdown("<div style='margin-bottom:25px;'></div>", unsafe_allow_html=True)

# --- صفحة التفاصيل (بالتنسيق الملكي) ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 عودة"): st.session_state.page = 'main'; st.rerun()
    
    st.markdown(f"""
        <div style="background-color: #003366; padding: 30px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;">
            <h1 style="margin:0;">{item.get('Developer')}</h1>
            <p style="opacity:0.8;">{item.get('Area')}</p>
        </div>
        <div style="background: white; padding: 25px; border-radius: 15px; border-right: 8px solid #D4AF37; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
            <h3 style="color:#003366;">💡 الزتونة الفنية</h3>
            <p style="font-size:1.15rem; line-height:1.8; color:#1e293b;">{item.get('Detailed_Info', 'لا توجد بيانات تفصيلية.')}</p>
            <hr style="border:0; border-top: 1px solid #eee; margin:20px 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <p><b>👤 المالك:</b> {item.get('Owner', '-')}</p>
                <p><b>💰 السعر:</b> {item.get('Price', '-')}</p>
                <p><b>⏳ التقسيط:</b> {item.get('Installments', '-')}</p>
                <p><b>🕒 الاستلام:</b> {item.get('Delivery', '-')}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
