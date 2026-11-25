import streamlit as st
from chatbot import get_reply, reset_chat

st.set_page_config(
    page_title="Nova AI",
    page_icon="✨",
    layout="centered"
)

# ---------------------------------------------------------------------------
# Design system
# Fonts : Sora (headings) + DM Sans (body)
# Colors: midnight base, indigo-violet primary, warm gold "nova" accent
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Sora:wght@500;600;700&display=swap');

    :root {
        --bg: #0b1020;
        --bg-soft: #0f1630;
        --surface: #141b33;
        --surface-2: #19223f;
        --border: #263050;
        --border-strong: #34406a;
        --text: #e8ecf8;
        --text-soft: #b4bdd8;
        --muted: #8591b3;
        --primary: #7c83ff;
        --primary-deep: #5b5fe8;
        --violet: #a78bfa;
        --gold: #ffd27a;
        --radius-lg: 20px;
        --radius-md: 14px;
        --radius-sm: 10px;
        --ease: cubic-bezier(.22, .61, .36, 1);
        color-scheme: dark;
    }

    /* ---------- Base ---------- */
    html { scroll-behavior: smooth; }

    .stApp {
        background-color: var(--bg);
        background-image:
            radial-gradient(900px 480px at 50% -8%, rgba(124, 131, 255, .16), transparent 70%),
            radial-gradient(600px 400px at 100% 100%, rgba(167, 139, 250, .08), transparent 70%);
        background-attachment: fixed;
        color: var(--text);
    }

    .stApp, .stApp p, .stApp li, .stApp label, .stApp textarea, .stApp input,
    .stApp button, .stApp .stMarkdown {
        font-family: 'DM Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
    }

    .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        font-family: 'Sora', 'DM Sans', system-ui, sans-serif;
        letter-spacing: -0.02em;
        color: var(--text);
    }

    .stApp p, .stApp li { line-height: 1.7; }

    ::selection { background: rgba(124, 131, 255, .35); color: #fff; }

    /* ---------- Text visibility (safe in both light and dark Streamlit themes) ---------- */
    .stApp,
    .stApp [data-testid="stMarkdownContainer"],
    .stApp [data-testid="stMarkdownContainer"] p,
    .stApp [data-testid="stMarkdownContainer"] li,
    .stApp [data-testid="stMarkdownContainer"] strong,
    .stApp [data-testid="stMarkdownContainer"] em,
    .stApp [data-testid="stMarkdownContainer"] td,
    .stApp [data-testid="stMarkdownContainer"] th,
    .stApp [data-testid="stChatMessage"],
    .stApp label {
        color: var(--text) !important;
    }

    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: var(--text) !important;
    }

    .stApp [data-testid="stCaptionContainer"],
    .stApp [data-testid="stCaptionContainer"] p {
        color: var(--muted) !important;
    }

    .stApp [data-testid="stMarkdownContainer"] .app-header p,
    .stApp [data-testid="stMarkdownContainer"] .welcome p {
        color: var(--text-soft) !important;
    }

    /* Top toolbar and sidebar toggle icons */
    [data-testid="stToolbar"],
    [data-testid="stToolbar"] button,
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stExpandSidebarButton"],
    [data-testid="collapsedControl"] {
        color: var(--text-soft) !important;
    }

    /* Streamlit chrome: keep the toolbar and sidebar toggle, quiet the rest */
    [data-testid="stHeader"] { background: transparent; }
    footer { visibility: hidden; }
    [data-testid="stHeaderActionElements"] { display: none; }

    /* Scrollbars */
    * { scrollbar-width: thin; scrollbar-color: var(--border-strong) transparent; }
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 8px; }
    ::-webkit-scrollbar-thumb:hover { background: #4a5894; }

    /* Keyboard focus */
    .stApp button:focus-visible,
    .stApp a:focus-visible {
        outline: 2px solid var(--primary);
        outline-offset: 2px;
    }

    /* ---------- Layout ---------- */
    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }

    /* ---------- Header ---------- */
    .app-header {
        position: relative;
        overflow: hidden;
        text-align: center;
        padding: 40px 24px 34px;
        margin-bottom: 28px;
        background:
            linear-gradient(180deg, rgba(124, 131, 255, .09), rgba(124, 131, 255, 0) 60%),
            var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        box-shadow: 0 24px 60px -30px rgba(0, 0, 0, .7);
        animation: headerIn .7s var(--ease) both;
    }

    /* The one memorable element: a slow, soft nova burst behind the title */
    .app-header::before {
        content: "";
        position: absolute;
        left: 50%;
        top: 38%;
        width: 360px;
        height: 360px;
        transform: translate(-50%, -50%);
        background: radial-gradient(circle,
            rgba(255, 210, 122, .20) 0%,
            rgba(167, 139, 250, .14) 34%,
            transparent 68%);
        animation: novaPulse 6s ease-in-out infinite;
        pointer-events: none;
    }

    .app-header > * { position: relative; }

    .app-header h1 {
        color: var(--text);
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1.15;
        margin: 0;
        padding: 0;
    }

    .app-header p {
        color: var(--text-soft);
        font-size: 1.05rem;
        margin: 12px 0 0;
    }

    @keyframes headerIn {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes novaPulse {
        0%, 100% { opacity: .75; transform: translate(-50%, -50%) scale(.94); }
        50%      { opacity: 1;   transform: translate(-50%, -50%) scale(1.08); }
    }

    /* ---------- Welcome ---------- */
    .welcome {
        text-align: center;
        padding: 28px 20px 10px;
        animation: fadeIn .6s var(--ease) .15s both;
    }

    .welcome h3 {
        font-size: 1.6rem;
        font-weight: 600;
        margin: 0 0 8px;
        padding: 0;
    }

    .welcome p {
        color: var(--text-soft);
        font-size: 1.05rem;
        margin: 0;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ---------- Chat messages ---------- */
    [data-testid="stChatMessage"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 16px 18px;
        margin-bottom: 14px;
        gap: 14px;
        animation: messageIn .35s var(--ease) both;
        transition: border-color .25s var(--ease), box-shadow .25s var(--ease);
    }

    [data-testid="stChatMessage"]:hover {
        border-color: var(--border-strong);
    }

    /* Your messages: tinted so the two voices are easy to tell apart */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, rgba(124, 131, 255, .16), rgba(167, 139, 250, .08));
        border-color: rgba(124, 131, 255, .32);
    }

    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"] {
        border-radius: 12px;
    }

    [data-testid="stChatMessageAvatarAssistant"] {
        background: linear-gradient(135deg, var(--primary-deep), var(--violet));
        color: #fff;
    }

    [data-testid="stChatMessageAvatarUser"] {
        background: var(--surface-2);
        color: var(--text);
    }

    @keyframes messageIn {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* Message content */
    [data-testid="stChatMessage"] p { margin-bottom: .6rem; }
    [data-testid="stChatMessage"] p:last-child { margin-bottom: 0; }

    [data-testid="stChatMessage"] a {
        color: var(--primary);
        text-decoration: none;
        border-bottom: 1px solid rgba(124, 131, 255, .4);
        transition: color .2s var(--ease), border-color .2s var(--ease);
    }

    [data-testid="stChatMessage"] a:hover {
        color: #b3b8ff;
        border-color: #b3b8ff;
    }

    [data-testid="stChatMessage"] code {
        background: rgba(124, 131, 255, .12);
        color: #c9ccff;
        border-radius: 6px;
        padding: 2px 6px;
        font-size: .88em;
    }

    [data-testid="stChatMessage"] pre {
        background: #0a0f20;
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        overflow-x: auto;
    }

    [data-testid="stChatMessage"] pre code {
        background: transparent;
        padding: 0;
        color: var(--text);
    }

    [data-testid="stChatMessage"] table {
        display: block;
        max-width: 100%;
        overflow-x: auto;
    }

    [data-testid="stChatMessage"] blockquote {
        border-left: 3px solid var(--primary);
        color: var(--text-soft);
        padding-left: 14px;
        margin-left: 0;
    }

    /* ---------- Thinking indicator ---------- */
    [data-testid="stSpinner"] {
        color: var(--text-soft);
    }

    [data-testid="stSpinner"] p {
        color: var(--text-soft);
        animation: thinking 1.6s ease-in-out infinite;
    }

    @keyframes thinking {
        0%, 100% { opacity: .55; }
        50%      { opacity: 1; }
    }

    /* ---------- Chat input ---------- */
    [data-testid="stBottom"] {
        background: linear-gradient(to top, var(--bg) 60%, rgba(11, 16, 32, 0)) !important;
    }

    [data-testid="stBottom"] > div {
        background: transparent !important;
    }

    [data-testid="stBottomBlockContainer"] {
        max-width: 850px;
    }

    [data-testid="stChatInput"] {
        background: var(--surface) !important;
        border: 1px solid var(--border-strong);
        border-radius: 18px;
        box-shadow: 0 12px 34px -16px rgba(0, 0, 0, .8);
        transition: border-color .25s var(--ease), box-shadow .25s var(--ease);
    }

    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] [data-baseweb="textarea"],
    [data-testid="stChatInput"] [data-baseweb="base-input"] {
        background: transparent !important;
        border: none;
        box-shadow: none;
    }

    [data-testid="stChatInput"]:hover {
        border-color: #4a5894;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: var(--primary);
        box-shadow:
            0 0 0 3px rgba(124, 131, 255, .22),
            0 12px 34px -16px rgba(0, 0, 0, .8);
    }

    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text);
        font-size: 1rem;
        caret-color: var(--primary);
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--muted) !important;
        -webkit-text-fill-color: var(--muted);
        opacity: 1;
    }

    [data-testid="stChatInputSubmitButton"] {
        background: linear-gradient(135deg, var(--primary-deep), var(--violet));
        color: #fff;
        border-radius: 12px;
        transition: transform .2s var(--ease), box-shadow .2s var(--ease), opacity .2s var(--ease);
    }

    [data-testid="stChatInputSubmitButton"]:hover:not(:disabled) {
        transform: translateY(-1px) scale(1.04);
        box-shadow: 0 8px 20px -6px rgba(124, 131, 255, .7);
    }

    [data-testid="stChatInputSubmitButton"]:active:not(:disabled) {
        transform: scale(.97);
    }

    [data-testid="stChatInputSubmitButton"]:disabled {
        background: var(--surface-2);
        color: var(--muted);
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111936 0%, #0d1329 100%);
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 1.55rem;
        font-weight: 700;
        padding-top: .25rem;
        padding-bottom: .1rem;
    }

    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: var(--muted);
    }

    hr {
        border: none;
        height: 1px;
        background: var(--border);
        margin: 1.1rem 0;
    }

    /* ---------- Buttons ---------- */
    .stButton button {
        width: 100%;
        border-radius: var(--radius-sm);
        background: var(--surface-2);
        color: var(--text);
        border: 1px solid var(--border-strong);
        padding: .6rem 1rem;
        font-weight: 500;
        transition:
            background .25s var(--ease),
            border-color .25s var(--ease),
            transform .2s var(--ease),
            box-shadow .25s var(--ease);
    }

    .stButton button:hover {
        background: linear-gradient(135deg, rgba(91, 95, 232, .35), rgba(167, 139, 250, .25));
        border-color: var(--primary);
        color: #fff;
        transform: translateY(-1px);
        box-shadow: 0 10px 24px -12px rgba(124, 131, 255, .65);
    }

    .stButton button:active {
        transform: translateY(0) scale(.99);
    }

    /* ---------- Tablet ---------- */
    @media (max-width: 992px) {
        .block-container {
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }
    }

    /* ---------- Mobile ---------- */
    @media (max-width: 640px) {
        .block-container {
            padding: 1rem .9rem 6.5rem;
        }

        .app-header {
            padding: 28px 16px 24px;
            margin-bottom: 20px;
            border-radius: 16px;
        }

        .app-header::before {
            width: 260px;
            height: 260px;
        }

        .app-header h1 { font-size: 1.85rem; }
        .app-header p  { font-size: .98rem; }

        .welcome { padding: 18px 8px 6px; }
        .welcome h3 { font-size: 1.35rem; }
        .welcome p  { font-size: 1rem; }

        [data-testid="stChatMessage"] {
            padding: 12px 13px;
            gap: 10px;
            border-radius: 12px;
        }

        [data-testid="stChatInput"] { border-radius: 16px; }
    }

    /* ---------- Respect reduced-motion settings ---------- */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation: none !important;
            transition: none !important;
            scroll-behavior: auto !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("✨ Nova AI")
    st.caption("Your personal AI assistant")
    st.divider()

    if st.button("🗑️ New chat", use_container_width=True):
        st.session_state.messages = []
        reset_chat()
        st.rerun()

    st.divider()
    st.caption("Built with Python and Streamlit")

# Header
st.markdown("""
<div class="app-header">
    <h1>✨ Nova AI</h1>
    <p>A simple, smart AI assistant</p>
</div>
""", unsafe_allow_html=True)

# Welcome message
if not st.session_state.messages:
    st.markdown("""
<div class="welcome">
    <h3>Welcome! 👋</h3>
    <p>I'm Nova AI. Ask me a question to get started.</p>
</div>
""", unsafe_allow_html=True)

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask Nova AI anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Nova AI is thinking..."):
            response = get_reply(prompt)
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
