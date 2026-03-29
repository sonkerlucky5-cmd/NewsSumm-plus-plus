from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.config_utils import load_config, resolve_project_path


PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG = load_config(PROJECT_ROOT / "config.yaml")
PATHS = CONFIG["paths"]
PARAMETERS = CONFIG["parameters"]

RAW_DATA_PATH = resolve_project_path(PROJECT_ROOT, PATHS["raw_data"])
PROCESSED_DATA_PATH = resolve_project_path(PROJECT_ROOT, PATHS["processed_data"])
TABLES_DIR = resolve_project_path(PROJECT_ROOT, PATHS["metrics_output"])
GRAPHS_DIR = resolve_project_path(PROJECT_ROOT, PATHS["graphs_output"])
RESULTS_DIR = resolve_project_path(PROJECT_ROOT, PATHS["results_output"])


st.set_page_config(page_title="NewsSumm Dashboard", layout="wide")

if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False


def build_theme_css(is_dark: bool) -> str:
    if is_dark:
        colors = {
            "app_bg": "linear-gradient(180deg, #08141d 0%, #102533 52%, #0d1d29 100%)",
            "sidebar_bg": "linear-gradient(180deg, #08131d 0%, #143042 100%)",
            "sidebar_text": "#e8f4fb",
            "sidebar_subtext": "#cfe3ef",
            "sidebar_label_bg": "rgba(255, 255, 255, 0.05)",
            "sidebar_label_hover": "rgba(255, 255, 255, 0.12)",
            "card_bg": "#112532",
            "card_bg_alt": "#10212d",
            "card_border": "#284457",
            "text_primary": "#edf6fb",
            "text_secondary": "#c5d8e5",
            "text_muted": "#97b4c7",
            "metric_shadow": "0 12px 28px rgba(0, 0, 0, 0.28)",
            "hero_gradient": "linear-gradient(135deg, #102a3a 0%, #1a4d68 52%, #2d82b7 100%)",
            "pill_bg": "rgba(255, 255, 255, 0.10)",
            "pill_border": "rgba(255, 255, 255, 0.18)",
            "input_bg": "#0d1d29",
            "button_bg": "#1b5e83",
            "button_hover": "#2574a1",
            "button_text": "#ffffff",
            "accent_text": "#9bd4ff",
            "tab_active_bg": "#17384b",
            "tab_hover_bg": "#143042",
            "notice_bg": "rgba(155, 212, 255, 0.10)",
            "notice_border": "rgba(155, 212, 255, 0.24)",
        }
    else:
        colors = {
            "app_bg": "linear-gradient(180deg, #f4f7fb 0%, #ffffff 50%, #f8fafc 100%)",
            "sidebar_bg": "linear-gradient(180deg, #143a52 0%, #1f5a7a 100%)",
            "sidebar_text": "#f5fbff",
            "sidebar_subtext": "#dcebf5",
            "sidebar_label_bg": "rgba(255, 255, 255, 0.08)",
            "sidebar_label_hover": "rgba(255, 255, 255, 0.18)",
            "card_bg": "#ffffff",
            "card_bg_alt": "#ffffff",
            "card_border": "#d7e3f0",
            "text_primary": "#143a52",
            "text_secondary": "#23465d",
            "text_muted": "#6a8194",
            "metric_shadow": "0 10px 28px rgba(20, 58, 82, 0.08)",
            "hero_gradient": "linear-gradient(135deg, #143a52 0%, #2e6f95 55%, #5fa8d3 100%)",
            "pill_bg": "rgba(255, 255, 255, 0.16)",
            "pill_border": "rgba(255, 255, 255, 0.22)",
            "input_bg": "#ffffff",
            "button_bg": "#2e6f95",
            "button_hover": "#225a79",
            "button_text": "#ffffff",
            "accent_text": "#2e6f95",
            "tab_active_bg": "#e6f0f7",
            "tab_hover_bg": "#eff5fa",
            "notice_bg": "rgba(255, 255, 255, 0.10)",
            "notice_border": "rgba(255, 255, 255, 0.18)",
        }

    mode_specific_css = f"""
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6,
    .stApp label,
    .stApp strong,
    .stApp b {{
        color: {colors["text_primary"] if is_dark else "#143a52"} !important;
    }}
    .stApp div[data-testid="stMetricValue"] *,
    .stApp div[data-testid="stMetricLabel"] *,
    .stApp div[data-testid="stMetricDelta"] * {{
        color: {colors["text_primary"]} !important;
    }}
    """

    if is_dark:
        mode_specific_css += f"""
        .stApp p,
        .stApp li,
        .stApp div[data-testid="stMarkdownContainer"] *,
        .stApp div[data-testid="stText"] * {{
            color: {colors["text_secondary"]} !important;
        }}
        .stApp div[data-testid="stCaptionContainer"] *,
        .stApp div[data-testid="stImageCaption"] * {{
            color: {colors["text_muted"]} !important;
        }}
        .stApp div[data-testid="stDataFrame"],
        .stApp div[data-testid="stVerticalBlockBorderWrapper"],
        .stApp div[data-testid="stAlert"] {{
            background: {colors["card_bg"]} !important;
            border: 1px solid {colors["card_border"]} !important;
            border-radius: 18px !important;
        }}
        .stApp div[data-testid="stAlert"] * {{
            color: {colors["text_primary"]} !important;
        }}
        .stApp div[data-testid="stDataFrame"] * {{
            color: {colors["text_primary"]} !important;
        }}
        .stApp div[data-testid="stDataFrame"] [role="grid"],
        .stApp div[data-testid="stDataFrame"] [role="columnheader"],
        .stApp div[data-testid="stDataFrame"] [role="gridcell"] {{
            background: {colors["card_bg"]} !important;
        }}
        .stApp .stTextInput input,
        .stApp textarea,
        .stApp div[data-baseweb="select"] > div,
        .stApp pre,
        .stApp code {{
            background: {colors["input_bg"]} !important;
            color: {colors["text_primary"]} !important;
            border: 1px solid {colors["card_border"]} !important;
            border-radius: 12px !important;
        }}
        .stApp .stTextInput input::placeholder {{
            color: {colors["text_muted"]} !important;
        }}
        .stApp div[data-baseweb="select"] span,
        .stApp div[data-baseweb="select"] input,
        .stApp div[data-baseweb="popover"] *,
        .stApp ul[role="listbox"] *,
        .stApp div[role="listbox"] * {{
            color: {colors["text_primary"]} !important;
            background: {colors["card_bg"]} !important;
        }}
        .stApp button[data-baseweb="tab"] {{
            color: {colors["text_primary"]} !important;
            background: transparent !important;
            border-radius: 12px 12px 0 0 !important;
        }}
        .stApp button[data-baseweb="tab"]:hover {{
            background: {colors["tab_hover_bg"]} !important;
        }}
        .stApp button[data-baseweb="tab"][aria-selected="true"] {{
            background: {colors["tab_active_bg"]} !important;
            color: {colors["accent_text"]} !important;
        }}
        """
    else:
        mode_specific_css += """
        .stApp div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 18px !important;
        }
        """

    return f"""
    <style>
    :root {{
        color-scheme: {"dark" if is_dark else "light"};
    }}
    .stApp {{
        background: {colors["app_bg"]};
        color: {colors["text_secondary"]};
    }}
    .block-container {{
        padding-top: 1.35rem;
        padding-bottom: 2rem;
    }}
    section[data-testid="stSidebar"] {{
        background: {colors["sidebar_bg"]};
    }}
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] *,
    section[data-testid="stSidebar"] div[data-testid="stText"] *,
    section[data-testid="stSidebar"] strong {{
        color: {colors["sidebar_text"]} !important;
    }}
    .sidebar-brand {{
        display: flex;
        align-items: center;
        gap: 0.85rem;
        padding: 0.9rem 0.2rem 1.15rem 0.2rem;
    }}
    .sidebar-logo {{
        width: 48px;
        height: 48px;
        border-radius: 16px;
        background: linear-gradient(135deg, #ffb703 0%, #ffd166 100%);
        color: #143a52 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1rem;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.18);
        transition: transform 0.22s ease, box-shadow 0.22s ease;
    }}
    .sidebar-logo:hover {{
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 14px 28px rgba(0, 0, 0, 0.22);
    }}
    .sidebar-brand-text h1 {{
        font-size: 1.15rem;
        line-height: 1.1;
        margin: 0;
        color: {colors["sidebar_text"]} !important;
    }}
    .sidebar-brand-text p {{
        margin: 0.2rem 0 0 0;
        font-size: 0.82rem;
        opacity: 0.92;
        color: {colors["sidebar_subtext"]} !important;
    }}
    div[data-testid="stRadio"] label,
    div[data-testid="stToggle"] {{
        background: {colors["sidebar_label_bg"]};
        border-radius: 12px;
        padding: 0.45rem 0.6rem;
        margin-bottom: 0.3rem;
        transition: transform 0.18s ease, background 0.18s ease;
    }}
    div[data-testid="stRadio"] label:hover,
    div[data-testid="stToggle"]:hover {{
        background: {colors["sidebar_label_hover"]};
        transform: translateX(2px);
    }}
    div[data-testid="stMetric"],
    .info-card,
    .mini-card,
    .graph-caption,
    div[data-testid="stImage"] {{
        background: {colors["card_bg"]};
        border: 1px solid {colors["card_border"]};
        box-shadow: {colors["metric_shadow"]};
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }}
    div[data-testid="stMetric"]:hover,
    .info-card:hover,
    .mini-card:hover,
    .graph-caption:hover,
    div[data-testid="stImage"]:hover {{
        transform: translateY(-4px);
        box-shadow: 0 16px 34px rgba(20, 58, 82, 0.18);
        border-color: {colors["accent_text"]};
    }}
    div[data-testid="stMetric"] {{
        border-radius: 16px;
        padding: 0.8rem;
    }}
    div[data-testid="stImage"] {{
        border-radius: 18px;
        overflow: hidden;
        padding: 0.35rem;
    }}
    .stApp a {{
        color: {colors["accent_text"]} !important;
    }}
    .info-card {{
        border-radius: 18px;
        padding: 1rem 1.1rem;
        margin-bottom: 1rem;
        color: {colors["text_secondary"]};
    }}
    .mini-grid {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.9rem;
        margin: 0.6rem 0 1rem 0;
    }}
    .mini-card {{
        border-radius: 18px;
        padding: 1rem 1rem 0.9rem 1rem;
    }}
    .mini-card .label {{
        font-size: 0.74rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: {colors["text_muted"]};
        margin-bottom: 0.4rem;
    }}
    .mini-card .value {{
        font-size: 1.45rem;
        font-weight: 700;
        color: {colors["text_primary"]};
    }}
    .mini-card .hint {{
        margin-top: 0.28rem;
        font-size: 0.84rem;
        color: {colors["text_muted"]};
    }}
    .badge-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-top: 0.85rem;
    }}
    .pill {{
        background: {colors["pill_bg"]};
        color: #ffffff;
        border: 1px solid {colors["pill_border"]};
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        font-size: 0.8rem;
        transition: transform 0.18s ease, background 0.18s ease;
    }}
    .pill:hover {{
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.24);
    }}
    .sidebar-panel {{
        background: {colors["sidebar_label_bg"]};
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 18px;
        padding: 0.9rem 1rem;
        margin: 0.7rem 0 1rem 0;
        transition: transform 0.18s ease, background 0.18s ease;
    }}
    .sidebar-panel:hover {{
        transform: translateY(-2px);
        background: {colors["sidebar_label_hover"]};
    }}
    .sidebar-notice {{
        background: {colors["notice_bg"]};
        border: 1px solid {colors["notice_border"]};
        border-radius: 16px;
        padding: 0.8rem 0.95rem;
        margin: 0.55rem 0 0.9rem 0;
        color: {colors["sidebar_text"]} !important;
    }}
    .sidebar-path {{
        margin-top: 0.45rem;
        padding: 0.75rem 0.8rem;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.14);
        color: {colors["sidebar_text"]} !important;
        font-family: Consolas, monospace;
        font-size: 0.78rem;
        line-height: 1.35;
        word-break: break-word;
    }}
    .sidebar-panel-title {{
        font-size: 0.74rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: {colors["sidebar_subtext"]} !important;
        margin-bottom: 0.55rem;
    }}
    .theme-label {{
        margin-top: 0.2rem;
        margin-bottom: 0.55rem;
        font-size: 0.78rem;
        color: {colors["sidebar_subtext"]} !important;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }}
    .sidebar-stat {{
        display: flex;
        justify-content: space-between;
        gap: 0.75rem;
        margin-bottom: 0.4rem;
        font-size: 0.9rem;
    }}
    .sidebar-stat strong {{
        color: {colors["sidebar_text"]} !important;
    }}
    .graph-caption {{
        border-radius: 16px;
        padding: 0.9rem 1rem;
        margin-top: 0.7rem;
        color: {colors["text_secondary"]};
    }}
    .hero-card {{
        background: {colors["hero_gradient"]};
        border-radius: 24px;
        padding: 1.5rem 1.7rem;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 12px 32px rgba(20, 58, 82, 0.22);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .hero-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 18px 38px rgba(20, 58, 82, 0.28);
    }}
    .section-label {{
        font-size: 0.9rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: {colors["text_muted"]};
        margin-top: 0.2rem;
        margin-bottom: 0.5rem;
    }}
    .stDownloadButton > button,
    .stButton > button {{
        background: {colors["button_bg"]} !important;
        color: {colors["button_text"]} !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 24px rgba(20, 58, 82, 0.18) !important;
        transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease !important;
    }}
    .stDownloadButton > button:hover,
    .stButton > button:hover {{
        background: {colors["button_hover"]} !important;
        transform: translateY(-2px);
        box-shadow: 0 14px 28px rgba(20, 58, 82, 0.22) !important;
    }}
    .stDownloadButton > button *,
    .stButton > button * {{
        color: {colors["button_text"]} !important;
    }}
    div[data-testid="stRadio"] label *,
    div[data-testid="stToggle"] *,
    div[data-testid="stCheckbox"] * {{
        color: {colors["sidebar_text"]} !important;
    }}
    div[data-baseweb="tab-list"] {{
        gap: 0.4rem;
    }}
    {mode_specific_css}
    @media (max-width: 1100px) {{
        .mini-grid {{
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }}
    }}
    @media (max-width: 680px) {{
        .mini-grid {{
            grid-template-columns: repeat(1, minmax(0, 1fr));
        }}
    }}
    </style>
    """


