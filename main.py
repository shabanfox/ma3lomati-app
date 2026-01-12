# تنظيف أسماء الأعمدة من أي مسافات زائدة
df.columns = [c.strip() for c in df.columns]

if selected == "🏢 المطورين":
    st.markdown("<h2 style='color:#f59e0b; text-align:center; margin-bottom:30px;'>🏢 سجل كبار المطورين العقاريين</h2>", unsafe_allow_html=True)
    
    # التأكد من وجود الأعمدة المطلوبة قبل البدء
    required_cols = ['Developer', 'Owner', 'Detailed_Info']
    if all(col in df.columns for col in required_cols):
        devs = df[required_cols].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        
        # باقي كود العرض...
        s_d = st.text_input("🔍 ابحث عن المطور...")
        # ... تكملة الكود ...
    else:
        st.error(f"⚠️ خطأ في الشيت: الأعمدة المطلوبة غير موجودة. تأكد من تسمية الأعمدة في الشيت بـ: {required_cols}")
        st.info(f"الأعمدة الموجودة حالياً في الشيت الخاص بك هي: {list(df.columns)}")
