import streamlit as st
import pandas as pd
import requests
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. روابط البيانات (تأكد من نشر الشيت CSV) ---
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

# --- 3. إدارة حالة الجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'selected_launch' not in st.session_state: st.session_state.selected_launch = None

# --- 4. وظائف جلب البيانات ---
@st.cache_data(ttl=60)
def load_launches():
    try:
        df = pd.read_csv(URL_LAUNCHES).fillna("---")
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

# --- 5. التنسيق الجمالي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
    /* ستايل الكروت كأزرار */
    div.stButton > button[key^="lnch_"] {
        background: #161616 !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-top: 5px solid #f59e0b !important;
        border-radius: 15px !important;
        height: 180px !important;
        width: 100% !important;
        font-weight: bold !important;
        font-size: 18px !important;
        white-space: pre-line !important;
    }
    .detail-card { background: #111; padding: 25px; border-radius: 15px; border-right: 5px solid #f59e0b; margin-top: 20px; text-align: right; }
    .label { color: #f59e0b; font-weight: bold; font-size: 14px; margin-bottom: 2px; }
    .value { color: #fff; font-size: 18px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- 6. شاشة الدخول ---
if not st.session_state.auth:
    _, col_mid, _ = st.columns([1, 1.2, 1])
    with col_mid:
        st.markdown("<br><br><br><h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
        pwd = st.text_input("كلمة المرور", type="password")
        if st.button("دخول", use_container_width=True):
            if pwd == "2026": st.session_state.auth = True; st.rerun()
            else: st.error("خطأ!")
    st.stop()

# --- 7. تعريف المنيو (هنا تعريف متغير menu) ---
c_out, c_empty = st.columns([0.15, 0.85])
with c_out:
    if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
    icons=["briefcase", "building", "search", "robot", "rocket"], 
    default_index=4, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- 8. منطق الأقسام ---
if menu == "اللونشات":
    df_l = load_launches()
    
    # حالة عرض التفاصيل الكاملة
    if st.session_state.selected_launch is not None:
        item = st.session_state.selected_launch
        if st.button("⬅️ عودة للقائمة"):
            st.session_state.selected_launch = None
            st.rerun()
        
        st.markdown(f"<div class='detail-card'>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='color:#f59e0b; margin-top:0;'>{item.get('Project', 'مشروع جديد')}</h1>", unsafe_allow_html=True)
        
        # توزيع البيانات في أعمدة داخل التفاصيل
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.markdown(f"<p class='label'>🏢 المطور</p><p class='value'>{item.get('Developer', '---')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='label'>📍 الموقع</p><p class='value'>{item.get('Location', '---')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='label'>📐 المساحات والأنواع</p><p class='value'>{item.get('Types', '---')}</p>", unsafe_allow_html=True)
        with d_col2:
            st.markdown(f"<p class='label'>💰 مبلغ الجدية (EOI)</p><p class='value' style='color:#00ff00; font-weight:bold;'>{item.get('EOI', '---')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='label'>💵 متوسط الأسعار</p><p class='value'>{item.get('Prices', '---')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='label'>💳 نظام السداد</p><p class='value'>{item.get('Payment', '---')}</p>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
        st.markdown(f"<p class='label'>📝 ملاحظات هامة</p><p style='color:#ccc; line-height:1.6;'>{item.get('Notes', 'لا توجد ملاحظات')}</p>", unsafe_allow_html=True)
        
        # زر البروشور
        link = item.get('Brochure', '---')
        if link != "---":
            st.link_button("📂 فتح البروشور والصور", link, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("<h2 style='text-align:center; color:white;'>🚀 لونشات 2026</h2>", unsafe_allow_html=True)
        if not df_l.empty:
            cols = st.columns(3)
            for index, row in df_l.iterrows():
                with cols[index % 3]:
                    label = f"🏢 {row.get('Developer', 'مطور')}\n{row.get('Project', 'مشروع')}\n📍 {row.get('Location', '---')}"
                    if st.button(label, key=f"lnch_{index}"):
                        st.session_state.selected_launch = row
                        st.rerun()
        else:
            st.warning("تأكد من تعبئة بيانات في الشيت.")

elif menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align:center;'>🛠️ أدوات البروكر</h2>")
    # ... باقي الأقسام ...

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
