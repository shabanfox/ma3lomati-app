# 4. التنسيق الجمالي (CSS) - نسخة التباين العالي 2026
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* الحاوية الرئيسية والخلفية */
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ 
        background-color: #000000 !important; /* أسود صريح لزيادة التباين */
        direction: rtl !important; 
        text-align: right !important; 
        font-family: 'Cairo', sans-serif; 
    }}
    
    /* وضوح الكتابة والنصوص العامة */
    p, span, div, label {{ 
        color: #FFFFFF !important; /* أبيض ناصع بدلاً من الرمادي */
        font-weight: 600 !important; 
        font-size: 16px !important;
    }}
    
    /* العناوين الكبيرة */
    h1, h2, h3 {{ 
        color: #f59e0b !important; /* ذهبي ساطع للعناوين */
        font-weight: 900 !important; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}

    /* شريط الأخبار المتحرك */
    .ticker-wrap {{ width: 100%; background: #111; padding: 10px 0; border-bottom: 2px solid #f59e0b; margin-bottom: 20px; }}
    .ticker {{ color: #FFFFFF !important; font-weight: bold; font-size: 15px; }}

    /* الأزرار والكروت (Buttons) */
    div.stButton > button {{ 
        border-radius: 12px !important; 
        font-family: 'Cairo', sans-serif !important; 
        transition: 0.3s !important; 
        border: 1px solid #333 !important;
    }}
    
    /* كروت المشاريع - جعل الخط أسود على خلفية بيضاء للوضوح المطلق */
    div.stButton > button[key*="card_"] {{
        background-color: #ffffff !important; 
        color: #000000 !important; /* خط أسود غامق على خلفية بيضاء */
        min-height: 140px !important; 
        text-align: right !important;
        font-weight: 800 !important; 
        font-size: 17px !important;
        border: 2px solid #f59e0b !important;
    }}
    
    /* الصناديق الذكية (Smart Box) */
    .smart-box {{ 
        background: #111; 
        border: 2px solid #f59e0b; 
        padding: 25px; 
        border-radius: 20px; 
        color: #ffffff !important; 
    }}
    
    /* حقول الإدخال (Inputs) - جعل الكتابة داخلها واضحة */
    .stTextInput input, .stSelectbox div, .stNumberInput input {{
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #f59e0b !important;
        font-weight: bold !important;
    }}
    
    /* تسميات الحقول (Labels) */
    .stSelectbox label, .stTextInput label, .stNumberInput label {{ 
        color: #f59e0b !important; 
        font-weight: 800 !important; 
        font-size: 18px !important;
    }}
    </style>
""", unsafe_allow_html=True)

