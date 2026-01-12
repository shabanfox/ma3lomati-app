import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO - النسخة المدمجة", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 15px; border-radius: 0 0 15px 15px; border-right: 12px solid #f59e0b; text-align: center; margin-bottom: 25px; }
    .header-title { font-weight: 900; font-size: 30px !important; color: #f59e0b; margin: 0; }
    .pro-card { background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 20px; text-align: center; height: 100%; min-height: 220px; }
    .detail-box { background: #0d0d0d; border-right: 6px solid #f59e0b; border-radius: 12px; padding: 25px; color: #eee; border: 1px solid #222; }
    .card-title { color: #f59e0b; font-size: 19px !important; font-weight: 900; }
    .stButton button { background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; border-radius: 8px; font-weight: bold; width: 100%; }
    .tool-container { background: #111; border-radius: 15px; padding: 20px; border: 1px solid #222; }
    </style>
""", unsafe_allow_html=True)

# 3. وظيفة دمج الروابط
@st.cache_data(ttl=60)
def load_combined_data():
    urls = [
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    ]
    all_dfs = []
    for url in urls:
        try:
            temp_df = pd.read_csv(url)
            temp_df.columns = [str(c).strip() for c in temp_df.columns]
            all_dfs.append(temp_df)
        except: continue
    
    if not all_dfs: return pd.DataFrame()
    
    combined = pd.concat(all_dfs, ignore_index=True)
    # حذف التكرار بناءً على اسم المشروع والمطور
    combined = combined.drop_duplicates(subset=['Project Name', 'Developer'], keep='first')
    return combined.fillna("غير متوفر").astype(str)

df = load_combined_data()

# 4. الحالة
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'active_proj' not in st.session_state: st.session_state.active_proj = None

# الهيدر
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية PRO</h1></div>', unsafe_allow_html=True)

selected = option_menu(None, ["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
                       icons=["tools", "building", "person-badge"], orientation="horizontal",
                       styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}})

# --- 🏗️ قسم المشاريع المدمج ---
if selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b;'>🏗️ قاعدة بيانات المشاريع (الرابطين)</h2>", unsafe_allow_html=True)
    
    search_p = st.text_input("🔍 ابحث في مئات المشاريع بالاسم، المطور، أو المنطقة...")
    dff = df.copy()
    if search_q := search_p:
        dff = dff[dff.apply(lambda row: search_q.lower() in row.astype(str).str.lower().values, axis=1)]

    items_per_page = 9
    total_pages = max(1, math.ceil(len(dff) / items_per_page))
    start_idx = st.session_state.p_page * items_per_page
    curr_p = dff.iloc[start_idx : start_idx + items_per_page].reset_index()

    for i in range(0, len(curr_p), 3):
        row_indices = curr_p['index'].iloc[i:i+3].tolist()
        if st.session_state.active_proj in row_indices:
            p_data = df.loc[st.session_state.active_proj]
            st.markdown("---")
            c1, c2 = st.columns([0.3, 0.7])
            with c1:
                st.markdown(f"<div class='pro-card'><div class='card-title'>{p_data['Project Name']}</div><p>{p_data['Developer']}</p></div>", unsafe_allow_html=True)
                if st.button("⬅️ إغلاق", key=f"cls_{p_data.name}"): st.session_state.active_proj = None; st.rerun()
            with c2:
                st.markdown(f"""<div class='detail-box'>
                    <h3 style='color:#f59e0b;'>🏗️ {p_data['Project Name']}</h3>
                    <p><b>📍 المنطقة:</b> {p_data.get('Area')} | <b>📏 المساحة:</b> {p_data.get('Size (Acres)')} فدان</p>
                    <p><b>👷 الاستشاري:</b> {p_data.get('Consultant')}</p>
                    <p><b>⭐ الميزة التنافسية:</b> {p_data.get('Competitive Advantage')}</p>
                    <hr style='border: 0.5px solid #222'>
                    <p><b>👤 المالك:</b> {p_data.get('Owner')}</p>
                    <p><b>📜 عن المطور:</b> {p_data.get('Detailed_Info')}</p>
                </div>""", unsafe_allow_html=True)
            st.markdown("---")
        else:
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(curr_p):
                    item = curr_p.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='pro-card'><div class='card-title'>{item['Project Name']}</div><p style='color:#888;'>{item['Developer']}</p><p style='font-size:12px; color:#f59e0b;'>📍 {item['Area']}</p></div>", unsafe_allow_html=True)
                        if st.button("🔍 عرض التفاصيل", key=f"btn_{item['index']}"):
                            st.session_state.active_proj = item['index']; st.rerun()

    # أزرار التنقل
    st.write("---")
    n1, n2, n3 = st.columns([1, 2, 1])
    if n3.button("التالي ⬅️") and st.session_state.p_page < total_pages-1: st.session_state.p_page += 1; st.rerun()
    n2.markdown(f"<center>صفحة {st.session_state.p_page+1} من {total_pages}</center>", unsafe_allow_html=True)
    if n1.button("➡️ السابق") and st.session_state.p_page > 0: st.session_state.p_page -= 1; st.rerun()

# --- 🛠️ قسم الأدوات (شامل) ---
elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b;'>🛠️ الأدوات الذكية</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns([0.4, 0.6])
    with c1:
        st.markdown("<div class='tool-container'>", unsafe_allow_html=True)
        st.markdown("### 💰 حاسبة القسط")
        price = st.number_input("سعر الوحدة", value=5000000)
        years = st.slider("سنوات التقسيط", 1, 15, 8)
        st.markdown(f"<h2 style='color:#f59e0b;'>{price/(years*12):,.0f} <small>ج.م/شهري</small></h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='tool-container'>", unsafe_allow_html=True)
        st.markdown("### 📝 مفكرة متابعة العملاء")
        st.text_area("سجل هنا ملاحظاتك...", height=200)
        st.markdown("</div>", unsafe_allow_html=True)

# باقي الأقسام (المطورين) تعمل بنفس المنطق المدمج...
