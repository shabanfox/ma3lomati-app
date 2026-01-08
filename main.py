import streamlit as st
import pandas as pd

st.set_page_config(page_title="منصة معلوماتي", layout="wide")

# الرابط بتاعك
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSNSOFbm5Qcr_da2U_wV4BvDyX4VRFwrAZrhgLfJlf9RYrVmF4Onyf5EaATSmY-ow/pub?output=xlsx"

@st.cache_data
def get_data():
    return pd.read_excel(URL)

st.title("🏙️ منصة معلوماتي العقارية")

try:
    df = get_data()
    
    # فلاتر علوية بسيطة
    cols = st.columns(len(df.columns[:3])) # فلاتر لأول 3 أعمدة أهم حاجة
    for i, col_name in enumerate(df.columns[:3]):
        with cols[i]:
            option = st.selectbox(f"فلتر بـ {col_name}", ["الكل"] + list(df[col_name].unique()))
            if option != "الكل":
                df = df[df[col_name] == option]

    # عرض الجدول بكامل عرض الشاشة مع إمكانية البحث والترتيب
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        column_config={col: st.column_config.TextColumn(col) for col in df.columns}
    )

except Exception as e:
    st.error(f"فيه مشكلة في الربط: {e}")