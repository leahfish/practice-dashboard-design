# Roadmap

Phases in critical-path order: each one needs the one before it. Every task
is a GitHub Issue small enough to finish in one fresh session, with its
acceptance criteria and the tests that prove it.

| Phase | Goal | Issues |
|---|---|---|
| 1. Data connection | The app reads the team's database, locally and on Community Cloud | #3 |
| 2. Data layer | Every metric in the spec has a tested function in `dashboard/metrics.py` | #4, #5, #6, #7, #8, #9, #10, #11 |
| 3. Views | Each stakeholder question has a screen section that answers it, built as `design.md` draws it | #12, #13, #14, #15 |
| 4. Filters | The interactions the spec lists work, and the numbers still reconcile | #16 |
| 5. Polish and deploy | The app follows every rule in `design.md`; `mockup.py` is gone; the live app link is in the README | #17 |

## Critical path

Each line lists an Issue and the Issues it waits on. Work them in this order;
Issues on the same line can run in any order.

1. #3 (connection and hello-world deploy) blocks everything.
2. #4 (grand total and Finance gap) waits on #3, and blocks #5 – #11.
3. #5 – #11 (the other seven metrics) each wait on #4 only.
4. #12 (Screen 1) waits on #5, #6, #7.
5. #13 (Screen 2) waits on #8, #9, #12; #14 (Screen 3) waits on #10, #12;
   #15 (Screen 4) waits on #11, #12.
6. #16 (year picker) waits on #12, #13, #14, #15.
7. #17 (polish, delete the mockup, final deploy) waits on #16.

Longest chain: #3 → #4 → #5 → #12 → #13 → #16 → #17.

---

## Dashboard review

When the dashboard is finished, the Pitch Lead runs the final review. Each fix
becomes a GitHub Issue labeled `phase-1` through `phase-5`, for the phase it
belongs to, and each review adds one line below.

<Filled in by /dashkit:review-dashboard: one line per review, "- YYYY-MM-DD: fixes in #n, #n".>
