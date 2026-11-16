"""Clickable mockup of the four screens drawn in design.md.

Fixed numbers only: real names and rough totals from one read-only query,
pasted in. This file never connects to the database. Run with
`streamlit run mockup.py`.
"""

import pandas as pd
import streamlit as st

from dashboard import charts

st.set_page_config(page_title="Vinyl Vault (mockup)", layout="wide")

GRAND_TOTAL = 2328.60
PERIOD_NOTE = (
    "Revenue = unit price × quantity on each invoice line. "
    "1 Jan 2021 – 22 Dec 2025 (2025 ends 22 Dec)."
)

YEARS = pd.DataFrame(
    {"Year": [2021, 2022, 2023, 2024, 2025],
     "Revenue": [449.46, 481.45, 469.58, 477.53, 450.58]}
)
GENRES = pd.DataFrame(
    {"Genre": ["Rock", "Latin", "Metal", "Alternative & Punk", "TV Shows"],
     "Revenue": [826.65, 382.14, 261.36, 241.56, 93.53]}
)
COUNTRIES = pd.DataFrame(
    {"Country": ["USA", "Canada", "France", "Brazil", "Germany"],
     "Revenue": [523.06, 303.96, 195.10, 190.10, 156.48]}
)
PAIRS = pd.DataFrame(
    {"Pair": ["USA · Rock", "Canada · Rock", "USA · Latin", "Brazil · Rock",
              "France · Rock", "USA · Metal", "Germany · Rock", "Canada · Latin",
              "Brazil · Latin", "USA · Alternative & Punk"],
     "Revenue": [155.43, 105.93, 90.09, 80.19, 64.35, 63.36, 61.38, 59.40, 52.47, 49.50]}
)
MONTHS = pd.DataFrame(
    {"Month": pd.date_range("2024-01-01", "2025-12-01", freq="MS"),
     "Revenue": [37.62, 37.62, 37.62, 37.62, 37.62, 37.62, 39.62, 47.62, 46.71, 42.62,
                 37.62, 37.62, 37.62, 27.72, 37.62, 33.66, 37.62, 37.62, 37.62, 37.62,
                 37.62, 37.62, 49.62, 38.62]}
)
CUSTOMERS = pd.DataFrame(
    {"Customer": ["Helena Holý", "Richard Cunningham", "Luis Rojas", "Hugh O'Reilly",
                  "Ladislav Kovács", "Julia Barnett", "Fynn Zimmermann", "Frank Ralston",
                  "Victor Stevens", "Astrid Gruber"],
     "Revenue": [49.62, 47.62, 46.62, 45.62, 45.62, 43.62, 43.62, 43.62, 42.62, 42.62],
     "Years active (of 5)": [4, 5, 4, 3, 3, 4, 5, 3, 4, 4]}
)
REPS = pd.DataFrame(
    {"Rep": ["Jane", "Margaret", "Steve"],
     "Revenue": [833.04, 775.40, 720.16],
     "Customers": [21, 20, 18]}
)
REPS["Revenue per customer"] = REPS["Revenue"] / REPS["Customers"]
CUSTOMER_COUNT = int(REPS["Customers"].sum())


def finance_tile(total: float = GRAND_TOTAL) -> dict:
    return {"label": "Ties to Finance", "value": total, "kind": "cents",
            "delta": 0.0, "versus": "gap vs invoice totals"}


def cents_table(df: pd.DataFrame, money_cols: list[str]) -> None:
    shown = df.copy()
    for col in money_cols:
        shown[col] = shown[col].map(lambda v: charts.fmt(v, "cents"))
    st.dataframe(shown, hide_index=True, width="stretch")


