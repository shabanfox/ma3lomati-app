import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. التصميم البصري (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; }
    [data-testid="stAppViewContainer"] {
        background: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }
    .royal-header { 
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover; background-position: center; border-bottom: 4px solid #f59e0b; padding: 50px 20px; text-align: center; border-radius: 0 0 50px 50px;
    }
    .royal-header h1 { color: #f59e0b; font-size: 3.5rem; font-weight: 900; margin: 0; }
    
    /* كروت العرض */
    div.stButton > button[key*="card_"] { 
        background: white !important; color: #000 !important; border-right: 12px solid #f59e0b !important; border-radius: 15px !important; text-align: right !important; min-height: 110px !important; font-weight: 900 !important; font-size: 1.1rem !important;
    }
    
    /* كروت التفاصيل (تأخذ العرض كاملاً) */
    .detail-row {
        background: #111; padding: 25px; border-radius: 15px; border: 1px solid #333; border-right: 8px solid #f59e0b; margin-bottom: 15px; width: 100%;
    }
    .detail-label { color: #f59e0b; font-size: 1.1rem; font-weight: bold; margin-bottom: 5px; }
    .detail-value { color: white; font-size: 1.7rem; font-weight: 900; }

    /* الحاسبات */
    .tool-box { background: #111; padding: 20px; border-radius: 15px; border: 1px solid #f59e0b; margin-bottom: 20px; }
    .res-box { background: rgba(245, 158, 11, 0.2); padding: 15px; border-radius: 10px; color: #fff; font-weight: bold; text-align: center; font-size: 1.3rem; border: 1px dashed #f59e0b; }
    </style>
""", unsafe_allow_html=True)

# --- 3. البيانات والربط ---
@st.cache_data(ttl=300)
def load_data():
    urls = [
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv", # المشاريع
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv", # المطورين
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"  # مشاريع جديدة
    ]
    dfs = []
    for u in urls:
        df = pd.read_csv(u).fillna("---")
        df.columns = [c.strip() for c in df.columns]
        df.rename(columns={'Area':'Location','الموقع':'Location','السعر':'Price','الاونر':'Owner','صاحب الشركة':'Owner'}, inplace=True, errors="ignore")
        dfs.append(df)
    return dfs

# --- 4. الدخول ---
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h1 style='color:#f59e0b; text-align:center; padding-top:100px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    u = st.text_input("اسم المستخدم")
    p = st.text_input("كلمة المرور", type="password")
    if st.button("دخول الملكي 🚀"):
        if p == "2026" or p == "1234": st.session_state.auth, st.session_state.user = True, "Admin"; st.rerun()
    st.stop()

# --- 5. الهيكل ---
df_p, df_d, df_n = load_data()
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b;">مرحباً بك في عالم العقارات الذكي</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع"], 
    icons=["calculator", "building", "search"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight":"900"}})

if 'view' not in st.session_state: st.session_state.view = "grid"

def format_price(val):
    try:
        v = float(val)
        return f"{v/1_000_000:,.2f} مليون ج.م" if v >= 1_000_000 else f"{v:,.0f} ج.م"
    except: return val

# --- 6. منطق العرض (100% للتفاصيل) ---
def display_logic(df, prefix):
    # حالة التفاصيل (تأخذ الشاشة كلها)
    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}"):
            st.session_state.view = "grid"; st.rerun()
        
        item = df.iloc[st.session_state.current_index]
        st.markdown(f"<h1 style='color:#f59e0b; margin-top:20px;'>{item.iloc[0]}</h1>", unsafe_allow_html=True)
        st.write("---")
        
        # عرض التفاصيل في كروت عرض كاملة (Full Width)
        for col in df.columns:
            val = format_price(item[col]) if col == 'Price' else item[col]
            st.markdown(f"""
                <div class="detail-row">
                    <div class="detail-label">{col}</div>
                    <div class="detail-value">{val}</div>
                </div>
            """, unsafe_allow_html=True)

    # حالة الشبكة (70% - 30%)
    else:
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            search = st.text_input("🔍 ابحث هنا...", key=f"s_{prefix}")
            filt = df[df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else df
            
            grid = st.columns(2)
            for i, (idx, r) in enumerate(filt.head(10).iterrows()):
                with grid[i%2]:
                    lbl = f"🏢 {r[0]}\n📍 {r.get('Location','---')}"
                    if st.button(lbl, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
        with c_side:
            st.markdown("<h3 style='color:#f59e0b;'>⭐ مقترحات</h3>", unsafe_allow_html=True)
            for si, sr in df.head(8).iterrows():
                if st.button(f"📌 {sr.iloc[0]}", key=f"side_{prefix}_{si}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = si, f"details_{prefix}"; st.rerun()

# --- 7. الأقسام ---
if menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ جميع المشاريع", "🚀 مشاريع جديدة"])
    with t1: display_logic(df_p, "p")
    with t2: display_logic(df_n, "n")

elif menu == "المطورين":
    display_logic(df_d, "d")

elif menu == "أدوات الحساب":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات البروكر المحترف</h2>", unsafe_allow_html=True)
    t1, t2, t3, t4, t5, t6 = st.tabs(["💰 القسط", "📊 العمولة", "📈 ROI", "🏦 تمويل", "🎁 كاش باك", "🔮 تضخم"])
    
    with t1:
        st.markdown('<div class="tool-box">', unsafe_allow_html=True)
        p1 = st.number_input("سعر الوحدة", value=10000000)
        d1 = st.number_input("المقدم %", value=10)
        y1 = st.number_input("السنين", value=8)
        st.markdown(f'<div class="res-box">القسط الشهري: {(p1*(1-d1/100))/(y1*12):,.0f} ج.م</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="tool-box">', unsafe_allow_html=True)
        v2 = st.number_input("قيمة الصفقة", value=5000000)
        c2 = st.number_input("العمولة %", value=2.5)
        st.markdown(f'<div class="res-box">صافي العمولة: {v2*(c2/100):,.0f} ج.م</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="tool-box">', unsafe_allow_html=True)
        i3 = st.number_input("سعر الشراء", value=8000000)
        r3 = st.number_input("الإيجار الشهري", value=40000)
        st.markdown(f'<div class="res-box">ROI السنوي: {((r3*12)/i3)*100:.2f} %</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with t4:
        st.markdown('<div class="tool-box">', unsafe_allow_html=True)
        b4 = st.number_input("مبلغ التمويل", value=2000000)
        y4 = st.number_input("مدة التمويل", value=10)
        st.markdown(f'<div class="res-box">قسط البنك التقريبي: {(b4*1.8)/(y4*12):,.0f} ج.م</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with t5:
        st.markdown('<div class="tool-box">', unsafe_allow_html=True)
        p5 = st.number_input("إجمالي السعر قبل الخصم", value=10000000)
        disc = st.slider("نسبة الخصم %", 0, 45, 15)
        st.markdown(f'<div class="res-box">السعر بعد الخصم: {p5*(1-disc/100):,.0f} ج.م</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with t6:
        st.markdown('<div class="tool-box">', unsafe_allow_html=True)
        v6 = st.number_input("السعر اليوم", value=5000000)
        inf = st.slider("الزيادة السنوية %", 10, 50, 25)
        st.markdown(f'<div class="res-box">السعر بعد 3 سنوات: {v6*(1+inf/100)**3:,.0f} ج.م</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
