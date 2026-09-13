"""
dashboard.py
============
Week 6 Project — Interactive Sales Dashboard (pipeline script)

Builds the full visualization suite from sales_data.csv:
  - Seaborn statistical plots: box plot, violin plot, correlation heatmap,
    region x product heatmap
  - A 2x2 static subplot dashboard combining 4 chart types
  - Interactive Plotly charts: hover scatter, dropdown-driven bar chart,
    and an animated "sales race" bar chart with a play button + slider
  - A combined dashboard.html page embedding everything

Shared data loading, color palette, and the Plotly HTML renderer live in
data_utils.py so this script and dashboard.ipynb never drift apart.

Run with:
    python dashboard.py
"""
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from data_utils import (
    load_and_prepare, REGION_COLORS, PRODUCT_COLORS, SEABORN_PALETTE,
    render_plotly_html, PLOTLY_AVAILABLE,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "sales_data.csv")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")
os.makedirs(VIZ_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette=SEABORN_PALETTE)
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
})


# ---------------------------------------------------------------------------
# Day 1-2: Seaborn statistical plots (box + violin)
# ---------------------------------------------------------------------------
def make_box_plot(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 5.5))
    order = df.groupby("Product")["Total_Sales"].median().sort_values(ascending=False).index
    sns.boxplot(x="Product", y="Total_Sales", data=df, order=order,
                hue="Product", palette=PRODUCT_COLORS, legend=False, ax=ax)
    sns.stripplot(x="Product", y="Total_Sales", data=df, order=order,
                  color="black", alpha=0.35, size=3, jitter=True, ax=ax)
    ax.set_title("Order Value Distribution by Product")
    ax.set_xlabel("Product"); ax.set_ylabel("Total Sales ($)")
    plt.tight_layout()
    path = os.path.join(VIZ_DIR, "01_box_plot_product.png")
    plt.savefig(path, dpi=150); plt.close()
    print(f"Saved: {path}")


def make_violin_plot(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 5.5))
    order = df.groupby("Region")["Total_Sales"].median().sort_values(ascending=False).index
    sns.violinplot(x="Region", y="Total_Sales", data=df, order=order,
                    hue="Region", palette=REGION_COLORS, legend=False,
                    inner="quartile", cut=0, ax=ax)
    medians = df.groupby("Region")["Total_Sales"].median()
    for i, region in enumerate(order):
        ax.annotate(f"median: ${medians[region]:,.0f}",
                    xy=(i, medians[region]), xytext=(i, medians[region] + 60000),
                    ha="center", fontsize=9, color="#333333",
                    arrowprops=dict(arrowstyle="->", color="#666666", lw=0.8))
    ax.set_title("Order Value Distribution by Region (with medians)")
    ax.set_xlabel("Region"); ax.set_ylabel("Total Sales ($)")
    plt.tight_layout()
    path = os.path.join(VIZ_DIR, "02_violin_plot_region.png")
    plt.savefig(path, dpi=150); plt.close()
    print(f"Saved: {path}")


# ---------------------------------------------------------------------------
# Day 3: Heatmaps
# ---------------------------------------------------------------------------
def make_correlation_heatmap(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6.5, 5))
    corr = df[["Quantity", "Price", "Total_Sales"]].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
                vmin=-1, vmax=1, square=True, linewidths=0.5, ax=ax,
                cbar_kws={"label": "Correlation", "shrink": 0.85})
    ax.set_title("Correlation Heatmap: Numeric Fields", pad=14)
    plt.tight_layout()
    path = os.path.join(VIZ_DIR, "03_correlation_heatmap.png")
    plt.savefig(path, dpi=150); plt.close()
    print(f"Saved: {path}")


def make_region_product_heatmap(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 5))
    pivot = pd.pivot_table(df, index="Region", columns="Product",
                            values="Total_Sales", aggfunc="sum", fill_value=0)
    sns.heatmap(pivot, annot=True, fmt=",.0f", cmap="Blues", linewidths=0.5,
                ax=ax, cbar_kws={"label": "Total Sales ($)"})
    ax.set_title("Total Sales Heatmap: Region x Product")
    plt.tight_layout()
    path = os.path.join(VIZ_DIR, "04_region_product_heatmap.png")
    plt.savefig(path, dpi=150); plt.close()
    print(f"Saved: {path}")


