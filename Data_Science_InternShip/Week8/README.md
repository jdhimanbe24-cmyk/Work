# Reducing New-Customer Churn: A Complete Business Analysis

**Capstone Project — Week 8, Data Analysis Bootcamp**

## 1. Project Overview

A subscription business needs to reduce customer churn: every lost customer
is lost recurring revenue and a wasted acquisition cost. This capstone
conducts a complete, end-to-end analysis — from raw data to a phased
business implementation plan — to answer: **who is at risk of churning, why,
and what should the business do about it?**

**Objectives**
1. Quantify the current churn rate and its business cost.
2. Identify statistically-validated churn drivers (not just visual correlations).
3. Build a predictive model that flags at-risk customers before they leave.
4. Segment the customer base to prioritize retention spend.
5. Translate all of the above into a concrete, phased implementation plan.

**Headline finding:** 100% of churned customers left within their first 11
months of tenure — churn beyond that point is effectively zero. This
reframes the whole problem from general churn prediction to **first-year
retention**, and drives every recommendation in this project.

**Success metrics set at the start of the project:**
- A churn-driver list validated by hypothesis testing.
- A predictive model with recall ≥ 0.90 on churners (a missed churner costs
  more than an unnecessary retention email, so recall was prioritized).
- A segmentation identifying which customer group carries disproportionate risk.
- A written implementation plan with phases, owners, and trackable metrics.

All of these were met — see Section 7 for results.

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
4. Open and run `capstone_analysis.ipynb` in Jupyter — it already contains
   its own saved output (tables, charts, printed results), so you can also
   just read it top to bottom without re-running it. Running it fresh
   regenerates `data/cleaned_data.csv`, everything in `visualizations/`, and
   `reports/key_findings.txt`.
5. Read `reports/executive_summary.pdf` (1 page) for the business-facing
   summary, or `reports/technical_report.pdf` (9 pages) for full methodology.
6. Open `presentation/business_presentation.pptx` for the stakeholder
   presentation (13 slides).

## 3. Code Structure

```
capstone-churn-analysis/
├── README.md                          # This file
├── capstone_analysis.ipynb            # Full end-to-end analysis, with saved output
├── requirements.txt                   # Python dependencies
├── data/
│   ├── raw_data.csv                   # Raw source: customer_churn.csv (500 rows)
│   ├── cleaned_data.csv               # Cleaned + feature-engineered version
│   ├── sales_data_not_used.csv        # Considered, not selected (see Section 4)
│   └── house_prices_not_used.csv      # Considered, not selected (see Section 4)
├── reports/
│   ├── executive_summary.pdf          # 1-page business summary
│   ├── technical_report.pdf           # 9-page full methodology & results
│   └── key_findings.txt               # Machine-generated summary of all key numbers
├── presentation/
│   └── business_presentation.pptx     # 13-slide stakeholder deck
└── visualizations/
    ├── 01_churn_overview.png
    ├── 02_distributions_by_churn.png
    ├── 03_churn_by_category.png
    ├── 04_churn_by_tenure_bucket.png  # The "First-Year Cliff" chart
    ├── 05_correlation_heatmap.png
    ├── 06_model_performance.png       # Confusion matrix + ROC curve
    ├── 07_feature_importance.png
    └── 08_customer_segments.png
```

The notebook follows the assignment's 5-phase structure (Planning → Data
Collection & Prep → EDA → Advanced Analysis → Insights & Recommendations) in
a single notebook, matching the required submission structure
(`capstone_analysis.ipynb` at the root, rather than three separate
phase-notebooks).

## 4. Dataset Selection

Three datasets were available. The assignment requires a minimum of 500
rows; only one qualifies:

| Dataset | Rows | Selected? |
|---|---|---|
| `sales_data.csv` | 100 | No — below the 500-row minimum |
| `house_prices.csv` | 300 | No — below the 500-row minimum |
| `customer_churn.csv` | **500** | **Yes** |

`customer_churn.csv` is used as the sole dataset. It's also the strongest
fit for a retention-focused business problem, which is common and
high-value across subscription businesses. The other two are kept in
`data/` (suffixed `_not_used`) purely for transparency about what was
considered.

**Raw data:** `CustomerID, Tenure, MonthlyCharges, TotalCharges, Contract,
PaymentMethod, PaperlessBilling, SeniorCitizen, Churn`. Data quality checks
found zero missing values, zero duplicate rows, zero duplicate customer IDs,
no implausible numeric ranges, and consistent categorical labels — no
repair was required, though a cleaning/feature-engineering pipeline was
still built (tenure buckets, paperless-billing flag, average monthly
spend-to-date) so it's ready for messier future data refreshes.

## 5. Technical Details

