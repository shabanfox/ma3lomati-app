import streamlit as st

# كود الـ CSS لازم يتحط جوه دالة markdown مع خاصية unsafe_allow_html
st.markdown("""
    <style>
        .detailed-location {
            background-color: #fff5f4;
            padding: 20px; /* السطر اللي كان فيه المشكلة */
            border-right: 5px solid #e74c3c;
            border-radius: 5px;
            margin: 10px 0;
        }
    </style>
    
    <div class="detailed-location">
        <b>الموقع بالتفصيل:</b>
        هنا نكتب العنوان اللي جاي من الشيت
    </div>
""", unsafe_allow_html=True)
