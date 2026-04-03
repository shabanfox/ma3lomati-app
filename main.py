import streamlit as st
import pandas as pd
import requests
import feedparser
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. روابط الصور ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 3. جلب البيانات ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    try:
        p, d = pd.read_csv(U_P), pd.read_csv(U_D)
        for df in [p, d]: 
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# --- 4. التصميم الجمالي (تناسق الكروت 100%) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header {{ visibility: hidden; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.97), rgba(0,0,0,0.97)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}

    /* تصميم الكرت المتناسق */
    div.stButton > button[key*="card_"] {{
        background-color: #ffffff !important; 
        color: #111111 !important;
        border-right: 12px solid #f59e0b !important;
        border-left: 1px solid #ddd !important;
        border-top: 1px solid #ddd !important;
        border-bottom: 1px solid #ddd !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4) !important;
        
        /* التناسق الإجباري */
        width: 100% !important;
        min-height: 180px !important; 
        max-height: 180px !important;
        overflow: hidden !important;
        
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: flex-start !important;
        transition: all 0.3s ease !important;
    }}
    
    div.stButton > button[key*="card_"]:hover {{
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 35px rgba(245,158,11,0.3) !important;
        background-color: #fffdf9 !important;
    }}

    /* الخطوط داخل الكرت */
    .card-title {{ font-size: 20px; font-weight: 900; color: #000; margin-bottom: 5px; }}
    .card-sub {{ font-size: 15px; color: #555; font-weight: 700; }}

    /* ستايل التيكر والهيدر */
    .ticker-bar {{ background: #f59e0b; color: black; padding: 10px; font-weight: 900; text-align: center; border-radius: 0 0 20px 20px; }}
    .detail-card {{ background: rgba(255,255,255,0.05); border-top: 5px solid #f59e0b; padding: 20px; border-radius: 15px; color: white; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. إدارة الدخول ---
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    c1, c2, c3 = st.columns([1,1.2,1])
    with c2:
        st.markdown("<div style='background:white; padding:40px; border-radius:25px; text-align:center; margin-top:100px;'><h2 style='color:black;'>MA3LOMATI PRO</h2>", unsafe_allow_html=True)
        pwd = st.text_input("كلمة السر", type="password")
        if st.button("دخول آمن", use_container_width=True):
            if pwd == "2026": st.session_state.auth = True; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. القائمة العلوية ---
st.markdown('<div class="ticker-bar">🚀 سوق العقارات 2026 | تحديثات مباشرة للمشاريع والأسعار كل ساعة</div>', unsafe_allow_html=True)
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["tools", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"}})

col_main, col_side = st.columns([0.8, 0.2])

# --- 7. قسم أدوات البروكر (9 أدوات) ---
if menu == "أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات المساعدة (9)</h2>", unsafe_allow_html=True)
    a, b, c = st.columns(3)
    tools = [
        ("حاسبة القسط", "السعر", "السنين"), ("العمولة", "المبلغ", "النسبة %"), ("ROI الاستثمار", "الشراء", "الإيجار"),
        ("خصم الكاش", "السعر", "الخصم %"), ("نسبة التحميل", "الصافي", "الإجمالي"), ("سعر المتر", "الإجمالي", "المساحة"),
        ("التمويل العقاري", "القرض", "الفائدة"), ("الضريبة العقارية", "التقييم", "المعدل"), ("زيادة القسط", "القسط", "الزيادة %")
    ]
    for i, (name, l1, l2) in enumerate(tools):
        target_col = [a, b, c][i % 3]
        with target_col:
            with st.container(border=True):
                st.subheader(name)
                n1 = st.number_input(l1, value=1000, key=f"n1_{i}")
                n2 = st.number_input(l2, value=10, key=f"n2_{i}")
                st.info(f"النتيجة التقريبية: {n1+(n1*(n2/100)):,.0f}")

# --- 8. قسم المشاريع (الكروت المتناسقة) ---
elif menu == "المشاريع":
    with col_main:
        if st.session_state.get('view') == "details":
            if st.button("⬅️ عودة للقائمة"): st.session_state.view = "grid"; st.rerun()
            item = df_p.iloc[st.session_state.current_index]
            for k, v in item.items():
                st.markdown(f'<div class="detail-card"><b style="color:#f59e0b">{k}:</b> {v}</div>', unsafe_allow_html=True)
        else:
            search = st.text_input("🔍 ابحث عن مشروعك...", placeholder="اكتب اسم المشروع هنا")
            filt = df_p[df_p.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else df_p
            
            grid = st.columns(2)
            for i, (idx, r) in enumerate(filt.head(10).iterrows()):
                with grid[i%2]:
                    # تصميم النص داخل الكرت لضمان التناسق
                    card_content = f"""
                    <div style='text-align:right;'>
                        <div class='card-title'>🏢 {r.iloc[0][:30]}</div>
                        <div class='card-sub'>📍 {r.get('Location', 'غير محدد')}</div>
                        <div class='card-sub'>🏗️ {r.get('Developer', '---')}</div>
                    </div>
                    """
                    if st.button(card_content, key=f"card_{idx}", help="اضغط للتفاصيل"):
                        st.session_state.current_index = idx
                        st.session_state.view = "details"; st.rerun()

# --- 9. المساعد الذكي ---
elif menu == "المساعد الذكي":
    with col_main:
        st.markdown("<div class='detail-card'><h3>🤖 مساعد معلوماتي الذكي</h3></div>", unsafe_allow_html=True)
        if pmt := st.chat_input("اسألني عن أي مشروع..."):
            res = df_p[df_p.apply(lambda r: r.astype(str).str.contains(pmt, case=False).any(), axis=1)]
            if not res.empty: st.write(res.iloc[0].to_dict())
            else: st.warning("لم أجد نتائج، جرب كلمة أخرى.")

# --- 10. المقترحات الجانبية ---
with col_side:
    st.markdown("<h4 style='color:#f59e0b;'>⭐ مقترحات</h4>", unsafe_allow_html=True)
    for _, r in df_p.head(8).iterrows():
        st.markdown(f"""
            <div style='background:white; color:black; padding:10px; border-radius:10px; 
            margin-bottom:8px; border-right:5px solid #f59e0b; font-weight:bold; font-size:14px;'>
                {r.iloc[0][:25]}
            </div>
        """, unsafe_allow_html=True)
