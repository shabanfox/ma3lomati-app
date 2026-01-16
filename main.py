import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (Auth, Pagination, Selection)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None

# 3. التنسيق (CSS) - التركيز على الـ 60% والشبكة المتراصة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right; background-color: #f8fafc; }
    
    /* تحديد عرض المحتوى بـ 60% وجعله جهة اليمين */
    .main-container { width: 60%; margin-right: 0; margin-left: auto; }
    
    /* هيدر بسيط */
    .simple-header { background: #0f172a; padding: 15px; border-radius: 0 0 15px 15px; color: #f59e0b; margin-bottom: 20px; font-weight: 900; font-size: 20px; }

    /* كارت المطور (بسيط جداً - اسم فقط) */
    .dev-grid-card {
        background: white; border: 1px solid #e2e8f0; border-radius: 8px;
        padding: 15px; text-align: center; transition: 0.2s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02); height: 80px;
        display: flex; align-items: center; justify-content: center;
    }
    .dev-grid-card:hover { border-color: #f59e0b; background: #fffcf5; cursor: pointer; }
    .dev-name { color: #0f172a; font-weight: 700; font-size: 15px; margin: 0; }

    /* أزرار التنقل */
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 4. وظيفة جلب البيانات
@st.cache_data(ttl=60)
def load_all_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("").astype(str)
        d = pd.read_csv(u_d).fillna("").astype(str)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_all_data()

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if st.text_input("Passcode", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# 6. الهيدر والمنيو
st.markdown('<div class="simple-header">MA3LOMATI PRO 2026</div>', unsafe_allow_html=True)

# استخدام 60% من المساحة (عن طريق تقسيم الشاشة لأعمدة)
left_gap, main_content = st.columns([0.4, 0.6])

with main_content:
    if st.session_state.selected_dev:
        # --- صفحة تفاصيل المطور ---
        dev_name = st.session_state.selected_dev
        dev_info = df_d[df_d['Developer'] == dev_name].iloc[0]
        
        if st.button("⬅️ عودة للقائمة"):
            st.session_state.selected_dev = None
            st.rerun()
            
        st.markdown(f"""
            <div style="background:white; padding:25px; border-radius:15px; border-top:5px solid #f59e0b; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <h2 style="color:#0f172a;">{dev_name}</h2>
                <p style="color:#64748b;">👤 المالك: {dev_info.get('Owner')}</p>
                <hr>
                <p style="font-size:16px; line-height:1.7;">{dev_info.get('Detailed_Info', 'لا توجد سيرة ذاتية متوفرة.')}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # عرض مشاريع المطور
        st.write("### 🏗️ المشاريع")
        projects = df_p[df_p['Developer'] == dev_name]
        for _, p in projects.iterrows():
            st.success(f"**{p.get('Project Name')}** - {p.get('Area')}")

    else:
        # --- القائمة الرئيسية ---
        menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
            icons=["tools", "building", "person-vcard"], 
            default_index=2, orientation="horizontal",
            styles={"nav-link-selected": {"background-color": "#0f172a", "color": "#f59e0b"}}
        )

        if menu == "المطورين":
            search_d = st.text_input("🔍 ابحث عن مطور...")
            dff_d = df_d.copy()
            if search_d: dff_d = dff_d[dff_d.apply(lambda r: r.astype(str).str.contains(search_d, case=False).any(), axis=1)]
            
            # إعدادات الترقيم (8 مطورين في الصفحة)
            limit = 8
            total_pages = (len(dff_d) // limit) + (1 if len(dff_d) % limit > 0 else 0)
            start = st.session_state.d_idx * limit
            items = dff_d.iloc[start : start + limit]

            # عرض الشبكة (2 في كل صف، متراصة)
            cols = st.columns(2)
            for i, (idx, row) in enumerate(items.iterrows()):
                with cols[i % 2]:
                    # الكارت لعرض الاسم فقط
                    st.markdown(f"""<div class="dev-grid-card"><p class="dev-name">{row.get('Developer')}</p></div>""", unsafe_allow_html=True)
                    # زر شفاف أو صغير لفتح التفاصيل
                    if st.button(f"تفاصيل {row.get('Developer')}", key=f"btn_{idx}", use_container_width=True):
                        st.session_state.selected_dev = row.get('Developer')
                        st.rerun()

            # أزرار التنقل
            st.write("---")
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav1:
                if st.session_state.d_idx > 0:
                    if st.button("السابق"): st.session_state.d_idx -= 1; st.rerun()
            with nav2:
                st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.d_idx + 1} من {total_pages}</p>", unsafe_allow_html=True)
            with nav3:
                if (start + limit) < len(dff_d):
                    if st.button("التالي"): st.session_state.d_idx += 1; st.rerun()

        elif menu == "المشاريع":
            st.info("قسم المشاريع قيد التطوير بناءً على نفس النمط")
            
        elif menu == "الأدوات":
            st.subheader("🧮 حاسبة القسط")
            price = st.number_input("السعر", value=1000000)
            years = st.slider("السنين", 1, 15, 8)
            st.metric("القسط الشهري", f"{price/(years*12):,.0f}")

# زر خروج في أسفل الصفحة
if st.sidebar.button("🚪 خروج"):
    st.session_state.auth = False
    st.rerun()
