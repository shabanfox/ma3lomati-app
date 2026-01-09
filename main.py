import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS الجديد (الأزرار الحادة والتبسيط المطلق)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* الهيدر الرئيسي - تصميم قوي وواضح */
    .bold-header { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 0; /* حواف حادة */
        text-align: center; margin-bottom: 30px; border-bottom: 8px solid #f59e0b; /* خط ذهبي سميك */
    }
    .bold-header h1 { font-weight: 900; font-size: 3rem; margin: 0; color: #f59e0b !important; }
    .bold-header h2 { font-weight: 900; font-size: 2rem; margin: 0; color: #f59e0b !important; }

    /* الأزرار الرئيسية (Main Buttons) - قوية، حادة، بدون ظلال */
    div.stButton > button {
        width: 100% !important; height: 120px !important; /* حجم كبير */
        background-color: #000000 !important; /* خلفية سوداء */
        color: #f59e0b !important; /* نص ذهبي */
        border: 4px solid #f59e0b !important; /* إطار ذهبي حاد */
        border-radius: 0 !important; /* حواف حادة تمامًا */
        font-size: 2rem !important; font-weight: 900 !important;
        box-shadow: none !important; /* بدون أي ظلال */
        transition: background-color 0.2s, color 0.2s;
    }
    div.stButton > button:hover { /* تأثير بسيط عند المرور */
        background-color: #f59e0b !important; /* يصبح ذهبي */
        color: #000000 !important; /* والنص أسود */
        border-color: #000000 !important; /* والإطار أسود */
    }

    /* كروت المشاريع (Project Cards) - بسيطة، قوية، سهلة القراءة */
    .project-card {
        background: #ffffff; border: 2px solid #000000; /* إطار أسود رفيع */
        border-radius: 0; /* حواف حادة */
        padding: 15px; margin-bottom: 15px; /* مسافات واضحة */
        box-shadow: none; /* بدون ظلال */
        height: 170px; display: flex; flex-direction: column; justify-content: space-between;
        transition: border-color 0.2s;
    }
    .project-card:hover { border-color: #f59e0b; cursor: pointer; } /* إطار ذهبي عند المرور */
    .p-title { font-size: 1.3rem; font-weight: 900; color: #000000; line-height: 1.2; }
    .p-dev { color: #f59e0b; font-weight: 700; font-size: 0.9rem; margin-top: 5px; }
    .p-price { 
        background: #000000; color: #ffffff; font-size: 1rem; font-weight: 900; 
        padding: 5px; border-radius: 0; text-align: center; margin-top: 10px;
    }

    /* قسم الإضافة (Admin Panel) - تصميم نظيف وواضح */
    .admin-panel {
        background: #fcfcfc; border: 2px solid #000000; border-radius: 0; padding: 20px;
        position: sticky; top: 20px;
    }
    .admin-panel .stTextInput label, .admin-panel .stNumberInput label { color: #000000 !important; font-weight: 700 !important; }
    .admin-panel .stTextInput input, .admin-panel .stNumberInput input { border-color: #000000 !important; }
    .admin-panel .stButton button { 
        background-color: #f59e0b !important; color: #000000 !important; 
        border: 2px solid #000000 !important; height: 50px !important; font-size: 1.1rem !important;
    }

    /* صناديق الحاسبات - تصميم بسيط وقوي */
    .calc-box { 
        background: #000000; color: #ffffff; padding: 25px; border-radius: 0; /* حواف حادة */
        border: 4px solid #f59e0b; text-align: center; margin-bottom: 20px;
    }
    .val-text { font-size: 2.8rem; font-weight: 900; color: #f59e0b !important; }
    .label-text { font-size: 1.1rem; color: #ccc; font-weight: 700; }

    /* أزرار العودة - تصميم واضح */
    .stApp > div:first-child > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) button {
        background-color: #ffffff !important; color: #000000 !important;
        border: 2px solid #000000 !important; border-radius: 0 !important;
        font-size: 1rem !important; height: 40px !important;
    }
    .stApp > div:first-child > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) button:hover {
        background-color: #000000 !important; color: #f59e0b !important;
    }

    /* tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #e2e8f0; border-radius: 0; padding: 10px 20px; font-weight: 900; color: #000;
    }
    .stTabs [aria-selected="true"] { background-color: #000 !important; color: #f59e0b !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return pd.DataFrame(columns=['المشروع','نوعه','المطور','الموقع','السداد'])

if 'data' not in st.session_state: st.session_state.data = load_data()
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'selected_project' not in st.session_state: st.session_state.selected_project = None

# --- المحتوى الرئيسي ---
if st.session_state.data is not None:
    # أ. الصفحة الرئيسية
    if st.session_state.view == 'main':
        st.markdown('<div class="bold-header"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
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
        st.markdown('<div class="bold-header"><h2>🔍 إدارة المشاريع العقارية</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
        
        col_grid, col_admin = st.columns([0.72, 0.28], gap="large")

        with col_grid:
            st.markdown("### 🏢 المشاريع المتاحة")
            q = st.text_input("🔍 ابحث عن أي تفاصيل (مشروع، مطور، موقع)...", key="search_comp")
            
            df_f = st.session_state.data
            if q: df_f = df_f[df_f.apply(lambda r: q.lower() in r.astype(str).str.lower().values, axis=1)]
            
            # عرض شبكي 3x3 كأزرار بتصميم "الكارت الحاد"
            for i in range(0, len(df_f.head(18)), 3):
                grid_cols = st.columns(3)
                for j in range(3):
                    if i + j < len(df_f):
                        row = df_f.iloc[i + j]
                        with grid_cols[j]:
                            # استخدام Markdown داخل الزر لتصميمه ككارت
                            button_content = f"""
                            <div class="project-card">
                                <div class="p-title">{row[0]}</div>
                                <div class="p-dev">🏢 {row[2]}</div>
                                <div style="font-size:0.8rem; color:#555; margin-top:5px;">📍 {row[3]}</div>
                                <div class="p-price">{row[4]}</div>
                            </div>
                            """
                            # Streamlit button with custom HTML content
                            # Note: This is a common workaround for highly custom buttons
                            if st.markdown(f'<button class="project-card-button" style="all:unset; cursor:pointer;">{button_content}</button>', unsafe_allow_html=True, key=f"proj_btn_{i+j}"):
                                st.session_state.selected_project = row
                                st.session_state.view = 'details'
                                st.rerun()

        with col_admin:
            st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
            st.markdown("### ➕ إضافة مشروع")
            with st.form("add_form", clear_on_submit=True):
                n = st.text_input("اسم المشروع")
                d = st.text_input("اسم المطور")
                l = st.text_input("الموقع الجغرافي")
                p = st.text_input("السعر / نظام السداد")
                if st.form_submit_button("حفظ وإضافة للمنصة"):
                    if n:
                        new_r = pd.DataFrame([[n, "", d, l, p]], columns=st.session_state.data.columns)
                        st.session_state.data = pd.concat([new_r, st.session_state.data], ignore_index=True)
                        st.success("تم الحفظ!")
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ج. صفحة تفاصيل المشروع
    elif st.session_state.view == 'details':
        proj = st.session_state.selected_project
        st.markdown(f'<div class="bold-header"><h2>🏢 تفاصيل المشروع: {proj[0]}</h2></div>', unsafe_allow_html=True)
        
        if st.button("🔙 العودة لدليل المشاريع"): st.session_state.view = 'comp'; st.rerun()
        
        st.markdown(f"""
            <div style="background:#000; color:#fff; padding:40px; border-radius:0; border:4px solid #f59e0b; text-align:center; margin-top:20px;">
                <span style="font-size:1.5rem; color:#f59e0b;">المطور:</span><br>
                <span style="font-size:2.5rem; font-weight:900;">{proj[2]}</span>
                <hr style="border-color:#555">
                <span style="font-size:1.5rem; color:#f59e0b;">الموقع:</span><br>
                <span style="font-size:2rem; font-weight:900;">📍 {proj[3]}</span>
                <hr style="border-color:#555">
                <span style="font-size:1.5rem; color:#f59e0b;">نظام السداد والأسعار:</span><br>
                <span style="font-size:2.2rem; font-weight:900; color:#f59e0b;">{proj[4]}</span>
            </div>
        """, unsafe_allow_html=True)
        
        other_projs = st.session_state.data[st.session_state.data.iloc[:,2] == proj[2]]
        if len(other_projs) > 1:
            st.markdown(f"### 🏗️ مشاريع أخرى لشركة {proj[2]}:")
            st.dataframe(other_projs[[st.session_state.data.columns[0], st.session_state.data.columns[3], st.session_state.data.columns[4]]], use_container_width=True)

    # د. صفحة الأدوات
    elif st.session_state.view == 'tools':
        st.markdown('<div class="bold-header"><h2>🛠️ حاسبات البروكر الذكية</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية", key="back_from_tools"): st.session_state.view = 'main'; st.rerun()
        
        tab1, tab2 = st.tabs(["💰 حاسبة الأقساط", "📈 حاسبة العائد ROI"])
        
        with tab1:
            st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
            i1, i2, i3 = st.columns(3)
            with i1: pr = st.number_input("سعر الوحدة الإجمالي", value=3000000, step=100000, key="price_calc")
            with i2: dn = st.number_input("نسبة المقدم %", value=10, key="down_calc")
            with i3: yr = st.number_input("عدد السنين", value=8, key="years_calc")
            
            calc_dn = pr * (dn/100)
            calc_mo = (pr - calc_dn) / (yr * 12) if yr > 0 else 0
            
            st.markdown(f"""
                <div class="calc-box">
                    <span class="label-text">المقدم المطلوب كاش</span><br><span class="val-text">{calc_dn:,.0f} ج.م</span>
                    <hr style="border-color:#333">
                    <span class="label-text">القسط الشهري</span><br><span class="val-text" style="color:#22c55e !important;">{calc_mo:,.0f} ج.م</span>
                </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
            r1, r2, r3 = st.columns(3)
            with r1: buy = st.number_input("سعر الشراء", value=2000000, key="buy_roi")
            with r2: sell = st.number_input("سعر البيع", value=3500000, key="sell_roi")
            with r3: rent = st.number_input("الإيجار السنوي", value=200000, key="rent_roi")
            
            prof = sell - buy
            roi = ((prof + rent) / buy) * 100 if buy > 0 else 0
            
            st.markdown(f"""
                <div class="calc-box" style="border-color:#ffffff;">
                    <span class="label-text">إجمالي أرباح الاستثمار</span><br><span class="val-text" style="color:#f59e0b !important;">{prof+rent:,.0f} ج.م</span>
                    <hr style="border-color:#333">
                    <span class="label-text">نسبة العائد الإجمالية ROI</span><br><span class="val-text">%{roi:.1f}</span>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("لم يتم تحميل البيانات. يرجى التحقق من رابط Google Sheets.")
