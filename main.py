# --- صفحة التفاصيل الفنية المحدثة ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    
    # زر العودة بتنسيق شيك
    if st.button("🔙 العودة للموسوعة"): 
        st.session_state.page = 'main'
        st.rerun()
    
    # الهيدر بنفس لون البراند الكحلي
    st.markdown(f"""
        <div style="background-color: #003366; padding: 20px; border-radius: 12px; margin-bottom: 25px; text-align: center;">
            <h1 style="color: white; margin: 0; font-family: 'Cairo', sans-serif;">{item.get('Developer')}</h1>
            <p style="color: #cbd5e1; margin-top: 10px;">{item.get('Projects')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # عرض الأرقام الأساسية في كروت واضحة (نفس ستايل الصفحة الرئيسية)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='main-card' style='text-align:center;'><b>المقدم</b><br><span style='color:#003366; font-size:1.2rem;'>{item.get('Down_Payment')}</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='main-card' style='text-align:center;'><b>سنين القسط</b><br><span style='color:#003366; font-size:1.2rem;'>{item.get('Installments')} سنين</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='main-card' style='text-align:center;'><b>السعر يبدأ</b><br><span style='color:#003366; font-size:1.2rem;'>{item.get('Price')}</span></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='main-card' style='text-align:center;'><b>الاستلام</b><br><span style='color:#003366; font-size:1.2rem;'>{item.get('Delivery')}</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # تقسيم المحتوى (المعلومات التفصيلية والوصف)
    c_right, c_left = st.columns([2, 1])
    
    with c_right:
        st.markdown("### 💡 الزتونة الفنية (للبـروكـر)")
        # استخدام لون خلفية هادي يتماشى مع الصفحة الرئيسية
        st.markdown(f"""
            <div style="background-color: #e2e8f0; padding: 20px; border-radius: 10px; border-right: 5px solid #003366; color: #1e293b; line-height: 1.6;">
                {item.get('Detailed_Info', 'لا توجد معلومات إضافية حالياً')}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📝 وصف المطور")
        st.write(item.get('Description'))

    with c_left:
        st.markdown("### 🏢 بيانات الإدارة")
        st.markdown(f"""
            <div style="background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0;">
                <p><b>👤 المالك:</b> {item.get('Owner')}</p>
                <p><b>📍 المنطقة:</b> {item.get('Area')}</p>
                <p><b>🏗️ النوع:</b> {item.get('Type')}</p>
                <p><b>💰 أقل قيمة:</b> {item.get('Min_Val')}</p>
            </div>
        """, unsafe_allow_html=True)
