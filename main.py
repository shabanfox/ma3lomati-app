import streamlit as st
import pandas as pd
import requests
import feedparser
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الروابط ---
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

# --- 4. CSS الاحترافي (لضبط تناسق الكروت والأدوات) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* الخلفية والخط العام */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.98), rgba(0,0,0,0.98)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}

    /* تصميم الكرت (ارتفاع ثابت وتنسيق موحد) */
    div.stButton > button[key*="card_"] {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-right: 12px solid #f59e0b !important;
        border-radius: 15px !important;
        padding: 20px !important;
        height: 180px !important; /* ارتفاع ثابت لضمان التناسق */
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        align-items: flex-start !important;
        text-align: right !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5) !important;
        border: none !important;
        margin-bottom: 20px !important;
    }}
    
    div.stButton > button[key*="card_"]:hover {{
        transform: translateY(-5px) !important;
        background-color: #fcfcfc !important;
        box-shadow: 0 15px 30px rgba(245,158,11,0.2) !important;
    }}

    /* نصوص الكرت */
    .card-title {{ font-size: 22px; font-weight: 900; color: #111; margin-bottom: 8px; line-height: 1.2; }}
    .card-info {{ font-size: 16px; color: #444; font-weight: 700; }}

    /* الأدوات المساعدة */
    .stNumberInput label {{ color: #f59e0b !important; font-weight: 900 !important; }}
    .tool-card {{ background: #111; padding: 15px; border-radius: 15px; border: 1px solid #333; }}

    /* الهيدر وشريط الأخبار */
    .ticker-bar {{ background: #f59e0b; color: #000; padding: 10px; font-weight: 900; text-align: center; border-radius: 0 0 20px 20px; font-size: 18px; }}
    header {{ visibility: hidden; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. منطق الدخول ---
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    _, center, _ = st.columns([1,1.2,1])
    with center:
        st.markdown("<div style='background:white; padding:50px; border-radius:30px; text-align:center; margin-top:100px;'><h2 style='color:black;'>MA3LOMATI PRO</h2>", unsafe_allow_html=True)
        pwd = st.text_input("كلمة السر", type="password")
        if st.button("دخول", use_container_width=True):
            if pwd == "2026": st.session_state.auth = True; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. القائمة والهيدر ---
st.markdown('<div class="ticker-bar">🔥 تحديثات فورية: إطلاق مشاريع جديدة في العاصمة والشيخ زايد | أسعار 2026</div>', unsafe_allow_html=True)
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["calculator", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"}})

col_main, col_side = st.columns([0.75, 0.25])

# --- 7. قسم أدوات البروكر (9 أدوات منظمة) ---
if menu == "أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ الأدوات الحسابية (9 أدوات)</h2>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    
    with t1:
        with st.container(border=True):
            st.subheader("1. حاسبة القسط")
            p1 = st.number_input("إجمالي المبلغ", 1000000, key="t1_1")
            y1 = st.number_input("عدد السنين", 8, key="t1_2")
            st.success(f"القسط الشهري: {p1/(y1*12):,.0f}")
        with st.container(border=True):
            st.subheader("4. خصم الكاش")
            p4 = st.number_input("السعر الأصلي", 2000000, key="t4_1")
            d4 = st.slider("نسبة الخصم %", 0, 45, 20, key="t4_2")
            st.warning(f"السعر بعد الخصم: {p4*(1-d4/100):,.0f}")
        with st.container(border=True):
            st.subheader("7. مساحة التحميل")
            net = st.number_input("الصافي", 120, key="t7_1")
            gross = st.number_input("الإجمالي", 160, key="t7_2")
            st.info(f"نسبة التحميل: {((gross-net)/gross)*100:.1f}%")

    with t2:
        with st.container(border=True):
            st.subheader("2. حساب العمولة")
            p2 = st.number_input("قيمة الصفقة", 5000000, key="t2_1")
            c2 = st.slider("النسبة %", 1.0, 10.0, 2.5, key="t2_2")
            st.success(f"عمولتك: {p2*(c2/100):,.0f}")
        with st.container(border=True):
            st.subheader("5. سعر المتر")
            p5 = st.number_input("إجمالي السعر", 3500000, key="t5_1")
            m5 = st.number_input("المساحة م2", 150, key="t5_2")
            st.warning(f"سعر المتر: {p5/m5:,.0f}")
        with st.container(border=True):
            st.subheader("8. الضريبة العقارية")
            p8 = st.number_input("قيمة الوحدة", 2000000, key="t8_1")
            st.info(f"الضريبة التقريبية: {p8*0.001:,.0f}")

    with t3:
        with st.container(border=True):
            st.subheader("3. عائد الاستثمار ROI")
            p3 = st.number_input("سعر الشراء", 3000000, key="t3_1")
            r3 = st.number_input("الإيجار السنوي", 300000, key="t3_2")
            st.success(f"العائد السنوي: {(r3/p3)*100:.1f}%")
        with st.container(border=True):
            st.subheader("6. التمويل العقاري")
            p6 = st.number_input("مبلغ القرض", 1000000, key="t6_1")
            i6 = st.slider("الفائدة %", 5, 25, 12, key="t6_2")
            st.warning(f"الفائدة السنوية: {p6*(i6/100):,.0f}")
        with st.container(border=True):
            st.subheader("9. زيادة القسط 5%")
            p9 = st.number_input("قسط البداية", 10000, key="t9_1")
            st.info(f"القسط بعد 5 سنين: {p9*(1.05**5):,.0f}")

# --- 8. قسم المشاريع (الكروت المتناسقة) ---
elif menu == "المشاريع":
    with col_main:
        if st.session_state.get('view') == "details":
            if st.button("⬅️ عودة للقائمة"): st.session_state.view = "grid"; st.rerun()
            item = df_p.iloc[st.session_state.current_index]
            for k, v in item.items():
                st.markdown(f'<div style="background:#222; padding:15px; border-right:5px solid #f59e0b; margin-bottom:10px; border-radius:10px;"><b style="color:#f59e0b">{k}:</b> <span style="color:white; font-size:18px;">{v}</span></div>', unsafe_allow_html=True)
        else:
            search = st.text_input("🔍 ابحث عن أي مشروع أو مطور أو منطقة...", placeholder="اكتب هنا...")
            filt = df_p[df_p.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else df_p
            
            grid = st.columns(2)
            for i, (idx, r) in enumerate(filt.head(10).iterrows()):
                with grid[i%2]:
                    # الكرت بتصميم ثابت 100%
                    card_html = f"""
                    <div class='card-title'>🏢 {str(r.iloc[0])[:35]}</div>
                    <div class='card-info'>📍 {str(r.get('Location', '---'))[:30]}</div>
                    <div class='card-info'>🏗️ {str(r.get('Developer', '---'))[:30]}</div>
                    """
                    if st.button(card_html, key=f"card_{idx}"):
                        st.session_state.current_index = idx
                        st.session_state.view = "details"; st.rerun()

# --- 9. المقترحات الجانبية ---
with col_side:
    st.markdown("<h3 style='color:#f59e0b; text-align:center;'>⭐ مقترحات تهمك</h3>", unsafe_allow_html=True)
    for _, r in df_p.head(10).iterrows():
        st.markdown(f"""
            <div style='background:white; color:black; padding:12px; border-radius:12px; 
            margin-bottom:10px; border-right:8px solid #f59e0b; font-weight:900; font-size:15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);'>
                {str(r.iloc[0])[:25]}
            </div>
        """, unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026 | خبيرك العقاري</p>", unsafe_allow_html=True)
