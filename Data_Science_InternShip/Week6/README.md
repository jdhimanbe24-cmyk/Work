# Interactive Sales Dashboard

**Week 6 Project — Data Visualization Mastery with Seaborn & Plotly**

## 1. Project Overview

This project builds a full visualization suite from `sales_data.csv` (100
orders, Jan–Apr 2024): five statistical/static charts with Seaborn and
matplotlib, plus three interactive Plotly charts with hover tooltips, a
dropdown filter, and a play/pause animation — all combined into one cohesive
`dashboard.html` page. The goal is to practice advanced chart types (box,
violin, heatmap), multi-plot layouts, and interactivity, and to tell a clear
story about sales trends, customer segmentation, and product performance.

## 2. Setup Instructions

1. Clone or download this repository.
2. (Recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Generate everything (charts, interactive HTML, combined dashboard):
   ```bash
   python dashboard.py
   ```
5. Open `dashboard.html` in a browser for the full interactive experience,
   or open `dashboard.ipynb` in Jupyter to read the narrative walkthrough
   (it already contains its own saved output, so you can also just read it
   top to bottom without re-running it).

## 3. Code Structure

```
sales-dashboard-project/
├── README.md                    # This file
├── dashboard.py                 # Reproducible pipeline script (generates everything)
├── dashboard.ipynb              # Narrative walkthrough notebook, with saved output
├── data_utils.py                # Shared: data loading, color palette, Plotly HTML renderer
├── sales_data.csv               # 100 sales transactions
├── requirements.txt             # Python dependencies
├── dashboard_demo.gif           # Slideshow preview of the dashboard's charts
├── dashboard.html               # Combined dashboard page (static charts + interactive)
└── visualizations/
    ├── 00_basic_order_counts.png
    ├── 01_box_plot_product.png
    ├── 02_violin_plot_region.png
    ├── 03_correlation_heatmap.png
    ├── 04_region_product_heatmap.png
    ├── 05_2x2_subplot_dashboard.png
    ├── 06_interactive_scatter.html
    ├── 07_interactive_dropdown_bar.html
    └── 08_interactive_animated_race.html
```

`data_utils.py` holds everything shared between `dashboard.py` and
`dashboard.ipynb` (data loading/validation, the color palette, and the
Plotly HTML renderer) so the script and notebook never drift out of sync.
`dashboard.py` is organized as one function per chart, mirroring the
assignment's 7-day plan (Seaborn basics → statistical plots → heatmaps →
2x2 dashboard → interactive Plotly → integration → polish).

## 4. Dashboard Guide — Interpreting Each Visualization

| # | Chart | Type | What it shows | Key takeaway |
|---|---|---|---|---|
| 1 | Order Counts by Product | Bar (Seaborn) | How many orders per product | Tablet and Laptop have the most orders |
| 2 | Order Value by Product | Box plot | Spread & outliers of order value per product | Laptop & Phone have the widest, highest-value spread |
| 3 | Order Value by Region | Violin plot | Full distribution shape per region, with medians | East has the highest typical order; North has more large orders overall |
| 4 | Correlation Heatmap | Heatmap | Linear relationships between Quantity, Price, Total_Sales | Total_Sales tracks Quantity (0.69) slightly more than Price (0.65) |
| 5 | Region x Product Heatmap | Heatmap | Total sales for every region/product combination | North's Laptop sales dominate a single cell (~$1.8M) |
| 6 | Sales Overview | 2x2 subplot (bar, line, pie, box) | Four angles on the data at a glance | One-screen summary for a standup or exec update |
| 7 | Quantity vs. Price | Interactive scatter | Order-level detail with hover tooltips, bubble size = order total | Spot outlier orders (high quantity AND high price) instantly |
| 8 | Product Performance | Interactive dropdown bar | Same chart, four swappable metrics | Total Sales and Units Sold don't always agree on the "top" product |
| 9 | Cumulative Sales Race | Interactive animation | How product rankings evolve month by month | Laptop pulls ahead early and holds the lead throughout |

**Executive summary:** Laptop and Phone are the revenue anchors; North and
South are the strongest regions but with different product mixes, which
should inform regional stocking. The interactive scatter is the best tool
for spotting individual outlier orders worth a closer look, while the
animated race shows the product ranking has been stable since February.

## 5. Technical Details

- **Color scheme:** one shared palette (`REGION_COLORS`, `PRODUCT_COLORS` in
  `data_utils.py`) is used across every chart — Seaborn and Plotly alike —
  so the whole dashboard reads as one visual product.
