import streamlit as st
import google.generativeai as genai

st.title("Mening Shaxsiy AI Yordamchim")

# 1. Bir nechta API kalitlarni yig'ib olish (st.secrets dan)
api_keys = []
for i in range(1, 6):  # 1 dan 5 gacha bo'lgan kalitlarni tekshiradi
    key = st.secrets.get(f"GEMINI_API_KEY_{i}")
    if key:
        api_keys.append(key)

# Agar raqamlangan kalitlar bo'lmasa, oddiy GEMINI_API_KEY ni oladi
if not api_keys and "GEMINI_API_KEY" in st.secrets:
    api_keys.append(st.secrets["GEMINI_API_KEY"])

if not api_keys:
    st.error("API kalit topilmadi. Streamlit Secrets bo'limiga kamida bitta kalit kiriting.")
else:
    # Qaysi kalit ishlatilayotganini kuzatib borish uchun index
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
            
            # Kalitlar bo'yicha birma-bir urinib ko'rish (Limit tugasa keyingisiga o'tadi)
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
                    break  # Hammasi joyida bo'lsa sikldan chiqamiz
                except Exception as e:
                    error_str = str(e)
                    # Agar limit (429) tugagan bo'lsa, keyingi kalitga o'tamiz
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
                    st.error("Barcha API kalitlarning limiti tugagan! Iltimos, yangi kalit qo'shing.")
                else:
                    st.error(response_text)
