import streamlit as st
from google import genai

st.set_page_config(page_title="AI Assistant", page_icon="🤖")

st.title("🤖 Mening Shaxsiy AI Yordamchim")
st.write("Istalgan savolingizni bering, internet va Gemini AI orqali aniq javob topib beradi!")

# Streamlit maxfiy xotirasidan API kalitni olish
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

if api_key:
    client = genai.Client(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Oldingi xabarlarni chiqarish
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Foydalanuvchi xabar kiritganda
    if prompt := st.chat_input("Savolingizni yozing..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("O'ylamoqda va qidirmoqda..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config={
                            "tools": [{"google_search": {}}]
                        }
                    )
                    bot_response = response.text
                except Exception as e:
                    bot_response = f"Xatolik yuz berdi: {e}"

                st.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
else:
    st.warning("⚠️ API kalit topilmadi! Iltimos, Streamlit sozlamalariga API kalitingizni kiriting (2-qadamga qarang).")
