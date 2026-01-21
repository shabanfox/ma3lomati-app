import streamlit as st
# سنضيف هذا السطر في البداية (تحتاج لتثبيتها: pip install streamlit-autorefresh)
from streamlit_autorefresh import st_autorefresh

# 1. تحديث الصفحة كل ثانية لتحديث الساعة تلقائياً
st_autorefresh(interval=1000, key="datetimerefresh")

# ... (باقي كود التعريفات والـ CSS كما هو) ...

# 3. إعداد الوقت المصري الحالي
egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)
current_time = egypt_now.strftime('%I:%M:%S %p') # الساعة مع الثواني
current_date = egypt_now.strftime('%Y-%m-%d')

# --- الجزء الخاص بالهيدر العلوي (التعديل المطلوب) ---
# تقسيم الهيدر لثلاثة أعمدة: واحد لليوزر، واحد للساعة، واحد لزر الخروج
c_h1, c_h2, c_h3 = st.columns([0.5, 0.35, 0.15])

with c_h1:
    st.markdown(f"<div style='color:#888; padding-top:10px; font-weight:bold;'>👤 {st.session_state.current_user}</div>", unsafe_allow_html=True)

with c_h2:
    # عرض التاريخ والساعة بجانب بعض بتنسيق ذهبي فخم
    st.markdown(f"""
        <div style='text-align: left; padding-top: 5px;'>
            <span style='color: #f59e0b; font-size: 18px; font-weight: 900; font-family: monospace;'>🕒 {current_time}</span>
            <span style='color: #444; margin: 0 10px;'>|</span>
            <span style='color: #aaa; font-size: 14px;'>📅 {current_date}</span>
        </div>
    """, unsafe_allow_html=True)

with c_h3:
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("Logout"): 
        st.session_state.auth = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------

# ثم يكمل الكود باقي تصميم الهيدر الصوري (الصورة اللي في الخلفية)
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 180px; background-size: cover; background-position: center; border-radius: 25px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 5px solid #f59e0b; margin-top:10px;">
        <h1 style="color: white; margin: 0; font-size: 50px; font-weight:900;">KMT PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-size: 18px;">EGYPT REAL ESTATE INTELLIGENCE</p>
    </div>
""", unsafe_allow_html=True)
