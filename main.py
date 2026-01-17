import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'current_menu' not in st.session_state: st.session_state.current_menu = "المشاريع"

# 3. جلب البيانات وتصحيح الأعمدة تلقائياً
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        
        # ربط الأسماء الشائعة لتجنب KeyError
        p.rename(columns={
            'Project Name': 'ProjectName',
            'Area': 'Location',
            'الموقع': 'Location',
            'Delivery Date': 'Delivery_Date',
            'تاريخ الاستلام': 'Delivery_Date'
        }, inplace=True)
        
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 4. التوقيت المصري
egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# 5. الهيدر والمنيو
t1, t2 = st.columns([0.7, 0.3])
t1.markdown("<h1 style='color:#f59e0b; margin:0;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
with t2:
    st.markdown(f"<div style='text-align:left; color:#aaa;'>{egypt_now.strftime('%Y-%m-%d')} | {egypt_now.strftime('%I:%M %p')}</div>", unsafe_allow_html=True)
    if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()

selected_menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "حقيبة الأدوات"], 
    icons=["robot", "search", "building", "briefcase"], default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# حل مشكلة التعليق بين الصفحات
if selected_menu != st.session_state.current_menu:
    st.session_state.selected_item = None
    st.session_state.current_menu = selected_menu
    st.rerun()

# 6. منطق عرض "استلام فوري" بأمان (بدون KeyError)
def get_ready_units(df):
    # البحث عن عمود الاستلام مهما كان اسمه
    target_col = None
    possible_names = ['Delivery_Date', 'Delivery', 'استلام', 'تاريخ']
    for col in df.columns:
        if any(name in col for name in possible_names):
            target_col = col
            break
    
    if target_col:
        return df[df[target_col].astype(str).str.contains('فوري|جاهز', case=False)].head(10)
    return pd.DataFrame()

# 7. عرض المحتوى (المشاريع كمثال)
if selected_menu == "المشاريع":
    if st.session_state.selected_item is not None:
        if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
        st.write(st.session_state.selected_item)
    else:
        col_main, col_side = st.columns([0.7, 0.3])
        
        with col_side:
            st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري</h4>", unsafe_allow_html=True)
            ready_df = get_ready_units(df_p)
            if not ready_df.empty:
                for i, r in ready_df.iterrows():
                    if st.button(f"🏠 {r.get('ProjectName', 'مشروع')}", key=f"ready_{i}"):
                        st.session_state.selected_item = r; st.rerun()
            else:
                st.info("لا توجد مشاريع استلام فوري حالياً")

        with col_main:
            # هنا كود عرض المشاريع (الكروت) كما هو في نسختك السابقة
            st.subheader("دليل المشاريع العقارية")
            search = st.text_input("🔍 ابحث عن اسم المشروع")
            # ... تكملة كود الفلترة والعرض