def screen_money(year: str) -> None:
    st.warning("Mockup: made-up numbers")
    if year == "All years":
        total, scale, prior = GRAND_TOTAL, 1.0, None
        period = "all years"
    else:
        y = int(year)
        total = float(YEARS.loc[YEARS.Year == y, "Revenue"].iloc[0])
        scale = total / GRAND_TOTAL
        prior = YEARS.loc[YEARS.Year == y - 1, "Revenue"]
        prior = float(prior.iloc[0]) if len(prior) else None
        period = year
    genres = GENRES.assign(Revenue=GENRES.Revenue * scale)
    countries = COUNTRIES.assign(Revenue=COUNTRIES.Revenue * scale)
    pairs = PAIRS.assign(Revenue=PAIRS.Revenue * scale)
    genres["Share"] = genres.Revenue / total
    countries["Share"] = countries.Revenue / total
    g0, g1 = genres.iloc[0], genres.iloc[1]
    c0, c1 = countries.iloc[0], countries.iloc[1]

    st.header(
        f"{g0.Genre} and the {c0.Country} lead: {g0.Genre} earns "
        f"{charts.fmt(g0.Share, 'percent')} of revenue, the {c0.Country} "
        f"{charts.fmt(c0.Share, 'percent')}."
    )
    total_tile = {"label": "Total revenue", "value": total, "kind": "cents"}
    if prior is not None:
        total_tile.update(delta=total - prior, versus="vs prior year")
    charts.kpi_row([
        total_tile,
        {"label": f"Top genre: {g0.Genre}", "value": g0.Share, "kind": "percent",
         "delta": g0.Share - g1.Share, "versus": f"vs {g1.Genre}"},
        {"label": f"Top country: {c0.Country}", "value": c0.Share, "kind": "percent",
         "delta": c0.Share - c1.Share, "versus": f"vs {c1.Country}"},
        finance_tile(total),
    ])
    st.caption(PERIOD_NOTE)

    charts.headline(f"{g0.Genre} earns {charts.fmt(g0.Share, 'percent')} of revenue",
                    f"Share of revenue, top 5 genres · {period}")
    charts.show(charts.ranked_bar(genres, "Genre", "Share", kind="percent", top=5))

    charts.headline(f"The {c0.Country} earns {charts.fmt(c0.Share, 'percent')} of revenue",
                    f"Share of revenue, top 5 billing countries · {period}")
    charts.show(charts.ranked_bar(countries, "Country", "Share", kind="percent", top=5))

    p0 = pairs.iloc[0]
    charts.headline(f"{p0.Pair.replace(' · ', ' ')} is the top pair at {charts.fmt(p0.Revenue, 'money')}",
                    f"Revenue, top 10 genre-and-country pairs · {period}")
    charts.show(charts.ranked_bar(pairs, "Pair", "Revenue", top=10))


def screen_growth() -> None:
    st.warning("Mockup: made-up numbers")
    years = YEARS.copy()
    years["Change vs prior year"] = years.Revenue.pct_change()
    last, prev = years.iloc[-1], years.iloc[-2]
    best = years.loc[years.Revenue.idxmax()]
    avg = years.Revenue.mean()
    st.header(
        f"Revenue is flat: {charts.fmt(years.Revenue.min(), 'money')} to "
        f"{charts.fmt(years.Revenue.max(), 'money')} a year, and {int(last.Year)} is "
        f"{'down' if last['Change vs prior year'] < 0 else 'up'} "
        f"{charts.fmt(abs(last['Change vs prior year']), 'percent')}."
    )
    charts.kpi_row([
        {"label": f"{int(last.Year)} revenue", "value": last.Revenue, "kind": "money",
         "delta": last.Revenue - prev.Revenue, "versus": f"vs {int(prev.Year)}"},
        {"label": "Average year", "value": avg, "kind": "money",
         "delta": last.Revenue - avg, "versus": f"{int(last.Year)} vs average"},
        {"label": f"Best year: {int(best.Year)}", "value": best.Revenue, "kind": "money",
         "delta": best.Revenue - avg, "versus": "vs average"},
        finance_tile(),
    ])
    st.caption(PERIOD_NOTE)

    change = last["Change vs prior year"]
    charts.headline(
        f"{int(last.Year)} revenue {'fell' if change < 0 else 'rose'} "
        f"{charts.fmt(abs(change), 'percent')} from {int(prev.Year)}",
        "Revenue by calendar year · 2025 ends 22 Dec",
    )
    shown = pd.DataFrame({
        "Year": years.Year.astype(str),
        "Revenue": years.Revenue.map(lambda v: charts.fmt(v, "cents")),
        "Change vs prior year": years["Change vs prior year"].map(
            lambda v: "—" if pd.isna(v) else ("+" if v >= 0 else "−") + charts.fmt(abs(v), "percent")),
    })
    red = lambda v: f"color: {charts.NEGATIVE}" if str(v).startswith("−") else ""
    st.dataframe(shown.style.map(red, subset=["Change vs prior year"]),
                 hide_index=True, width="stretch")

    charts.headline(
        f"Over the last two years, monthly revenue holds near "
        f"{charts.fmt(MONTHS.Revenue.mean(), 'money')}",
        "Revenue by calendar month · Jan 2024 – Dec 2025 (2025 ends 22 Dec)",
    )
    charts.show(charts.trend_line(MONTHS, "Month", "Revenue"))


