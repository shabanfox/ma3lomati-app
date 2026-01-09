# كود صفحة التفاصيل المطور
if st.session_state.page == 'details':
    item = st.session_state.selected_item
    st.markdown(f"<h1 style='color:#003366;'>{item.get('Developer')}</h1>", unsafe_allow_html=True)
    
    # توزيع البيانات في كروت صغيرة
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("المقدم", f"{item.get('Down_Payment')}")
    c2.metric("القسط", f"{item.get('Installments')} سنين")
    c3.metric("الاستلام", f"{item.get('Delivery')}")
    c4.metric("السعر يبدأ", f"{item.get('Price')}")
    
    st.markdown("---")
    st.subheader("💡 معلومات تفصيلية للبروكر")
    st.success(item.get('Detailed_Info', 'لا توجد معلومات إضافية')) # الخانة الجديدة
    
    st.subheader("🏢 سابقة الأعمال والمالك")
    st.write(f"**المشاريع:** {item.get('Projects')}")
    st.write(f"**المالك:** {item.get('Owner')}")
    
    st.subheader("📝 الوصف العام")
    st.info(item.get('Description'))