**Exploratory Data Analysis:** descriptive statistics, distribution
histograms split by churn status, categorical breakdowns (churn rate by
contract type and payment method), tenure-bucket analysis (which surfaced
the First-Year Cliff), and a correlation heatmap.

**Analysis techniques (4, exceeding the required minimum of 3):**

1. **Hypothesis testing** — 5 tests (chi-square and independent t-tests,
   with Levene's test checking the equal-variance assumption first) validate
   which EDA patterns are statistically real: contract type (p<0.001) and
   tenure (p<0.001) are confirmed drivers; payment method (p=0.145) and
   senior citizen status (p=0.795) are not significant at this sample size.

2. **Predictive modeling** — a logistic regression (`scikit-learn`,
   `class_weight='balanced'` since churn is rare) trained on a stratified
   75/25 split. Achieves 100% recall, 65% precision, and 0.987 ROC AUC on
   held-out test data.

3. **A critical baseline check** — since 100% of churners have tenure
   ≤11 months, a one-line rule ("flag Tenure < 12 months") was tested
   against the full model and found to match its recall almost exactly
   (100% recall, 64% precision, 94% accuracy). This is reported as an
   honest finding, not hidden in favor of the fancier model: **the simple
   rule ships immediately; the model adds incremental value as a
   secondary risk-ranking layer.**

4. **Customer segmentation** — K-Means clustering (k=3, chosen via
   silhouette score comparison across k=2–6) on Tenure, MonthlyCharges, and
   TotalCharges. One segment (higher monthly charges, lower average tenure)
   shows 21.8% churn versus ~4.5% in the other two segments.

**Visualizations (8, exceeding the required minimum of 5):** churn overview
(bar + pie), tenure/charges distributions by churn, churn rate by category,
the First-Year Cliff bar chart, a correlation heatmap, confusion matrix + ROC
curve, feature-importance chart, and a segmentation scatter + churn-rate
comparison.

## 6. Testing Evidence

- All 39 notebook cells execute top-to-bottom with **zero errors** —
  verified by parsing the saved `.ipynb` JSON for `error` output types.
- Data quality was checked programmatically before any modeling began:
  missing values, duplicate rows, duplicate IDs, implausible numeric ranges,
  and categorical label consistency all passed.
- Levene's test validated the equal-variance assumption before each
  independent t-test (used to decide between Student's and Welch's t-test).
- The predictive model was evaluated on a **held-out test set** (stratified
  split, never seen during training) and cross-checked against an
  independent, simple baseline rule rather than trusting its metrics in
  isolation.
- K-Means cluster count (k=3) was chosen using silhouette scores computed
  across k=2–6, reported honestly as modest (0.25–0.31) rather than
  overclaiming sharp cluster separation.
- The presentation deck passed structural validation
  (`scripts/office/validate.py`: all checks passed), content QA (no
  placeholder text, no typos found via `markitdown` review), and slide-by-
  slide visual QA (rendered to images and inspected for overflow, overlap,
  contrast, and alignment issues).

## 7. Results Against Success Metrics

| Success metric (set in Phase 1) | Result |
|---|---|
| Validated churn-driver list | ✅ 2 of 5 hypothesis tests significant (contract type, tenure); reported honestly alongside 3 non-significant results |
| Model recall ≥ 0.90 on churners | ✅ 1.00 recall on held-out test set |
| Segmentation identifying disproportionate risk | ✅ One segment at 21.8% churn vs. ~4.5% elsewhere |
| Phased implementation plan with owners & metrics | ✅ 4-phase plan, Section 7 of the technical report |

## 8. Key Findings & Recommendations

See `reports/executive_summary.pdf` for the 1-page business summary and
`reports/technical_report.pdf` for full detail. In short:

1. **This is a first-year retention problem, not a general churn problem.**
2. **Contract length is the strongest actionable lever** — month-to-month
   customers churn far more than annual-contract customers.
3. **A one-line rule captures almost all the value of the full model** —
   ship it immediately.
4. **One customer segment carries disproportionate churn risk** and is the
   best target for a proactive retention campaign.

**Implementation plan:** (1) deploy the tenure flag in the CRM within 2
weeks, (2) incentivize contract upgrades within 6 weeks, (3) build a
dedicated onboarding track for the high-risk segment within 10 weeks, (4)
retrain the model quarterly on an ongoing basis.

## 9. Portfolio Note

This project demonstrates a full analysis lifecycle — business framing,
data quality validation, EDA, statistical hypothesis testing, predictive
modeling, unsupervised segmentation, and stakeholder communication (a
1-page executive summary, a 9-page technical report, and a 13-slide
presentation) — on a single, realistic business problem. The most
portfolio-worthy aspect isn't the modeling (a logistic regression is
standard), but the judgment calls made along the way: choosing the
qualifying dataset transparently, reporting non-significant hypothesis
tests honestly, and recommending a simpler solution over a fancier one
once the evidence supported it.
