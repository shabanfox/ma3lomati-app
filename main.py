import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS الفاخر (High-Contrast Neumorphism)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الزوائد لجعل المنصة تبدو كتطبيق مستقل */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* الهيدر الملكي */
    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
    }
    .hero-banner h1 { font-weight: 900; font-size: 2.8rem; margin: 0; color: #f59e0b !important; }

    /* الأزرار الرئيسية (Nano-Cards) */
    div.stButton > button {
        width: 100% !important; height: 130px !important;
        background-color: #ffffff !important; color: #000000 !important;
        border: 5px solid #000000 !important; border-radius: 25px !important;
        font-size: 1.8rem !important; font-weight: 900 !important;
        box-shadow: 10px 10px 0px 0px #000000 !important;
        transition: 0.2s;
    }
    div.stButton > button:hover { transform: translate(-3px, -3px); box-shadow: 13px 13px 0px #f59e0b !important; }

    /* كروت المشاريع المدمجة (Compact Micro-Cards) */
    .micro-card {
        background: #ffffff; border: 3px solid #000; padding: 12px; 
        border-radius: 18px; margin-bottom: 12px; box-shadow: 6px 6px 0px #000;
        height: 180px; display: flex; flex-direction: column; justify-content: space-between;
        transition: 0.3s;
    }
    .micro-card:hover { border-color: #f59e0b; box-shadow: 8px 8px 0px #f59e0b; }
    .m-title { font-size: 1.2rem; font-weight: 900; color: #000; line-height: 1.2; }
    .m-dev { color: #f59e0b; font-weight: 900; font-size: 0.9rem; margin-top: 5px; }
    .m-price { 
        background: #000; color: #fff; font-size: 1rem; font-weight: 900; 
        padding: 5px; border-radius: 8px; text-align: center; margin-top: 10px;
    }

    /* قسم الإضافة (الجانب الأيسر) */
    .admin-panel {
        background: #fcfcfc; border: 4px dashed #000; padding: 20px; 
        border-radius: 20px; position: sticky; top: 20px;
    }

    /* صناديق الحاسبات الفخمة */
    .calc-box { 
        background: #000; color: #fff; padding: 25px; border-radius: 25px; 
        border: 4px solid #f59e0b; text-align: center; margin-bottom: 20px;
    }
    .val-text { font-size: 2.8rem; font-weight: 900; color: #f59e0b !important; }
    .label-text { font-size: 1.1rem; color: #ccc; font-weight: 700; }

    /* تحسين المدخلات */
    input { border: 3px solid #000 !important; font-weight: 900 !important; border-radius: 10px !important; }
    label { font-weight: 900 !important; color: #000 !important; font-size: 1.2rem !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات من Google Sheets
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return pd.DataFrame(columns=['المشروع','نوعه','المطور','الموقع','السداد'])

if 'data' not in st.session_state: st.session_state.data = load_data()
if 'view' not in st.session_state: st.session_state.view = 'main'

# --- المحتوى الرئيسي ---
if st.session_state.data is not None:
    # أ. الصفحة الرئيسية
    if st.session_state.view == 'main':
        st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
        st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)
        _, mid_col, _ = st.columns([0.1, 0.8, 0.1])
        with mid_col:
            c1, c2 = st.columns(2, gap="large")
            with c1:
                if st.button("🏢\nدليل المشاريع"): st.session_state.view = 'comp'; st.rerun()
            with c2:
                if st.button("🛠️\nأدوات البروكر"): st.session_state.view = 'tools'; st.rerun()

    # ب. دليل المشاريع (شبكة 3x3 يميناً وإضافة يساراً)
    elif st.session_state.view == 'comp':
        st.markdown('<div class="hero-banner"><h2>🔍 إدارة المشاريع العقارية</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
        
        col_grid, col_admin = st.columns([0.72, 0.28], gap="large")

        with col_grid:
            st.markdown("### 🏢 المشاريع المتاحة")
            q = st.text_input("🔍 ابحث عن أي تفاصيل (مشروع، مطور، موقع)...")
            
            # فلترة
            df_f = st.session_state.data
            if q: df_f = df_f[df_f.apply(lambda r: q.lower() in r.astype(str).str.lower().values, axis=1)]
            
            # عرض شبكي 3x3
            for i in range(0, len(df_f.head(18)), 3):
                grid_cols = st.columns(3)
                for j in range(3):
                    if i + j < len(df_f):
                        row = df_f.iloc[i + j]
                        with grid_cols[j]:
                            st.markdown(f"""
                            <div class="micro-card">
                                <div>
                                    <div class="m-title">{row[0]}</div>
                                    <div class="m-dev">🏢 {row[2]}</div>
                                    <div style="font-size:0.8rem; color:#555; margin-top:5px;">📍 {row[3]}</div>
                                </div>
                                <div class="m-price">{row[4]}</div>
                            </div>
                            """, unsafe_allow_html=True)

        with col_admin:
            st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
            st.markdown("### ➕ إضافة مشروع")
            with st.form("add_form", clear_on_submit=True):
                n = st.text_input("اسم المشروع")
                d = st.text_input("اسم المطور")
                l = st.text_input("الموقع الجغرافي")
                p = st.text_input("السعر / نظام السداد")
                if st.form_submit_button("حفظ وإضافة للشبكة"):
                    if n:
                        new_r = pd.DataFrame([[n, "", d, l, p]], columns=st.session_state.data.columns)
                        st.session_state.data = pd.concat([new_r, st.session_state.data], ignore_index=True)
                        st.success("تم الحفظ!")
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ج. صفحة الأدوات والحاسبات
    elif st.session_state.view == 'tools':
        st.markdown('<div class="hero-banner"><h2>🛠️ الحاسبات والذكاء المالي</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()

        t1, t2 = st.tabs(["💰 حاسبة الأقساط", "📈 حاسبة العائد ROI"])
        
        with t1:
            st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
            i1, i2, i3 = st.columns(3)
            with i1: pr = st.number_input("سعر الوحدة الإجمالي", value=3000000, step=100000)
            with i2: dn = st.number_input("نسبة المقدم %", value=10)
            with i3: yr = st.number_input("عدد السنين", value=8)
            
            calc_dn = pr * (dn/100)
            calc_mo = (pr - calc_dn) / (yr * 12) if yr > 0 else 0
            
            st.markdown(f"""
                <div class="calc-box">
                    <span class="label-text">المقدم المطلوب كاش</span><br><span class="val-text">{calc_dn:,.0f} ج.م</span>
                    <hr style="border-color:#333">
                    <span class="label-text">القسط الشهري</span><br><span class="val-text" style="color:#22c55e !important;">{calc_mo:,.0f} ج.م</span>
                </div>
            """, unsafe_allow_html=True)

        with t2:
            st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
            r1, r2, r3 = st.columns(3)
            with r1: buy = st.number_input("سعر الشراء", value=2000000)
            with r2: sell = st.number_input("سعر البيع", value=3500000)
            with r3: rent = st.number_input("الإيجار السنوي", value=200000)
            
            prof = sell - buy
            roi = ((prof + rent) / buy) * 100 if buy > 0 else 0
            
            st.markdown(f"""
                <div class="calc-box" style="border-color:#fff;">
                    <span class="label-text">إجمالي أرباح الاستثمار</span><br><span class="val-text">{prof+rent:,.0f} ج.م</span>
                    <hr style="border-color:#333">
                    <span class="label-text">نسبة العائد الإجمالية ROI</span><br><span class="val-text">%{roi:.1f}</span>
                </div>
            """, unsafe_allow_html=True)
