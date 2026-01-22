import streamlit as st
import pandas as pd

# --- وظيفة جلب البيانات (تأكد أن رابط الـ CSV صحيح) ---
@st.cache_data(ttl=60)
def load_launches():
    URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        df = pd.read_csv(URL_LAUNCHES).fillna("---")
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

# --- قسم اللونشات المطور ---
if menu == "اللونشات":
    if st.session_state.selected_launch is not None:
        item = st.session_state.selected_launch
        
        # زر العودة
        if st.button("⬅️ عودة لجميع اللونشات"):
            st.session_state.selected_launch = None
            st.rerun()
        
        # تصميم صفحة تفاصيل اللونش الشاملة
        st.markdown(f"""
            <div style="background: #161616; padding: 30px; border-radius: 20px; border-right: 8px solid #f59e0b; text-align: right;">
                <h1 style="color: #f59e0b; margin-bottom: 5px;">{item.get('Project', 'مشروع جديد')}</h1>
                <h3 style="color: #eee;">🏢 المطور: {item.get('Developer', '---')}</h3>
                <hr style="border-color: #333;">
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <p style="color: #f59e0b; font-weight: bold; margin-bottom: 5px;">📍 الموقع</p>
                        <p style="font-size: 18px;">{item.get('Location', '---')}</p>
                    </div>
                    <div>
                        <p style="color: #f59e0b; font-weight: bold; margin-bottom: 5px;">💰 مبلغ جدية الحجز (EOI)</p>
                        <p style="font-size: 22px; font-weight: bold; color: #00ff00;">{item.get('EOI', '---')}</p>
                    </div>
                    <div>
                        <p style="color: #f59e0b; font-weight: bold; margin-bottom: 5px;">📐 أنواع الوحدات والمساحات</p>
                        <p style="font-size: 18px;">{item.get('Types', item.get('المساحات', '---'))}</p>
                    </div>
                    <div>
                        <p style="color: #f59e0b; font-weight: bold; margin-bottom: 5px;">💵 متوسط الأسعار</p>
                        <p style="font-size: 18px;">{item.get('Prices', item.get('الأسعار', '---'))}</p>
                    </div>
                    <div>
                        <p style="color: #f59e0b; font-weight: bold; margin-bottom: 5px;">💳 أنظمة السداد</p>
                        <p style="font-size: 18px;">{item.get('Payment', item.get('السداد', '---'))}</p>
                    </div>
                    <div>
                        <p style="color: #f59e0b; font-weight: bold; margin-bottom: 5px;">📅 تاريخ اللونش المتوقع</p>
                        <p style="font-size: 18px;">{item.get('Date', item.get('التاريخ', '---'))}</p>
                    </div>
                </div>
                
                <div style="margin-top: 30px; padding: 20px; background: #222; border-radius: 10px;">
                    <p style="color: #f59e0b; font-weight: bold;">📝 ملاحظات وتفاصيل إضافية:</p>
                    <p style="color: #ccc; line-height: 1.6;">{item.get('Notes', 'لا توجد ملاحظات إضافية متاحة حالياً.')}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # إضافة زر خارجي لو فيه لينك بروشور
        brochure_link = item.get('Brochure', item.get('الرابط', '---'))
        if brochure_link != "---":
            st.link_button("📂 تحميل البروشور / الصور", brochure_link, use_container_width=True)

    else:
        # عرض الشبكة (Grid) كما هي في الكود السابق
        st.markdown("<h2 style='text-align: center; color: white;'>🚀 أحدث انطلاقات 2026</h2>", unsafe_allow_html=True)
        df_l = load_launches()
        if not df_l.empty:
            cols = st.columns(3)
            for index, row in df_l.iterrows():
                with cols[index % 3]:
                    label = f"🏢 {row.get('Developer', 'مطور')}\n{row.get('Project', 'مشروع')}\n📍 {row.get('Location', '---')}"
                    if st.button(label, key=f"lnch_{index}"):
                        st.session_state.selected_launch = row
                        st.rerun()
