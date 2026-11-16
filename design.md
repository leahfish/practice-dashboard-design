# Design

How the dashboard looks: each screen as drawn, and the style rules every
chart follows. `/dashkit:design` draws the screens from `spec.md` and builds
`mockup.py`; `/dashkit:review-dashboard` checks the finished app against this
file. The rules live in code in `dashboard/charts.py` and
`.streamlit/config.toml`; change a rule here and there together.

---

## Screens

### Charts

One row per framed question in `spec.md`.

| # | Framed question | Chart | Why |
|---|---|---|---|
| 1 | Top five genres and each one's share of revenue | Horizontal bars of percentages (`charts.ranked_bar(kind="percent")`) | Shares of a whole, five parts |
| 2 | Top five countries and each one's share of revenue | Horizontal bars of percentages (`charts.ranked_bar(kind="percent")`) | Shares of a whole; matches question 1 so the two read side by side |
| 3 | Genre-and-country pairs that earn the most | Horizontal bars, top 10 pairs (`charts.ranked_bar`) | Items ranked by size |
| 4 | Revenue each year 2021-2025 and change from the prior year | Table: year · revenue · change vs prior year, drops in red (`st.dataframe`) | Five exact values and percentages Morgan will quote; question 5 shows the shape |
| 5 | Monthly revenue across the full period | A line, 60 months (`charts.trend_line`) | Change over time |
| 6 | Share of revenue from the top 10 customers | Horizontal bars of the top 10 customers' revenue (`charts.ranked_bar`) | Shows how concentrated revenue is; the headline gives the share |
| 7 | Years (of five) each top-10 customer bought in | Table: customer · revenue · years active (`st.dataframe`) | Ten names with exact counts to look up |
| 8 | Revenue from each sales support rep's customers | Horizontal bars (`charts.ranked_bar`) | Items ranked by size |
| 9 | Customers per rep and average revenue per customer | Table: rep · customers · revenue per customer (`st.dataframe`) | Two measures side by side; exact values |
| 10 | Do the totals tie out with Finance | A tile on every screen: grand total, date range, reconciliation gap $0.00 (`charts.kpi_row`) | The spec puts the grand total on every screen |

### Headline tiles

| Screen | Tiles (each against a comparison) |
|---|---|
| 1. Where the money comes from | Total revenue (vs prior year when one year is picked) · Top genre's share (Rock 35.5%) · Top country's share (USA 22.5%) · Ties to Finance (gap $0.00) |
| 2. Growth | Latest year's revenue (2025, vs 2024) · Average yearly revenue · Best year (2022) · Ties to Finance |
| 3. Customers | Top 10 customers' share (vs their share if all 59 customers spent equally, 16.9%) · Top-10 customers who bought in all five years (2 of 10) · Ties to Finance |
| 4. Sales reps | Top rep's customer revenue (vs the rep average) · Customers across reps (59 across 3) · Ties to Finance |

The Screen 1 year picker defaults to all years, as `spec.md` sets it; the
spec overrides the "most recent complete period" default below.

---

## Style rules

### Page

- Each screen opens with one sentence stating the main takeaway, then a row
  of three or four headline numbers (`charts.kpi_row`), each shown against a
  comparison: last year, a target, or the average.
- Then one section per framed question, in the order the stakeholder's
  decision needs them.
- Filters sit in the sidebar and apply to the whole screen. Their defaults
  show the most recent complete period.

### Choosing a chart

| The question compares | Chart | Helper |
|---|---|---|
| Items ranked by size | Horizontal bars, largest at the top | `charts.ranked_bar` |
| Change over time | A line | `charts.trend_line` |
| Shares of a whole (up to five parts) | Horizontal bars of percentages, not a pie | `charts.ranked_bar(kind="percent")` |
| Exact values someone will look up | A table | `st.dataframe` |

Anything else (a distribution, two measures against each other): agree on
the chart with the team before building it, and add a row here.

### Words

- Every section's headline states its takeaway with the number, computed
  from the data: "Rock earns 35% of revenue", not "Revenue by genre"
  (`charts.headline`).
- Under the headline, one caption: the metric, its period, and its filters,
  as `spec.md` defines them.
- Labels in plain words, never column names: "Revenue", not
  `total_revenue`. Sentence case.

### Numbers

- Money in whole dollars ($1,234), with cents under $10 ($5.65); counts
  with separators (1,234); percentages to one decimal (12.3%).
- Exception, so figures tie out to Finance to the cent: grand totals, the
  "ties to Finance" tile, and exact-value tables show cents ($2,328.60),
  using kind `"cents"`. Charts and other tiles stay in whole dollars.
- Bars start at zero.

### Color

- One accent color for what the headline is about; neutral gray for
  everything else; red only for a loss or a miss.
- A category keeps the same color on every chart.
- Color never carries a meaning alone: the headline or a label says it too.
- Nothing decorative: no 3-D, no background images, gridlines only where
  reading a value needs them.

### When there is nothing to show

- A filter that leaves no rows shows a short note (`charts.nothing_to_show`)
  in place of an error or an empty chart.
