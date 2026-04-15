import streamlit as st
from groq import Groq
import PyPDF2

st.set_page_config(page_title="🏆 المساعد الشخصي الشامل", page_icon="🧠", layout="wide")

# ============================================
GROQ_API_KEY = "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"
# ============================================

st.title("🧠 المساعد الشخصي الشامل")
st.markdown("**محادثة ذكية | تحليل ملفات PDF | تحليل مشاعر النصوص**")

tab1, tab2, tab3 = st.tabs(["💬 شات بوت ذكي", "📄 محلل PDF", "😊 محلل المشاعر"])

# ------------------- تبويبة الشات -------------------
with tab1:
    st.subheader("💬 تحدث مع Llama 3.3")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "أهلاً بك! كيف يمكنني مساعدتك اليوم؟"}]
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt := st.chat_input("اكتب سؤالك هنا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                client = Groq(api_key=GROQ_API_KEY)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    temperature=0.7
                )
                full_response = response.choices[0].message.content
                message_placeholder.markdown(full_response)
            except Exception as e:
                full_response = f"❌ خطأ: {e}"
                message_placeholder.error(full_response)
                
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# ------------------- تبويبة PDF -------------------
with tab2:
    st.subheader("📄 اسأل ملف PDF الخاص بك")
    uploaded_file = st.file_uploader("ارفع ملف PDF", type="pdf")
    
    if uploaded_file is not None:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        
        st.success("✅ تم قراءة الملف بنجاح!")
        question = st.text_input("اسأل سؤالاً عن محتوى الملف")
        
        if question:
            with st.spinner("🧠 جاري تحليل الملف والإجابة..."):
                client = Groq(api_key=GROQ_API_KEY)
                prompt = f"أجب عن السؤال التالي بناءً على محتوى الملف:\n\nالمحتوى: {pdf_text[:4000]}\n\nالسؤال: {question}"
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.markdown("### 📌 الإجابة:")
                st.markdown(response.choices[0].message.content)

# ------------------- تبويبة تحليل المشاعر -------------------
with tab3:
    st.subheader("😊 محلل المشاعر الذكي")
    text_input = st.text_area("اكتب النص الذي تريد تحليله:")
    
    if st.button("تحليل المشاعر"):
        if text_input:
            with st.spinner("🧠 جاري التحليل..."):
                client = Groq(api_key=GROQ_API_KEY)
                prompt = f"حلل مشاعر النص التالي واذكر إذا كان: (إيجابي، سلبي، محايد). قدم رداً موجزاً من سطر واحد يبدأ بالحالة ثم شرح بسيط.\n\nالنص: {text_input}"
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.markdown("### 📊 نتيجة التحليل:")
                st.success(response.choices[0].message.content)
