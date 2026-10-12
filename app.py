import Streamlite gr
import datetime

def calculate_math(text):
    expr = text.replace(' ', '')
    if any(op in expr for op in ['+', '-', '*', '/']) and all(c in "0123456789+-*/()." for c in expr):
        try:
            return f"🧮 Hisoblash natijasi: {text} = {eval(expr)}"
        except:
            pass
    return None

def answer_question(text):
    t = text.lower().strip()

    if "salom" in t or "assalomu alaykum" in t:
        return "Salom! Nima yordam kerak?"

    qa_base = {
        "matematika nima": "Matematika — miqdorlar, tuzilmalar, fazo va o'zgarishlarni o'rganadigan aniq fan.",
        "pifagor teoremasi": "Pifagor teoremasi: To'g'ri burchakli uchburchakda gipotenuzaning kvadrati katetlarning kvadratlari yig'indisiga teng (a² + b² = c²).",
        "tenglama nima": "Tenglama — noaniq miqdorni topish talab qilinadigan tenglikdir.",
        "tub sonlar": "Tub sonlar — faqat 1 ga va o'ziga bo'linadigan 1 dan katta butun sonlar (2, 3, 5, 7, 11...).",
        "pi soni": "Pi soni (π) — aylananing uzunligini uning diametriga nisbatidir. Taxminan 3.14159.",
        "foiz nima": "Foiz — sonning yuzdan bir qismi (1% = 1/100).",
        "python nima": "Python — sodda va kuchli dasturlash tili.",
        "sun'iy intellekt": "Sun'iy intellekt (AI) — kompyuterlarning inson kabi fikrlashi.",
        "o'zbekiston poytaxti": "O'zbekistonning poytaxti — Toshkent.",
        "isming nima": "🤖 Men sizning shaxsiy AI yordamchingizman!",
    }

    for key, answer in qa_base.items():
        if key in t:
            return answer

    if "soat" in t or "vaqt" in t:
        return f"⏰ Hozirgi vaqt: {datetime.datetime.now().strftime('%H:%M:%S')}"

    if "sana" in t or "bugun" in t:
        return f"📅 Bugungi sana: {datetime.datetime.now().strftime('%Y-%m-%d')}"

    return f"💡 \"{text}\" haqida bazamda ma'lumot topilmadi. Boshqa savol bering!"

def chat_response(message, history):
    response = calculate_math(message) or answer_question(message)
    return response

demo = gr.ChatInterface(
    fn=chat_response,
    title="🤖 Mening AI Yordamchim",
    description="Salom! Menga savol bering yoki misol yechishni so'rang.",
    examples=["salom", "2+2", "python nima", "soat nechchi", "o'zbekiston poytaxti"]
)

demo.launch()
