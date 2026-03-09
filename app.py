import streamlit as st
from google import genai

st.set_page_config(page_title="جاكارا | Jakara", page_icon="🔥", layout="centered")

st.title("🔥 جاكارا | Jakara")
st.caption("AI-Powered Arabic Hit Lab")
st.markdown("### من فكرة إلى ديمو وخطة إطلاق خلال دقائق")

API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not API_KEY:
    st.error("مفتاح Gemini غير موجود في Secrets.")
    st.stop()

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

st.markdown("### ✍️ صف لي فكرة الأغنية أو الإحساس")
brief = st.text_area(
    "",
    placeholder="مثال: أغنية حب مفاجئ صيفية شبابية، سهلة وسريعة، مناسبة لتيك توك",
    height=120
)

col1, col2 = st.columns(2)

with col1:
    market = st.selectbox(
        "🌍 اختر السوق",
        ["عربي عام", "الخليج", "مصر", "الشام", "المغرب", "العراق"]
    )

with col2:
    mode = st.selectbox(
        "🎵 اختر الجو",
        ["🔥 Viral TikTok", "❤️ Romantic Pop", "🌑 Dark Mood", "📻 Radio Hit"]
    )

generate = st.button("✨ اصنع الأغنية", use_container_width=True)

def build_prompt(user_brief, market, mode):
    return f"""
أنت خبير A&R عربي ومطور أغانٍ تجارية مخصصة للسوق العربي.

المطلوب: أنشئ أغنية عربية جديدة جاهزة للديمو + جاهزة للتسويق.

اعتمد على:
- ما ينجح عادة في TikTok وYouTube Shorts وInstagram Reels في السوق العربي
- بساطة الهوك
- قابلية التكرار
- هوية مناسبة للسوق المحدد

السوق المستهدف: {market}
الجو المطلوب: {mode}
فكرة المستخدم: {user_brief}

أعد النتيجة بهذا الترتيب الواضح تمامًا، واكتب بالعربية فقط:

## TITLE
عنوان الأغنية

## HOOK
جملة هوك قصيرة جدًا وقوية وقابلة للتكرار

## VIRAL_ANGLE
3 نقاط قصيرة تشرح لماذا قد تنتشر الأغنية على TikTok / Reels / Shorts

## BPM
رقم BPM مناسب

## PRODUCTION_NOTES
وصف مختصر للإيقاع، الجو، نوع التوزيع، والإحساس العام

## LYRICS
اكتب كلمات كاملة ومقسمة هكذا فقط:
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
اكتب فقط style prompt احترافي لسونو بدون كلمات.
يجب أن يتضمن:
- genre
- market flavor
- vocal tone
- BPM feel
- instrumentation
- mix direction

## SUNO_FULL_PROMPT
اكتب prompt كامل لسونو يتضمن:
- style direction
- structure direction
- mood
- hook direction
- ثم lyrics مختصرة/مهيأة لسونو

## MARKETING_IDEAS
اكتب 3 أفكار تسويق قصيرة:
1) فكرة TikTok
2) فكرة Instagram Reel
3) فكرة YouTube Short

لا تضف أي شرح خارج هذه الأقسام.
""".strip()

def extract_section(text, section_name):
    marker = f"## {section_name}"
    start = text.find(marker)
    if start == -1:
        return ""
    start += len(marker)
    next_pos = len(text)
    for sec in [
        "TITLE", "HOOK", "VIRAL_ANGLE", "BPM", "PRODUCTION_NOTES",
        "LYRICS", "SUNO_STYLE_PROMPT", "SUNO_FULL_PROMPT", "MARKETING_IDEAS"
    ]:
        if sec == section_name:
            continue
        idx = text.find(f"## {sec}", start)
        if idx != -1 and idx < next_pos:
            next_pos = idx
    return text[start:next_pos].strip()

if generate:
    if not brief.strip():
        st.warning("يرجى كتابة فكرة الأغنية أولاً.")
        st.stop()

    with st.spinner("جارٍ صناعة الأغنية... 🔥"):
        response = client.models.generate_content(
            model=MODEL,
            contents=build_prompt(brief, market, mode),
            config={"temperature": 0.85}
        )

    result = response.text

    title = extract_section(result, "TITLE")
    hook = extract_section(result, "HOOK")
    viral = extract_section(result, "VIRAL_ANGLE")
    bpm = extract_section(result, "BPM")
    production = extract_section(result, "PRODUCTION_NOTES")
    lyrics = extract_section(result, "LYRICS")
    suno_style = extract_section(result, "SUNO_STYLE_PROMPT")
    suno_full = extract_section(result, "SUNO_FULL_PROMPT")
    marketing = extract_section(result, "MARKETING_IDEAS")

    st.markdown("---")
    st.markdown("## 🎵 Title + Hook")
    st.subheader(title if title else "—")
    st.write(hook if hook else "—")

    st.markdown("## 📈 Viral Angle")
    st.write(viral if viral else "—")

    st.markdown("## 🥁 BPM")
    st.write(bpm if bpm else "—")

    st.markdown("## 🎚 Production Notes")
    st.write(production if production else "—")

    st.markdown("## 🎶 Lyrics")
    st.text_area("Lyrics", lyrics, height=320)

    st.markdown("## 🎧 Suno Style Prompt")
    st.code(suno_style if suno_style else "—", language="text")

    st.markdown("## 🎤 Suno Full Prompt")
    st.code(suno_full if suno_full else "—", language="text")

    st.markdown("## 🎬 Marketing Ideas")
    st.write(marketing if marketing else "—")
