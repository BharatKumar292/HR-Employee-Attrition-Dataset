"""
Exploratory Data Analysis — HR Employee Attrition Dataset

Pipeline:
  1. Load & lightly clean (dedupe, handle missing — EDA needs usable data too)
  2. Statistical summaries (describe, value counts, group-bys)
  3. Univariate visualizations (distributions)
  4. Bivariate visualizations (relationships with Attrition)
  5. Correlation analysis (heatmap)
  6. Key influencing factors summary
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.dpi"] = 110
os.makedirs("charts", exist_ok=True)

log_lines = []
def log(msg):
    print(msg)
    log_lines.append(str(msg))

# ---------------------------------------------------------------
# 1. LOAD & LIGHT CLEANING
# ---------------------------------------------------------------
df = pd.read_csv("data/hr_employee_data.csv")
log(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns\n")

before = len(df)
df = df.drop_duplicates()
log(f"Removed {before - len(df)} duplicate rows -> {len(df)} rows remain")

df["MonthlyIncome"] = df["MonthlyIncome"].fillna(df.groupby("JobRole")["MonthlyIncome"].transform("median"))
df["JobSatisfaction"] = df["JobSatisfaction"].fillna(df["JobSatisfaction"].median())
df["DistanceFromHome"] = df["DistanceFromHome"].fillna(df["DistanceFromHome"].median())
log(f"Missing values after cleaning:\n{df.isna().sum().to_string()}\n")

df = df.drop(columns=["EmployeeID"])
df.to_csv("data/hr_employee_cleaned.csv", index=False)

# ---------------------------------------------------------------
# 2. STATISTICAL SUMMARY
# ---------------------------------------------------------------
log("=== STATISTICAL SUMMARY (numeric features) ===")
summary = df.describe().T.round(2)
log(summary.to_string())
summary.to_csv("data/statistical_summary.csv")

log(f"\n=== ATTRITION RATE ===\n{(df['Attrition'].value_counts(normalize=True) * 100).round(1).to_string()}%")

log("\n=== ATTRITION RATE BY DEPARTMENT ===")
dept_attr = df.groupby("Department")["Attrition"].apply(lambda s: (s == "Yes").mean() * 100).round(1).sort_values(ascending=False)
log(dept_attr.to_string())

log("\n=== ATTRITION RATE BY OVERTIME ===")
ot_attr = df.groupby("OverTime")["Attrition"].apply(lambda s: (s == "Yes").mean() * 100).round(1)
log(ot_attr.to_string())

# ---------------------------------------------------------------
# 3. UNIVARIATE VISUALIZATIONS
# ---------------------------------------------------------------

# 3a. Age & Income distributions
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.histplot(df["Age"], bins=25, kde=True, color="#4C72B0", ax=axes[0])
axes[0].set_title("Age Distribution")
sns.histplot(df["MonthlyIncome"], bins=25, kde=True, color="#55A868", ax=axes[1])
axes[1].set_title("Monthly Income Distribution")
plt.suptitle("Univariate Distributions", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/01_age_income_distribution.png")
plt.close()

# 3b. Department & Job role counts
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
dept_order = df["Department"].value_counts().index
sns.countplot(data=df, y="Department", order=dept_order, hue="Department",
              palette="crest", legend=False, ax=axes[0])
axes[0].set_title("Employees by Department")
role_order = df["JobRole"].value_counts().index
sns.countplot(data=df, y="JobRole", order=role_order, hue="JobRole",
              palette="flare", legend=False, ax=axes[1])
axes[1].set_title("Employees by Job Role")
plt.tight_layout()
plt.savefig("charts/02_department_role_counts.png")
plt.close()

# ---------------------------------------------------------------
# 4. BIVARIATE: RELATIONSHIPS WITH ATTRITION
# ---------------------------------------------------------------

# 4a. Attrition rate by department (the strongest categorical driver)
plt.figure(figsize=(8, 5.5))
sns.barplot(x=dept_attr.values, y=dept_attr.index, hue=dept_attr.index, palette="rocket", legend=False)
plt.title("Attrition Rate by Department", fontsize=14, fontweight="bold")
plt.xlabel("Attrition Rate (%)")
plt.ylabel("")
plt.tight_layout()
plt.savefig("charts/03_attrition_by_department.png")
plt.close()

# 4b. Attrition by OverTime and BusinessTravel
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.barplot(data=df, x="OverTime", y=(df["Attrition"] == "Yes").astype(int) * 100,
            hue="OverTime", palette="mako", legend=False, ax=axes[0], estimator="mean", errorbar=None)
axes[0].set_title("Attrition Rate by OverTime")
axes[0].set_ylabel("Attrition Rate (%)")

travel_order = ["Non-Travel", "Travel_Rarely", "Travel_Frequently"]
sns.barplot(data=df, x="BusinessTravel", y=(df["Attrition"] == "Yes").astype(int) * 100,
            order=travel_order, hue="BusinessTravel", palette="mako", legend=False,
            ax=axes[1], estimator="mean", errorbar=None)
axes[1].set_title("Attrition Rate by Business Travel")
axes[1].set_ylabel("Attrition Rate (%)")
axes[1].tick_params(axis="x", rotation=15)
plt.tight_layout()
plt.savefig("charts/04_attrition_overtime_travel.png")
plt.close()

# 4c. Monthly Income by Attrition (boxplot)
plt.figure(figsize=(7.5, 5.5))
sns.boxplot(data=df, x="Attrition", y="MonthlyIncome", hue="Attrition", palette="Set2", legend=False)
plt.title("Monthly Income by Attrition Status", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/05_income_by_attrition.png")
plt.close()

# 4d. Job Satisfaction & Work-Life Balance vs Attrition
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.countplot(data=df, x="JobSatisfaction", hue="Attrition", palette="Set1", ax=axes[0])
axes[0].set_title("Job Satisfaction vs Attrition")
sns.countplot(data=df, x="WorkLifeBalance", hue="Attrition", palette="Set1", ax=axes[1])
axes[1].set_title("Work-Life Balance vs Attrition")
plt.tight_layout()
plt.savefig("charts/06_satisfaction_worklife_vs_attrition.png")
plt.close()

# 4e. Years at Company vs Attrition
plt.figure(figsize=(8, 5.5))
sns.boxplot(data=df, x="Attrition", y="YearsAtCompany", hue="Attrition", palette="Set3", legend=False)
plt.title("Years at Company by Attrition Status", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/07_tenure_by_attrition.png")
plt.close()

# ---------------------------------------------------------------
# 5. CORRELATION ANALYSIS
# ---------------------------------------------------------------
numeric_cols = ["Age", "MonthlyIncome", "YearsAtCompany", "DistanceFromHome",
                 "EducationLevel", "JobSatisfaction", "WorkLifeBalance",
                 "PerformanceRating", "NumCompaniesWorked", "PromotionLast5Years"]
corr = df[numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, linewidths=0.5)
plt.title("Correlation Heatmap — Numeric Features", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/08_correlation_heatmap.png")
plt.close()

log("\n=== TOP CORRELATIONS (|r| > 0.2, excluding self-correlation) ===")
corr_pairs = corr.abs().unstack().sort_values(ascending=False)
corr_pairs = corr_pairs[corr_pairs < 1.0]
seen = set()
top_corrs = []
for (a, b), val in corr_pairs.items():
    if (b, a) in seen:
        continue
    seen.add((a, b))
    if val > 0.2:
        top_corrs.append((a, b, corr.loc[a, b]))
for a, b, v in top_corrs:
    log(f"{a} <-> {b}: r = {v:.2f}")

# ---------------------------------------------------------------
# 6. KEY INFLUENCING FACTORS FOR ATTRITION (point-biserial via numeric encoding)
# ---------------------------------------------------------------
df["AttritionFlag"] = (df["Attrition"] == "Yes").astype(int)
influence = df[numeric_cols + ["AttritionFlag"]].corr()["AttritionFlag"].drop("AttritionFlag")
influence = influence.sort_values(key=abs, ascending=False)
log("\n=== CORRELATION OF NUMERIC FEATURES WITH ATTRITION ===")
log(influence.round(3).to_string())

plt.figure(figsize=(8, 6))
colors = ["#C44E52" if v > 0 else "#4C72B0" for v in influence.values]
sns.barplot(x=influence.values, y=influence.index, hue=influence.index, palette=colors, legend=False)
plt.title("Feature Correlation with Attrition", fontsize=14, fontweight="bold")
plt.xlabel("Correlation with Attrition (Yes=1)")
plt.ylabel("Feature")
plt.axvline(0, color="black", linewidth=0.8)
plt.tight_layout()
plt.savefig("charts/09_attrition_influence_factors.png")
plt.close()

with open("eda_log.txt", "w") as f:
    f.write("\n".join(log_lines))

print("\nDONE.")
