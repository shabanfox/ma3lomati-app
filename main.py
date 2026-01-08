import streamlit as st
import pandas as pd

# 1. إعدادات المنصة
st.set_page_config(page_title="رادار القاهرة الجديدة", layout="wide", page_icon="🏢")

# رابط جوجل شيت الجديد الخاص بك (تم تحويله لصيغة التحميل المباشر)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrbBIxAKkX8ltCSfCTZ7S-E83MPBu4XClC4FLRzvGhZPoHoOgaFOfN2MUm1scyeZRAyT32yxSZy1R2/pub?output=xlsx"

@st.cache_data(ttl=60)
def get_data():
    # قراءة البيانات من الرابط الجديد
    df = pd.read_excel(SHEET_URL)
    # تنظيف أسماء الأعمدة من أي مسافات زائدة
    df.columns = df.columns.str.strip()
    return df

# 2. تنسيق الواجهة (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; }
    .search-box { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .project-card { background: white; padding: 20px; border-radius: 12px; border-right: 8px solid #002B5B; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; direction: rtl; }
    .price-tag { color: #27ae60; font-weight: bold; font-size: 1.3em; }
    .label { color: #666; font-size: 0.85em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

try:
    df = get_data()
    
    st.markdown("<h1 style='text-align: center; color: #002B5B;'>🏙️ رادار معلومات القاهرة الجديدة</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>أداة البحث الذكية عن المطورين والمشاريع</p>", unsafe_allow_html=True)
    st.write("---")

    # 3. لوحة التحكم الثلاثية (The 3 Filters)
    with st.container():
        st.markdown('<div class="search-box">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        
        with c1:
            search_main = st.text_input("🏢 المطور أو المشروع", placeholder="ابحث باسم الشركة أو المشروع...")
        with c2:
            # التأكد من وجود عمود نوع الوحدة
            if 'نوع الوحدة' in df.columns:
                unit_types = ["الكل"] + sorted(list(df['نوع الوحدة'].dropna().unique()))
                selected_type = st.selectbox("🏠 نوع الوحدة", unit_types)
            else:
                st.warning("عمود 'نوع الوحدة' غير موجود")
                selected_type = "الكل"
        with c3:
            price_search = st.text_input("💰 ميزانية السعر", placeholder="ابحث بسعر معين...")
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. منطق الفلترة (Filtering Logic)
    filtered_df = df.copy()

    if search_main:
        # البحث في المطور واسم المشروع
        mask = (filtered_df['المطور'].astype(str).str.contains(search_main, case=False, na=False)) | \
               (filtered_df['اسم المشروع'].astype(str).str.contains(search_main, case=False, na=False))
        filtered_df = filtered_df[mask]
    
    if selected_type != "الكل":
        filtered_df = filtered_df[filtered_df['نوع الوحدة'] == selected_type]
        
    if price_search:
        filtered_df = filtered_df[filtered_df['السعر'].astype(str).str.contains(price_search, na=False)]

    # 5. عرض النتائج بشكل "موسوعة"
    st.subheader(f"🔍 النتائج المتاحة: ({len(filtered_df)})")

    if filtered_df.empty:
        st.info("لا توجد نتائج تطابق بحثك حالياً.")
    else:
        for _, row in filtered_df.iterrows():
            with st.container():
                st.markdown(f"""
                    <div class="project-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h2 style="margin:0; color:#002B5B;">{row.get('اسم المشروع', '-')}</h2>
                            <span style="background:#eef2ff; color:#002B5B; padding:5px 15px; border-radius:15px; font-weight:bold;">{row.get('المنطقة', '-')}</span>
                        </div>
                        <p style="margin: 10px 0; font-size: 1.1em;"><b>المطور العقاري:</b> {row.get('المطور', '-')}</p>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top: 15px; background: #fcfcfc; padding: 15px; border-radius: 8px; border: 1px solid #eee;">
                            <div><span class="label">نوع الوحدة</span><br>{row.get('نوع الوحدة', '-')}</div>
                            <div><span class="label">نظام السداد</span><br>{row.get('نظام السداد', '-')}</div>
                            <div><span class="label">إجمالي السعر</span><br><span class="price-tag">{row.get('السعر', '-')}</span></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل البيانات. تأكد من تطابق أسماء الأعمدة في الإكسيل (المطور، اسم المشروع، المنطقة، نوع الوحدة، السعر، نظام السداد).")
    st.write(f"تفاصيل الخطأ التقني: {e}")
