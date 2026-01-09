# --- صفحة التفاصيل (تعديل الألوان لتطابق الرئيسية) ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    
    # حاوية الصفحة بالكامل
    st.markdown('<div style="direction: rtl; text-align: right;">', unsafe_allow_html=True)
    
    # زر العودة بتنسيق بسيط
    if st.button("⬅️ عودة للقائمة الرئيسية"): 
        st.session_state.page = 'main'
        st.rerun()
    
    # هيدر الشركة بنفس لون البراند الكحلي
    st.markdown(f"""
        <div style="background-color: #003366; padding: 25px; border-radius: 12px; margin-bottom: 20px; text-align: center;">
            <h1 style="color: white; margin: 0; font-family: 'Cairo', sans-serif;">{item.get('Developer')}</h1>
            <p style="color: #cbd5e1; margin-top: 10px;">{item.get('Projects', 'مشاريع متميزة')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # عرض المعلومات في كروت "بيضاء" بنفس ستايل الصفحة الرئيسية
    st.markdown(f"""
        <div class="project-card-container" style="background-color: white; padding: 20px; display: block; border-right: 6px solid #003366;">
            <h3 style="color: #003366; border-bottom: 1px solid #eee; padding-bottom: 10px;">💡 الزتونة الفنية (للمستشار العقاري)</h3>
            <p style="font-size: 1.1rem; line-height: 1.8; color: #1e293b;">
                {item.get('Detailed_Info', 'لا توجد معلومات إضافية متوفرة حالياً.')}
            </p>
        </div>
        
        <div class="project-card-container" style="background-color: white; padding: 20px; display: block; border-right: 6px solid #D4AF37;">
            <h3 style="color: #003366; border-bottom: 1px solid #eee; padding-bottom: 10px;">📊 بيانات المطور والمشروع</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <p><b>👤 المالك:</b> {item.get('Owner', '-')}</p>
                <p><b>📍 المنطقة:</b> {item.get('Area', '-')}</p>
                <p><b>💰 السعر:</b> {item.get('Price', '-')}</p>
                <p><b>⏳ التقسيط:</b> {item.get('Installments', '-')}</p>
                <p><b>🕒 الاستلام:</b> {item.get('Delivery', '-')}</p>
                <p><b>🏗️ النوع:</b> {item.get('Type', '-')}</p>
            </div>
            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
            <p><b>📝 وصف عام:</b><br>{item.get('Description', '-')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