# ---------------------------------------------------------------------------
# Day 4: 2x2 subplot dashboard
# ---------------------------------------------------------------------------
def make_subplot_dashboard(df: pd.DataFrame):
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    fig.suptitle("Sales Overview Dashboard", fontsize=18, fontweight="bold", y=0.98)

    product_sales = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
    bars = axes[0, 0].bar(product_sales.index, product_sales.values,
                           color=[PRODUCT_COLORS[p] for p in product_sales.index])
    axes[0, 0].set_title("Total Sales by Product")
    axes[0, 0].set_ylabel("Total Sales ($)")
    axes[0, 0].bar_label(bars, fmt="${:,.0f}".format, padding=2, fontsize=8)
    axes[0, 0].tick_params(axis="x", rotation=15)

    monthly = df.groupby("Month")["Total_Sales"].sum().sort_index()
    axes[0, 1].plot(monthly.index.astype(str), monthly.values, marker="o",
                     color="#4C72B0", linewidth=2)
    axes[0, 1].set_title("Monthly Sales Trend")
    axes[0, 1].set_ylabel("Total Sales ($)")
    axes[0, 1].tick_params(axis="x", rotation=20)

    region_sales = df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
    axes[1, 0].pie(region_sales.values, labels=region_sales.index, autopct="%1.1f%%",
                    colors=[REGION_COLORS[r] for r in region_sales.index], startangle=90)
    axes[1, 0].set_title("Sales Share by Region")

    order = df.groupby("Product")["Price"].median().sort_values(ascending=False).index
    sns.boxplot(x="Product", y="Price", data=df, order=order, ax=axes[1, 1],
                hue="Product", palette=PRODUCT_COLORS, legend=False)
    axes[1, 1].set_title("Price Distribution by Product")
    axes[1, 1].set_ylabel("Unit Price ($)")
    axes[1, 1].tick_params(axis="x", rotation=15)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    path = os.path.join(VIZ_DIR, "05_2x2_subplot_dashboard.png")
    plt.savefig(path, dpi=150); plt.close()
    print(f"Saved: {path}")


# ---------------------------------------------------------------------------
# Day 5: Interactive Plotly charts (hover, dropdown, animation)
# ---------------------------------------------------------------------------
def make_interactive_scatter(df: pd.DataFrame):
    traces = []
    for region in sorted(df["Region"].unique()):
        sub = df[df["Region"] == region]
        traces.append({
            "type": "scatter", "mode": "markers", "name": region,
            "x": sub["Quantity"].tolist(), "y": sub["Price"].tolist(),
            "marker": {
                "size": (sub["Total_Sales"] / sub["Total_Sales"].max() * 40 + 8).tolist(),
                "color": REGION_COLORS[region], "opacity": 0.75,
                "line": {"width": 1, "color": "white"},
            },
            "customdata": list(zip(sub["Product"], sub["Customer_ID"], sub["Total_Sales"])),
            "hovertemplate": (
                "<b>%{customdata[0]}</b><br>Customer: %{customdata[1]}<br>"
                "Quantity: %{x}<br>Unit Price: $%{y:,.0f}<br>"
                "Total Sale: $%{customdata[2]:,.0f}<extra>" + region + "</extra>"
            ),
        })
    fig_dict = {
        "data": traces,
        "layout": {
            "title": {"text": "Quantity vs. Unit Price (bubble size = order total, hover for details)"},
            "xaxis": {"title": {"text": "Quantity"}},
            "yaxis": {"title": {"text": "Unit Price ($)"}},
            "legend": {"title": {"text": "Region"}},
            "template": "plotly_white", "height": 550,
        },
    }
    render_plotly_html(fig_dict, os.path.join(VIZ_DIR, "06_interactive_scatter.html"),
                        "Interactive: Quantity vs. Price by Region")
    return fig_dict


