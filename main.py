# 7. جلب البيانات (مع تعديل الدمج الذكي)
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        
        # تنظيف العناوين
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        
        # --- عملية الدمج الذكي للمطورين ---
        if 'Developer' in p.columns:
            # مسح أي مسافات زيادة وتوحيد النص
            p['Developer'] = p['Developer'].astype(str).apply(lambda x: " ".join(x.split()).strip())
        
        if 'Developer' in d.columns:
            d['Developer'] = d['Developer'].astype(str).apply(lambda x: " ".join(x.split()).strip())
            # حذف المطور المكرر في شيت المطورين
            d = d.drop_duplicates(subset=['Developer'], keep='first')

        # --- عملية الدمج الذكي للمشاريع ---
        if 'Project Name' in p.columns:
            p['Project Name'] = p['Project Name'].astype(str).apply(lambda x: " ".join(x.split()).strip())
            # لو اسم المشروع والمطور متطابقين، امسح المكرر وخلي نسخة واحدة
            p = p.drop_duplicates(subset=['Project Name', 'Developer'], keep='first')
            
        return p, d
    except: 
        return pd.DataFrame(), pd.DataFrame()
