import streamlit as st
import pandas as pd
import requests
import feedparser
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الروابط ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 4. جلب البيانات ---
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

# --- 5. التصميم الجمالي المطور (Focus on Contrast) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header {{ visibility: hidden; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}

    /* شريط الأخبار الـ PRO */
    .ticker-bar {{ background: #f59e0b; color: black; padding: 12px; font-weight: 900; font-size: 18px; text-align: center; border-radius: 0 0 20px 20px; margin-bottom: 25px; }}

    /* كروت المشاريع (تطوير شامل) */
    div.stButton > button[key*="card_"] {{
        background-color: #ffffff !important; 
        color: #000000 !important;
        border-right: 15px solid #f59e0b !important;
        padding: 25px !important;
        font-size: 20px !important; 
        font-weight: 900 !important; 
        text-align: right !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        width: 100% !important;
        min-height: 160px !important;
        margin-bottom: 20px !important;
        line-height: 1.6 !important;
    }}
    div.stButton > button[key*="card_"]:hover {{ transform: scale(1.02); background-color: #f8f9fa !important; }}

    /* تفاصيل البيانات */
    .detail-card {{ background: rgba(255,255,255,0.05); border: 1px solid #444; padding: 25px; border-radius: 20px; margin-bottom: 15px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 16px; }}
    .val-white {{ color: white; font-size: 22px; font-weight: 700; }}
    
    /* أدوات البروكر */
    .tool-box {{ background: #1a1a1a; padding: 20px; border-radius: 15px; border: 1px solid #333; margin-bottom: 15px; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. تسجيل الدخول ---
if not st.session_state.auth:
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        st.markdown("<div style='background:white; padding:40px; border-radius:25px; text-align:center; margin-top:100px;'><h1 style='color:black;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
        pwd = st.text_input("كلمة السر", type="password")
        if st.button("دخول آمن 🚀", use_container_width=True):
            if pwd == "2026": st.session_state.auth = True; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 7. الواجهة الداخلية ---
st.markdown('<div class="ticker-bar">🔥 MA3LOMATI PRO 2026 | خبيرك العقاري الذكي في جيبك</div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["grid-3x3-gap", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"}})

col_main, col_side = st.columns([0.8, 0.2])

# --- قسم أدوات البروكر (9 أدوات) ---
if menu == "أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ ترسانة البروكر (9 أدوات احترافية)</h2>", unsafe_allow_html=True)
    a1, a2, a3 = st.columns(3)
    with a1:
        with st.container(border=True):
            st.subheader("1. حاسبة القسط")
            v = st.number_input("السعر", 1000000, key="v1")
            y = st.number_input("السنين", 8, key="y1")
            st.metric("شهرياً", f"{v/(y*12):,.0f}")
        with st.container(border=True):
            st.subheader("4. السعر بعد الخصم")
            orig = st.number_input("السعر الأصلي", 1000000)
            dsc = st.slider("خصم %", 0, 50, 10)
            st.metric("بعد الخصم", f"{orig*(1-dsc/100):,.0f}")
        with st.container(border=True):
            st.subheader("7. التمويل العقاري")
            loan = st.number_input("قيمة التمويل", 500000)
            intr = st.slider("الفائدة %", 5, 25, 10)
            st.metric("الفائدة السنوية", f"{loan*(intr/100):,.0f}")

    with a2:
        with st.container(border=True):
            st.subheader("2. حساب العمولة")
            deal = st.number_input("قيمة البيعة", 5000000)
            comm = st.slider("عمولتك %", 1.0, 5.0, 2.5)
            st.metric("صافي الربح", f"{deal*(comm/100):,.0f}")
        with st.container(border=True):
            st.subheader("5. تحميل المساحة")
            net = st.number_input("المساحة الصافية", 120)
            gross = st.number_input("المساحة الإجمالية", 150)
            st.metric("نسبة التحميل", f"{((gross-net)/gross)*100:,.1f}%")
        with st.container(border=True):
            st.subheader("8. الضريبة العقارية")
            prop_v = st.number_input("القيمة السوقية", 2000000)
            st.metric("الضريبة التقديرية", f"{prop_v*0.001:,.0f}")

    with a3:
        with st.container(border=True):
            st.subheader("3. عائد الاستثمار ROI")
            buy = st.number_input("سعر الشراء", 3000000)
            rent = st.number_input("الإيجار السنوي", 300000)
            st.metric("ROI سنوي", f"{(rent/buy)*100:,.1f}%")
        with st.container(border=True):
            st.subheader("6. سعر المتر")
            tot = st.number_input("إجمالي المبلغ", 4000000)
            m2 = st.number_input("المساحة م2", 150)
            st.metric("سعر المتر", f"{tot/m2:,.0f}")
        with st.container(border=True):
            st.subheader("9. القسط المتزايد (5%)")
            start_p = st.number_input("قسط السنة الأولى", 10000)
            st.metric("بعد 5 سنوات", f"{start_p*(1.05**5):,.0f}")

# --- قسم المشاريع والمساعد ---
elif menu == "المساعد الذكي":
    with col_main:
        st.markdown("<div class='detail-card'><h3>🤖 مساعد معلوماتي الذكي</h3><p>اسألني عن أي مشروع وسأقوم بتحليل البيانات لك فوراً.</p></div>", unsafe_allow_html=True)
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.write(m["content"])
        
        if pmt := st.chat_input("مثال: معلومات عن مشروع [اسم المشروع]"):
            st.session_state.messages.append({"role": "user", "content": pmt})
            # بحث حقيقي
            match = df_p[df_p.apply(lambda r: r.astype(str).str.contains(pmt, case=False).any(), axis=1)]
            if not match.empty:
                res = f"✅ إليك تفاصيل **{match.iloc[0,0]}**:\n" + "\n".join([f"- **{k}**: {v}" for k, v in match.iloc[0].items()])
            else:
                res = "لم أجد هذا الاسم، حاول كتابة كلمات مفتاحية أدق."
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

else:
    active_df = df_p if menu=="المشاريع" else df_d
    with col_main:
        if st.session_state.view == "details":
            if st.button("⬅️ عودة"): st.session_state.view = "grid"; st.rerun()
            item = active_df.iloc[st.session_state.current_index]
            for k, v in item.items():
                st.markdown(f'<div class="detail-card"><p class="label-gold">{k}</p><p class="val-white">{v}</p></div>', unsafe_allow_html=True)
        else:
            search = st.text_input("🔍 ابحث الآن باسم المشروع أو المنطقة...", placeholder="مثال: التجمع الخامس")
            filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else active_df
            
            grid = st.columns(2)
            for i, (idx, r) in enumerate(filt.head(10).iterrows()):
                with grid[i%2]:
                    # الكرت المطور
                    card_text = f"🏢 {r.iloc[0]}\n📍 {r.get('Location', '---')}\n🏗️ {r.get('Developer', '---')}"
                    if st.button(card_text, key=f"card_{idx}"):
                        st.session_state.current_index = idx
                        st.session_state.view = "details"; st.rerun()

with col_side:
    st.markdown("<h3 style='color:#f59e0b; text-align:center;'>🏆 مقترحات PRO</h3>", unsafe_allow_html=True)
    for _, r in df_p.head(6).iterrows():
        st.markdown(f"<div style='background:white; color:black; padding:15px; border-radius:12px; margin-bottom:10px; border-right:5px solid #f59e0b; font-weight:900;'>{r.iloc[0][:20]}</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026 | النسخة الاحترافية</p>", unsafe_allow_html=True)
