# Exploratory Data Analysis (EDA) Project
### HR Employee Attrition — Analysis Report

---

## 1. Objective

Explore an HR dataset to understand **why employees leave** (attrition), using
statistical summaries and visualizations to uncover patterns, correlations,
and the key factors that influence attrition.

## 2. Dataset Overview

| | |
|---|---|
| **Rows (after cleaning)** | 1,500 employees |
| **Columns** | 15 features + target (`Attrition`) |
| **Overall attrition rate** | 25.5% (382 of 1,500 employees) |
| **Departments** | Sales, R&D, HR, Engineering, Marketing |
| **Data issues found & fixed** | 20 duplicate rows removed; missing values in `MonthlyIncome`, `JobSatisfaction`, `DistanceFromHome` imputed with median (grouped by role where relevant) |

## 3. Statistical Summary (Numeric Features)

| Feature | Mean | Std Dev | Min | Median | Max |
|---|---|---|---|---|---|
| Age | 35.6 | 8.4 | 20 | 36 | 60 |
| Monthly Income ($) | 6,987 | 2,878 | 2,200 | 6,579 | 18,305 |
| Years at Company | 3.8 | 3.5 | 0 | 3 | 33 |
| Distance from Home (km) | 7.6 | 7.6 | 1 | 5 | 40 |
| Job Satisfaction (1–4) | 2.8 | 0.9 | 1 | 3 | 4 |
| Work-Life Balance (1–4) | 2.7 | 0.9 | 1 | 3 | 4 |
| Num. Companies Worked | 2.1 | 1.5 | 0 | 2 | 8 |

Full table in `data/statistical_summary.csv`.

## 4. Univariate Findings

- **Age** is roughly normally distributed, centered around 36, consistent with a
  mature workforce rather than an entry-level-heavy one.
- **Monthly Income** is right-skewed — most employees earn $5K–$8K, with a long
  tail of senior/executive earners pulling the mean above the median.
- **Engineering, Sales, and R&D** are the largest departments; **HR** is the smallest.

## 5. Bivariate Findings — What Relates to Attrition?

| Factor | Pattern |
|---|---|
| **OverTime** | Employees working overtime leave at **40.6%**, more than double the rate of those who don't (**19.2%**) — the single strongest categorical driver found. |
| **Business Travel** | Frequent travelers have a higher attrition rate (~28.5%) than rare/non-travelers (~24–26%). |
| **Department** | R&D (29.1%) and Engineering (26.8%) have the highest attrition; Sales (21.9%) the lowest. |
| **Monthly Income** | Employees who left have a visibly lower median income than those who stayed (see boxplot). |
| **Job Satisfaction & Work-Life Balance** | Both skew lower among employees who left — dissatisfaction and poor balance precede attrition more often than not. |
| **Years at Company** | Employees who leave tend to have shorter tenure — attrition risk is front-loaded in the first few years. |

## 6. Correlation Analysis

- The only numeric-numeric correlation worth noting is **Age ↔ Years at Company
  (r = 0.26)** — a mild, expected relationship (older employees have had more
  time to accumulate tenure). All other numeric feature pairs are weakly
  correlated (|r| < 0.2), meaning multicollinearity isn't a major concern here.
- **Correlation with Attrition** (numeric features, Yes=1):
  1. Work-Life Balance: **r = -0.14** (lower balance → more attrition)
  2. Job Satisfaction: **r = -0.11**
  3. Monthly Income: **r = -0.09**
  4. Promotion in Last 5 Years: **r = -0.09**
  5. Years at Company: **r = -0.07**

  These are individually modest — consistent with attrition being driven by a
  *combination* of factors (especially OverTime, a categorical variable) rather
  than any single numeric measure acting alone.

## 7. Key Influencing Factors — Summary

Ranked by practical impact on attrition, based on this analysis:

1. **OverTime** — by far the clearest single signal; more than 2x the attrition rate.
2. **Work-life balance & job satisfaction** — both negatively correlated with staying.
3. **Department** — R&D and Engineering see meaningfully higher turnover than Sales.
4. **Compensation** — lower earners are somewhat more likely to leave.
5. **Tenure** — newer employees are a higher flight risk than long-tenured ones.

## 8. Recommendations (Data-Driven)

- Investigate workload distribution in **R&D and Engineering** — high overtime
  rates there likely explain much of the elevated attrition.
- Consider **overtime caps or compensation adjustments** for frequently
  over-worked employees, given the strong OverTime → Attrition link.
- Focus retention efforts on **employees in their first 1–3 years**, where
  attrition risk appears highest.
- Revisit **promotion cadence** — employees without a promotion in 5 years show
  somewhat higher attrition.

## 9. Files in This Project

| File | Description |
|---|---|
| `data/hr_employee_data.csv` | Raw synthetic dataset (with duplicates/missing values) |
| `data/hr_employee_cleaned.csv` | Cleaned dataset used for analysis |
| `data/statistical_summary.csv` | Full `.describe()` output |
| `generate_data.py` | Script that generates the synthetic dataset |
| `analyze.py` | Full EDA pipeline (reproducible) |
| `eda_log.txt` | Full analysis log (stats, correlations, group-bys) |
| `charts/01`–`09` | All visualizations referenced above |

## 10. How to Reproduce

```bash
pip install -r requirements.txt
python generate_data.py   # creates data/hr_employee_data.csv
python analyze.py         # cleans data, runs analysis, generates all charts
```
