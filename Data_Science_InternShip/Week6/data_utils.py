"""
data_utils.py
==============
Shared utilities for the Interactive Sales Dashboard project, used by both
dashboard.py (the reproducible pipeline script) and dashboard.ipynb (the
narrative walkthrough notebook), so the two never drift out of sync on
data prep or color scheme.
"""
import os
import sys
import json
import pandas as pd

# ---------------------------------------------------------------------------
# Shared color scheme (used by both seaborn and Plotly charts for a cohesive
# look across every visualization in the project)
# ---------------------------------------------------------------------------
REGION_COLORS = {
    "North": "#4C72B0",
    "South": "#DD8452",
    "East": "#55A868",
    "West": "#C44E52",
}
PRODUCT_COLORS = {
    "Laptop": "#4C72B0",
    "Tablet": "#DD8452",
    "Phone": "#55A868",
    "Headphones": "#C44E52",
    "Monitor": "#8172B2",
}
SEABORN_PALETTE = list(REGION_COLORS.values())

REQUIRED_COLUMNS = ["Date", "Product", "Quantity", "Price", "Customer_ID", "Region", "Total_Sales"]


def load_and_prepare(path: str) -> pd.DataFrame:
    """Load sales_data.csv, validate it, and add standard derived columns."""
    if not os.path.exists(path):
        print(f"ERROR: data file not found at {path}")
        sys.exit(1)
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"ERROR reading data file: {e}")
        sys.exit(1)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        print(f"ERROR: missing required column(s): {missing}")
        sys.exit(1)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    df["Product"] = df["Product"].str.strip().str.title()
    df["Region"] = df["Region"].str.strip().str.title()
    df["Month"] = df["Date"].dt.to_period("M")
    df["MonthLabel"] = df["Date"].dt.strftime("%b %Y")
    return df


try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


PLOTLY_HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
<style>
  body {{ font-family: -apple-system, Arial, sans-serif; margin: 0; padding: 16px; background: #fafafa; }}
  h2 {{ color: #2C3E50; margin: 4px 0 12px 0; }}
  #chart {{ background: white; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.12); }}
</style>
</head>
<body>
<h2>{title}</h2>
<div id="chart"></div>
<script>
  var fig = {fig_json};
  Plotly.newPlot('chart', fig.data, fig.layout, {{responsive: true}});
  {frames_js}
</script>
</body>
</html>
"""


def plotly_fragment_html(fig_dict: dict, div_id: str = "chart") -> str:
    """
    Return a self-contained HTML fragment (CDN script + a div + the JS call)
    for embedding a Plotly figure dict inline in a notebook cell's output or
    a larger dashboard page.
    """
    frames_js = ""
    if fig_dict.get("frames"):
        frames_js = f"Plotly.addFrames('{div_id}', fig.frames);\n"
    return (
        f'<div id="{div_id}" style="width:100%;"></div>\n'
        f"<script src=\"https://cdn.plot.ly/plotly-2.32.0.min.js\"></script>\n"
        f"<script>\n"
        f"  var fig = {json.dumps(fig_dict)};\n"
        f"  Plotly.newPlot('{div_id}', fig.data, fig.layout, {{responsive: true}});\n"
        f"  {frames_js}"
        f"</script>\n"
    )


def render_plotly_html(fig_dict: dict, path: str, title: str):
    """
    Write a Plotly figure dict to a standalone interactive HTML file.
    Uses the real `plotly` package if available; otherwise falls back to a
    hand-built HTML template that loads plotly.js from a CDN and renders the
    exact same figure JSON. Both paths produce an equivalent interactive chart.
    """
    if PLOTLY_AVAILABLE:
        fig = go.Figure(fig_dict)
        fig.write_html(path, include_plotlyjs="cdn", full_html=True)
    else:
        frames_js = ""
        if fig_dict.get("frames"):
            frames_js = "Plotly.addFrames('chart', fig.frames);\n"
        html = PLOTLY_HTML_TEMPLATE.format(
            title=title,
            fig_json=json.dumps(fig_dict),
            frames_js=frames_js,
        )
        with open(path, "w") as f:
            f.write(html)
    print(f"Saved: {path}")
