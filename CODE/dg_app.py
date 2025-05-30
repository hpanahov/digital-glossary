import streamlit as st
import pandas as pd

# 1. Page config + CSS
st.set_page_config(
    page_title="Digital Glossary",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /*  ─── Remove the top header entirely ───────────────── */
    header { visibility: hidden; }

    /*  ─── Pull content up to the very top ───────────────── */
    .block-container { padding-top: 0rem; }

    /* hide built-in hamburger & footer */
    #MainMenu { visibility: hidden; } 
    footer { visibility: hidden; }

    /* ─── Sidebar (filter pane) background ───────────────────── */
    [data-testid="stSidebar"] {
        background-color: #0a66c2 !important;
    }

    /* ─── Sidebar input fields ───────────────────────────────── */
    [data-testid="stSidebar"] .stTextInput>div>div>input,
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #e6f7ff !important;
        color: #000000 !important;
    }

    /* ─── Main content background & text ────────────────────── */
    [data-testid="stAppViewContainer"] {
        background-color: #e6f7ff !important;
    }
    [data-testid="stAppViewContainer"] * {
        color: #000000 !important;
    }


    /* ─── Global scrollbar track ─────────────────────────────── */
    /* fixed wide track */
    ::-webkit-scrollbar {width: 20px; }
    /* light track */
    ::-webkit-scrollbar-track { background: #f1f1f1; }

    /* ─── Scrollbar thumb (consistent color) ───────────────── */
    ::-webkit-scrollbar-thumb,
    ::-webkit-scrollbar-thumb:hover {
        background-color: #0a66c2 !important; /* same WB blue always */
        border-radius: 10px;
        border: none;
        min-height: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2. Load & prepare data

# Google Sheets CSV URL
SHEET_ID = "12IsT3AZ1wrN1ECn3snwPf5M9oYP5geb1"
GID      = "1289983907"
CSV_URL = (
    f"https://docs.google.com/spreadsheets"
    f"/d/{SHEET_ID}"
    f"/export?format=csv&gid={GID}"
)

@st.cache_data(ttl=10)
def load_data():
    return pd.read_csv(CSV_URL)

df = load_data()
df = df[df["Publish_bnry"] == 1].drop(columns=["Comment"])
df["Term"] = df["Term"].astype(str)
df = df.sort_values("Term", key=lambda col: col.str.lower())

# 3. Header & caption
st.title("📖 Digital Glossary")
st.caption("Published and maintained by the World Bank / Digital Transformation VPU / DSODR")

# 4. Sidebar filters
st.sidebar.title("🔍 Filters")

# seed session_state defaults
if "letter" not in st.session_state:
    st.session_state.letter = "All"
if "query" not in st.session_state:
    st.session_state.query = ""

# reset callback
def reset_filters():
    st.session_state.letter = "All"
    st.session_state.query = ""

# place one single reset‐filters button with a unique key
st.sidebar.button(
    "Reset filters",
    key="btn_reset_filters",    
    on_click=reset_filters
)

# the widgets
letters = sorted({t[0].upper() for t in df["Term"]})
letter = st.sidebar.selectbox(
    "First letter",
    ["All"] + letters,
    key="letter"
)
query = st.sidebar.text_input(
    "Search term or definition",
    key="query"
)

# 5. Apply filters
filtered = df.copy()
if letter != "All":
    filtered = filtered[
        filtered["Term"].str.upper().str.startswith(letter)
    ]
if query:
    mask = (
        filtered["Term"].str.contains(query, case=False, na=False)
        | filtered["Definition"].str.contains(query, case=False, na=False)
    )
    filtered = filtered[mask]

# 6. Main display
st.markdown(f"**{len(filtered):,}** terms found.")
for _, row in filtered.iterrows():
    st.subheader(row["Term"])
    if pd.notna(row.get("Abbreviation")):
        st.markdown(f"**Abbreviation:** {row['Abbreviation']}")
    st.markdown(f"**Definition:** {row['Definition']}")
    st.markdown(f"**Category:** {row['Category_1']}")
    if pd.notna(row.get("Source_url")):
        st.markdown(
            f"**Source:** [{row['Source_name']}]({row['Source_url']})"
        )
    st.markdown("---")
