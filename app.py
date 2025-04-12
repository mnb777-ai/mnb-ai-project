import streamlit as st
from openai import OpenAI

# إعدادات الصفحة
st.set_page_config(
    page_title="MNB AI Pro",
    page_icon="🤖",
    layout="wide"
)

# إدارة حالة التطبيق
if 'client' not in st.session_state:
    st.session_state.client = None

# الشريط الجانبي للإعدادات
with st.sidebar:
    st.header("⚙️ الإعدادات")
    api_key = st.text_input("أدخل مفتاح OpenAI API", type="password")
    
    if api_key:
        st.session_state.client = OpenAI(api_key=api_key)
        st.success("تم الاتصال بنجاح!")
    else:
        st.warning("الرجاء إدخال المفتاح لتفعيل جميع الميزات")

# الواجهة الرئيسية
st.title("🚀 MNB AI - مساعد الذكاء الاصطناعي المتكامل")
st.markdown("---")

# تبويبات الوظائف
tab1, tab2, tab3 = st.tabs(["💬 الدردشة الذكية", "🎨 توليد الصور", "🎤 تحويل الصوت"])

# تبويب الدردشة
with tab1:
    st.subheader("محادثة مع الذكاء الاصطناعي")
    user_input = st.text_area("اكتب رسالتك هنا...", height=150)
    
    if st.button("إرسال", key="chat_btn") and st.session_state.client:
        with st.spinner("جارٍ معالجة طلبك..."):
            try:
                response = st.session_state.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": user_input}],
                    temperature=0.7
                )
                st.success(response.choices[0].message.content)
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")

# تبويب توليد الصور
with tab2:
    st.subheader("توليد صور بالذكاء الاصطناعي")
    image_prompt = st.text_input("وصف الصورة المطلوبة", placeholder="صورة لشروق الشمس فوق الجبال")
    
    if st.button("توليد الصورة", key="image_btn") and st.session_state.client:
        with st.spinner("جارٍ إنشاء الصورة..."):
            try:
                response = st.session_state.client.images.generate(
                    model="dall-e-3",
                    prompt=image_prompt,
                    size="1024x1024",
                    quality="standard"
                )
                st.image(response.data[0].url, caption=image_prompt)
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")

# تبويب تحويل الصوت
with tab3:
    st.subheader("تحويل الصوت إلى نص")
    audio_file = st.file_uploader("ارفع ملف صوتي (MP3, WAV)", type=["mp3", "wav"])
    
    if audio_file and st.button("تحويل إلى نص", key="audio_btn") and st.session_state.client:
        with st.spinner("جارٍ تحويل الصوت..."):
            try:
                transcript = st.session_state.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                st.write("**النص المقروء:**")
                st.code(transcript.text)
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")

# تذييل الصفحة
st.markdown("---")
st.caption("MNB AI © 2024 | تطبيق ذكاء اصطناعي متكامل | جميع الحقوق محفوظة")