st.markdown(build_theme_css(st.session_state["dark_mode"]), unsafe_allow_html=True)


@st.cache_data
def load_raw_data() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_PATH)


@st.cache_data
def load_processed_data() -> pd.DataFrame:
    return pd.read_excel(PROCESSED_DATA_PATH)


@st.cache_data
def load_table(table_name: str) -> pd.DataFrame:
    csv_path = TABLES_DIR / f"{table_name}.csv"
    return pd.read_csv(csv_path)


@st.cache_data
def load_evaluation_results() -> pd.DataFrame:
    evaluation_path = RESULTS_DIR / "rouge_comparison.csv"
    if not evaluation_path.exists():
        return pd.DataFrame()
    return pd.read_csv(evaluation_path)


@st.cache_data
def build_processed_csv(dataframe: pd.DataFrame) -> bytes:
    return dataframe.to_csv(index=False).encode("utf-8")


def create_stat_card(label: str, value: str, hint: str) -> str:
    return f"""
    <div class="mini-card">
        <div class="label">{label}</div>
        <div class="value">{value}</div>
        <div class="hint">{hint}</div>
    </div>
    """


def filter_dataframe(dataframe: pd.DataFrame, query: str) -> pd.DataFrame:
    if not query.strip():
        return dataframe

    search_value = query.strip().lower()
    mask = dataframe.apply(
        lambda row: row.astype(str).str.lower().str.contains(search_value, regex=False).any(),
        axis=1,
    )
    return dataframe.loc[mask].reset_index(drop=True)


