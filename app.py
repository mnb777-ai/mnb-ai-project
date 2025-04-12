import streamlit as st
from openai import OpenAI
import requests
import tempfile
import os

# إعدادات أساسية
st.set_page_config(
    page_title="MNB AI Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# إدارة حالة التطبيق
if 'client' not in st.session_state:
    st.session_state.client = None

# واجهة المستخدم
with st.sidebar:
    st.title("⚙️ إعدادات API")
    api_key = st.text_input("أدخل مفتاح OpenAI API", type="password")
    
    if st.button("تفعيل المفتاح"):
        if api_key:
            try:
                test_client = OpenAI(api_key=api_key)
                test_client.models.list()  # اختبار اتصال
                st.session_state.client = test_client
                st.success("تم التفعيل بنجاح!")
            except Exception as e:
                st.error(f"خطأ في المفتاح: {str(e)}")
        else:
            st.warning("الرجاء إدخال المفتاح")

st.title("🤖 MNB AI Assistant")

# تبويبات الوظائف
tab1, tab2 = st.tabs(["💬 الدردشة", "🎤 تحويل الصوت"])

with tab1:
    st.subheader("محادثة مع GPT-4")
    prompt = st.text_area("اكتب رسالتك هنا...")
    
    if st.button("إرسال") and st.session_state.client:
        try:
            response = st.session_state.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")

with tab2:
    st.subheader("تحويل الصوت إلى نص")
    audio_file = st.file_uploader("ارفع ملف صوتي", type=["mp3", "wav"])
    
    if audio_file and st.session_state.client:
        with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp:
            tmp.write(audio_file.read())
            try:
                transcript = st.session_state.client.audio.transcriptions.create(
                    file=open(tmp.name, "rb"),
                    model="whisper-1"
                )
                st.write(transcript.text)
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")

st.caption("MNB AI © 2024 - جميع الحقوق محفوظة")
