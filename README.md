# Part 2, policy rules

## Files

| File | What it is |
| --- | --- |
| `part2_rules.py` | Written by Claude for this project. The formulas are the brief's Part 2 and the inputs follow Appendix A and the lecturer's 6 Nov instruction. The lecturer gave no template for Part 2, so the layout is our own, and it runs with `python3 part2_rules.py`. |
| `part2_rules_history.png` | The chart the script draws when it runs. |
| `part2_rules_2026Q3.csv`, `part2_rules_history.csv` | Left over from the first version of the script and no longer used, so they can be deleted. |

## Inputs and sources

| Input | Value | Source | Published |
| --- | ---: | --- | --- |
| CPI inflation, 2026 Q3 | 3.17 | [ONS MM23, series D7G7](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7g7/mm23), the average of Jul 2.9, Aug 3.1 and Sep 3.5, as Appendix A asks | 21 Oct 2026 |
| Output gap, 2026 Q3 | -1.1 | [OBR October 2026 EFO](https://obr.uk/efo/economic-and-fiscal-outlook-october-2026/), detailed economy tables. Real GDP (Table 1.1) over potential output (Table 1.15) gives -1.11, and the same method reproduces the OBR's gap table (1.14) exactly for 2025 Q3 to 2026 Q2 (workbook saved in `../Data/`). | 28 Oct 2026 |
| Cross-check of the gap | -1.1 | [Bank of England July 2026 MPR](https://www.bankofengland.co.uk/monetary-policy-report/2026/july-2026), Table 3.B, excess supply in 2026 Q3; the two sources agree | 30 Jul 2026 |
| Bank Rate, 2026 Q2 and Q3 | 3.75 | [Bank Rate history](https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp), and the lecturer's instruction fixes 3.75 for both quarters | |
| r*, low, median, high | 1.00, 1.25, 1.50 | [September 2026 MaPS](https://www.bankofengland.co.uk/markets/market-participants-survey), question 1bi, neutral Bank Rate of 3.00, 3.25 and 3.50 (25th, 50th and 75th percentiles) minus 2, the values the brief itself prints in Appendix A | Sep 2026 |

For the history table the CPI figures are quarter averages from the same ONS file. The gaps are the OBR's October 2026 estimates for each quarter, which the Bank did not have at the time. Bank Rate is the level at each quarter end, after the cuts of 7 Nov 2024 (4.75), 6 Feb 2025 (4.50), 8 May 2025 (4.25), 7 Aug 2025 (4.00) and 18 Dec 2025 (3.75).

## Results

Prescriptions for 2026 Q3, against Bank Rate of 3.75.

| r* | Taylor (1993) | Balanced approach | Inertial |
| --- | ---: | ---: | ---: |
| 1.00 (low) | 4.21 | 3.65 | 3.74 |
| 1.25 (median) | 4.46 | 3.90 | 3.77 |
| 1.50 (high) | 4.71 | 4.15 | 3.81 |

The same rules against what the Bank did, with r* at 1.25.

| Quarter | CPI | Gap | Bank Rate | Taylor | Balanced | Inertial |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2025 Q1 | 2.80 | -0.6 | 4.50 | 4.15 | 3.85 | 4.61 |
| 2025 Q2 | 3.50 | -0.7 | 4.25 | 5.15 | 4.80 | 4.54 |
| 2025 Q3 | 3.80 | -0.8 | 4.00 | 5.55 | 5.15 | 4.38 |
| 2025 Q4 | 3.40 | -0.9 | 3.75 | 4.90 | 4.45 | 4.07 |
| 2026 Q1 | 3.10 | -1.0 | 3.75 | 4.40 | 3.90 | 3.77 |
| 2026 Q2 | 2.73 | -1.1 | 3.75 | 3.79 | 3.24 | 3.67 |
| 2026 Q3 | 3.17 | -1.1 | 3.75 | 4.46 | 3.90 | 3.77 |
| Average distance from Bank Rate | | | | 0.76 | 0.55 | 0.18 |

## Answers, with our view

**(a) Which rule describes the Bank.** The inertial rule fits best, at 0.18 points from Bank Rate on average. Part of that fit is built in, because the rule starts from last quarter's actual rate. The more telling fact is the direction in which the Bank moved. Through 2025 the Bank cut by a full point while both static rules asked for rates half a point to a point and a half higher. So the Bank looked through above-target inflation and moved in small steps, which is what an inertial rule describes.

**(b) Which rule should guide the decision.** In our view the balanced approach at the median r* should guide it. It gives 3.90, a 15bp rise that rounds to one 25bp step. The inertial rule cannot guide, because it mostly repeats the last decision. Between the static rules the only difference is the weight on the gap, and two independent sources put slack at 1.1% of potential right now. Box G of the April 2026 MPR also says that policy "typically does not respond to the near-term effects of an energy shock on inflation but leans against any second-round effects", and slack is what limits those effects. The hawk's counter is the Taylor rule at 4.46, close to three steps, because CPI has been above target every month since October 2024 and one-year expected inflation in the survey is 2.5. Both static rules say raise, so the committee is arguing about the size of the move, not its direction.

**(c) How much r* matters.** It matters a great deal for the static rules and hardly at all for the inertial one. Each 0.25 on r* moves the Taylor and balanced rules by 0.25 and the inertial rule by 0.04. Across the survey's interquartile range the balanced approach runs from 3.65, a hold, to 4.15, almost two steps. The uncertainty about r* is therefore as wide as the decision itself, so we would report the balanced prescription as a range, not a point. The Taylor rule says raise at every value in the range. After the cut-off the November survey's median neutral rate rose to 3.50, which was September's high case, and that belongs in the minutes' paragraph on what has changed.