def make_interactive_dropdown_bar(df: pd.DataFrame):
    by_product = df.groupby("Product")
    metrics = {
        "Total Sales ($)": by_product["Total_Sales"].sum(),
        "Average Order Value ($)": by_product["Total_Sales"].mean(),
        "Units Sold": by_product["Quantity"].sum(),
        "Orders Count": by_product["Total_Sales"].count(),
    }
    order = metrics["Total Sales ($)"].sort_values(ascending=False).index.tolist()
    metrics = {k: v.reindex(order) for k, v in metrics.items()}
    metric_names = list(metrics.keys())
    initial = metric_names[0]

    trace = {"type": "bar", "x": order, "y": metrics[initial].tolist(),
              "marker": {"color": [PRODUCT_COLORS[p] for p in order]}, "name": initial}

    buttons = [{"label": name, "method": "update",
                "args": [{"y": [metrics[name].tolist()]},
                         {"yaxis": {"title": {"text": name}}}]}
               for name in metric_names]

    fig_dict = {
        "data": [trace],
        "layout": {
            "title": {"text": "Product Performance (use the dropdown to change metric)"},
            "xaxis": {"title": {"text": "Product"}},
            "yaxis": {"title": {"text": initial}},
            "updatemenus": [{"type": "dropdown", "x": 1.0, "xanchor": "right",
                              "y": 1.18, "yanchor": "top", "buttons": buttons}],
            "template": "plotly_white", "height": 550,
        },
    }
    render_plotly_html(fig_dict, os.path.join(VIZ_DIR, "07_interactive_dropdown_bar.html"),
                        "Interactive: Product Performance (Dropdown)")
    return fig_dict


def make_interactive_animated_race(df: pd.DataFrame):
    months = sorted(df["Month"].unique())
    products = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False).index.tolist()

    cumulative = pd.DataFrame(0.0, index=months, columns=products)
    for m in months:
        totals = df[df["Month"] <= m].groupby("Product")["Total_Sales"].sum()
        for p in products:
            cumulative.loc[m, p] = totals.get(p, 0.0)

    frames = [{"name": str(m),
               "data": [{"type": "bar", "x": products,
                         "y": cumulative.loc[m, products].tolist(),
                         "marker": {"color": [PRODUCT_COLORS[p] for p in products]}}]}
              for m in months]

    slider_steps = [{"label": str(m), "method": "animate",
                      "args": [[str(m)], {"mode": "immediate",
                                           "frame": {"duration": 600, "redraw": True},
                                           "transition": {"duration": 300}}]}
                     for m in months]

    fig_dict = {
        "data": frames[0]["data"],
        "layout": {
            "title": {"text": "Cumulative Product Sales by Month (press Play)"},
            "xaxis": {"title": {"text": "Product"}},
            "yaxis": {"title": {"text": "Cumulative Total Sales ($)"},
                      "range": [0, cumulative.values.max() * 1.1]},
            "template": "plotly_white", "height": 550,
            "updatemenus": [{"type": "buttons", "x": 1.0, "xanchor": "right",
                              "y": 1.18, "yanchor": "top", "buttons": [
                {"label": "Play", "method": "animate",
                 "args": [None, {"fromcurrent": True,
                                  "frame": {"duration": 600, "redraw": True},
                                  "transition": {"duration": 300}}]},
                {"label": "Pause", "method": "animate",
                 "args": [[None], {"mode": "immediate", "frame": {"duration": 0}}]},
            ]}],
            "sliders": [{"active": 0, "x": 0.1, "len": 0.85, "steps": slider_steps}],
        },
        "frames": frames,
    }
    render_plotly_html(fig_dict, os.path.join(VIZ_DIR, "08_interactive_animated_race.html"),
                        "Interactive: Cumulative Sales Race")
    return fig_dict


