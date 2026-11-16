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

### Drawings

Headlines below show the all-years figures from the spec's acceptance
criteria; on screen they are computed from the data. Every screen's caption
under the tiles reads "Revenue = unit price × quantity on each invoice line.
1 Jan 2021 – 22 Dec 2025 (2025 ends 22 Dec)."

**Screen 1. Where the money comes from**

```
SIDEBAR                       | Rock and the USA lead: Rock earns 35.5% of revenue, the USA 22.5%.
  Screen: (•) Where the money |
          ( ) Growth          | [Total revenue] [Top genre]  [Top country] [Ties to Finance]
          ( ) Customers       |  $2,328.60       Rock 35.5%   USA 22.5%     Gap $0.00
          ( ) Sales reps      |  (vs prior yr    of revenue   of revenue    sum of invoices
                              |   when 1 year)                              = $2,328.60
  Year: [All years ▾]         |
        2021 … 2025           | ── Rock earns 35.5% of revenue ─────────────────────────────
                              |    Share of revenue, top 5 genres · all years
                              |    Rock               ████████████████████ 35.5%
                              |    Latin              █████████ 16.4%
                              |    Metal              ██████ 11.2%
                              |    Alternative & Punk ██████ 10.4%
                              |    TV Shows           ██ 4.0%
                              |    Q1 · percent bars
                              |
                              | ── The USA earns 22.5% of revenue ──────────────────────────
                              |    Share of revenue, top 5 billing countries · all years
                              |    USA     ████████████████████ 22.5%
                              |    Canada  ████████████ 13.1%
                              |    France  ████████ 8.4%
                              |    Brazil  ███████ 8.2%
                              |    Germany ██████ 6.7%
                              |    Q2 · percent bars
                              |
                              | ── USA Rock is the top pair at $155 ────────────────────────
                              |    Revenue, top 10 genre-and-country pairs · all years
                              |    USA · Rock     ████████████████████ $155
                              |    Canada · Rock  █████████████ $106
                              |    USA · Latin    ███████████ $90
                              |    … 7 more
                              |    Q3 · ranked bars
```

**Screen 2. Growth**

```
SIDEBAR                       | Revenue is flat: $449 to $481 a year, and 2025 is down 5.6%.
  Screen: ( ) Where the money |
          (•) Growth          | [2025 revenue]  [Average year] [Best year]  [Ties to Finance]
          ( ) Customers       |  $451            $466           2022, $481   $2,328.60
          ( ) Sales reps      |  −5.6% vs 2024                               Gap $0.00
                              |
  (no filters: always the     | ── 2025 revenue fell 5.6% from 2024 ───────────────────────
   full period)               |    Revenue by calendar year · 2025 ends 22 Dec
                              |    Year   Revenue    Change vs prior year
                              |    2021   $449.46    —
                              |    2022   $481.45    +7.1%
                              |    2023   $469.58    −2.5%   (red)
                              |    2024   $477.53    +1.7%
                              |    2025   $450.58    −5.6%   (red)
                              |    Q4 · table
                              |
                              | ── Monthly revenue holds near $39 a month ─────────────────
                              |    Revenue by calendar month · Jan 2021 – Dec 2025
                              |    $ ┤  ╱╲_╱‾╲_╱╲__╱‾╲_╱╲_╱‾╲__╱╲_╱‾╲_
                              |      └──────────────────────────────────
                              |       2021   2022   2023   2024   2025
                              |    Q5 · line
```

**Screen 3. Customers**

```
SIDEBAR                       | No small group carries us: the top 10 customers bring in 19.4%.
  Screen: ( ) Where the money |
          ( ) Growth          | [Top 10 share]       [Loyal top 10]       [Ties to Finance]
          (•) Customers       |  19.4% of revenue     2 of 10 bought in     $2,328.60
          ( ) Sales reps      |  vs 16.9% if all 59   all 5 years           Gap $0.00
                              |  spent equally
  (no filters: always the     |
   full period)               | ── The top 10 customers bring in $451, 19.4% of revenue ───
                              |    Revenue, top 10 customers (ties for 10th included) · all years
                              |    Customer A ████████████████████ $50
                              |    Customer B ███████████████████ $48
                              |    … 8 more
                              |    Q6 · ranked bars
                              |
                              | ── Every top-10 customer bought in at least 3 of 5 years ──
                              |    Years with at least one invoice, top 10 customers
                              |    Customer    Revenue   Years active (of 5)
                              |    Customer A  $49.62    5
                              |    …
                              |    Q7 · table
```

**Screen 4. Sales reps**

```
SIDEBAR                       | Each rep's customers bring in a similar amount: $720 to $833.
  Screen: ( ) Where the money |
          ( ) Growth          | [Top rep]              [Customers]       [Ties to Finance]
          ( ) Customers       |  Jane, $833             59 across 3 reps  $2,328.60
          (•) Sales reps      |  +$57 vs rep average                      Gap $0.00
                              |
  (no filters: always the     | ── Jane's customers bring in the most, $833 ───────────────
   full period)               |    Revenue from each rep's customers · Sales Support Agents · all years
                              |    Jane     ████████████████████ $833
                              |    Margaret ██████████████████ $775
                              |    Steve    █████████████████ $720
                              |    Q8 · ranked bars
                              |
                              | ── Revenue per customer is nearly equal: $38.77 to $40.01 ─
                              |    Customers and average revenue per customer, by rep
                              |    Rep       Customers   Revenue per customer
                              |    Jane      21          $39.67
                              |    Margaret  20          $38.77
                              |    Steve     18          $40.01
                              |    Q9 · table
                              |    Shows revenue per rep as context; it does not show
                              |    that a rep caused the sales.
```

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
