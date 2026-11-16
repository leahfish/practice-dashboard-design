# Roadmap

Phases in critical-path order: each one needs the one before it. Every task
is a GitHub Issue small enough to finish in one fresh session, with its
acceptance criteria and the tests that prove it.

| Phase | Goal | Issues |
|---|---|---|
| 1. Data connection | The app reads the team's database, locally and on Community Cloud | |
| 2. Data layer | Every metric in the spec has a tested function in `dashboard/metrics.py` | |
| 3. Views | Each stakeholder question has a screen section that answers it, built as `design.md` draws it | |
| 4. Filters | The interactions the spec lists work, and the numbers still reconcile | |
| 5. Polish and deploy | The app follows every rule in `design.md`; `mockup.py` is gone; the live app link is in the README | |

## Critical path

<Which Issues block which; filled in from the spec.>

---

## Dashboard review

When the dashboard is finished, the Pitch Lead runs the final review. Each fix
becomes a GitHub Issue labeled `phase-1` through `phase-5`, for the phase it
belongs to, and each review adds one line below.

<Filled in by /dashkit:review-dashboard: one line per review, "- YYYY-MM-DD: fixes in #n, #n".>

## Task draft

| # | Phase | Task | AC IDs | Tests to write first | Depends on | Assignee |
|---|---|---|---|---|---|---|
| T1 | 1 | Connect to the database and deploy a hello-world page showing the live grand total | Task criteria: the page shows revenue locally; the app is deployed on Community Cloud; its live link opens it | Tests: none new; the full suite stays green | — | leahfish |
| T2 | 2 | Grand total and Finance reconciliation gap | AC-11 | `test_ac11_grand_total_reconciles_to_invoice_totals`, `test_ac11_reconciliation_gap_is_zero` | T1 | leahfish |
| T3 | 2 | Genre revenue and share | AC-1, AC-12 (genre) | `test_ac1_genre_revenue_reconciles`, `test_ac1_top_five_genres_and_shares`, `test_ac12_genre_revenue_adds_to_grand_total` | T2 | leahfish |
| T4 | 2 | Country revenue and share | AC-3, AC-12 (country) | `test_ac3_country_revenue_reconciles`, `test_ac3_top_five_countries_and_shares`, `test_ac12_country_revenue_adds_to_grand_total` | T2 | leahfish |
| T5 | 2 | Genre-and-country pair revenue | AC-4 | `test_ac4_pair_revenue_reconciles`, `test_ac4_top_three_pairs` | T2 | leahfish |
| T6 | 2 | Yearly revenue and change from the prior year | AC-5, AC-12 (year) | `test_ac5_yearly_revenue_reconciles`, `test_ac5_yearly_revenue_and_change`, `test_ac12_yearly_revenue_adds_to_grand_total` | T2 | leahfish |
| T7 | 2 | Monthly revenue, Jan 2024 – Dec 2025 | AC-6 | `test_ac6_monthly_revenue_reconciles`, `test_ac6_24_months_sum_to_928_11` | T2 | leahfish |
| T8 | 2 | Customer revenue, top-10 share, years active | AC-7, AC-8 | `test_ac7_customer_revenue_reconciles`, `test_ac7_top_ten_share`, `test_ac8_top_ten_years_active` | T2 | leahfish |
| T9 | 2 | Rep revenue, customers, revenue per customer | AC-9, AC-10, AC-12 (rep) | `test_ac9_rep_revenue_reconciles`, `test_ac9_rep_revenue`, `test_ac10_rep_customers_and_revenue_per_customer`, `test_ac12_rep_revenue_adds_to_grand_total` | T2 | leahfish |
| T10 | 3 | Screen 1 view, Where the money comes from (with the sidebar screen picker) | AC-1, AC-3, AC-4, AC-11 | `test_ac1_screen1_shows_top_genres`, `test_ac3_screen1_shows_top_countries`, `test_ac4_screen1_shows_top_pairs`, `test_ac11_screen1_shows_grand_total` | T3, T4, T5 | leahfish |
| T11 | 3 | Screen 2 view, Growth | AC-5, AC-6, AC-11 | `test_ac5_screen2_shows_yearly_table`, `test_ac6_screen2_shows_24_months`, `test_ac11_screen2_shows_grand_total` | T6, T7, T10 | leahfish |
| T12 | 3 | Screen 3 view, Customers | AC-7, AC-8, AC-11 | `test_ac7_screen3_shows_top_ten_share`, `test_ac8_screen3_shows_years_active`, `test_ac11_screen3_shows_grand_total` | T8, T10 | leahfish |
| T13 | 3 | Screen 4 view, Sales reps | AC-9, AC-10, AC-11 | `test_ac9_screen4_shows_rep_revenue`, `test_ac10_screen4_shows_customers_per_rep`, `test_ac11_screen4_shows_grand_total` | T9, T10 | leahfish |
| T14 | 4 | Screen 1 year picker | AC-2, AC-13 | `test_ac2_year_2023_totals_and_top_genre`, `test_ac13_other_screens_keep_full_period` | T10, T11, T12, T13 | leahfish |
| T15 | 5 | Polish, delete the mockup, final deploy | Task criteria: every `design.md` style rule holds; `mockup.py` is deleted; the final app is deployed; the README's live link opens the app | Tests: none new; the full suite stays green | T14 | leahfish |
