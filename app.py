import streamlit as st
import google.generativeai as genai

st.title("Mening Shaxsiy AI Yordamchim")
st.write("Istalgan savolingizni bering, internet va Gemini AI orqali aniq javob topib beradi!")

# API kalitni o'qib olish
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API kalit topilmadi. Streamlit Secrets bo'limiga GEMINI_API_KEY joylang.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.8-flash')

    # Chat tarixini saqlash
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Foydalanuvchi savoli
    if prompt := st.chat_input("Savolingizni yozing..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Xatolik yuz berdi: {e}")
