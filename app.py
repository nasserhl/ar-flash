import streamlit as st
from google import genai

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="جاكارا | Jakara",
    page_icon="🔥",
    layout="centered"
)

# -----------------------------
# Secrets / API
# -----------------------------
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not API_KEY:
    st.error("مفتاح Gemini غير موجود في Secrets.")
    st.stop()

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

# -----------------------------
# UI Header
# -----------------------------
st.title("🔥 جاكارا | Jakara")
st.caption("AI-Powered Arabic Hit Lab")
st.markdown("### من فكرة إلى ديمو وخطة إطلاق خلال دقائق")

# -----------------------------
# Inputs
# -----------------------------
st.markdown("### ✍️ صف لي فكرة الأغنية أو الإحساس")
brief = st.text_area(
    "",
    placeholder="مثال: أغنية حب مفاجئ صيفية شبابية، سهلة وسريعة، مناسبة لتيك توك",
    height=120
)

col1, col2, col3 = st.columns(3)

with col1:
    market = st.selectbox(
        "🌍 السوق",
        ["عربي عام", "الخليج", "مصر", "الشام", "المغرب", "العراق"]
    )

with col2:
    voice_type = st.selectbox(
        "🎤 نوع الأداء",
        ["محايد", "مغني", "مغنية", "ديو"]
    )

with col3:
    mode = st.selectbox(
        "🎵 الجو",
        ["🔥 Viral TikTok", "❤️ Romantic Pop", "🌑 Dark Mood", "📻 Radio Hit"]
    )

generate = st.button("✨ اصنع الأغنية", use_container_width=True)

# -----------------------------
# Prompt builder
# -----------------------------
def build_prompt(user_brief: str, market: str, mode: str, voice_type: str) -> str:
    return f"""
أنت خبير A&R عربي ومطور أغانٍ تجارية مخصصة للسوق العربي.

مهمتك أن تبني أغنية عربية جديدة جاهزة كديمو أولي، بشكل مناسب للسوق المطلوب.

المعطيات:
- السوق المستهدف: {market}
- نوع الأداء: {voice_type}
- الجو العام: {mode}
- فكرة المستخدم: {user_brief}

التعليمات:
- اكتب بالعربية فقط
- اجعل النتيجة واضحة ومقسمة
- افصل الكلمات عن برومبتات سونو
- استند إلى منطق السوق العربي وما ينجح عادة على TikTok / Reels / Shorts
- لا تدّعِ أنك قرأت بيانات حية من الإنترنت
- قدم تحليل سوق مبسط مبني على فهم السوق، لا على بيانات مباشرة

أعد النتيجة بالأقسام التالية فقط وبنفس الترتيب:

## MARKET_SNAPSHOT
3 نقاط قصيرة عن ملامح هذا السوق: نوع الموضوعات الجاذبة، طبيعة الهوك، والإحساس العام المناسب.

## TITLE
عنوان جذاب للأغنية.

## HOOK
جملة هوك قصيرة جدًا وقابلة للتكرار.

## VIRAL_ANGLE
3 نقاط قصيرة تشرح لماذا قد تكون الأغنية قابلة للانتشار.

## BPM
رقم BPM مناسب.

## PRODUCTION_NOTES
وصف مختصر للإيقاع، نوع التوزيع، الإحساس، والجو العام.

## LYRICS
اكتب كلمات كاملة ومقسمة بالشكل التالي فقط:
Verse 1:
...
Pre-Chorus:
...
Chorus:
...
Verse 2:
...
Bridge:
...

## SUNO_STYLE_PROMPT
اكتب فقط برومبت ستايل احترافي لسونو بدون أي كلمات أغنية نهائيًا.
يجب أن يتضمن فقط:
- genre
- regional flavor
- vocal tone
- BPM feel
- instrumentation
- energy
- mix direction
- arrangement feel

## SUNO_DIRECTION_PROMPT
اكتب برومبت توجيهي متقدم لسونو بدون كلمات الأغنية.
يجب أن يتضمن:
- style direction
- structure direction
- mood direction
- vocal direction
- hook feel
- arrangement direction
- sonic references

## MARKETING_IDEAS
اكتب 3 أفكار تسويق قصيرة:
1) فكرة TikTok
2) فكرة Instagram Reel
3) فكرة YouTube Short

لا تضف أي أقسام إضافية.
""".strip()


# -----------------------------
# Section extractor
# -----------------------------
SECTION_NAMES = [
    "MARKET_SNAPSHOT",
    "TITLE",
    "HOOK",
    "VIRAL_ANGLE",
    "BPM",
    "PRODUCTION_NOTES",
    "LYRICS",
    "SUNO_STYLE_PROMPT",
    "SUNO_DIRECTION_PROMPT",
    "MARKETING_IDEAS"
]

def extract_section(text: str, section_name: str) -> str:
    marker = f"## {section_name}"
    start = text.find(marker)
    if start == -1:
        return ""
    start += len(marker)

    next_pos = len(text)
    for sec in SECTION_NAMES:
        if sec == section_name:
            continue
        idx = text.find(f"## {sec}", start)
        if idx != -1 and idx < next_pos:
            next_pos = idx

    return text[start:next_pos].strip()

# -----------------------------
# Generate result
# -----------------------------
if generate:
    if not brief.strip():
        st.warning("يرجى كتابة فكرة الأغنية أولاً.")
        st.stop()

    prompt = build_prompt(brief.strip(), market, mode, voice_type)

    with st.spinner("🔥 جارٍ صناعة الأغنية..."):
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config={"temperature": 0.85}
        )

    result = response.text

    market_snapshot = extract_section(result, "MARKET_SNAPSHOT")
    title = extract_section(result, "TITLE")
    hook = extract_section(result, "HOOK")
    viral_angle = extract_section(result, "VIRAL_ANGLE")
    bpm = extract_section(result, "BPM")
    production_notes = extract_section(result, "PRODUCTION_NOTES")
    lyrics = extract_section(result, "LYRICS")
    suno_style_prompt = extract_section(result, "SUNO_STYLE_PROMPT")
    suno_direction_prompt = extract_section(result, "SUNO_DIRECTION_PROMPT")
    marketing_ideas = extract_section(result, "MARKETING_IDEAS")

    st.markdown("---")

    st.markdown("## 📊 Market Snapshot")
    st.write(market_snapshot if market_snapshot else "—")

    st.markdown("## 🎵 Title + Hook")
    st.subheader(title if title else "—")
    st.write(hook if hook else "—")

    st.markdown("## 📈 Viral Angle")
    st.write(viral_angle if viral_angle else "—")

    st.markdown("## 🥁 BPM")
    st.write(bpm if bpm else "—")

    st.markdown("## 🎚 Production Notes")
    st.write(production_notes if production_notes else "—")

    st.markdown("## 🎶 Lyrics")
    st.text_area("Lyrics", value=lyrics, height=320)

    st.markdown("## 📋 Copy Lyrics")
    st.code(lyrics if lyrics else "—", language="text")

    st.markdown("## 🎧 Suno Style Prompt")
    st.code(suno_style_prompt if suno_style_prompt else "—", language="text")

    st.markdown("## 🎛 Suno Direction Prompt")
    st.code(suno_direction_prompt if suno_direction_prompt else "—", language="text")

    st.markdown("## 🎬 Marketing Ideas")
    st.write(marketing_ideas if marketing_ideas else "—")
