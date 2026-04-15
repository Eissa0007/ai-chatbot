import streamlit as st
from groq import Groq

st.set_page_config(page_title="المساعد الذكي | Groq", page_icon="🤖")

# ============================================
# 🔑 ضع مفتاح Groq API الخاص بك هنا مباشرة
# ============================================
DEFAULT_API_KEY = "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"

# ============================================
# قائمة النماذج المتاحة والمحدثة
# ============================================
AVAILABLE_MODELS = {
    "Llama 3.3 70B (الأقوى - عربي)": "llama-3.3-70b-versatile",
    "Llama 3.1 8B (الأسرع)": "llama-3.1-8b-instant",
    "Qwen 2.5 32B (متعدد اللغات)": "qwen-2.5-32b",
    "DeepSeek R1 70B (تفكير عميق)": "deepseek-r1-distill-llama-70b"
}

# ============================================
# واجهة المستخدم
# ============================================
st.title("🤖 المساعد الذكي | Groq")
st.markdown("مدعوم بأحدث نماذج Groq - سريع ومجاني")

# ============================================
# الشريط الجانبي
# ============================================
with st.sidebar:
    st.header("⚙️ الإعدادات")
    
    # اختيار النموذج
    model_choice = st.selectbox("اختر النموذج", list(AVAILABLE_MODELS.keys()))
    model_name = AVAILABLE_MODELS[model_choice]
    
    st.markdown("---")
    
    # اختيار طريقة إدخال المفتاح
    key_method = st.radio(
        "طريقة إدخال مفتاح API",
        ["استخدام المفتاح المدمج", "إدخال مفتاحي الخاص"],
        help="اختر 'المفتاح المدمج' إذا كنت قد أضفته في الكود"
    )
    
    if key_method == "إدخال مفتاحي الخاص":
        api_key = st.text_input("مفتاح Groq API", type="password", placeholder="gsk_...")
        if not api_key:
            st.warning("⚠️ الرجاء إدخال المفتاح")
        else:
            st.success("✅ تم استخدام مفتاحك")
    else:
        api_key = DEFAULT_API_KEY
        if api_key == "ضع_مفتاح_Groq_هنا":
            st.error("❌ لم تقم بإضافة المفتاح في الكود")
            st.info("💡 قم بتعديل السطر 7 في الملف وأضف مفتاحك")
        else:
            st.success("✅ المفتاح المدمج مفعل")
    
    st.markdown("---")
    st.markdown("### ℹ️ معلومات")
    st.markdown("""
    - **حد مجاني**: 1000 طلب/يوم
    - **سرعة فائقة**
    - **نماذج متنوعة**
    """)
    
    st.markdown("---")
    if st.button("🧹 مسح المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ============================================
# تهيئة سجل المحادثة
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً! أنا مساعدك الذكي المدعوم من Groq. اسألني أي شيء."}
    ]

# ============================================
# عرض الرسائل
# ============================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================
# حقل الإدخال
# ============================================
prompt = st.chat_input("اكتب سؤالك هنا...")

if prompt:
    # التحقق من المفتاح
    if not api_key or api_key == "ضع_مفتاح_Groq_هنا":
        st.error("❌ الرجاء إضافة مفتاح Groq API صحيح في الكود أو اختيار 'إدخال مفتاحي الخاص'")
        st.stop()
    
    # التحقق من صحة المفتاح (يجب أن يبدأ بـ gsk_)
    if not api_key.startswith("gsk_"):
        st.error("❌ المفتاح غير صالح. يجب أن يبدأ بـ 'gsk_'")
        st.stop()
    
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # الرد من المساعد
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            with st.spinner(f"🔄 جاري استخدام {model_choice}..."):
                # إنشاء عميل Groq
                client = Groq(api_key=api_key)
                
                # تجهيز سجل المحادثة للسياق (آخر 6 رسائل)
                messages = []
                for msg in st.session_state.messages[-6:]:
                    role = msg["role"]
                    content = msg["content"]
                    messages.append({"role": role, "content": content})
                
                # استدعاء API
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1024
                )
                
                full_response = response.choices[0].message.content
                
                if not full_response:
                    full_response = "عذراً، لم أحصل على رد. حاول مرة أخرى."
                    
        except Exception as e:
            error_msg = str(e)
            
            if "401" in error_msg or "invalid_api_key" in error_msg.lower():
                full_response = "🔑 المفتاح غير صالح. تأكد من صحته وأنه يبدأ بـ 'gsk_'"
            elif "429" in error_msg or "rate_limit" in error_msg.lower():
                full_response = "⚠️ تم تجاوز الحد اليومي (1000 طلب). جرب غداً."
            elif "decommissioned" in error_msg.lower():
                full_response = "⚠️ هذا النموذج لم يعد متاحاً. اختر نموذجاً آخر من القائمة."
            else:
                full_response = f"❌ حدث خطأ: {error_msg[:150]}"
        
        message_placeholder.markdown(full_response)
    
    # حفظ الرد
    st.session_state.messages.append({"role": "assistant", "content": full_response})                    model="llama-3.3-70b-versatile",
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