def render_dataframe(title: str, dataframe: pd.DataFrame, key_prefix: str) -> None:
    st.markdown(f"**{title}**")
    search_query = st.text_input(
        f"Search inside {title}",
        placeholder="Type keyword to filter rows...",
        key=f"{key_prefix}_search",
    )
    filtered_df = filter_dataframe(dataframe, search_query)
    st.caption(f"Showing {len(filtered_df)} of {len(dataframe)} rows")
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        height=430,
        column_config={
            "article": st.column_config.TextColumn("article", width="large"),
            "summary": st.column_config.TextColumn("summary", width="large"),
        },
    )


def show_sidebar_brand() -> None:
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">NS++</div>
            <div class="sidebar-brand-text">
                <h1>NewsSumm++</h1>
                <p>Data-centric NLP workspace</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_panel(title: str, stats: list[tuple[str, str]]) -> None:
    stats_html = "".join(
        f'<div class="sidebar-stat"><span>{label}</span><strong>{value}</strong></div>'
        for label, value in stats
    )
    st.sidebar.markdown(
        f"""
        <div class="sidebar-panel">
            <div class="sidebar-panel-title">{title}</div>
            {stats_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_notice(message: str) -> None:
    st.sidebar.markdown(
        f'<div class="sidebar-notice">{message}</div>',
        unsafe_allow_html=True,
    )


def render_sidebar_path(path_label: str, path_value: str) -> None:
    st.sidebar.markdown(
        f"""
        <div class="sidebar-panel">
            <div class="sidebar-panel-title">{path_label}</div>
            <div class="sidebar-path">{path_value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_status(kpis: dict[str, float | int], processed_df: pd.DataFrame) -> str:
    show_sidebar_brand()
    current_theme = "Dark" if st.session_state["dark_mode"] else "Light"
    current_theme_icon = "🌙" if st.session_state["dark_mode"] else "☀️"
    st.sidebar.markdown(
        f'<div class="theme-label">{current_theme_icon} {current_theme} Mode</div>',
        unsafe_allow_html=True,
    )
    st.sidebar.toggle("Theme Switch", key="dark_mode")
    page = st.sidebar.radio(
        "Menu",
        ["Data Overview", "Quality Metrics", "Visualizations", "Model Evaluation"],
    )

    required_paths = [
        PROCESSED_DATA_PATH,
        TABLES_DIR / "dataset_stats.csv",
        TABLES_DIR / "main_results.csv",
        TABLES_DIR / "error_analysis.csv",
        GRAPHS_DIR / "document_length_distribution.png",
        GRAPHS_DIR / "readability_comparison.png",
    ]

    ready = all(path.exists() for path in required_paths)
    if ready:
        render_sidebar_notice("Outputs are ready.")
    else:
        render_sidebar_notice("Run ./run_all.sh to generate all outputs.")

    render_sidebar_panel(
        "Quick Stats",
        [
            ("Rows", str(kpis["total_rows"])),
            ("Retention", f"{kpis['retention_rate']}%"),
            ("Avg Length", str(kpis["avg_doc_length"])),
            ("Avg Readability", str(kpis["avg_readability"])),
        ],
    )
    render_sidebar_panel(
        "Pipeline Settings",
        [
            ("spaCy Model", str(PARAMETERS["spacy_model"])),
            ("Min Doc Length", str(PARAMETERS["min_doc_length"])),
            ("Min Summary Length", str(PARAMETERS["min_summary_length"])),
            ("Top Entities", str(int(processed_df["entity_count"].max()))),
        ],
    )
    render_sidebar_path(
        "Config-driven output path",
        str(PROCESSED_DATA_PATH.relative_to(PROJECT_ROOT)),
    )
    return page


def compute_kpis(raw_df: pd.DataFrame, processed_df: pd.DataFrame) -> dict[str, float | int]:
    duplicate_count = int(raw_df.duplicated(subset=["article", "summary"]).sum())
    retention_rate = round((len(processed_df) / max(len(raw_df), 1)) * 100, 1)
    return {
        "total_rows": len(processed_df),
        "removed_duplicates": duplicate_count,
        "avg_compression_ratio": round(processed_df["compression_ratio"].mean(), 4),
        "avg_entity_count": round(processed_df["entity_count"].mean(), 2),
        "avg_doc_length": round(processed_df["doc_length"].mean(), 2),
        "avg_summary_length": round(processed_df["summary_length"].mean(), 2),
        "avg_readability": round(processed_df["readability_score"].mean(), 2),
        "retention_rate": retention_rate,
    }


def show_header(kpis: dict[str, float | int]) -> None:
    st.markdown(
        """
        <div class="hero-card">
            <div style="font-size:0.9rem; letter-spacing:0.08em; text-transform:uppercase; opacity:0.85;">
                NewsSumm Data Science App
            </div>
            <div style="font-size:2rem; font-weight:700; margin-top:0.35rem;">
                Summarization pipeline monitoring in one place
            </div>
            <div style="margin-top:0.4rem; font-size:1rem; opacity:0.92;">
                Track data quality, review outputs, inspect visuals, and compare baseline ROUGE scores.
            </div>
            <div class="badge-row">
                <span class="pill">Config Driven</span>
                <span class="pill">spaCy Features</span>
                <span class="pill">Analytics Ready</span>
                <span class="pill">Streamlit Dashboard</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Rows", kpis["total_rows"])
    col2.metric("Removed Duplicates", kpis["removed_duplicates"])
    col3.metric("Avg Compression Ratio", kpis["avg_compression_ratio"])
    col4.metric("Avg Entity Count", kpis["avg_entity_count"])

    st.markdown(
        f"""
        <div class="mini-grid">
            {create_stat_card("Retention Rate", f"{kpis['retention_rate']}%", "Rows preserved after cleaning")}
            {create_stat_card("Avg Doc Length", str(kpis["avg_doc_length"]), "Average article word count")}
            {create_stat_card("Avg Summary Length", str(kpis["avg_summary_length"]), "Average summary word count")}
            {create_stat_card("Avg Readability", str(kpis["avg_readability"]), "Automated readability index")}
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_data_overview(
    raw_df: pd.DataFrame,
    processed_df: pd.DataFrame,
    kpis: dict[str, float | int],
) -> None:
    st.markdown('<div class="section-label">Data Overview</div>', unsafe_allow_html=True)
    st.subheader("Raw vs Processed Data")

    info_col1, info_col2 = st.columns([1.2, 1])
    with info_col1:
        st.markdown(
            """
            <div class="info-card">
                Compare the original dataset with the cleaned NewsSumm++ version.
                Use the search boxes below to filter rows and inspect how the pipeline
                changed the data.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with info_col2:
        st.download_button(
            label="Download processed dataset as CSV",
            data=build_processed_csv(processed_df),
            file_name="newssum_plus_plus.csv",
            mime="text/csv",
        )

    st.markdown(
        f"""
        <div class="mini-grid">
            {create_stat_card("Raw Rows", str(len(raw_df)), "Initial dataset size")}
            {create_stat_card("Processed Rows", str(len(processed_df)), "Rows after cleaning")}
            {create_stat_card("Duplicates Removed", str(kpis['removed_duplicates']), "Exact duplicate pairs removed")}
            {create_stat_card("Mean Entities", str(kpis['avg_entity_count']), "Average entity count per article")}
        </div>
        """,
        unsafe_allow_html=True,
    )

    raw_tab, processed_tab = st.tabs(["Raw Dataset", "Processed Dataset"])
    with raw_tab:
        render_dataframe("Raw Dataset Preview", raw_df, "raw_dataset")
    with processed_tab:
        render_dataframe("Processed Dataset Preview", processed_df, "processed_dataset")


def show_quality_metrics() -> None:
    st.markdown('<div class="section-label">Quality Metrics</div>', unsafe_allow_html=True)
    st.subheader("Generated Tables")
    st.markdown(
        """
        <div class="info-card">
            Review the core analytical artifacts generated by the pipeline. Each table is searchable,
            interactive, and available for download.
        </div>
        """,
        unsafe_allow_html=True,
    )

    table_specs = [
        ("Dataset Stats", "dataset_stats"),
        ("Main Results", "main_results"),
        ("Error Analysis", "error_analysis"),
    ]

    for title, table_name in table_specs:
        table_df = load_table(table_name)
        with st.container(border=True):
            render_dataframe(title, table_df, table_name)
            st.download_button(
                label=f"Download {table_name}.csv",
                data=table_df.to_csv(index=False).encode("utf-8"),
                file_name=f"{table_name}.csv",
                mime="text/csv",
                key=f"download_{table_name}",
            )


def show_visualizations() -> None:
    st.markdown('<div class="section-label">Visualizations</div>', unsafe_allow_html=True)
    st.subheader("Saved Analysis Graphs")
    st.markdown(
        """
        <div class="info-card">
            These graphs are generated by the pipeline and saved to the outputs folder.
            Use them to quickly inspect document length patterns and readability trends.
        </div>
        """,
        unsafe_allow_html=True,
    )

    graph_col1, graph_col2 = st.columns(2)

    with graph_col1:
        st.image(
            str(GRAPHS_DIR / "document_length_distribution.png"),
            caption="Document length distribution",
            use_container_width=True,
        )
        st.markdown(
            """
            <div class="graph-caption">
                Shows how article lengths are distributed after the cleaning stage. Useful for spotting
                skew, outliers, and overall dataset balance.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with graph_col2:
        st.image(
            str(GRAPHS_DIR / "readability_comparison.png"),
            caption="Readability comparison",
            use_container_width=True,
        )
        st.markdown(
            """
            <div class="graph-caption">
                Compares average readability between articles and summaries to highlight how condensed
                and simplified the generated dataset targets are.
            </div>
            """,
            unsafe_allow_html=True,
        )


def show_model_evaluation() -> None:
    st.markdown('<div class="section-label">Model Evaluation</div>', unsafe_allow_html=True)
    st.subheader("Baseline ROUGE Comparison")

    evaluation_df = load_evaluation_results()
    if evaluation_df.empty:
        st.info(
            "No baseline comparison found yet. Run `python evaluate_baseline.py` after "
            "installing optional evaluation dependencies from `requirements-eval.txt`."
        )
        return

    st.markdown(
        """
        <div class="info-card">
            This section compares baseline ROUGE scores between the raw dataset and the cleaned
            NewsSumm++ dataset.
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_dataframe("ROUGE Comparison", evaluation_df, "rouge_comparison")
    st.download_button(
        label="Download ROUGE comparison CSV",
        data=evaluation_df.to_csv(index=False).encode("utf-8"),
        file_name="rouge_comparison.csv",
        mime="text/csv",
    )


def main() -> None:
    if not PROCESSED_DATA_PATH.exists():
        st.error("Processed dataset not found. Run ./run_all.sh first.")
        return

    raw_df = load_raw_data()
    processed_df = load_processed_data()
    kpis = compute_kpis(raw_df, processed_df)
    page = show_status(kpis, processed_df)

    show_header(kpis)

    if page == "Data Overview":
        show_data_overview(raw_df, processed_df, kpis)
    elif page == "Quality Metrics":
        show_quality_metrics()
    elif page == "Visualizations":
        show_visualizations()
    elif page == "Model Evaluation":
        show_model_evaluation()


if __name__ == "__main__":
    main()
