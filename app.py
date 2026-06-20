import streamlit as st
import os
import html
import time
from werkzeug.utils import secure_filename

# إعدادات الصفحة
st.set_page_config(
    page_title="عمر عبدالعزيز الصلاحي | معرض الأعمال",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# الحصول على كلمة المرور من Secrets
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "omar2026")

# CSS للتنسيق
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    
    html, body, [data-testid="stSidebar"], .main {
        font-family: 'Tajawal', sans-serif;
        direction: RTL;
        text-align: right;
    }
    
    .main-title {
        background: linear-gradient(45deg, #FF4B4B, #1E3A8A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #6B7280;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 40px;
    }
    
    .project-card {
        background-color: #f8fafc;
        border-radius: 10px;
        padding: 20px;
        border-right: 5px solid #1E3A8A;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# تهيئة قاعدة البيانات في الذاكرة
if "projects" not in st.session_state:
    st.session_state.projects = []

# الهيدر الرئيسي
st.markdown('<p class="main-title">عمر عبدالعزيز الصلاحي</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">البرمجة وإنشاء المواقع والتطبيقات</p>', unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ لوحة التحكم (خاصة بعمر)")
    st.write("لا يمكن لأحد إضافة محتوى سوى صاحب الموقع.")
    
    password = st.text_input("أدخل كلمة المرور للإضافة:", type="password")
    
    if password == ADMIN_PASSWORD:
        st.success("تم التحقق بنجاح! يمكنك الإضافة الآن.")
        st.subheader("➕ إضافة مشروع جديد")
        
        title = st.text_input("اسم المشروع:")
        desc = st.text_area("وصف المشروع:")
        
        media_type = st.radio("نوع الملف المرفق:", ["بدون", "صورة", "فيديو"])
        
        media_file = None
        if media_type != "بدون":
            media_file = st.file_uploader(f"ارفع ملف الـ {media_type}:", type=["png", "jpg", "jpeg", "mp4", "mov"])
        
        if st.button("نشر المشروع في المعرض ✨"):
            if title and desc:
                media_path = None
                if media_file:
                    os.makedirs("media", exist_ok=True)
                    safe_name = secure_filename(media_file.name)
                    timestamp = int(time.time())
                    media_path = os.path.join("media", f"{timestamp}_{safe_name}")
                    with open(media_path, "wb") as f:
                        f.write(media_file.getbuffer())
                
                st.session_state.projects.append({
                    "title": title,
                    "desc": desc,
                    "media_type": media_type,
                    "media_path": media_path
                })                st.sidebar.balloons()
                st.success("تمت إضافة المشروع بنجاح إلى المعرض!")
            else:
                st.error("الرجاء ملء اسم المشروع ووصفه.")
    elif password != "":
        st.error("كلمة المرور غير صحيحة!")

# عرض المشاريع
st.subheader("📂 معرض المشاريع البرمجية")
st.write("---")

if not st.session_state.projects:
    st.info("المعرض فارغ حالياً. استخدم لوحة التحكم الجانبية بكلمة المرور لإضافة مشاريعك الأولى!")
else:
    for project in reversed(st.session_state.projects):
        with st.container():
            safe_title = html.escape(project['title'])
            safe_desc = html.escape(project['desc'])
            
            st.markdown(f"""
                <div class="project-card">
                    <h3>{safe_title}</h3>
                    <p>{safe_desc}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if project['media_path'] and os.path.exists(project['media_path']):
                if project['media_type'] == "صورة":
                    st.image(project['media_path'], use_container_width=True)
                elif project['media_type'] == "فيديو":
                    st.video(project['media_path'])
            
            st.write("---")