def screen_customers() -> None:
    st.warning("Mockup: made-up numbers")
    top_total = CUSTOMERS.Revenue.sum()
    share = top_total / GRAND_TOTAL
    equal = len(CUSTOMERS) / CUSTOMER_COUNT
    loyal = int((CUSTOMERS["Years active (of 5)"] == 5).sum())
    fewest = int(CUSTOMERS["Years active (of 5)"].min())
    st.header(
        f"No small group carries us: the top 10 customers bring in "
        f"{charts.fmt(share, 'percent')}."
    )
    charts.kpi_row([
        {"label": "Top 10 customers' share", "value": share, "kind": "percent",
         "delta": share - equal, "versus": f"vs {charts.fmt(equal, 'percent')} if all spent equally"},
        {"label": "Top 10 buying in all 5 years", "value": loyal, "kind": "count"},
        finance_tile(),
    ])
    st.caption(PERIOD_NOTE)

    charts.headline(
        f"The top 10 customers bring in {charts.fmt(top_total, 'money')}, "
        f"{charts.fmt(share, 'percent')} of revenue",
        "Revenue, top 10 customers (ties for 10th included) · all years",
    )
    charts.show(charts.ranked_bar(CUSTOMERS, "Customer", "Revenue", top=len(CUSTOMERS)))

    charts.headline(
        f"Every top-10 customer bought in at least {fewest} of 5 years",
        "Years with at least one invoice, top 10 customers",
    )
    cents_table(CUSTOMERS, ["Revenue"])


def screen_reps() -> None:
    st.warning("Mockup: made-up numbers")
    top = REPS.loc[REPS.Revenue.idxmax()]
    avg = REPS.Revenue.mean()
    st.header(
        f"Each rep's customers bring in a similar amount: "
        f"{charts.fmt(REPS.Revenue.min(), 'money')} to {charts.fmt(REPS.Revenue.max(), 'money')}."
    )
    charts.kpi_row([
        {"label": f"Top rep: {top.Rep}", "value": top.Revenue, "kind": "money",
         "delta": top.Revenue - avg, "versus": "vs rep average"},
        {"label": f"Customers across {len(REPS)} reps", "value": CUSTOMER_COUNT, "kind": "count"},
        finance_tile(),
    ])
    st.caption(PERIOD_NOTE)

    charts.headline(
        f"{top.Rep}'s customers bring in the most, {charts.fmt(top.Revenue, 'money')}",
        "Revenue from each rep's customers · Sales Support Agents · all years",
    )
    charts.show(charts.ranked_bar(REPS, "Rep", "Revenue"))

    rpc = REPS["Revenue per customer"]
    charts.headline(
        f"Revenue per customer is nearly equal: {charts.fmt(rpc.min(), 'cents')} "
        f"to {charts.fmt(rpc.max(), 'cents')}",
        "Customers and average revenue per customer, by rep · all years",
    )
    cents_table(REPS[["Rep", "Customers", "Revenue per customer"]], ["Revenue per customer"])
    st.caption("Shows revenue per rep as context; it does not show that a rep caused the sales.")


SCREENS = ["Where the money comes from", "Growth", "Customers", "Sales reps"]
screen = st.sidebar.radio("Screen", SCREENS)
if screen == SCREENS[0]:
    year = st.sidebar.selectbox("Year", ["All years"] + [str(y) for y in YEARS.Year])
    screen_money(year)
elif screen == SCREENS[1]:
    st.sidebar.caption("No filters: the yearly table covers the full period; the monthly line covers Jan 2024 – Dec 2025.")
    screen_growth()
elif screen == SCREENS[2]:
    st.sidebar.caption("No filters: always the full period.")
    screen_customers()
else:
    st.sidebar.caption("No filters: always the full period.")
    screen_reps()
