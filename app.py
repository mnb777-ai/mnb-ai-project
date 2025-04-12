import streamlit as st
from openai import OpenAI
import tempfile
import os
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="MNB AI Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# إدارة حالة التطبيق
if 'client' not in st.session_state:
    st.session_state.client = None
    st.session_state.api_key_valid = False
    st.session_state.conversation_history = []

# الشريط الجانبي
with st.sidebar:
    st.title("⚙️ إعدادات API")
    api_key = st.text_input("أدخل مفتاح OpenAI API", type="password", key="api_key")
    
    if st.button("تفعيل المفتاح"):
        if api_key:
            try:
                client = OpenAI(api_key=api_key)
                models = client.models.list()
                available_models = [m.id for m in models.data]
                
                if "gpt-4" in available_models:  # تغيير للنموذج المتاح
                    st.session_state.client = client
                    st.session_state.api_key_valid = True
                    st.success("✅ تم تفعيل المفتاح بنجاح!")
                else:
                    st.error("❌ النموذج غير متاح في حسابك")
            except Exception as e:
                st.error(f"❌ خطأ في المفتاح: {str(e)}")
        else:
            st.warning("⚠️ الرجاء إدخال المفتاح")

# الواجهة الرئيسية
st.title("🤖 MNB AI Assistant")

# تبويبات الوظائف
tab1, tab2, tab3 = st.tabs(["💬 الدردشة", "🎨 توليد الصور", "🎤 تحويل الصوت"])

# تبويب الدردشة
with tab1:
    st.subheader("محادثة مع الذكاء الاصطناعي")
    user_input = st.text_area("اكتب رسالتك هنا...", height=150, key="chat_input")
    
    if st.button("إرسال", key="send_btn") and st.session_state.api_key_valid:
        with st.spinner("جارٍ معالجة طلبك..."):
            try:
                # إضافة رسالة المستخدم للسجل
                st.session_state.conversation_history.append({
                    "role": "user",
                    "content": user_input,
                    "timestamp": datetime.now().isoformat()
                })
                
                response = st.session_state.client.chat.completions.create(
                    model="gpt-4",  # تغيير للنموذج المتاح
                    messages=[{"role": "user", "content": user_input}],
                    temperature=0.7,
                    max_tokens=2000
                )
                
                # استخراج الرد
                ai_response = response.choices[0].message.content
                
                # إضافة رد الذكاء الاصطناعي للسجل
                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": ai_response,
                    "timestamp": datetime.now().isoformat()
                })
                
                st.markdown(f"""
                <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-top: 10px;'>
                    {ai_response}
                </div>
                """, unsafe_allow_html=True)
                
                # خيار لتنزيل سجل المحادثة
                history_text = "\n\n".join(
                    f"{msg['role']} ({msg['timestamp']}):\n{msg['content']}" 
                    for msg in st.session_state.conversation_history
                )
                
                st.download_button(
                    label="حفظ المحادثة",
                    data=history_text,
                    file_name="conversation_history.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")

# باقي التبويبات (الصوت والصورة) تبقى كما هي في الكود السابق...
with tab2:
    st.subheader("توليد صور بالذكاء الاصطناعي")
    image_prompt = st.text_input("وصف الصورة المطلوبة", placeholder="صورة لشروق الشمس فوق الجبال", key="image_prompt")
    
    if st.button("توليد الصورة", key="generate_btn") and st.session_state.api_key_valid:
        with st.spinner("جارٍ إنشاء الصورة (قد يستغرق 20-30 ثانية)..."):
            try:
                response = st.session_state.client.images.generate(
                    model="dall-e-3",
                    prompt=image_prompt,
                    size="1024x1024",
                    quality="hd",
                    style="vivid"
                )
                st.image(response.data[0].url, caption=image_prompt, use_column_width=True)
                st.success("تم توليد الصورة بنجاح!")
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")
                if "content_policy_violation" in str(e):
                    st.warning("الوصف يحتوي على محتوى غير مسموح به")

with tab3:
    st.subheader("تحويل الصوت إلى نص")
    st.info("الحد الأقصى لحجم الملف: 25MB")
    audio_file = st.file_uploader("ارفع ملف صوتي", type=["mp3", "wav", "m4a"], key="audio_uploader")
    
    if audio_file and st.session_state.api_key_valid:
        with st.spinner("جارٍ تحويل الصوت..."):
            try:
                with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp:
                    tmp.write(audio_file.read())
                    tmp.seek(0)
                    
                    transcript = st.session_state.client.audio.transcriptions.create(
                        file=tmp,
                        model="whisper-1",
                        response_format="text"
                    )
                    
                    st.markdown(f"""
                    <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-top: 10px;'>
                        {transcript}
                    </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")

# تذييل الصفحة
st.markdown("---")
st.caption("MNB AI © 2024 - جميع الحقوق محفوظة")
