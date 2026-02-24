import streamlit as st
from google import genai

st.set_page_config(page_title="جاكارا | Jakara", page_icon="🔥", layout="centered")

st.title("🔥 جاكارا | Jakara")
st.caption("AI-Powered Arabic Hit Lab")

API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not API_KEY:
    st.error("مفتاح Gemini غير موجود في Secrets.")
    st.stop()

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

st.markdown("### ✍️ صف لي إحساس الأغنية أو الفكرة")
brief = st.text_area("", placeholder="مثال: أغنية حب مفاجئ بإحساس صيفي شبابي مناسبة لتيك توك")

st.markdown("### 🎵 اختر الجو")
mode = st.selectbox(
    "",
    ["🔥 فيرال تيك توك", "❤️ رومانسي عاطفي", "🌑 دارك / غامض", "📻 راديو تجاري"]
)

generate = st.button("✨ اصنع أغنيتي", use_container_width=True)

def build_prompt(user_brief, mode):
    return f"""
أنت منتج موسيقي عربي محترف.

المطلوب:
1- ابتكر عنوان جذاب.
2- اكتب كلمات كاملة لأغنية (Verse 1, Pre-Chorus, Chorus, Verse 2, Bridge).
3- اقترح BPM مناسب.
4- اكتب برومبت جاهز لاستخدامه في Suno لإنتاج ديمو احترافي.

الجو المطلوب: {mode}
فكرة المستخدم: {user_brief}

اكتب كل شيء بالعربية.
"""

if generate:
    if not brief.strip():
        st.warning("يرجى كتابة فكرة أولاً.")
        st.stop()

    with st.spinner("جارٍ صناعة الأغنية... 🎶"):
        response = client.models.generate_content(
            model=MODEL,
            contents=build_prompt(brief, mode),
            config={"temperature": 0.8}
        )

    st.markdown("## 🎵 النتيجة")
    st.write(response.text)
