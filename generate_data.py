"""
Generates a realistic synthetic HR / EMPLOYEE ATTRITION dataset for
exploratory data analysis. Features carry genuine, interpretable
relationships with each other and with Attrition, so EDA on this
data surfaces real, explainable patterns rather than pure noise.
"""
import numpy as np
import pandas as pd

np.random.seed(7)
N = 1500

departments = np.random.choice(
    ["Sales", "R&D", "HR", "Engineering", "Marketing"],
    size=N, p=[0.25, 0.25, 0.10, 0.25, 0.15]
)
job_role = np.random.choice(
    ["Executive", "Manager", "Senior", "Junior", "Intern"],
    size=N, p=[0.05, 0.15, 0.35, 0.35, 0.10]
)
age = np.random.normal(36, 9, size=N).clip(20, 60).astype(int)
years_at_company = (np.random.exponential(4, size=N) + (age - 22) * 0.05).clip(0, 35).astype(int)
years_at_company = np.minimum(years_at_company, age - 20)  # can't exceed working years
distance_from_home = np.random.exponential(8, size=N).clip(1, 40).astype(int)
education_level = np.random.choice([1, 2, 3, 4, 5], size=N, p=[0.05, 0.2, 0.35, 0.3, 0.1])
business_travel = np.random.choice(
    ["Non-Travel", "Travel_Rarely", "Travel_Frequently"], size=N, p=[0.15, 0.65, 0.20]
)
overtime = np.random.choice(["Yes", "No"], size=N, p=[0.3, 0.7])

# Job satisfaction & work-life balance (1-4 scale), correlated with overtime/travel
job_satisfaction = np.clip(
    np.random.normal(3, 0.9, size=N) - np.where(overtime == "Yes", 0.5, 0), 1, 4
).round().astype(int)
work_life_balance = np.clip(
    np.random.normal(3, 0.8, size=N)
    - np.where(overtime == "Yes", 0.7, 0)
    - np.where(business_travel == "Travel_Frequently", 0.4, 0), 1, 4
).round().astype(int)

# Monthly income driven by job role, education, years at company
role_base = {"Intern": 2800, "Junior": 4200, "Senior": 6500, "Manager": 9500, "Executive": 15000}
monthly_income = np.array([role_base[r] for r in job_role]).astype(float)
monthly_income += years_at_company * 180
monthly_income += (education_level - 3) * 400
monthly_income += np.random.normal(0, 600, size=N)
monthly_income = monthly_income.clip(2200, 22000).round(2)

performance_rating = np.random.choice([1, 2, 3, 4], size=N, p=[0.05, 0.15, 0.55, 0.25])
num_companies_worked = np.random.poisson(2.2, size=N).clip(0, 9)
promotion_last_5years = np.random.choice([0, 1], size=N, p=[0.75, 0.25])

# --- Attrition driven by realistic underlying signal ---
logit = (
    -2.2
    + np.where(overtime == "Yes", 1.0, 0)
    + 0.15 * (4 - job_satisfaction)
    + 0.15 * (4 - work_life_balance)
    - 0.05 * years_at_company
    + 0.02 * distance_from_home
    + np.where(business_travel == "Travel_Frequently", 0.5, 0)
    - 0.00006 * (monthly_income - 6000)
    + 0.1 * num_companies_worked
    - 0.4 * promotion_last_5years
    + np.random.normal(0, 0.7, size=N)
)
attrition_prob = 1 / (1 + np.exp(-logit))
attrition = np.where(np.random.rand(N) < attrition_prob, "Yes", "No")

df = pd.DataFrame({
    "EmployeeID": [f"EMP{i:05d}" for i in range(1, N + 1)],
    "Age": age,
    "Department": departments,
    "JobRole": job_role,
    "MonthlyIncome": monthly_income,
    "YearsAtCompany": years_at_company,
    "DistanceFromHome": distance_from_home,
    "EducationLevel": education_level,
    "BusinessTravel": business_travel,
    "OverTime": overtime,
    "JobSatisfaction": job_satisfaction,
    "WorkLifeBalance": work_life_balance,
    "PerformanceRating": performance_rating,
    "NumCompaniesWorked": num_companies_worked,
    "PromotionLast5Years": promotion_last_5years,
    "Attrition": attrition,
})

# Inject a bit of realistic missingness and a few duplicate rows (typical raw-data mess)
for col, frac in [("MonthlyIncome", 0.02), ("JobSatisfaction", 0.015), ("DistanceFromHome", 0.01)]:
    idx = df.sample(frac=frac, random_state=3).index
    df.loc[idx, col] = np.nan

dupes = df.sample(n=20, random_state=11)
df = pd.concat([df, dupes], ignore_index=True).sample(frac=1, random_state=2).reset_index(drop=True)

df.to_csv("data/hr_employee_data.csv", index=False)
print("Dataset created:", df.shape)
print(df["Attrition"].value_counts(normalize=True))