# ---------------------------------------------------------------------------
# Combine into one dashboard.html page
# ---------------------------------------------------------------------------
def build_dashboard_html(scatter_fig, dropdown_fig, race_fig):
    charts = [
        ("chart1", scatter_fig, "Quantity vs. Price by Region"),
        ("chart2", dropdown_fig, "Product Performance (Dropdown)"),
        ("chart3", race_fig, "Cumulative Sales Race (Animated)"),
    ]
    static_imgs = [
        ("01_box_plot_product.png", "Order Value Distribution by Product"),
        ("02_violin_plot_region.png", "Order Value Distribution by Region"),
        ("03_correlation_heatmap.png", "Correlation Heatmap"),
        ("04_region_product_heatmap.png", "Region x Product Sales Heatmap"),
        ("05_2x2_subplot_dashboard.png", "Sales Overview (2x2 Dashboard)"),
    ]

    divs, scripts = "", ""
    for div_id, fig, title in charts:
        divs += f'<div class="card"><h3>{title}</h3><div id="{div_id}" class="plotly-chart"></div></div>\n'
        scripts += f"var {div_id}_fig = {json.dumps(fig)};\n"
        scripts += f"Plotly.newPlot('{div_id}', {div_id}_fig.data, {div_id}_fig.layout, {{responsive:true}});\n"
        if fig.get("frames"):
            scripts += f"Plotly.addFrames('{div_id}', {div_id}_fig.frames);\n"

    img_cards = ""
    for fname, title in static_imgs:
        img_cards += (f'<div class="card"><h3>{title}</h3>'
                       f'<img src="visualizations/{fname}" style="width:100%;border-radius:6px;"></div>\n')

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Interactive Sales Dashboard</title>
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
<style>
  body {{ font-family: -apple-system, Arial, sans-serif; background: #F4F6F7; margin: 0; padding: 0 0 40px 0; }}
  header {{ background: linear-gradient(135deg, #4C72B0, #55A868); color: white; padding: 28px 40px; }}
  header h1 {{ margin: 0; font-size: 26px; }}
  header p {{ margin: 6px 0 0 0; opacity: 0.9; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(460px, 1fr)); gap: 20px; padding: 24px 40px; }}
  .card {{ background: white; border-radius: 10px; box-shadow: 0 1px 4px rgba(0,0,0,0.12); padding: 16px; }}
  .card h3 {{ margin: 0 0 10px 0; color: #2C3E50; font-size: 15px; }}
  .plotly-chart {{ width: 100%; }}
  .section-title {{ padding: 20px 40px 0 40px; color: #2C3E50; }}
</style>
</head>
<body>
<header>
  <h1>Interactive Sales Dashboard</h1>
  <p>Sales trends, customer segmentation, and product performance &mdash; sales_data.csv</p>
</header>
<h2 class="section-title">Interactive (Plotly)</h2>
<div class="grid">
{divs}
</div>
<h2 class="section-title">Statistical Views (Seaborn)</h2>
<div class="grid">
{img_cards}
</div>
<script>
{scripts}
</script>
</body>
</html>
"""
    path = os.path.join(BASE_DIR, "dashboard.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"Saved: {path}")


def main():
    print("=" * 60)
    print("INTERACTIVE SALES DASHBOARD")
    print("=" * 60)
    if not PLOTLY_AVAILABLE:
        print("NOTE: 'plotly' package not found — using the built-in HTML/JS "
              "fallback renderer. Interactive charts still work when opened "
              "in a browser. Install requirements.txt for the standard path.")

    df = load_and_prepare(DATA_PATH)
    print(f"Loaded and prepared {len(df)} rows.")

    make_box_plot(df)
    make_violin_plot(df)
    make_correlation_heatmap(df)
    make_region_product_heatmap(df)
    make_subplot_dashboard(df)

    scatter_fig = make_interactive_scatter(df)
    dropdown_fig = make_interactive_dropdown_bar(df)
    race_fig = make_interactive_animated_race(df)

    build_dashboard_html(scatter_fig, dropdown_fig, race_fig)
    print("\nDone. Open dashboard.html in a browser for the full interactive experience.")


if __name__ == "__main__":
    main()
