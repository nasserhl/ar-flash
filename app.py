import streamlit as st
from google import genai

st.set_page_config(page_title="A&R Flash", page_icon="🔥", layout="centered")

st.title("🔥 A&R Flash")
st.caption("AI Trend Scout for Arabic Pop (V1)")

# --- Secrets ---
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not API_KEY:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets. Go to Manage app → Settings → Secrets.")
    st.stop()

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

# --- UI ---
brief = st.text_area(
    "اكتب brief سريع (موضوع/فكرة/جمهور/مزاج):",
    placeholder="مثال: أغنية بوب عربية للشباب 17-24 عن كسر الروتين، طاقة ومرح، مناسبة لتيك توك.",
    height=120
)

col1, col2 = st.columns(2)
with col1:
    n_ideas = st.slider("عدد الأفكار", 5, 20, 10)
with col2:
    temp = st.slider("الـ Temperature", 0.0, 1.0, 0.7)

generate = st.button("⚡ Generate", use_container_width=True)

# --- Prompt template ---
def build_prompt(user_brief: str, ideas: int) -> str:
    return f"""
أنت فريق A&R محترف (Trend Scout + A&R Judge). اكتب بالعربية فقط.

المطلوب:
1) ولّد {ideas} أفكار لأغاني بوب عربية جديدة ومناسبة لتيك توك (للشباب 17-24).
لكل فكرة اكتب:
- Title (عنوان)
- Core Emotion (المشاعر الأساسية)
- Hook sentence (سطر عربي قصير “لازم يعلق”)
- BPM suggestion
- Production vibe (وصف إنتاج/جينرا/إيقاع)

2) بعدها قيّم الأفكار واختر أفضل 3 من ناحية:
TikTok potential / Live performance / Spotify replay
واعطِ لكل واحدة:
- Score من 10 لكل بند (3 بنود)
- سبب سريع
- Production brief مختصر (ملامح توزيع/صوت/هيكل كورس)

الـ Brief من المستخدم:
{user_brief}
""".strip()

if generate:
    if not brief.strip():
        st.warning("اكتب brief صغير قبل ما نولّد الأفكار.")
        st.stop()

    prompt = build_prompt(brief.strip(), n_ideas)

    with st.spinner("عم نطبخ أفكار… 🔥"):
        resp = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config={"temperature": temp}
        )

    st.subheader("النتيجة")
    st.write(resp.text)
