import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container { padding-top: 0rem !important; margin-top: -10px; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    [data-testid="stAppViewContainer"] { 
        background-color: #050505; 
        direction: RTL !important; 
        text-align: right !important; 
        font-family: 'Cairo', sans-serif; 
    }

    /* زر الخروج في اليسار العلوي */
    .logout-container { position: absolute; left: 20px; top: 10px; z-index: 999; }

    .oval-header {
        background-color: #000;
        border: 3px solid #f59e0b;
        border-radius: 50px;
        padding: 10px 30px;
        width: fit-content;
        margin: 10px auto 20px auto;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(245, 158, 11, 0.4);
    }
    .header-title { color: #f59e0b; font-weight: 900; font-size: 26px !important; margin: 0; }

    .login-box {
        max-width: 400px; margin: 50px auto; padding: 30px;
        background: #111; border-radius: 20px; border: 1px solid #222; text-align: center;
    }
    div[data-baseweb="input"] { background-color: white !important; border-radius: 8px !important; }
    input { color: black !important; font-weight: bold !important; text-align: center !important; }

    .right-header {
        color: #f59e0b; font-weight: 900; border-right: 8px solid #f59e0b;
        padding-right: 15px; margin-bottom: 20px; font-size: 22px;
    }

    .grid-card {
        background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b;
        border-radius: 12px; padding: 15px; height: 160px; margin-bottom: 10px;
    }

    /* تحسين أزرار البروكر */
    .broker-tool-card {
        background: #1a1a1a; border: 1px solid #333; border-radius: 15px;
        padding: 20px; margin-bottom: 20px; border-right: 5px solid #f59e0b;
    }

    .stButton button { 
        background-color: #1a1a1a !important; color: #f59e0b !important; 
        border: 1px solid #333 !important; width: 100% !important;
    }
    .logout-btn button {
        background-color: #ff4b4b !important; color: white !important;
        border: none !important; width: auto !important; padding: 0 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. نظام الدخول
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown('<div class="oval-header"><h1 class="header-title">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#f59e0b; font-size:60px;'>🔒</h1>", unsafe_allow_html=True)
    pwd = st.text_input("أدخل الباسورد", type="password")
    if st.button("دخول للنظام"):
        if pwd == "2026":
            st.session_state.auth = True; st.rerun()
        else: st.error("عفواً، الباسورد خطأ")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- بعد الدخول ---

# زر الخروج في اليسار العلوي
col_top_L, col_top_R = st.columns([1, 1])
with col_top_L:
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("🚪 خروج"):
        st.session_state.auth = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="oval-header"><h1 class="header-title">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# المنيو الرئيسي
menu = option_menu(None, ["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
                  icons=["tools", "building", "person-vcard"], 
                  orientation="horizontal")

# تحميل البيانات
@st.cache_data(ttl=60)
def load_data():
    u1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u2 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        df1 = pd.read_csv(u1); df2 = pd.read_csv(u2)
        combined = pd.concat([df1, df2], ignore_index=True)
        combined.columns = [str(c).strip() for c in combined.columns]
        return combined.fillna("غير متوفر").astype(str)
    except: return pd.DataFrame()

df = load_data()
grid_limit = 9

# تقسيم الشاشة 70% يمين للمحتوى
main_col, empty_col = st.columns([0.7, 0.3])

with main_col:
    # --- قسم المشاريع ---
    if menu == "🏗️ المشاريع":
        st.markdown("<h1 class='right-header'>دليل المشاريع</h1>", unsafe_allow_html=True)
        f1, f2 = st.columns([0.6, 0.4])
        with f1: search = st.text_input("🔍 بحث ذكي...", placeholder="اسم المشروع أو المنطقة")
        with f2: 
            areas = ["كل المناطق"] + sorted(df['Area'].unique().tolist())
            selected_area = st.selectbox("📍 تصفية بالمنطقة", areas)

        dff = df.copy()
        if search: dff = dff[dff.apply(lambda r: search.lower() in r.astype(str).str.lower().values, axis=1)]
        if selected_area != "كل المناطق": dff = dff[dff['Area'] == selected_area]

        if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
        total_p = math.ceil(len(dff) / grid_limit)
        curr_df = dff.iloc[st.session_state.p_idx * grid_limit : (st.session_state.p_idx + 1) * grid_limit]

        for i in range(0, len(curr_df), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(curr_df):
                    row = curr_df.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"""<div class='grid-card'>
                            <h3 style='color:#f59e0b; font-size:16px;'>{row['Project Name']}</h3>
                            <p style='font-size:13px;'>🏢 {row['Developer']}</p>
                            <p style='font-size:12px; color:#888;'>📍 {row['Area']}</p>
                        </div>""", unsafe_allow_html=True)
                        with st.expander("🔎 التفاصيل"):
                            st.write(f"👷 الاستشاري: {row['Consultant']}")
                            st.write(f"⭐ الميزة: {row['Competitive Advantage']}")

        st.write("---")
        b1, b2, _ = st.columns([0.2, 0.2, 0.6])
        if b1.button("التالي ⬅️", key="p_next") and st.session_state.p_idx < total_p - 1:
            st.session_state.p_idx += 1; st.rerun()
        if b2.button("➡️ السابق", key="p_prev") and st.session_state.p_idx > 0:
            st.session_state.p_idx -= 1; st.rerun()

    # --- قسم المطورين ---
    elif menu == "🏢 المطورين":
        st.markdown("<h1 class='right-header'>دليل المطورين</h1>", unsafe_allow_html=True)
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer'])
        curr_devs = devs.head(grid_limit) # تبسيط للعرض

        for i in range(0, len(curr_devs), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(curr_devs):
                    row = curr_devs.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h3 style='color:#f59e0b;'>{row['Developer']}</h3><p>👤 {row['Owner']}</p></div>", unsafe_allow_html=True)
                        with st.expander("الملف"): st.write(row['Detailed_Info'])

    # --- قسم أدوات البروكر (شامل) ---
    elif menu == "🛠️ أدوات البروكر":
        st.markdown("<h1 class='right-header'>صندوق أدوات البروكر المحترف</h1>", unsafe_allow_html=True)
        
        t1, t2 = st.columns(2)
        
        with t1:
            st.markdown("<div class='broker-tool-card'>", unsafe_allow_html=True)
            st.subheader("💰 حاسبة الأقساط المتطورة")
            total_price = st.number_input("إجمالي سعر الوحدة (ج.م)", value=1000000, step=100000)
            down_payment_pct = st.slider("نسبة المقدم %", 0, 50, 10)
            years = st.number_input("عدد سنوات التقسيط", 1, 15, 8)
            
            down_val = total_price * (down_payment_pct/100)
            remaining = total_price - down_val
            monthly = remaining / (years * 12)
            
            st.markdown(f"**المقدم:** {down_val:,.0f} ج.م")
            st.markdown(f"**القسط الشهري:** <span style='color:#f59e0b; font-size:20px;'>{monthly:,.0f} ج.م</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='broker-tool-card'>", unsafe_allow_html=True)
            st.subheader("📈 حاسبة العمولة")
            comm_pct = st.number_input("نسبة العمولة %", 1.0, 10.0, 1.5)
            st.markdown(f"**صافي عمولتك:** {total_price * (comm_pct/100):,.0f} ج.م")
            st.markdown("</div>", unsafe_allow_html=True)

        with t2:
            st.markdown("<div class='broker-tool-card'>", unsafe_allow_html=True)
            st.subheader("📝 مفكرة المتابعة السريعة")
            st.text_input("اسم العميل المهتم")
            st.selectbox("حالة العميل", ["متابعة", "معاينة", "تعاقد", "مؤجل"])
            st.text_area("ملاحظات المكالمة...", height=100)
            st.button("حفظ الملاحظة (تجريبي)")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='broker-tool-card'>", unsafe_allow_html=True)
            st.subheader("📏 محول المساحات")
            sqm = st.number_input("المساحة بالمتر المربع", value=100)
            st.markdown(f"**المساحة بالقدم:** {sqm * 10.764:,.2f} قدم")
            st.markdown("</div>", unsafe_allow_html=True)
