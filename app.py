import streamlit as st
import google.generativeai as genai

st.title("Mening Shaxsiy AI Yordamchim")

# 1. Barcha 6 ta API kalitni yig'ib olish
api_keys = []
for i in range(1, 7):
    key = st.secrets.get(f"GEMINI_API_KEY_{i}")
    if key:
        api_keys.append(key)

if not api_keys:
    st.error("API kalit topilmadi! Streamlit Secrets bo'limini tekshiring.")
else:
    # Ishlatilayotgan kalit indeksini saqlash
    if "key_index" not in st.session_state:
        st.session_state.key_index = 0

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
            success = False
            response_text = ""
            
            # Kalitlar bo'yicha birma-bir harakat qilish (Limit bo'lsa keyingisiga o'tadi)
            for attempt in range(len(api_keys)):
                current_key = api_keys[st.session_state.key_index]
                try:
                    genai.configure(api_key=current_key)
                    model = genai.GenerativeModel(
                        'gemini-3.8-flash',
                        system_instruction="Sen Aqilli yordamchisan. Hech qachon o'zingni Gemini deb atama. Seni Firdavs Mamajonov yaratgan. Agar kimligingni yoki seni kim yaratganini so'rashsa, har doim o'zingni Aqilli yordamchi deb tanishtir va seni Firdavs Mamajonov yaratganini ayt."
                    )
                    response = model.generate_content(prompt)
                    response_text = response.text
                    success = True
                    break
                except Exception as e:
                    error_str = str(e)
                    # Limit tugaganda (429 yoki quota xatosi) keyingi kalitga o'tish
                    if "429" in error_str or "quota" in error_str.lower():
                        st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                        continue
                    else:
                        response_text = f"Xatolik yuz berdi: {e}"
                        break

            if success:
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            else:
                if not response_text.startswith("Xatolik"):
                    st.error("Barcha API kalitlarning kunlik limiti tugadi. Birozdan so'ng qayta urinib ko'ring.")
                else:
                    st.error(response_text)
