import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="دليل المشاريع العقارية", layout="wide")

# 2. إضافة كود CSS لتنسيق الكروت (داخل دالة markdown)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .project-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #eee;
        margin-bottom: 20px;
        height: 100%;
    }
    
    .project-name {
        color: #2c3e50;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .project-area {
        color: #7f8c8d;
        font-size: 1rem;
        margin-bottom: 15px;
    }
    
    /* الخانة الجديدة التي طلبتها: Detailed Location */
    .detailed-location {
        background-color: #fff5f4;
        padding: 15px;
        border-right: 5px solid #e74c3c;
        border-radius: 8px;
        font-size: 0.9rem;
        color: #555;
        line-height: 1.6;
    }
    
    .loc-label {
        display: block;
        color: #e74c3c;
        font-weight: bold;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# 3. محاكاة بيانات الشيت (يمكنك استبدال هذا الجزء بقراءة ملف Excel)
# df = pd.read_excel("projects.xlsx")
data = {
    'Project Name': ['SouthMed', 'Mivida', 'O West', 'Il Bosco'],
    'Area': ['الساحل الشمالي', 'القاهرة الجديدة', 'أكتوبر والشيخ زايد', 'العاصمة الإدارية'],
    'Detailed Location': [
        'سيدي عبد الرحمن، الكيلو 165 طريق إسكندرية مطروح بجوار الضبعة.',
        'التجمع الخامس، مباشرة على شارع التسعين الجنوبي بجوار الجامعة الأمريكية.',
        'طريق الواحات، خلف مدينة الإنتاج الإعلامي ومول مصر.',
        'منطقة المستثمرين، مباشرة على محور بن زايد الجنوبي.'
    ]
}
df = pd.DataFrame(data)

# 4. واجهة التطبيق
st.title("🏡 منصة معلومات المشاريع العقارية")
st.write("عرض تفصيلي لبيانات الـ 1000 مشروع")

# محرك بحث بسيط
search_query = st.text_input("ابحث باسم المشروع أو المنطقة...", "")

filtered_df = df[
    df['Project Name'].str.contains(search_query, case=False) | 
    df['Area'].str.contains(search_query, case=False)
]

# 5. عرض المشاريع في كروت (Grid System)
cols = st.columns(3) # عرض 3 كروت في كل صف

for index, row in filtered_df.iterrows():
    with cols[index % 3]:
        st.markdown(f"""
        <div class="project-card">
            <div class="project-name">{row['Project Name']}</div>
            <div class="project-area">📍 {row['Area']}</div>
            <div class="detailed-location">
                <span class="loc-label">الموقع بالتفصيل:</span>
                {row['Detailed Location']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("") # مسافة بسيطة
