import streamlit as st
import pandas as pd
import requests
import feedparser
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. روابط الداتا والصور ---
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
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# --- 4. الـ CSS الاحترافي (ضبط الكروت والتقسيمة) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.98), rgba(0,0,0,0.98)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}

    /* كرت المشروع: أبيض، مسطرة، وكلام أسود عريض */
    div.stButton > button[key*="card_"] {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-right: 15px solid #f59e0b !important;
        border-radius: 20px !important;
        padding: 25px !important;
        height: 200px !important; /* ارتفاع ثابت لضمان التناسق */
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        text-align: right !important;
        box-shadow: 0 12px 25px rgba(0,0,0,0.6) !important;
        border: none !important;
        margin-bottom: 25px !important;
    }}
    
    div.stButton > button[key*="card_"]:hover {{
        transform: translateY(-8px) !important;
        box-shadow: 0 20px 40px rgba(245,158,11,0.25) !important;
    }}

    .card-title {{ font-size: 24px; font-weight: 900; color: #111; margin-bottom: 10px; line-height: 1.2; }}
    .card-info {{ font-size: 17px; color: #444; font-weight: 700; }}

    /* شريط الأخبار والهيدر */
    .ticker-bar {{ background: #f59e0b; color: #000; padding: 12px; font-weight: 900; text-align: center; border-radius: 0 0 25px 25px; font-size: 20px; }}
    header {{ visibility: hidden; }}
    
    /* ستايل الأدوات الحسابية */
    .stNumberInput label {{ color: #f59e0b !important; font-weight: 900 !important; font-size: 16px !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. منطق الدخول ---
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    _, center, _ = st.columns([1,1.5,1])
    with center:
        st.markdown("<div style='background:white; padding:50px; border-radius:35px; text-align:center; margin-top:80px;'><h1 style='color:black;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
        pwd = st.text_input("كلمة السر الخاصة بك", type="password")
        if st.button("دخول المنصة 🚀", use_container_width=True):
            if pwd == "2026": st.session_state.auth = True; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. القائمة والهيدر ---
st.markdown('<div class="ticker-bar">🏆 MA3LOMATI PRO 2026 | خبيرك العقاري الأول في مصر</div>', unsafe_allow_html=True)
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["calculator", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"}})

col_main, col_side = st.columns([0.75, 0.25])

# --- 7. قسم أدوات البروكر (9 أدوات منظمة 3x3) ---
if menu == "أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center; margin-bottom:30px;'>🛠️ ترسانة الأدوات العقارية (9)</h2>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    
    with t1:
        with st.container(border=True):
            st.subheader("1️⃣ حاسبة القسط")
            v1 = st.number_input("إجمالي المبلغ", 1000000, key="v1")
            y1 = st.number_input("عدد السنين", 8, key="y1")
            st.info(f"القسط الشهري: {v1/(y1*12):,.0f}")
        with st.container(border=True):
            st.subheader("4️⃣ العائد السنوي ROI")
            v4 = st.number_input("سعر الوحدة", 3000000, key="v4")
            r4 = st.number_input("الإيجار السنوي", 300000, key="r4")
            st.warning(f"نسبة العائد: {(r4/v4)*100:.1f}%")
        with st.container(border=True):
            st.subheader("7️⃣ مساحة التحميل")
            net = st.number_input("المساحة الصافية", 100, key="net")
            gross = st.number_input("المساحة الإجمالية", 135, key="gross")
            st.info(f"نسبة التحميل: {((gross-net)/gross)*100:.1f}%")

    with t2:
        with st.container(border=True):
            st.subheader("2️⃣ حساب العمولة")
            v2 = st.number_input("قيمة الصفقة", 5000000, key="v2")
            c2 = st.slider("النسبة %", 1.0, 10.0, 2.5, key="c2")
            st.info(f"عمولتك الصافية: {v2*(c2/100):,.0f}")
        with st.container(border=True):
            st.subheader("5️⃣ سعر المتر")
            v5 = st.number_input("إجمالي السعر", 4000000, key="v5")
            m5 = st.number_input("المساحة م2", 160, key="m5")
            st.warning(f"سعر المتر: {v5/m5:,.0f}")
        with st.container(border=True):
            st.subheader("8️⃣ التمويل العقاري")
            v8 = st.number_input("قيمة القرض", 1000000, key="v8")
            i8 = st.slider("الفائدة %", 5, 25, 11, key="i8")
            st.info(f"الفائدة السنوية: {v8*(i8/100):,.0f}")

    with t3:
        with st.container(border=True):
            st.subheader("3️⃣ خصم الكاش")
            v3 = st.number_input("السعر قبل الخصم", 2500000, key="v3")
            d3 = st.slider("نسبة الخصم %", 0, 50, 25, key="d3")
            st.info(f"السعر بعد الخصم: {v3*(1-d3/100):,.0f}")
        with st.container(border=True):
            st.subheader("6️⃣ الضريبة العقارية")
            v6 = st.number_input("التقييم السوقي", 2000000, key="v6")
            st.warning(f"الضريبة التقريبية: {v6*0.001:,.0f}")
        with st.container(border=True):
            st.subheader("9️⃣ زيادة القسط")
            v9 = st.number_input("القسط الحالي", 15000, key="v9")
            st.info(f"بعد زيادة 5% سنوياً (5 سنين): {v9*(1.05**5):,.0f}")

# --- 8. قسم المشاريع (كروت مسطرة بالملي) ---
elif menu == "المشاريع":
    with col_main:
        if st.session_state.get('view') == "details":
            if st.button("⬅️ العودة للقائمة"): st.session_state.view = "grid"; st.rerun()
            item = df_p.iloc[st.session_state.current_index]
            for k, v in item.items():
                st.markdown(f"<div style='background:#111; padding:15px; border-right:6px solid #f59e0b; margin-bottom:10px; border-radius:12px;'><b style='color:#f59e0b'>{k}:</b> <span style='color:white; font-size:18px;'>{v}</span></div>", unsafe_allow_html=True)
        else:
            search = st.text_input("🔍 ابحث عن أي شيء (مشروع، منطقة، مطور)...", placeholder="اكتب هنا للبحث الفوري")
            filt = df_p[df_p.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else df_p
            
            grid = st.columns(2)
            for i, (idx, r) in enumerate(filt.head(10).iterrows()):
                with grid[i%2]:
                    # تصميم الكرت الثابت
                    card_html = f"""
                    <div class='card-title'>🏢 {str(r.iloc[0])[:35]}</div>
                    <div class='card-info'>📍 الموقع: {str(r.get('Location', '---'))[:30]}</div>
                    <div class='card-info'>🏗️ المطور: {str(r.get('Developer', '---'))[:30]}</div>
                    """
                    if st.button(card_html, key=f"card_{idx}"):
                        st.session_state.current_index = idx
                        st.session_state.view = "details"; st.rerun()

# --- 9. المساعد الذكي ---
elif menu == "المساعد الذكي":
    with col_main:
        st.markdown("<div style='background:rgba(255,255,255,0.05); padding:25px; border-radius:20px; border:1px solid #333;'><h3>🤖 مساعدك العقاري الذكي</h3><p>اسألني عن أي مشروع وسأقوم بتحليل البيانات لك فوراً.</p></div>", unsafe_allow_html=True)
        if prompt := st.chat_input("عايز تفاصيل عن مشروع..."):
            res = df_p[df_p.apply(lambda r: r.astype(str).str.contains(prompt, case=False).any(), axis=1)]
            if not res.empty: st.write(res.iloc[0].to_dict())
            else: st.warning("لم أجد هذا المشروع، حاول كتابة الاسم بدقة.")

# --- 10. المقترحات الجانبية (ثابتة في كل الصفحات) ---
with col_side:
    st.markdown("<h3 style='color:#f59e0b; text-align:center;'>⭐ مقترحات PRO</h3>", unsafe_allow_html=True)
    for _, r in df_p.head(12).iterrows():
        st.markdown(f"""
            <div style='background:white; color:black; padding:15px; border-radius:15px; 
            margin-bottom:12px; border-right:10px solid #f59e0b; font-weight:900; font-size:16px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.4);'>
                {str(r.iloc[0])[:25]}
            </div>
        """, unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026 | جميع الحقوق محفوظة</p>", unsafe_allow_html=True)
