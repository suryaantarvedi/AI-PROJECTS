import html
import json
import re

import requests
import streamlit as st

st.set_page_config(
    page_title="Review Analyzer",
    page_icon="🤖",
    layout="centered",
)

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"

# ---------------------------------------------------------------------------
# Styling (Streamlit + custom CSS only)
# ---------------------------------------------------------------------------
CSS = """
<style>
:root {
    --ivory: #FAF7F2;
    --ivory-deep: #F3EDE3;
    --white: #FFFFFF;
    --amber: #D99A65;
    --amber-soft: #F8EBDD;
    --amber-dark: #B97C47;
    --sage: #78947A;
    --sage-soft: #E8EFE8;
    --coral: #D9877D;
    --coral-soft: #F9E8E5;
    --charcoal: #55504A;
    --charcoal-soft: #8A837A;
    --border: #E8E1D5;
    --shadow: 0 2px 10px rgba(85, 80, 74, 0.07);
}

/* ---------- Base ---------- */
.stApp { background-color: var(--ivory); color: var(--charcoal); }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stHeader"] * { color: var(--charcoal) !important; }
.block-container {
    max-width: 960px;
    padding-top: 2.2rem;
    padding-bottom: 5rem;
}
html, body, [class*="css"] { color: var(--charcoal); }
p, label, span, li { color: var(--charcoal); }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background-color: var(--ivory-deep);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--charcoal); }
.side-title { font-size: 21px; font-weight: 700; color: var(--charcoal); margin: 0; }
.side-sub { font-size: 13.5px; color: var(--charcoal-soft); margin: 2px 0 14px 0; }
.side-divider { height: 1px; background: var(--border); margin: 6px 0 18px 0; }

/* ---------- Hero ---------- */
.hero { text-align: center; padding: 6px 8px 22px 8px; }
.model-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--white); color: var(--charcoal);
    border: 1px solid var(--border); border-radius: 999px;
    padding: 6px 14px; font-size: 13px; font-weight: 500;
    box-shadow: var(--shadow); margin-bottom: 18px;
}
.model-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--sage); display: inline-block; }
.hero-title {
    font-size: 38px; font-weight: 800; color: var(--charcoal);
    letter-spacing: -0.5px; line-height: 1.15; margin-bottom: 10px;
}
.hero-subtitle { font-size: 16px; color: var(--charcoal-soft); max-width: 560px; margin: 0 auto; line-height: 1.6; }

/* ---------- Input section ---------- */
.section-label { font-size: 15px; font-weight: 700; color: var(--charcoal); margin: 8px 0 2px 0; }
.section-hint { font-size: 13px; color: var(--charcoal-soft); margin-bottom: 8px; }

.stTextArea textarea {
    background-color: var(--white) !important;
    color: var(--charcoal) !important;
    font-size: 15px !important;
    line-height: 1.65 !important;
    padding: 16px 18px !important;
}
.stTextArea div[data-baseweb="textarea"],
.stTextArea div[data-baseweb="base-input"] {
    background-color: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    box-shadow: var(--shadow);
}
.stTextArea div[data-baseweb="textarea"]:focus-within {
    border: 1px solid var(--amber) !important;
    box-shadow: 0 0 0 3px rgba(217, 154, 101, 0.20) !important;
}

.count-pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--sage-soft); color: #4F6B52;
    border: 1px solid #CFDCCF; border-radius: 999px;
    padding: 9px 16px; font-size: 14px; font-weight: 600;
}
.count-pill.empty { background: var(--coral-soft); color: #A9594F; border-color: #EFCBC6; }

/* ---------- Buttons ---------- */
.stButton button, .stDownloadButton button {
    border-radius: 12px; font-weight: 600; font-size: 15px;
    padding: 0.6rem 1.2rem; transition: all 0.15s ease;
}
button[kind="primary"], [data-testid="stBaseButton-primary"] {
    background-color: var(--amber) !important;
    color: #FFFFFF !important;
    border: none !important;
    width: 100%;
    box-shadow: 0 4px 12px rgba(217, 154, 101, 0.35);
}
button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover {
    background-color: var(--amber-dark) !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
}
button[kind="primary"] p, [data-testid="stBaseButton-primary"] p { color: #FFFFFF !important; }
button[kind="secondary"], [data-testid="stBaseButton-secondary"] {
    background-color: var(--white) !important;
    color: var(--charcoal) !important;
    border: 1px solid var(--border) !important;
}
button[kind="secondary"]:hover, [data-testid="stBaseButton-secondary"]:hover {
    border-color: var(--amber) !important;
    color: var(--amber-dark) !important;
}
.stDownloadButton button {
    background-color: var(--white) !important;
    color: var(--charcoal) !important;
    border: 1px solid var(--amber) !important;
}
.stDownloadButton button:hover { background-color: var(--amber-soft) !important; }
[data-testid="stSidebar"] .stButton button { width: 100%; }

/* ---------- Select boxes & slider ---------- */
[data-baseweb="select"] > div {
    background-color: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--charcoal) !important;
}
[data-baseweb="select"] * { color: var(--charcoal) !important; }
[data-baseweb="popover"] ul, [data-baseweb="menu"] {
    background-color: var(--white) !important;
}
[data-baseweb="popover"] li { color: var(--charcoal) !important; }
[data-baseweb="popover"] li:hover { background-color: var(--amber-soft) !important; }
div[data-baseweb="slider"] div[role="slider"] {
    background-color: var(--amber) !important;
    box-shadow: 0 0 0 4px rgba(217, 154, 101, 0.25) !important;
}
div[data-baseweb="slider"] div[data-testid="stSliderThumbValue"],
[data-testid="stSliderThumbValue"] { color: var(--amber-dark) !important; font-weight: 600; }
[data-testid="stTickBarMin"], [data-testid="stTickBarMax"] { color: var(--charcoal-soft) !important; }

/* ---------- Alerts ---------- */
[data-testid="stAlert"] { border-radius: 14px; }

/* ---------- Results ---------- */
.results-heading {
    font-size: 24px; font-weight: 800; color: var(--charcoal);
    margin: 34px 0 4px 0;
}
.results-sub { font-size: 14px; color: var(--charcoal-soft); margin-bottom: 16px; }

.metric-card {
    background: var(--white); border: 1px solid var(--border);
    border-radius: 18px; padding: 18px 18px 16px 18px;
    box-shadow: var(--shadow); height: 100%; min-height: 150px;
    border-top: 4px solid var(--charcoal-soft);
}
.metric-card.positive { border-top-color: var(--sage); }
.metric-card.negative { border-top-color: var(--coral); }
.metric-card.neutral  { border-top-color: var(--amber); }
.metric-card.rating   { border-top-color: var(--amber); }
.metric-card.verdict  { border-top-color: var(--charcoal); }
.metric-label {
    font-size: 12px; font-weight: 700; letter-spacing: 0.8px;
    text-transform: uppercase; color: var(--charcoal-soft); margin-bottom: 10px;
}
.metric-value { font-size: 26px; font-weight: 800; color: var(--charcoal); line-height: 1.2; }
.metric-value.positive { color: #5C7C5F; }
.metric-value.negative { color: #BF6A60; }
.metric-value.neutral  { color: var(--amber-dark); }
.metric-verdict { font-size: 16px; font-weight: 600; line-height: 1.5; color: var(--charcoal); }
.rating-number { font-size: 36px; font-weight: 800; color: var(--charcoal); line-height: 1; }
.rating-number span { font-size: 17px; font-weight: 600; color: var(--charcoal-soft); }
.stars { font-size: 20px; letter-spacing: 3px; color: var(--amber); margin-top: 8px; }
.stars .off { color: #E6DDD0; }
.rating-bar { height: 7px; background: #F0E9DD; border-radius: 99px; margin-top: 10px; overflow: hidden; }
.rating-fill { height: 100%; background: var(--amber); border-radius: 99px; }

.card {
    background: var(--white); border: 1px solid var(--border);
    border-radius: 18px; padding: 20px 22px; margin: 14px 0;
    box-shadow: var(--shadow);
}
.card-title {
    display: flex; align-items: center; gap: 10px;
    font-size: 17px; font-weight: 700; color: var(--charcoal); margin-bottom: 12px;
}
.title-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; flex-shrink: 0; }
.dot-sage { background: var(--sage); }
.dot-coral { background: var(--coral); }
.dot-amber { background: var(--amber); }
.dot-charcoal { background: var(--charcoal); }
.card-text { color: var(--charcoal); line-height: 1.8; font-size: 15.5px; }

.item {
    border-radius: 12px; padding: 11px 14px; margin: 8px 0;
    font-size: 15px; line-height: 1.6; color: var(--charcoal);
    border: 1px solid transparent; word-wrap: break-word;
}
.item.good { background: var(--sage-soft); border-color: #D3E0D3; border-left: 4px solid var(--sage); }
.item.bad  { background: var(--coral-soft); border-color: #F0D2CE; border-left: 4px solid var(--coral); }
.item.warn { background: var(--amber-soft); border-color: #F0DCC6; border-left: 4px solid var(--amber); }
.item.info { background: var(--ivory); border-color: var(--border); border-left: 4px solid var(--charcoal-soft); }

.chips { display: flex; flex-wrap: wrap; gap: 8px; }
.chip {
    padding: 7px 14px; border-radius: 999px; font-size: 14px; font-weight: 500;
    border: 1px solid transparent;
}
.chip.sage  { background: var(--sage-soft); color: #4F6B52; border-color: #D3E0D3; }
.chip.amber { background: var(--amber-soft); color: #9A6531; border-color: #F0DCC6; }
.empty-note { color: var(--charcoal-soft); font-size: 14px; font-style: italic; }

hr { border-color: var(--border); }

/* ---------- Report layout ---------- */
.section-heading { font-size: 19px; font-weight: 700; color: var(--charcoal); margin: 18px 0 12px 0; }
.custom-card {
    background: var(--white); border: 1px solid var(--border);
    border-radius: 16px; padding: 22px; margin-bottom: 16px; box-shadow: var(--shadow);
}
.card-label { color: var(--charcoal-soft); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.7px; margin-bottom: 10px; }
.card-value { color: var(--charcoal); font-size: 26px; font-weight: 800; }
.card-description { color: var(--charcoal-soft); font-size: 13px; margin-top: 6px; }
.positive-card { background: #EDF4EB; border: 1px solid #D8E7D5; }
.negative-card { background: #FAECE9; border: 1px solid #F0D8D2; }
.neutral-card  { background: #F5F0E8; border: 1px solid #EAE0D2; }
.result-item {
    background: #FBF9F6; border: 1px solid #EFE8DF; border-radius: 10px;
    padding: 12px 15px; margin-bottom: 9px; color: #62584E; font-size: 14.5px; line-height: 1.6;
}
.verdict-box {
    background: #F6EDE1; border-left: 4px solid var(--amber); border-radius: 10px;
    padding: 18px; color: #65513E; font-size: 15.5px; line-height: 1.7; margin-bottom: 20px;
}

/* ---------- Responsive ---------- */
@media (max-width: 992px) {
    .block-container { padding-left: 1.5rem; padding-right: 1.5rem; }
    .hero-title { font-size: 33px; }
}
@media (max-width: 768px) {
    [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; gap: 0.75rem !important; }
    [data-testid="stColumn"], [data-testid="column"] {
        min-width: 100% !important; flex: 1 1 100% !important;
    }
    .hero-title { font-size: 28px; }
    .hero-subtitle { font-size: 15px; }
    .metric-card { min-height: 0; }
}
@media (max-width: 480px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; padding-top: 1.2rem; }
    .hero-title { font-size: 24px; }
    .card { padding: 16px; }
    .metric-value { font-size: 22px; }
    .rating-number { font-size: 30px; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Backend logic (unchanged behaviour)
# ---------------------------------------------------------------------------
def check_ollama_running():
    try:
        response = requests.get("http://localhost:11434", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def extract_json(text):
    try:
        return json.loads(text)
    except Exception:
        pass
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        return json.loads(match.group())
    raise ValueError("Could not parse JSON from model response. Try temperature 0.1 or 0.2.")


def analyse_reviews_ollama(reviews_text, output_language, model_name, temperature):
    system_prompt = '''
You are an expert customer review analyst.
You convert unstructured customer reviews into a clean structured business report.
Return valid JSON only.
No markdown.
No explanation outside JSON.
'''
    user_prompt = f'''
Analyse these customer reviews.

REVIEWS:
{reviews_text}

Return ONLY valid JSON in this exact format:
{{
  "overall_sentiment": "Positive / Neutral / Negative / Mixed",
  "estimated_rating_out_of_5": 4.2,
  "one_line_verdict": "short verdict",
  "summary": "short paragraph summary",
  "top_positives": ["point 1", "point 2", "point 3"],
  "top_negatives": ["point 1", "point 2", "point 3"],
  "customer_pain_points": ["point 1", "point 2", "point 3"],
  "business_suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"],
  "best_for": ["customer type 1", "customer type 2", "customer type 3"],
  "keywords": ["keyword 1", "keyword 2", "keyword 3"]
}}

Output language: {output_language}
Keep the response practical, concise and useful.
'''
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "options": {"temperature": temperature}
    }
    response = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=180)
    response.raise_for_status()
    raw_text = response.json()["message"]["content"]
    return extract_json(raw_text)


# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------
def esc(value):
    return html.escape(str(value))


def as_list(value):
    """Model output can occasionally be a string instead of a list."""
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [v for v in value if str(v).strip()]
    return [value] if str(value).strip() else []


def sentiment_class(sentiment):
    s = str(sentiment).lower()
    if "mixed" in s or "neutral" in s:
        return "neutral"
    if "positive" in s:
        return "positive"
    if "negative" in s:
        return "negative"
    return "neutral"


def to_rating(value):
    try:
        return max(0.0, min(5.0, float(value)))
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="side-title">⚙️ App Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-sub">Customize your analysis experience</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-divider"></div>', unsafe_allow_html=True)

    model_name = st.selectbox(
        "Ollama Model",
        ["qwen2.5:3b", "llama3.2:1b", "llama3.2", "mistral"],
        index=0
    )

    output_language = st.selectbox(
        "Output Language",
        ["English", "Telugu", "Tenglish"],
        index=0
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="Low temperature gives more stable structured JSON output."
    )

    st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
    if st.button("Clear Results"):
        st.session_state.pop("analysis_result", None)
        st.rerun()


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(f'''
<div class="hero">
    <div class="model-badge"><span class="model-dot"></span>Powered by Ollama</div>
    <div class="hero-title">Customer Review Analyzer</div>
    <div class="hero-subtitle">Paste your reviews and convert them into clear AI-powered business reports.</div>
</div>
''', unsafe_allow_html=True)

if not check_ollama_running():
    st.error("Ollama is not running.")
    st.info("Open a terminal and run: ollama serve")
    st.code(f"ollama serve\nollama pull {model_name}", language="bash")
    st.stop()

# ---------------------------------------------------------------------------
# Review input
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Enter Customer Reviews</div>', unsafe_allow_html=True)
st.markdown('<div class="section-hint">Paste one review per line for the best results.</div>', unsafe_allow_html=True)

reviews_text = st.text_area(
    "Paste 5–20 customer reviews",
    label_visibility="collapsed",
    value="",
    height=280,
    placeholder=(
        "Example:\n\n"
        "The product quality is excellent and delivery was fast.\n"
        "Customer service was helpful.\n"
        "The packaging was damaged.\n"
        "The price is slightly expensive."
    ),
)
review_count = len([r for r in reviews_text.splitlines() if r.strip()])

pill_class = "count-pill" if review_count else "count-pill empty"
label = "review" if review_count == 1 else "reviews"
st.markdown(f'<div class="{pill_class}">📝 {review_count} {label} detected</div>', unsafe_allow_html=True)
st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
analyse_button = st.button("Analyse Reviews 🚀", type="primary")

if analyse_button:
    if not reviews_text.strip():
        st.warning("Please paste some reviews first.")
    else:
        with st.spinner("Analysing reviews locally using Ollama..."):
            try:
                result = analyse_reviews_ollama(reviews_text, output_language, model_name, temperature)
                st.session_state["analysis_result"] = result
            except requests.exceptions.HTTPError as e:
                st.error(f"HTTP Error: {e}")
                st.info(f"If model is missing, run: ollama pull {model_name}")
                st.stop()
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Try temperature 0.1 or 0.2 if JSON parsing fails.")
                st.stop()

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
def display_card(label, value, description="", css_class=""):
    st.markdown(
        f'<div class="custom-card {css_class}">'
        f'<div class="card-label">{esc(label)}</div>'
        f'<div class="card-value">{esc(value)}</div>'
        f'<div class="card-description">{esc(description)}</div></div>',
        unsafe_allow_html=True,
    )


def display_list(title, items):
    st.markdown(f'<div class="section-heading">{esc(title)}</div>', unsafe_allow_html=True)
    items = as_list(items)
    if not items:
        st.caption("No information available.")
        return
    for item in items:
        st.markdown(f'<div class="result-item">• {esc(item)}</div>', unsafe_allow_html=True)


if "analysis_result" in st.session_state:
    result = st.session_state["analysis_result"]

    st.divider()
    st.markdown('<div class="results-heading" style="margin-top:6px;">Analysis Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="results-sub">Here is the AI-generated report based on your customer reviews.</div>', unsafe_allow_html=True)

    sentiment = result.get("overall_sentiment", "Not available")
    raw_rating = result.get("estimated_rating_out_of_5", "N/A")
    rating = to_rating(raw_rating)
    rating_text = f"{rating:g} / 5" if rating is not None else f"{raw_rating} / 5"

    col1, col2 = st.columns(2)
    with col1:
        display_card(
            "Overall Sentiment", sentiment, "Overall customer opinion",
            f"{sentiment_class(sentiment)}-card",
        )
    with col2:
        display_card("Estimated Rating", rating_text, "AI-estimated customer rating")

    st.markdown('<div class="section-heading">Overall Verdict</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="verdict-box">{esc(result.get("one_line_verdict", "No verdict available."))}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-heading">Review Summary</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="custom-card"><div style="font-size:15px;line-height:1.8;color:#62584E;">'
        f'{esc(result.get("summary", "No summary available."))}</div></div>',
        unsafe_allow_html=True,
    )

    positive_col, negative_col = st.columns(2)
    with positive_col:
        display_list("Top Positives", result.get("top_positives"))
    with negative_col:
        display_list("Top Negatives", result.get("top_negatives"))

    st.divider()
    display_list("Customer Pain Points", result.get("customer_pain_points"))

    st.divider()
    display_list("Business Suggestions", result.get("business_suggestions"))

    st.divider()
    display_list("Best For", result.get("best_for"))

    st.markdown('<div class="section-heading">Important Keywords</div>', unsafe_allow_html=True)
    keywords = as_list(result.get("keywords"))
    if keywords:
        keyword_text = "  ·  ".join(esc(k) for k in keywords)
        st.markdown(
            f'<div class="custom-card"><div style="color:#8A613D;font-weight:600;line-height:1.8;">'
            f'{keyword_text}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.caption("No keywords available.")

    st.divider()
    st.markdown('<div class="section-heading">Export Analysis</div>', unsafe_allow_html=True)
    st.download_button(
        label="Download Analysis as JSON",
        data=json.dumps(result, indent=2, ensure_ascii=False),
        file_name="customer_review_analysis.json",
        mime="application/json",
    )