# --- التعديل في الجزء الخاص بالمقترحات الجانبية ---
with side_c:
    st.markdown("<p style='color:#f59e0b; font-weight:bold;'>🏆 مقترحات</p>", unsafe_allow_html=True)
    
    # بناخد أول 6 صفوف من البيانات المفلترة أو الأصلية
    suggestions = active_df.head(6) 
    
    for idx, s in suggestions.iterrows():
        # جعل اسم المقترح يظهر بشكل مختصر
        short_name = str(s[col_main])[:25]
        
        # تحويل المقترح لزرار شغال
        if st.button(f"📍 {short_name}", key=f"side_{idx}", use_container_width=True):
            st.session_state.current_index = idx
            st.session_state.view = "details"
            st.rerun()
