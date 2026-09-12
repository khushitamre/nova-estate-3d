from pathlib import Path
from urllib.request import urlopen

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="NOVA / Estate 3D", page_icon="◈", layout="wide", initial_sidebar_state="collapsed")

DATA_PATH = Path(__file__).parent / "data" / "ames_housing.csv"
DATA_URL = "https://raw.githubusercontent.com/wblakecannon/ames/master/data/housing.csv"
CYAN = "#63F3E8"
VIOLET = "#9B7BFF"
INK = "#F4F7FB"
MUTED = "#A7B0C0"
BG = "#080A11"
PANEL = "#111622"
LINE = "#263044"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root {{ --cyan:{CYAN}; --violet:{VIOLET}; --ink:{INK}; --muted:{MUTED}; --bg:{BG}; --panel:{PANEL}; --line:{LINE}; }}
.stApp {{ background:radial-gradient(circle at 78% 0%,#202442 0%,#0b0e17 28%,#080a11 68%); color:var(--ink) !important; font-family:'Manrope',sans-serif; }}
/* Explicitly force readable light text on the dark product surface. */
.stApp, .stApp p, .stApp label, .stApp span, .stApp div, .stMarkdown, .stMarkdown p, .stMarkdown li {{ color:var(--ink); }}
.stApp h1,.stApp h2,.stApp h3,.stApp h4 {{ color:var(--ink) !important; font-family:'Manrope',sans-serif !important; }}
[data-testid="stSidebar"] {{ background:#0C101A; border-right:1px solid var(--line); }}
[data-testid="stSidebar"] * {{ color:#EAF1FB !important; }}
.block-container {{ max-width:1500px; padding:1.3rem 2.2rem 1.5rem; }}
.brand-row {{ display:flex; align-items:center; justify-content:space-between; margin-bottom:1.1rem; }}
.brand {{ display:flex; align-items:center; gap:.7rem; }}
.logo {{ width:36px; height:36px; border:1px solid var(--cyan); border-radius:12px; display:grid; place-items:center; color:var(--cyan) !important; font-size:1.2rem; box-shadow:0 0 22px #63f3e855; }}
.brand-name {{ font-weight:800; letter-spacing:.18em; color:#fff !important; font-size:.92rem; }}
.brand-sub {{ font-family:'DM Mono',monospace; color:#8793AA !important; font-size:.62rem; letter-spacing:.13em; text-transform:uppercase; }}
.live {{ font-family:'DM Mono',monospace; color:var(--cyan) !important; border:1px solid #315D61; border-radius:999px; padding:.4rem .75rem; font-size:.64rem; letter-spacing:.1em; }}
.hero {{ border:1px solid #2F3B5A; border-radius:22px; padding:1.45rem 1.65rem; background:linear-gradient(120deg,#121827,#141A2C 55%,#18213D); box-shadow:0 18px 55px #00000045; position:relative; overflow:hidden; }}
    .hero:after {{ content:'3D'; position:absolute; right:2%; top:-25%; font-size:10rem; font-weight:800; color:#63f3e810; letter-spacing:-.12em; }}
.eyebrow {{ color:var(--cyan) !important; font-family:'DM Mono',monospace; font-size:.65rem; letter-spacing:.15em; text-transform:uppercase; }}
.hero h1 {{ margin:.35rem 0 .45rem; font-size:2.7rem !important; line-height:1.03; letter-spacing:-.05em; }}
.hero p {{ color:#B8C3D3 !important; max-width:820px; font-size:.9rem; line-height:1.5; margin:0; }}
.hero-meta {{ color:#8290A6 !important; font-family:'DM Mono',monospace; font-size:.65rem; margin-top:.8rem; letter-spacing:.06em; }}
div[data-testid="stMetric"] {{ background:#111722; border:1px solid #28354A; border-radius:13px; padding:.75rem .9rem; box-shadow:0 7px 22px #00000026; }}
div[data-testid="stMetricLabel"] {{ color:#95A3B6 !important; font-family:'DM Mono',monospace; font-size:.62rem !important; letter-spacing:.08em; text-transform:uppercase; }}
div[data-testid="stMetricValue"] {{ color:#fff !important; font-size:1.45rem; }}
div[data-testid="stMetricDelta"] {{ color:var(--cyan) !important; }}
.section {{ color:var(--violet) !important; font-family:'DM Mono',monospace; font-size:.63rem; letter-spacing:.16em; text-transform:uppercase; margin:.95rem 0 .25rem; }}
.lead {{ color:#A7B0C0 !important; font-size:.78rem; margin:0 0 .55rem; }}
.panel {{ background:#101621; border:1px solid #28354A; border-radius:15px; padding:.9rem 1rem; box-shadow:0 10px 28px #00000028; }}
.panel * {{ color:#E8EEF7 !important; }}
.panel .muted {{ color:#A7B0C0 !important; font-size:.76rem; line-height:1.45; }}
.signal {{ background:linear-gradient(135deg,#101A23,#11152A); border:1px solid #294B56; border-radius:14px; padding:.85rem 1rem; min-height:105px; }}
.signal * {{ color:#EAF8F7 !important; }}
.signal .value {{ color:var(--cyan) !important; font-size:1.35rem; font-weight:800; margin:.12rem 0; }}
.signal .label {{ color:#8BA6AE !important; font-family:'DM Mono',monospace; font-size:.62rem; text-transform:uppercase; letter-spacing:.1em; }}
.stTabs [data-baseweb="tab-list"] {{ gap:1.3rem; border-bottom:1px solid #263044; }}
.stTabs [data-baseweb="tab"] {{ color:#8996AA !important; font-family:'DM Mono',monospace; font-size:.65rem; letter-spacing:.12em; padding:.55rem 0; }}
.stTabs [aria-selected="true"] {{ color:var(--cyan) !important; border-bottom-color:var(--cyan) !important; }}
[data-baseweb="select"] {{ background:#111722 !important; border-color:#354258 !important; }}
[data-baseweb="select"] * {{ color:#EEF4FC !important; }}
[data-testid="stSlider"] * {{ color:#DDE6F3 !important; }}
[data-testid="stDataFrame"] {{ border:1px solid #28354A; border-radius:10px; overflow:hidden; }}
.stDownloadButton button {{ background:#13222A; color:var(--cyan) !important; border:1px solid #35606A; border-radius:999px; }}
footer {{ visibility:hidden; }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    drop = [c for c in df.columns if c.lower().startswith("unnamed") or c == ""]
    if drop:
        df = df.drop(columns=drop)
    df.columns = [str(c).strip().replace(" ", "_") for c in df.columns]
    return df


def ensure_dataset() -> Path:
    """Find the bundled CSV or fetch a reproducible copy for a GitHub clone."""
    candidates = [
        DATA_PATH,
        Path(__file__).parent / "ames_housing.csv",
        Path.cwd() / "data" / "ames_housing.csv",
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.stat().st_size > 0:
            return candidate
    try:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        with urlopen(DATA_URL, timeout=15) as response:
            DATA_PATH.write_bytes(response.read())
        return DATA_PATH
    except Exception as exc:
        st.error("Dataset missing. Add `data/ames_housing.csv` beside `app.py`, then restart Streamlit.")
        st.info(f"Automatic download was not available ({type(exc).__name__}). The required file is the Ames Housing CSV.")
        st.stop()


def money(value: float) -> str:
    return f"${value:,.0f}"


def clean_data(raw: pd.DataFrame, strategy: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = raw.copy(); before = df.isna().sum()
    if strategy == "Median / mode imputation":
        for c in df.select_dtypes(include=np.number):
            df[c] = df[c].fillna(df[c].median())
        for c in df.select_dtypes(exclude=np.number):
            mode = df[c].mode(dropna=True)
            df[c] = df[c].fillna(mode.iloc[0] if len(mode) else "Unknown")
    else:
        df = df.dropna().copy()
    report = pd.DataFrame({"Column": before.index, "Missing before": before.values})
    report["Missing after"] = df.reindex(columns=before.index).isna().sum().values
    report["Handled"] = report["Missing before"] - report["Missing after"]
    return df, report


def style_plot(fig: go.Figure, height: int = 400) -> go.Figure:
    fig.update_layout(height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(10,15,24,.65)", font=dict(family="Manrope", color="#AEB9C9", size=10), margin=dict(l=8,r=8,t=20,b=8), legend=dict(font=dict(color="#C8D3E0")), coloraxis_colorbar=dict(title="", tickfont=dict(color="#AEB9C9")))
    fig.update_xaxes(showgrid=True, gridcolor="#263044", zeroline=False, linecolor="#354258")
    fig.update_yaxes(showgrid=True, gridcolor="#263044", zeroline=False, linecolor="#354258")
    return fig


def add_trend(fig: go.Figure, data: pd.DataFrame, x: str, y: str) -> go.Figure:
    clean = data[[x,y]].dropna()
    if len(clean) > 1 and clean[x].nunique() > 1:
        m,b = np.polyfit(clean[x].astype(float), clean[y].astype(float), 1)
        xs = np.linspace(clean[x].min(), clean[x].max(), 100)
        fig.add_trace(go.Scatter(x=xs, y=m*xs+b, mode="lines", name="Linear trend", line=dict(color=CYAN, width=3, dash="dash"), hoverinfo="skip"))
    return fig


DATA_FILE = ensure_dataset()
raw = load_data(str(DATA_FILE))
with st.sidebar:
    st.markdown("## NOVA / ESTATE 3D")
    st.caption("Obsidian Aurora edition")
    strategy = st.radio("Data treatment", ["Median / mode imputation", "Drop incomplete rows"], index=0)
    st.caption("The interface is intentionally limited to three short views.")

df, report = clean_data(raw, strategy)
features = [c for c in df.select_dtypes(include=np.number).columns if c not in ["SalePrice", "Order", "PID"]]
corr = df[features + ["SalePrice"]].corr(numeric_only=True)["SalePrice"].drop("SalePrice").sort_values(key=abs, ascending=False)

st.markdown('<div class="brand-row"><div class="brand"><div class="logo">◈</div><div><div class="brand-name">NOVA / ESTATE 3D</div><div class="brand-sub">residential market intelligence</div></div></div><div class="live">● LIVE ANALYSIS</div></div>', unsafe_allow_html=True)
st.markdown('<div class="hero"><div class="eyebrow">Portfolio system · 3D exploratory intelligence</div><h1>A market you can<br>see from every angle.</h1><p>A clean way to read the Ames Housing dataset: living area, overall quality, and sale price in one interactive 3D market landscape.</p><div class="hero-meta">2,930 records &nbsp; / &nbsp; 81 attributes &nbsp; / &nbsp; 3 spatial dimensions &nbsp; / &nbsp; explainable signals</div></div>', unsafe_allow_html=True)

m1,m2,m3,m4 = st.columns(4)
m1.metric("Properties", f"{len(df):,}", "Ames, Iowa")
m2.metric("Median price", money(df.SalePrice.median()), f"Mean {money(df.SalePrice.mean())}")
m3.metric("3D dimensions", "3 signals", "Area · quality · price")
m4.metric("Top signal", corr.index[0].replace("_", " "), f"r = {corr.iloc[0]:.3f}")

tab1, tab2, tab3 = st.tabs(["01 · ORBIT / 3D MARKET", "02 · SIGNAL LAB", "03 · EVIDENCE ROOM"])

with tab1:
    st.markdown('<div class="section">Three-dimensional market orbit</div><div class="lead">Rotate the chart to explore the market. X = living area, Y = quality, Z = sale price. Marker size represents garage capacity.</div>', unsafe_allow_html=True)
    sample = df.sample(min(900, len(df)), random_state=17)
    fig = px.scatter_3d(sample, x="Gr_Liv_Area", y="Overall_Qual", z="SalePrice", color="SalePrice", size="Garage_Cars", hover_data=["Neighborhood","Year_Built","Yr_Sold"], color_continuous_scale=[[0,"#33245E"],[.45,"#7257C7"],[.75,"#63F3E8"],[1,"#EFFFFD"]], range_x=[0, int(df.Gr_Liv_Area.quantile(.995))], range_y=[int(df.Overall_Qual.min()), int(df.Overall_Qual.max())], range_z=[0, int(df.SalePrice.quantile(.995))])
    fig.update_traces(marker=dict(line=dict(width=.2, color="#98FFF5")))
    fig.update_layout(height=470, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Manrope", color="#B9C5D6"), scene=dict(bgcolor="rgba(0,0,0,0)", xaxis_title="Living area", yaxis_title="Quality", zaxis_title="Sale price", xaxis=dict(showbackground=False, gridcolor="#263044"), yaxis=dict(showbackground=False, gridcolor="#263044"), zaxis=dict(showbackground=False, gridcolor="#263044")), coloraxis_colorbar=dict(title="Sale price", tickfont=dict(color="#B9C5D6")))
    st.plotly_chart(fig, use_container_width=True, config={"displaylogo":False})
    a,b,c = st.columns(3)
    a.markdown('<div class="signal"><div class="label">Dimension 01 / scale</div><div class="value">Living area</div><div>More space expands the market surface.</div></div>', unsafe_allow_html=True)
    b.markdown('<div class="signal"><div class="label">Dimension 02 / quality</div><div class="value">Overall quality</div><div>The strongest observed price signal.</div></div>', unsafe_allow_html=True)
    c.markdown('<div class="signal"><div class="label">Dimension 03 / outcome</div><div class="value">Sale price</div><div>Read the value surface in 3D.</div></div>', unsafe_allow_html=True)

with tab2:
    left,right = st.columns([.9,1.1])
    with left:
        st.markdown('<div class="section">Scenario engine</div><div class="lead">A transparent profile explorer. Educational market band—not a valuation.</div>', unsafe_allow_html=True)
        area = st.slider("Living area (sq ft)", int(df.Gr_Liv_Area.quantile(.05)), int(df.Gr_Liv_Area.quantile(.99)), int(df.Gr_Liv_Area.median()), 25)
        quality = st.slider("Overall quality", int(df.Overall_Qual.min()), int(df.Overall_Qual.max()), int(df.Overall_Qual.median()))
        garage = st.slider("Garage capacity", int(df.Garage_Cars.min()), int(df.Garage_Cars.max()), int(df.Garage_Cars.median()))
        year = st.slider("Year built", int(df.Year_Built.min()), int(df.Year_Built.max()), int(df.Year_Built.median()))
        norm = lambda v,c: float((v-df[c].min())/(df[c].max()-df[c].min()))
        score = 100*(.50*norm(quality,"Overall_Qual")+.28*norm(area,"Gr_Liv_Area")+.12*norm(garage,"Garage_Cars")+.10*norm(year,"Year_Built"))
        comps = df[df.Gr_Liv_Area.between(area-250,area+250)&df.Overall_Qual.between(quality-1,quality+1)]
        anchor = comps.SalePrice.median() if len(comps) else df.SalePrice.median(); estimate = anchor*(.82+score/260)
        st.markdown(f'<div class="panel"><div class="eyebrow">Signal output</div><h2>{money(estimate)}</h2><div class="muted">Anchored to {len(comps):,} comparable records · signal score <b>{score:.0f}/100</b></div><hr><div class="muted">This is a learning lens: the formula is visible, the uncertainty is acknowledged, and no false appraisal claim is made.</div></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="section">Signal constellation</div><div class="lead">The strongest numeric associations with observed SalePrice.</div>', unsafe_allow_html=True)
        cards = st.columns(3)
        for card,(feature,value) in zip(cards,corr.head(3).items()):
            card.markdown(f'<div class="signal"><div class="label">Ranked driver</div><div class="value">{feature.replace("_"," ")}</div><div>Correlation r = {value:.3f}</div></div>', unsafe_allow_html=True)
        f = px.bar(corr.head(8).sort_values(), orientation="h", color_discrete_sequence=[CYAN], labels={"value":"Pearson correlation","index":"Feature"})
        f.update_layout(showlegend=False)
        st.plotly_chart(style_plot(f, 300), use_container_width=True)

with tab3:
    st.markdown('<div class="section">Evidence room</div><div class="lead">A compact audit trail: distribution, locality, and data quality in one view.</div>', unsafe_allow_html=True)
    left,right = st.columns([1.15,.85])
    with left:
        f = px.scatter(df.sample(min(1100,len(df)),random_state=4), x="Gr_Liv_Area", y="SalePrice", color="Overall_Qual", opacity=.65, color_continuous_scale=[[0,"#4C3A8C"],[1,"#63F3E8"]], hover_data=["Neighborhood","Yr_Sold"])
        f = add_trend(f, df, "Gr_Liv_Area", "SalePrice")
        st.plotly_chart(style_plot(f, 360), use_container_width=True)
    with right:
        n = df.groupby("Neighborhood").agg(Median_Price=("SalePrice","median"), Homes=("SalePrice","size")).reset_index().sort_values("Median_Price", ascending=False).head(10)
        f2 = px.bar(n.sort_values("Median_Price"), x="Median_Price", y="Neighborhood", orientation="h", color_discrete_sequence=[VIOLET])
        st.plotly_chart(style_plot(f2, 360), use_container_width=True)
    missing = report[report["Missing before"] > 0].sort_values("Missing before", ascending=False)
    with st.expander("Open data-quality audit", expanded=False):
        st.dataframe(missing, use_container_width=True, hide_index=True)
        st.download_button("Download cleaned dataset", df.to_csv(index=False).encode("utf-8"), "nova_estate_3d_cleaned.csv", "text/csv")

st.markdown('<div style="text-align:center;color:#718096 !important;font-family:DM Mono,monospace;font-size:.62rem;letter-spacing:.12em;text-transform:uppercase;margin-top:.9rem">NOVA / ESTATE 3D · exploratory intelligence · not a valuation</div>', unsafe_allow_html=True)