- **Statistical plots:** `sns.boxplot` + `sns.stripplot` (individual points
  overlaid on the box plot); `sns.violinplot` with `inner='quartile'`,
  `cut=0` (so the KDE doesn't imply impossible negative sales), and manual
  median annotations via `ax.annotate`.
- **Heatmaps:** a correlation matrix (`df.corr()`) and a custom heatmap built
  from a `pd.pivot_table` (Region × Product), both via `sns.heatmap`.
- **2×2 dashboard:** `plt.subplots(2, 2, ...)` combining a bar chart, line
  chart, pie chart, and box plot into one static figure with a shared title.
- **Interactive charts:** each is built as a plain Python dict following the
  Plotly.js figure schema (`{"data": [...], "layout": {...}, "frames": [...]}`).
  `render_plotly_html()` / `plotly_fragment_html()` in `data_utils.py` render
  that dict two ways:
  1. If the `plotly` package is installed, wrap it in `go.Figure(...)` and
     use the standard `fig.write_html(...)`.
  2. If not installed, write the exact same figure JSON into a small HTML
     template that loads plotly.js from a CDN and calls `Plotly.newPlot` /
     `Plotly.addFrames` directly.
  Both paths feed plotly.js identical JSON, so the rendered chart is the
  same either way — hover tooltips (`hovertemplate` + `customdata`), a
  dropdown (`updatemenus` with `method: "update"` swapping the y-data), and
  an animation (`frames` + a slider + Play/Pause buttons via
  `method: "animate"`).
- **Dashboard integration:** `build_dashboard_html()` assembles all 8 charts
  (5 static images + 3 interactive) into one page with a shared gradient
  header, a card-based CSS grid, and consistent typography.

## 6. A Note on the Build Environment (Plotly & the Demo GIF)

This project was built in a sandbox with **no internet access**, which
affected two things worth being upfront about:

- **The `plotly` Python package could not be installed.** `dashboard.py`
  and `dashboard.ipynb` both detect this (`PLOTLY_AVAILABLE` in
  `data_utils.py`) and fall back to the hand-built HTML/JS renderer
  described above. The figure dicts are identical either way — running
  `pip install -r requirements.txt` (which includes `plotly`) switches you
  onto the standard `go.Figure(...).write_html(...)` code path with no
  other changes needed.
- **The interactive charts require internet access in the browser that
  opens them**, because they load plotly.js from a CDN
  (`cdn.plot.ly`) — this is standard behavior, identical to what
  `fig.write_html(..., include_plotlyjs='cdn')` does by default. In the
  build sandbox, a headless-browser test confirmed the JSON figure specs
  are valid and load-ready, but the actual CDN request returned a 403 in
  that sandboxed network, so a live screenshot couldn't be captured there.
  This will not affect you opening the files normally.
- **`dashboard_demo.gif` is a static slideshow**, not a screen recording of
  live interaction — no screen-recording tool was available in the build
  environment. It cycles through the dashboard's charts with captions. For
  the real interactive experience (hover, dropdown, play button), open
  `dashboard.html` or `visualizations/06_interactive_scatter.html` /
  `07_interactive_dropdown_bar.html` / `08_interactive_animated_race.html`
  directly in a browser.

## 7. Testing Evidence

- `dashboard.py` was run end-to-end with zero errors; every chart function
  printed a confirmation line with its saved file path.
- `dashboard.ipynb`'s 22 cells were all executed for real (not just
  written) — 6 cells produced captured chart images and 3 produced captured
  interactive HTML fragments, with zero error outputs.
- Each interactive chart's figure dict was independently validated by
  re-parsing the embedded JSON out of the generated HTML files and checking
  trace/frame counts match expectations (scatter: 4 region traces;
  dropdown bar: 1 trace + 4-option dropdown; animated race: 1 trace + 4
  monthly frames + play/pause buttons).
- A headless Chromium browser (Playwright) was used to load the generated
  HTML files and capture console/network errors — confirming the only
  failure mode in this sandbox is the blocked CDN request (403), not a
  defect in the generated markup or JSON.
- `load_and_prepare()` in `data_utils.py` validates required columns and
  exits with a clear error message on a missing file, empty file, or
  missing column — this defensive path was exercised manually against a
  nonexistent file path and an empty CSV during development.

## 8. Visual Documentation

All 5 static charts are in `visualizations/` as PNGs and are also embedded
directly in `dashboard.ipynb` and `dashboard.html`. The 3 interactive charts
are in `visualizations/` as standalone HTML files (openable directly) and
are also embedded in `dashboard.html` and `dashboard.ipynb`.
`dashboard_demo.gif` gives a quick visual tour of the whole set.
